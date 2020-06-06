# package imports
from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import logging

# import from modules
from juneau_extension.jupyter import store_var, connect_psql, exec_ipython


def get_input_value(arguments, key):
    return str(arguments[key][0])[2:-1]


class JuneauHandler2(IPythonHandler):
    done = {}

    def get(self):
        self.write('successful get operation!')

    def put(self):
        kernel_id = get_input_value(self.request.arguments, 'kernel_id')
        var_name = get_input_value(self.request.arguments, 'var')

        if kernel_id not in self.done:
            o2, err = exec_ipython(kernel_id, var_name, 'connect_psql')
            # o2, err = data_extension.jupyter.connect_psql(kernel_id, search_var)
            self.done[kernel_id] = {}
            logging.info(o2)
            logging.info(err)

        print("---second time connecting to Postgres---")
        output, error = connect_psql(kernel_id, var_name)
        print(output)
        print("-----second time done!-----")
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
