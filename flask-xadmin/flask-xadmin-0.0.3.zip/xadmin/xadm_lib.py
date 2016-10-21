# -*- coding: utf-8 -*-
# __author__ = 'dsedad'

from uuid import uuid4

import inspect

from xadm_salib import *
from flask import flash
from flask import redirect
from flask import request
from flask import url_for
from flask import session
from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.admin.helpers import get_redirect_target
from flask.ext.admin.form import FormOpts
from flask_admin.model.base import get_mdict_item_or_list
from flask.ext.security import current_user, logout_user
from flask.ext.admin import Admin, expose, AdminIndexView, BaseView
from sqlalchemy.ext.declarative import AbstractConcreteBase
from flask.ext.admin.contrib.fileadmin import FileAdmin

XADMIN_SUPERADMIN="xadmin_superadmin"
LIST_TEMPLATE = 'admin/models/custom_list.html'
FILE_LIST_TEMPLATE = 'admin/files/custom_file_list.html'
DETAILS_TEMPLATE = 'admin/models/custom_details.html'
EDIT_TEMPLATE = 'admin/models/custom_edit.html'
CREATE_TEMPLATE = 'admin/models/custom_create.html'

PAGE_SIZE = 10

def super_admin(user):
    return user.has_role(XADMIN_SUPERADMIN)

def current_edit_mode():
    return session.get('xadm_edit_mode', False)

def set_edit_mode(mode):
    session['xadm_edit_mode'] = mode

class BaseClass(AbstractConcreteBase):
    # table page size
    page_size = PAGE_SIZE
    details_modal = False

    def is_accessible(self):
        if current_user.is_authenticated():
            return super_admin(current_user)

    list_template = LIST_TEMPLATE
    details_template = DETAILS_TEMPLATE
    edit_template = EDIT_TEMPLATE
    create_template = CREATE_TEMPLATE


class xModelView(BaseClass, ModelView):
    column_display_pk = True
    read_only = False

    def set_permissions(self, edit_mode):
        """
        edit_mode == True => allow edit, delete, create. Otherwise prevent edit, delete, create.
        :return:
        """
        if not(edit_mode):
            self.can_create = False
            self.can_edit = False
            self.can_delete = False
            self.can_view_details = True
        else:
            if (hasattr(self, 'read_only') and self.read_only):
                self.can_create = False
                self.can_edit = False
                self.can_delete = False
                self.can_view_details = True
            else:
                self.can_create = True
                self.can_edit = True
                self.can_delete = True
                self.can_view_details = True
                    # return dict(edit_mode=True)
    def doc(self):
        return inspect.getdoc(self.model).strip()

    @expose('/details/', methods=('GET', 'POST'))
    def details_view(self):

        return_url = get_redirect_target() or self.get_url('.index_view')
        id = get_mdict_item_or_list(request.args, 'id')
        if id is None:
            return redirect(return_url)
        model = self.get_one(id)
        if model is None:
            return redirect(return_url)
        form = self.edit_form(obj=model)
        form_opts = FormOpts(widget_args=self.form_widget_args,
                             form_rules=self._form_edit_rules)

        self.on_form_prefill(form, id)

        return self.render(self.details_template,
                           model=model,
                           form=form,
                           form_opts=form_opts,
                           return_url=return_url)

    def scaffold_list_filters(self):
        cols = self.scaffold_list_columns()
        # Columns
        res_cols = []
        # Relationships
        res_rels = []
        for c in cols:
            col_type = sa_column_type(self.model, c)
            if col_type is None:
                res_rels.append(c)
            elif sa_column_type(self.model, c) not in ('guid', 'largebinary'):
                res_cols.append(c)
        # Filter show list of columns, then list of relationships
        return res_cols + res_rels

    def get_form_columns(self, directions=[MANYTOMANY, ONETOMANY]):
        return self.scaffold_list_columns() + sa_relationships_keys(self.model, directions=directions)

    def get_column_searchable_list(self):
        return sa_column_searchable_list(self.model)

    def get_column_list(self):
        return self.scaffold_list_columns()

    def get_column_list_filters(self):
        return self.scaffold_list_filters()

    def get_column_descriptions(self):
        return sa_column_descriptions(self.model)

    def get_column_formatters(self):
        return gen_href_formatter(self.model)

    def get_column_details_list(self):
        return self.get_form_columns(directions=[MANYTOMANY, ONETOMANY])

    def __init__(self, *args, **kwargs):
        # if not(self.column_formatters):
        #    self.column_formatters = gen_href_formatter(model, relationship_names=['log_create_user'])
        self.model = kwargs.get('model')
        if not self.model:
            self.model = args[0]

        ahref_fmt = '<a href="#" data-toggle="modal" title="View Record" data-target="#fa_modal_window" data-remote="%s&modal=True">%s</a>'
        if not getattr(self, "column_formatters"):
            formatters = dict(self.get_column_formatters())
            self.column_formatters = formatters

        if not getattr(self, "column_descriptions"):
            self.column_descriptions = self.get_column_descriptions()

        if not getattr(self, "column_filters"):
            self.column_filters = self.get_column_list_filters()
            pass

        if not getattr(self, "column_list"):
            self.column_list = self.get_column_list()

        if not getattr(self, "column_searchable_list"):
            self.column_searchable_list = self.get_column_searchable_list()

        if not getattr(self, "form_columns"):
            self.form_columns = self.get_form_columns(directions=[MANYTOMANY, ONETOMANY])

        if not getattr(self, "column_details_list"):
            self.column_details_list = self.get_column_details_list()

        super(xModelView, self).__init__(*args, **kwargs)


class xAdminIndexView(AdminIndexView):
    @expose('/')
    def index(self):
        return super(xAdminIndexView, self).index()

    @expose('/logout/')
    def logout_view(self):
        set_edit_mode(False)
        logout_user()
        return redirect(url_for('.index'))


class xEditModeView(BaseView):
    def is_accessible(self):
        if current_user.is_authenticated():
            return super_admin(current_user)
        return False

    def is_visible(self):
        return False

    @expose('/', methods=('GET', 'POST'))
    def change_mode(self):
        from flask.ext.security.utils import verify_and_update_password
        if request.method == 'GET':
            return self.render('admin/edit_mode.html')
        else:
            password = request.form['password']

            if verify_and_update_password(password, current_user):
                session['xadm_edit_mode'] = True
                flash(u'You are in EDIT mode. Be wise and careful!')
                return redirect('/')
                #return self.render('index.html')
            else:
                flash(u'Wrong password', category='error')
                return self.render('admin/edit_mode.html')

    @expose('/leave_edit', methods=['GET'])
    def leave_edit(self):
        try:
            session['xadm_edit_mode'] = False
        except:
            pass
        flash(u"You've left EDIT mode.")
        return redirect('/')

# Custom base file admin class
class xFileAdmin(FileAdmin):
    list_template = FILE_LIST_TEMPLATE
    read_only = False
    def doc(self):
        return ""

    def is_accessible(self):
        if current_user.is_authenticated():
            return super_admin(current_user)
        return False

    def set_permissions(self, edit_mode):
        """
        edit_mode == True => allow edit, delete, create. Otherwise prevent edit, delete, create.
        :return:
        """
        if not (edit_mode):
            self.can_download = True
            self.can_mkdir = False
            self.can_delete_dirs = False
            self.can_delete = False
            self.can_rename = False
            self.can_upload = False
        else:
            if (hasattr(self, 'read_only') and self.read_only):
                self.can_download = True
                self.can_mkdir = False
                self.can_delete_dirs = False
                self.can_delete = False
                self.can_rename = False
                self.can_upload = False
            else:
                self.can_download = True
                self.can_mkdir = True
                self.can_delete_dirs = True
                self.can_delete = True
                self.can_rename = True
                self.can_upload = True
                # return dict(edit_mode=True)
