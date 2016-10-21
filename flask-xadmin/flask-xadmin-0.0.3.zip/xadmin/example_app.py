# -*- coding: utf-8 -*-
# __author__ = 'dsedad'

from flask import Flask, redirect

# Import SQLAlchemy Models for User, Role, custom models ... and db instance
from db.models import User, Role, Bank, db

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


APP_ADMIN_SECRET_KEY='afdaodfadoiusgljdsgaspoiupowqefflksdafj'
app = Flask(__name__)
app.secret_key = APP_ADMIN_SECRET_KEY
app.config.update(SESSION_COOKIE_NAME='session-{}'.format(__name__))

from xadmin.xadm_lib import xAdminIndexView, xEditModeView, current_edit_mode, xModelView, xFileAdmin
from xadmin import xadm_app, gen_xadmin

class myModelView(xModelView):
    # Customize your generic model -view
    pass

class myFileAdmin(xFileAdmin):
    # Customize your File Admin model -view
    pass


app.register_blueprint(xadm_app)

# IMPORTANT: Authorized users should have granted xadmin_superadmin role

# Prepare view list
views = [
    myModelView(model=User, session=db.session, category='Users'),
    myModelView(model=Role, session=db.session, category='Users'),
    myFileAdmin(base_path='/', name="Temp files", category='Files')]

# Make an instance of xadmin
xadmin = gen_xadmin(app = app, title = 'MyProduct', db=db, user_model=User, role_model=Role, views=views)

@app.route('/')
def home():
    return redirect('/admin')

if __name__ == "__main__":
    app.run(debug=True, port=8001)
    print('Try url: /admin')
