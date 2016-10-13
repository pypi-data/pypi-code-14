import datetime
import uuid
from mambo import (Mambo, models, nav_menu, page_meta, init_app,
                         route, get_config, session, request, redirect,
                         url_for, get, post, flash, flash_success, flash_error,
                         abort, recaptcha, storage)

from flask_login import fresh_login_required
from mambo.exceptions import AppError
from mambo import utils
from . import (current_user, authenticated, logout_user,
               is_authenticated, not_authenticated,
               require_login_allowed, require_signup_allowed,
               require_social_login_allowed,
               send_mail_password_reset, send_mail_verification_email,
               send_mail_signup_welcome,
               accepts_roles, accepts_admin_roles, accepts_manager_roles,
               visible_to_managers)
import arrow
import functools


def main(**kwargs):

    options = kwargs.get("options", {})
    nav_kwargs = kwargs.get("nav_menu", {})

    @nav_menu(title=nav_kwargs.pop("title", "User Admin") or "User Admin",
              visible=visible_to_managers,
              css_id=nav_kwargs.pop("css_id", "auth-user-admin-menu"),
              css_class=nav_kwargs.pop("css_class", "auth-user-admin-menu"),
              order=nav_kwargs.pop("order", 10),
              **nav_kwargs)
    class AuthAdmin(Mambo):
        base_route = kwargs.get("route") or "/users/"
        decorators = [authenticated, accepts_manager_roles] + kwargs.get("decorators")

        def _confirm_password(self):
            user_login = current_user.user_login("email")
            password = request.form.get("confirm-password")
            if not user_login.password_matched(password):
                raise AppError("Invalid password")
            return True

        @classmethod
        def _user_roles_options(cls):
            _r = models.AuthRole.query()\
                .filter(models.AuthRole.level <= current_user.role.level)\
                .order_by(models.AuthRole.level.desc())
            return [(r.id, r.name.upper()) for r in _r]

        @nav_menu("All Users")
        @get("/")
        def index(self):
            page_meta(title="All Users")

            per_page = get_config("PAGINATION_PER_PAGE", 25)

            page = request.args.get("page", 1)
            include_deleted = True if request.args.get("include-deleted") == "y" else False
            name = request.args.get("name")
            email = request.args.get("email")
            role = request.args.get("role")
            sorting = request.args.get("sorting", "name__asc")

            users = models.AuthUser.query(include_deleted=include_deleted)
            users = users.join(models.AuthRole).filter(models.AuthRole.level <= current_user.role.level)

            if name:
                users = models.AuthUser.search_by_name(users, name)
            if email:
                users = users.join(models.AuthUserLogin).filter(models.AuthUserLogin.email.contains(email))
            if role:
                users = users.filter(models.AuthUser.role_id == int(role))
            if sorting and "__" in sorting:
                col, dir = sorting.split("__", 2)
                if dir == "asc":
                    users = users.order_by(getattr(models.AuthUser, col).asc())
                else:
                    users = users.order_by(getattr(models.AuthUser, col).desc())

            users = users.paginate(page=page, per_page=per_page)

            sorting = [("name__asc", "Name ASC"),
                       ("name__desc", "Name DESC"),
                       ("first_name__asc", "First Name ASC"),
                       ("first_name__desc", "First Name DESC"),
                       ("last_name__asc", "Last Name ASC"),
                       ("last_name__desc", "Last Name DESC"),
                       ("email__asc", "Email ASC"),
                       ("email__desc", "Email DESC"),
                       ("created_at__asc", "Signup ASC"),
                       ("created_at__desc", "Signup DESC"),
                       ("last_login__asc", "Login ASC"),
                       ("last_login__desc", "Login DESC")]
            return dict(user_roles_options=self._user_roles_options(),
                        sorting_options=sorting,
                        users=users,
                        search_query={
                            "include-deleted": request.args.get("include-deleted", "n"),
                            "role": int(request.args.get("role")) if request.args.get("role") else "",
                            "status": request.args.get("status"),
                            "name": request.args.get("name", ""),
                            "email": request.args.get("email", ""),
                            "sorting": request.args.get("sorting")})

        @nav_menu("User Info", visible=False)
        def info(self, id):
            page_meta(title="User Info")
            user = models.AuthUser.get(id, include_deleted=True)
            if not user:
                abort(404, "User doesn't exist")

            if current_user.role.level < user.role.level:
                abort(403, "Not enough rights to access this user info")

            return {
                "user": user,
                "user_roles_options": self._user_roles_options()
            }

        @post()
        def save(self):
            id = request.form.get("id")
            action = request.form.get("action")

            try:
                user = models.AuthUser.get(id, include_deleted=True)

                if not user:
                    abort(404, "User doesn't exist or has been deleted!")
                if current_user.role.level < user.role.level:
                    abort(403, "Not enough power level to update this user info")

                if current_user.id != user.id:
                    if action == "activate":
                        user.update(active=True)
                        flash_success("User has been ACTIVATED")
                    elif action == "deactivate":
                        user.update(active=False)
                        flash_success("User is now DEACTIVATED")
                    elif action == "delete":
                        user.delete()
                        flash_success("User has been DELETED")
                    elif action == "undelete":
                        user.delete(False)
                        flash_success("User is now RESTORED")

                if action == "info":
                    data = {
                        "name": request.form.get("name"),
                        "first_name": request.form.get("first_name"),
                        "last_name": request.form.get("last_name"),
                        "address": request.form.get("address"),
                        "address_city": request.form.get("address_city"),
                        "address_state": request.form.get("address_state"),
                        "address_country": request.form.get("address_country"),
                        "address_zip_code": request.form.get("address_zip_code"),
                        "telephone": request.form.get("telephone"),
                    }
                    dob = request.form.get("dob")
                    if dob:
                        data["date_of_birth"] = arrow.get(dob, models.AuthUser.DOB_FORMAT).datetime

                    if current_user.id != user.id:
                        user_role = request.form.get("user_role")
                        _role = models.AuthRole.get(user_role)
                        if not _role:
                            raise AppError("Invalid ROLE selected")
                        data["role"] = _role

                    user.update(**data)
                    flash_success("User info updated successfully!")

                elif action == "email":
                    user_login = user.get_email_login()
                    if not user_login:
                        raise AppError("This account doesn't have an email login type")
                    email = request.form.get("email")
                    if email != user_login.email:
                        user_login.change_email(email)
                        flash_success("Email '%s' updated successfully!" % email)
            except AppError as ae:
                flash_error(ae.message)
            return redirect(self.info, id=id)

        @post()
        def create(self):
            try:
                email = request.form.get("email")
                data = {
                    "name": request.form.get("name"),
                    "first_name": request.form.get("first_name"),
                    "last_name": request.form.get("last_name"),
                    "address": request.form.get("address"),
                    "address_city": request.form.get("address_city"),
                    "address_state": request.form.get("address_state"),
                    "address_country": request.form.get("address_country"),
                    "address_zip_code": request.form.get("address_zip_code"),
                    "telephone": request.form.get("telephone"),
                }
                dob = request.form.get("dob")
                if dob:
                    data["date_of_birth"] = arrow.get(dob, models.AuthUser.DOB_FORMAT).datetime

                user_role = request.form.get("user_role")
                _role = models.AuthRole.get(user_role)
                if not _role:
                    raise AppError("Invalid ROLE selected")
                data["role"] = _role.name

                new_user = models.AuthUserLogin.new(login_type=models.AuthUserLogin.TYPE_EMAIL,
                                                   email=email,
                                                   user_info=data)
                if new_user:
                    flash_success("New account created successfully!")
                    return redirect(self.info, id=new_user.user.id)
                else:
                    raise AppError("Account couldn't be created")
            except AppError as ae:
                flash_error(ae.message)

            return redirect(self.index)


        @nav_menu("User Roles", order=2)
        @get()
        @post()
        @accepts_admin_roles
        def roles(self):
            """
            Only admin and super admin can add/remove roles
            RESTRICTED ROLES CAN'T BE CHANGED
            """
            roles_max_range = 11
            if request.method == "POST":
                try:
                    id = request.form.get("id")
                    name = request.form.get("name")
                    level = request.form.get("level")
                    action = request.form.get("action")

                    if name and level:
                        level = int(level)
                        name = name.upper()
                        _levels = [r[0] for r in models.AuthRole.ROLES]
                        _names = [r[1] for r in models.AuthRole.ROLES]
                        if level in _levels or name in _names:
                            raise AppError("Can't modify PRIMARY Roles - name: %s, level: %s " % (name, level))
                        else:
                            if id:
                                role = models.AuthRole.get(id)
                                if role:
                                    if action == "delete":
                                        role.delete()
                                        flash_success("Role '%s' deleted successfully!" % role.name)
                                    elif action == "update":
                                        if role.level != level and models.AuthRole.get_by_level(level):
                                            raise AppError("Role Level '%s' exists already" % level)
                                        elif role.name != name and models.AuthRole.get_by_name(name):
                                            raise AppError("Role Name '%s'  exists already" % name)
                                        else:
                                            role.update(name=name, level=level)
                                            flash_success("Role '%s (%s)' updated successfully" % (name, level))
                                else:
                                    raise UserError("Role doesn't exist")
                            else:
                                if models.AuthRole.get_by_level(level):
                                    raise AppError("Role Level '%s' exists already" % level)
                                elif models.AuthRole.get_by_name(name):
                                    raise AppError( "Role Name '%s'  exists already" % name)
                                else:
                                    models.AuthRole.new(name=name, level=level)
                                    flash_success("New Role '%s (%s)' addedd successfully" % (name, level))
                except AppError as ex:
                    flash_error("%s" % ex.message)
                return redirect(self.roles)

            page_meta(title="User Roles")
            roles = models.AuthRole.query().order_by(models.AuthRole.level.desc())

            allocated_levels = [r.level for r in roles]
            levels_options = [(l, l) for l in range(1, roles_max_range) if l not in allocated_levels]

            return {
                    "roles": roles,
                    "levels_options": levels_options
                    }

        @post()
        def reset_password(self):
            id = request.form.get("id")
            user = models.AuthUser.get(id)

            if not user:
                abort(404, "User doesn't exist or has been deleted!")
            try:
                user_login = user.get_email_login()
                if not user_login:
                    raise AppError("This account doesn't have an email login type")
                send_mail_password_reset(user_login)
            except AppError as ae:
                flash_error(ae.message)

            return redirect(self.info, id=id)


    return AuthAdmin



