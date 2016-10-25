"""
    Flask-Pages - Another? flask extension that provides dynamic pages.

    Author: Bill Schumacher <bill@servernet.co>
    License: LGPLv3
    Copyright: 2016 Bill Schumacher, Cerebral Power
** GNU Lesser General Public License Usage
** This file may be used under the terms of the GNU Lesser
** General Public License version 3 as published by the Free Software
** Foundation and appearing in the file LICENSE.LGPLv3 included in the
** packaging of this file. Please review the following information to
** ensure the GNU Lesser General Public License version 3 requirements
** will be met: https://www.gnu.org/licenses/lgpl.html.


    Some code copied from:
    https://github.com/maxcountryman/flask-login and https://github.com/mattupstate/flask-security  See LICENSE
"""
from flask import current_app, Blueprint, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import current_user
from werkzeug.local import LocalProxy
from jinja2 import Template
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text, create_engine, MetaData
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from ._compat import PY2, text_type
from sqlalchemy.engine.reflection import Inspector
# Find the stack on which we want to store the database connection.
# Starting with Flask 0.9, the _app_ctx_stack is the correct one,
# before that we need to use the _request_ctx_stack.
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

_page = LocalProxy(lambda: current_app.extensions['pages'])

_datastore = LocalProxy(lambda: _page.datastore)

_default_config = {
    'DATABASE': 'sqlite',
    'DATABASE_URI': 'sqlite:///page.db',
    'DATABASE_TABLE_PREFIX': 'fpages',
    'SUBDOMAIN': None,
    'URL_PREFIX': None,
    'BLUEPRINT_NAME': 'pages',
    'RENDER_URL': '/'
}


def get_config(app):
    """Conveniently get the pages configuration for the specified
    application without the annoying 'PAGES_' prefix.
    :param app: The application to inspect
    """
    items = app.config.items()
    prefix = 'PAGES_'

    def strip_prefix(tup):
        return tup[0].replace('PAGES_', ''), tup[1]

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def _get_state(app, datastore, **kwargs):
    for key, value in get_config(app).items():
        kwargs[key.lower()] = value

    kwargs.update(dict(
        app=app,
        datastore=datastore,
    ))

    return _PagesState(**kwargs)


class _PagesState(object):

    def __init__(self, **kwargs):
        self.blueprint_name = ""
        self.url_prefix = ""
        self.subdomain = ""
        for key, value in kwargs.items():
            setattr(self, key.lower(), value)


class Pages(object):

    def __init__(self, app=None, datastore=None, **kwargs):
        self.app = app
        self.datastore = datastore
        self._engine = None
        self._db = None
        if app is not None and datastore is not None:
            self._state = self.init_app(app, datastore, **kwargs)

    def init_app(self, app, datastore=None, register_blueprint=True):
        datastore = datastore or self.datastore
        if datastore is None:
            self._engine = create_engine('sqlite:///:memory:')
            Session = sessionmaker(bind=self._engine)
            self._db = Session()
            self.datastore = SQLAlchemyPageDataStore(self._db, page_model=PageModel)
            datastore = self.datastore
            Base.metadata.bind = self._engine
        inspector = Inspector.from_engine(self._engine)
        page_model_created = False
        for table_name in inspector.get_table_names():
            if self.datastore.page_model.__tablename__ == table_name:
                page_model_created = True

        if not page_model_created:
            Base.metadata.create_all()

        for key, value in _default_config.items():
            app.config.setdefault('PAGES_' + key, value)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        state = _get_state(app, datastore)

        if register_blueprint:
            app.register_blueprint(create_blueprint(state, __name__))
            # app.context_processor(_context_processor)

        state.render_template = self.render_template
        app.extensions['pages'] = state

        return state

    def render_template(self, *args, **kwargs):
        return render_template(*args, **kwargs)

    def __getattr__(self, name):
        return getattr(self._state, name, None)

    def connect(self):
        return SQLAlchemy(self.app)

    def teardown(self, exception):
        ctx = stack.top
        if hasattr(ctx, 'sqlite3_db'):
            ctx.sqlite3_db.close()

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'sqlite3_db'):
                ctx.sqlite3_db = self.connect()
            return ctx.sqlite3_db


class Datastore(object):
    def __init__(self, db):
        self.db = db

    def commit(self):
        pass

    def add(self, model):
        raise NotImplementedError

    def delete(self, model):
        raise NotImplementedError

    def create_all(self):
        raise NotImplementedError

    def drop_all(self):
        raise NotImplementedError


class SQLAlchemyDatastore(Datastore):
    def commit(self):
        self.db.commit()

    def add(self, model):
        self.db.add(model)
        self.commit()
        return model

    def delete(self, model):
        self.db.delete(model)

    def create_all(self):
        self.db.create_all()

    def drop_all(self):
        self.db.drop_all()


class PageDatastore(object):
    def __init__(self, page_model):
        self.page_model = page_model

    def _create_page_defaults(self, **kwargs):
        kwargs.setdefault('active', True)
        kwargs.setdefault('hidden', False)
        kwargs.setdefault('vertical', False)
        kwargs.setdefault('css_classes', 'nav')
        return kwargs

    def get_page(self, id_or_name):
        raise NotImplementedError

    def create_page(self, **kwargs):
        kwargs = self._create_page_defaults(**kwargs)
        page = self.page_model(**kwargs)
        return self.add(page)


class SQLAlchemyPageDataStore(SQLAlchemyDatastore, PageDatastore):
    """A SQLAlchemy datastore implementation for Flask-Pages that assumes the
    use of the Flask-SQLAlchemy extension.
    """
    def __init__(self, db, page_model):
        SQLAlchemyDatastore.__init__(self, db)
        PageDatastore.__init__(self, page_model)

    def get_page(self, identifier):
        if type(identifier) == int:
            return self.db.query(self.page_model).get(identifier)
        elif type(identifier) == str:
            return self.db.query(self.page_model).filter(self.page_model.name == identifier).first()
        return None


class PageMixin(object):
    """
    This provides default implementations for the methods that Flask-Pages expect Pages objects to have.
    """

    if not PY2:  # pragma: no cover
        # Python 3 implicitly set __hash__ to None if we override __eq__
        # We set it back to its default implementation
        __hash__ = object.__hash__

    def get_id(self):
        try:
            return text_type(self.id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

    def __eq__(self, other):
        """
        Checks the equality of two `PageMixin` objects using `get_id`.
        """
        if isinstance(other, PageMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        """
        Checks the inequality of two `PageMixin` objects using `get_id`.
        """
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal


def create_blueprint(state, import_name):
    """Creates the pages extension blueprint"""

    bp = Blueprint(state.blueprint_name, import_name,
                   url_prefix=state.url_prefix,
                   subdomain=state.subdomain,
                   template_folder='templates')

    return bp


def render_page(page=None):
    if page is not None:
        page_obj = _datastore.get_page(page)
        if page_obj:
            return page_template.render(page=page_obj, request_path=request.path, user=current_user, url_for=url_for)
    return """Page Not Found"""

page_metadata = MetaData()
Base = declarative_base(metadata=page_metadata)


class PageModel(Base):
    __tablename__ = 'fpages_page'
    id = Column(Integer(), primary_key=True)
    name = Column(String(256))


page_template = Template("")
