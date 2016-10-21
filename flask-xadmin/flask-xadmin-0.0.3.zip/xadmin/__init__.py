# -*- coding: utf-8 -*-
from flask import Blueprint, redirect
from flask.ext.security import Security, SQLAlchemyUserDatastore
from flask.ext.admin import Admin
from xadm_lib import xAdminIndexView, xEditModeView, xModelView, current_edit_mode
xadm_app = Blueprint('xadm_app', __name__, template_folder='templates')

# wrap admin
def gen_xadmin(app, title, db, user_model, role_model, views=[]):
    db.init_app(app)

    # init_login()
    user_datastore = SQLAlchemyUserDatastore(db=db, user_model=user_model, role_model=role_model)
    security = Security(app, user_datastore)
    xadmin = Admin(app, title, index_view=xAdminIndexView(), base_template='index.html')

    for v in views:
        xadmin.add_view(v)

    # Add view for enter/leave edit mode
    xadmin.add_view(xEditModeView(name='EditMode'))

    return xadmin

@xadm_app.before_app_request
def reset_views():
    """ Before each request - reset permissions for views, regarding edit_mode """
    from flask import current_app
    admins = current_app.extensions.get('admin', [])
    for adm in admins:
        for v in adm._views:
            if hasattr(v, 'set_permissions'):
                v.set_permissions(current_edit_mode())


@xadm_app.errorhandler(403)
def page_not_found(e):
    return redirect('/')
