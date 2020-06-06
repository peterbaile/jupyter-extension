from jupyter_client import find_connection_file
from jupyter_client import MultiKernelManager, BlockingKernelClient, KernelClient
import logging
from queue import Empty
import sys
import site
import subprocess

import juneau_extension.config as cfg
from juneau_extension.file_lock import FileLock

logging.basicConfig(level=logging.DEBUG)
jupyter_lock = FileLock('my.lock')
TIMEOUT = 6


# Execute via IPython kernel
def exec_ipython(kernel_id, search_var, py_file):
    global jupyter_lock

    jupyter_lock.acquire()
    try:
        logging.debug('Exec ' + py_file)
        file_name = site.getsitepackages()[0] + '/juneau_extension/' + py_file + '.py'
        try:
            if sys.version_info[0] >= 3:
                msg_id = subprocess.Popen(['python3', file_name, \
                                           kernel_id, search_var], \
                                          stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            else:
                msg_id = subprocess.Popen(['python', file_name, \
                                           kernel_id, search_var], \
                                          stderr=subprocess.PIPE, stdout=subprocess.PIPE)
        except FileNotFoundError:
            msg_id = subprocess.Popen(['python', file_name, \
                                       kernel_id, search_var], \
                                      stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        output, error = msg_id.communicate()
    finally:
        jupyter_lock.release()

    if sys.version[0] == '3':
        output = output.decode("utf-8")
        error = error.decode("utf-8")
    output = output.strip('\n')

    msg_id.stdout.close()
    msg_id.stderr.close()

    logging.debug(output)

    return output, error


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

        reply = km.get_shell_msg(msg_id, timeout=60)
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
with engine.connect() as conn:
    result = conn.execute("select * from {cfg.sql_schema_name}.{cfg.sql_table_name}")
    for row in result:
        print(row)
    """

    print("---Attempting to execute SQL code---")

    return exec_code(kid, var, code)


def store_var(kernel_id, var_name):
    return 'n'
