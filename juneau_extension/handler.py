from notebook.utils import url_path_join
from notebook.base.handlers import IPythonHandler
import json


class JuneauHandler2(IPythonHandler):
    def get(self):
        self.write('successful get operation!')

    def put(self):
        print(self.request.arguments)
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
