import json
from tornado import gen, web
from notebook.base.handlers import APIHandler
from nbconvert import ScriptExporter
import nbformat
import urllib.parse
import time
from .schedule import add_job, remove_job
from .schedule import default_scheduler


class FunctionHandler(APIHandler):
    """
    A handler that manage serverless functions.
    """

    def initialize(self, app):
        self.logger = app.log
        self.db = app.db

    @web.authenticated
    @gen.coroutine
    def get(self, function=''):
        """
        List All Saved Functions

        Parameters
        ----------
        function:
            function name
        returns A JSON object containing all saved functions.
        """
        if not function:
            data = self.db.query_function(function) if function else self.db.all_functions()
            self.logger.info('query functions {function} {data}'.format(function=function, data=data))
            self.finish({'code': 'success', 'data': [a.as_dict() for a in data]})

        else:
            args = {}
            for a, b in self.request.arguments:
                args[a] = self.get_argument(a, default='')
            self.trigger_function(function, "GET", args, {})

    def trigger_function(self, function, method, query, body):
        data = {'method': method, 'query': query, 'body': body}
        self.logger.info('handle trigger function start: {name}, {data}'.format(name=function, data=data))
        func = self.db.query_function(function)
        if func is None:
            self.finish({'code': 'fail', 'message': 'function not found'})
            return
        func.trigger += 1
        func.logger = self.logger
        start = time.time()
        try:
            res = func(data)
            self.finish({'code': 'success', 'data': res})
            self.logger.info('handle trigger function success: {name}, {res}'.format(name=function, res=res))
            func.success += 1
        except Exception as e:
            func.fail += 1
            self.logger.error('call function {name} failed {error}'.format(name=function, error=e))
            self.finish({'code': 'fail', 'message': 'call function failed {e}'.format(e=e)})
            self.logger.info('handle trigger function fail: {name}, {error}'.format(name=function, error=e))
        func.cost += time.time() - start
        self.db.save()

    @gen.coroutine
    def post(self, function=''):
        param = self.request.body.decode('utf-8')
        try:
            data = json.loads(param)
        except Exception as e:
            data = param
        self.trigger_function(function, "POST", self.request.arguments, data)

    @web.authenticated
    @gen.coroutine
    def put(self, function=''):
        script_exporter = ScriptExporter()
        path = urllib.parse.unquote(function)
        out, resources = script_exporter.from_notebook_node(nbformat.read(path, as_version=4))
        data = {'name':function, 'script':out, 'raw': path}
        if function:
            self.logger.info('add functions {path}: {data}'.format(path=path, data=data))
            self.db.add_function(**data)
            func = self.db.query_function(function)
            func = func.front()
            func.logger = self.logger
            schedule = func.get_schedule()
            if schedule and isinstance(schedule, dict):
                data = {'method': 'SCHEDULE', 'query': {}, 'body': {}}
                add_job(function, schedule, func, data)
                self.logger.info(
                    'add function to schedule, current scheduled: {count}'.format(count=len(default_scheduler.jobs)))
            else:
                self.logger.info('schedule not found or not valid, '
                                 'current scheduled: {count}'.format(count=len(default_scheduler.jobs)))
                remove_job(function)

            self.logger.info('handle add function {data}'.format(data=data))
            self.finish({'code': 'success'})
        else:
            self.finish({'code': 'fail', 'message': 'function name not found'})

    @web.authenticated
    @gen.coroutine
    def delete(self, function=''):
        remove_job(function)
        self.db.del_function(function)
        self.finish({'message': 'success'})
