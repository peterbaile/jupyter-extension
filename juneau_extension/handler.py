# package imports
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import logging
import time
import asyncio
import tornado
import json
# from sqlalchemy import create_engine
import asyncio
import concurrent.futures

# import from modules
from juneau_extension.jupyter import store_var, connect_psql, exec_ipython, request_var


def get_input_value(arguments, key):
    return str(arguments[key][0])[2:-1]


class JuneauHandler2(IPythonHandler):
    done = {}

    def get(self):
        print("---RECEIVE REQUEST!---")
        self.write('successful get operation!')

    def put(self):
        kernel_id = get_input_value(self.request.arguments, 'kernel_id')
        var_name = get_input_value(self.request.arguments, 'var')

        # if kernel_id not in self.done:
        #     # o2, err = exec_ipython(kernel_id, var_name, 'connect_psql')
        #     # o2, err = data_extension.jupyter.connect_psql(kernel_id, search_var)
        #     self.done[kernel_id] = {}
        #     # logging.info(o2)
        #     # logging.info(err)

        o2, err = exec_ipython(kernel_id, var_name, 'connect_psql')
        logging.info(o2)
        logging.info(err)
        # success = exec_ipython(kernel_id, var_name, 'connect_psql')
        # pid = f'process {var_name}'

        # async def index():
        #     with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        #         loop = asyncio.get_event_loop()
        #         # futures = [
        #         #     loop.run_in_executor(executor, instance, '1'),
        #         #     loop.run_in_executor(executor, instance, '2')
        #         #     # loop.run_in_executor(executor, request, '3')
        #         # ]
        #         # for response in await asyncio.gather(*futures):
        #         #     pass
        #         for i in range(5):
        #             loop.run_in_executor(executor, exec_ipython, kernel_id, f'df{i}', 'connect_psql')
        #
        # event_loop = asyncio.get_event_loop()
        # event_loop.run_until_complete(index())
        # event_loop.close()

        print("!hello!")
        print("---done!---")

        # print("---request var [NO SUBPROCESS]---")
        # output, error = request_var(kernel_id, var_name)
        # print(output)
        # print("---done!---")
        # store_var(kernel_id, var_name)

        self.write({'message': 'Hello, world!'})
        self.finish()


def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookWebApplication): handle to the Notebook webserver instance.
    """
    print("----------The actual Juneau Server Extension is loaded----------")
    web_app = nb_server_app.web_app
    host_pattern = '.*$'
    route_pattern = url_path_join(web_app.settings['base_url'], '/juneau-2')
    web_app.add_handlers(host_pattern, [(route_pattern, JuneauHandler2)])
