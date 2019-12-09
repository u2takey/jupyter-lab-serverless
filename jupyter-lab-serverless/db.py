from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time


Base = declarative_base()


class Function(Base):
    __tablename__ = 'functions'

    name = Column(String(64), primary_key = True)
    script = Column(TEXT)
    raw = Column(TEXT)
    trigger = Column(Integer)
    cost = Column(Float)
    success = Column(Integer)
    fail = Column(Integer)
    created = Column(Integer)
    updated = Column(Integer)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def __repr__(self):
        return "<Function(name='%s', created='%s', updated='%s')>" % (
            self.name, self.created, self.updated)

    def __call__(self, *args, **kwargs):
        import imp
        module = imp.new_module(self.name)
        exec(self.script, module.__dict__)
        return module.handle(*args, **kwargs)

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class FunctionDB(metaclass=Singleton):

    def __init__(self, db_path):
        engine = create_engine(db_path)
        self.Session = sessionmaker(bind=engine)
        Base.metadata.create_all(engine)
        self.sess = self.Session()

    def session(self):
        return self.sess

    def all_functions(self):
        return self.session().query(Function).all()

    def query_function(self, name):
        return self.session().query(Function).filter_by(name=name).first()

    def add_function(self, name, script, raw):
        function = self.query_function(name)
        if function:
            function.script = script
            function.raw = raw
            function.updated = int(time.time())
        else:
            self.session().add(Function(
                name=name,
                script=script,
                raw=raw,
                created=int(time.time()),
                trigger=0,
                cost = 0,
                success = 0,
                fail = 0,
            ))
        self.session().commit()

    def del_function(self, name):
        function = self.session().query_function(name)
        if function:
            self.session().delete(function)
            self.session().commit()

    def save(self):
        self.session().commit()
