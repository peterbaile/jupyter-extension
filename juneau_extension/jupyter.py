from jupyter_client import find_connection_file
from jupyter_client import MultiKernelManager, BlockingKernelClient, KernelClient
import logging
from queue import Empty
import sys
import site
import subprocess
import json
import asyncio

import juneau_extension.config as cfg
from juneau_extension.file_lock import FileLock

logging.basicConfig(level=logging.DEBUG)
jupyter_lock = FileLock('my.lock')
TIMEOUT = 6


# AsyncIO subprocess: adapted from https://docs.python.org/3/library/asyncio-subprocess.html#subprocesses
async def exec_ipython_asyncio(kernel_id, search_var, py_file):
    pid = f'process {search_var}'
    file_name = "/Users/peterchan/Desktop/GitHub/jupyter-extension/juneau_extension/connect_psql.py"

    proc = await asyncio.create_subprocess_exec('python3', file_name, kernel_id, search_var, pid, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    stdout, stderr = await proc.communicate()

    # if stdout:
    #     print(f'[stdout]\n{stdout.decode()}')
    # if stderr:
    #     print(f'[stderr]\n{stderr.decode()}')

    return stdout, stderr


# Execute via IPython kernel in the PARALLEL way
async def exec_ipython(kernel_id, search_var, py_file):
    pid = f'process {search_var}'

    logging.debug('Exec ' + py_file)
    file_name = "/Users/peterchan/Desktop/GitHub/jupyter-extension/juneau_extension/connect_psql.py"
    # file_name = site.getsitepackages()[0] + '/juneau_extension/' + py_file + '.py'
    try:
        if sys.version_info[0] >= 3:
            subprocess.Popen(['python3', file_name, \
                                       kernel_id, search_var, pid], \
                                      stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        else:
            subprocess.Popen(['python', file_name, \
                                       kernel_id, search_var, pid], \
                                      stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    except FileNotFoundError:
        subprocess.Popen(['python', file_name, \
                                   kernel_id, search_var, pid], \
                                  stderr=subprocess.PIPE, stdout=subprocess.PIPE)

    while True:
        json_file_name = "/Users/peterchan/Desktop/GitHub/jupyter-extension/juneau_extension/data_file.json"
        with open(json_file_name, "r") as file:
            try:
                data = json.load(file)
                if data.get(str(pid)):
                    print(f'process {pid}: {data[str(pid)]}')

                if data.get(str(pid)) == "done":
                    return True

            except Exception as e:
                continue

# # Execute via IPython kernel
# async def exec_ipython(kernel_id, search_var, py_file):
#     global jupyter_lock
#
#     jupyter_lock.acquire()
#
#     # set pid to 1 for test purpose
#     pid = f'process {search_var}'
#
#     try:
#         logging.info('Exec ' + py_file)
#         file_name = "/Users/peterchan/Desktop/GitHub/jupyter-extension/juneau_extension/connect_psql.py"
#         # file_name = site.getsitepackages()[0] + '/juneau_extension/' + py_file + '.py'
#         try:
#             if sys.version_info[0] >= 3:
#                 proc = subprocess.Popen(['python3', file_name, \
#                                            kernel_id, search_var, pid], \
#                                           stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#             else:
#                 proc = subprocess.Popen(['python', file_name, \
#                                            kernel_id, search_var, pid], \
#                                           stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#         except FileNotFoundError:
#             proc = subprocess.Popen(['python', file_name, \
#                                        kernel_id, search_var, pid], \
#                                       stderr=subprocess.PIPE, stdout=subprocess.PIPE)
#
#         output, error = proc.communicate()
#     finally:
#         jupyter_lock.release()
#
#     if sys.version[0] == '3':
#         output = output.decode("utf-8")
#         error = error.decode("utf-8")
#     output = output.strip('\n')
#
#     proc.stdout.close()
#     proc.stderr.close()
#
#     logging.debug(output)
#     logging.debug(error)
#
#     return output, error


def exec_code(kid, var, code):
    # load connection info and init communication
    cf = find_connection_file(kid)  # str(port))

    global jupyter_lock

    jupyter_lock.acquire()

    try:
        km = BlockingKernelClient(connection_file=cf)
        km.load_connection_file()
        km.start_channels()

        # logging.debug('Executing:\n' + str(code))
        msg_id = km.execute(code, store_history=False)

        reply = km.get_shell_msg(msg_id, timeout=10)
        # logging.info('Execution reply:\n' + str(reply))
        state = 'busy'

        output = None
        idle_count = 0
        try:
            while km.is_alive():
                try:
                    msg = km.get_iopub_msg(timeout=10)
                    # logging.debug('Read ' + str(msg))
                    if not 'content' in msg:
                        continue
                    if 'name' in msg['content'] and msg['content']['name'] == 'stdout':
                        # logging.debug('Got data '+ msg['content']['text'])
                        output = msg['content']['text']
                        break
                    if 'execution_state' in msg['content']:
                        # logging.debug('Got state')
                        state = msg['content']['execution_state']
                    if state == 'idle':
                        idle_count = idle_count + 1
                except Empty:
                    pass
        except KeyboardInterrupt:
            logging.error('Keyboard interrupt')
            pass
        finally:
            # logging.info('Kernel IO finished')
            km.stop_channels()

        # logging.info(str(output))
        error = ''
        if reply['content']['status'] != 'ok':
            logging.error('Status is ' + reply['content']['status'])
            logging.error(str(output))
            error = output
            output = None
    finally:
        jupyter_lock.release()

    return output, error


def connect_psql(kid, var):
    """
    Create a juneau_connect() function for use in the notebook

    :param kid:
    :param var:
    :return:
    """

    code = f"""from sqlalchemy import create_engine
conn_string = f"postgresql://{cfg.sql_name}:{cfg.sql_password}@localhost/{cfg.sql_dbname}"
engine = create_engine(conn_string)
with engine.begin() as conn:
    conn.execute("INSERT INTO {cfg.sql_schema_name}.{cfg.sql_table_name} (var_value, var_name) VALUES (9,'c')")
    result = conn.execute("select * from {cfg.sql_schema_name}.{cfg.sql_table_name}")
    for row in result:
        print(row)
    """

    print("---Attempting to execute SQL code---")

    return exec_code(kid, var, code)


def request_var(kid, var):
    """
    Request the contents of a dataframe or matrix
    :param kid:
    :param var:
    :return: Tuple with first parameter being JSON form of output, 2nd parameter being error if
             1st is None
    """
    code = "import pandas as pd\nimport numpy as np\nif type(" + var + ") " \
                                                                       "is pd.DataFrame or type(" + var + ") is np.ndarray or type(" + var + ") is list:\n"
    code = code + "\tprint(" + var + ".to_json(orient='split', index = False))\n"
    return exec_code(kid, var, code)


def store_var(kernel_id, var_name):
    return 'n'
