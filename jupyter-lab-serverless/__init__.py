from .serverless import FunctionHandler
from notebook.utils import url_path_join
from .schedule import default_scheduler
from .db import FunctionDB
from .schedule import add_job

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

    default_scheduler.run_continuously()

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

    recover_jobs(nb_server_app)

    web_app.add_handlers('.*$', handlers)


def recover_jobs(app):
    logger = app.log
    db_url = 'sqlite:///' + app.notebook_dir + '/severless.db'
    logger.info('init db at {path}'.format(path=db_url))
    store = FunctionDB(db_url)
    app.db = store

    for func in store.all_functions():
        func = func.front()
        func.logger = logger
        sche = func.get_schedule()
        if sche and isinstance(sche, dict):
            data = {'method': 'SCHEDULE', 'query': {}, 'body': {}}
            add_job(func.name, sche, func, data)
            logger.info(
                'add function to schedule, current scheduled: {count}'.format(count=len(default_scheduler.jobs)))

