import json
from tornado import gen, web
from notebook.base.handlers import APIHandler
from .db import FunctionDB
from nbconvert import ScriptExporter
import nbformat
import urllib.parse
import time

class FunctionHandler(APIHandler):
    """
    A handler that manage serverless functions.
    """

    def initialize(self, app):
        self.logger = app.log
        self.db_url = 'sqlite:///' + app.notebook_dir + '/severless.db'
        # self.db_url = 'sqlite:///:memory:'
        self.logger.info('init db at {path}'.format(path=self.db_url))
        self.db = FunctionDB(self.db_url)

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
        data = self.db.query_function(function) if function else self.db.all_functions()
        self.logger.info('query functions {function} {data}'.format(function=function, data=data))
        self.finish({'code': 'success', 'data': [a.as_dict() for a in data]})

    @gen.coroutine
    def post(self, function=''):
        param = self.request.body.decode('utf-8')
        data = json.loads(param)
        self.logger.info('handle trigger function {name}'.format(name=function))
        func = self.db.query_function(function)
        if func is None:
            self.finish({'code': 'fail', 'message': 'function not found'})
            return
        func.trigger += 1
        start = time.time()
        try:
            res = func(data)
            self.finish({'code': 'success', 'data': res})
            func.success += 1
        except Exception as e:
            func.fail += 1
            self.logger.error('call function {name} failed {error}'.format(name=function, error=e))
            self.finish({'code': 'fail', 'message': 'call function failed {e}'.format(e=e)})
        func.cost += time.time() - start
        self.db.save()

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
            self.logger.info('handle add function {data}'.format(data=data))
            self.finish({'code': 'success'})
        else:
            self.finish({'code': 'fail', 'message': 'function name not found'})

    @web.authenticated
    @gen.coroutine
    def delete(self, function=''):
        self.db.del_function(function)
        self.finish({'message': 'success'})

