from .serverless import FunctionHandler
from notebook.utils import url_path_join

def _jupyter_server_extension_paths():
    return [{
        'module': 'jupyter-lab-serverless'
    }]

def load_jupyter_server_extension(nb_server_app):
    """
    Called when the extension is loaded.

    Args:
        nb_server_app (NotebookApp): handle to the Notebook webserver instance.
    """
    nb_server_app.log.info('serverless module enabled!')
    web_app = nb_server_app.web_app
    # Prepend the base_url so that it works in a jupyterhub setting
    base_url = web_app.settings['base_url']
    base_url = url_path_join(base_url, 'function')

    handlers = [('{base}/(?P<function>[^?/]+)'.format(base=base_url),
                 FunctionHandler,
                 {"app": nb_server_app}
                ),
                ('{base}'.format(base=base_url),
                 FunctionHandler,
                 {"app": nb_server_app}
                 )
                ]
    nb_server_app.log.info(handlers)

    web_app.add_handlers('.*$', handlers)
