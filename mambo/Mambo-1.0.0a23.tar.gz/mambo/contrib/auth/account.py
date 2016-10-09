import datetime
import uuid
from mambo import (Mambo, models, nav_menu, page_meta, init_app,
                         route, get_config, session, request, redirect,
                         url_for, get, post, flash_success, flash_error,
                         abort, recaptcha, storage)

from flask_login import fresh_login_required
from mambo.exceptions import AppError
from mambo import utils
from . import (current_user, authenticated, logout_user,
               is_authenticated, not_authenticated, require_login_allowed,
               require_signup_allowed, require_social_login_allowed,
               send_mail_password_reset, send_mail_verification_email,
               send_mail_signup_welcome, session_set_require_password_change)
import arrow


def main(**kwargs):

    options = kwargs.get("options", {})
    nav_title_partial = "AuthAccount/nav_title_partial.html"
    nav_kwargs = kwargs.get("nav_menu", {})
    verify_email = options.get("verify_email") or False

    @nav_menu(title=nav_kwargs.pop("title", "My Account") or "My Account",
              visible=is_authenticated,
              css_id=nav_kwargs.pop("css_id", "auth-account-menu"),
              css_class=nav_kwargs.pop("css_class", "auth-account-menu"),
              align_right=nav_kwargs.pop("align_right", True),
              title_partial=nav_kwargs.pop("title_partial", nav_title_partial),
              **nav_kwargs)
    class AuthAccount(Mambo):
        base_route = kwargs.get("route") or "/"
        decorators = Mambo.decorators + [authenticated] + kwargs.get("decorators")

        def _confirm_password(self):
            user_login = current_user.user_login("email")
            password = request.form.get("confirm-password")
            if not user_login.password_matched(password):
                raise AppError("Invalid password")
            return True

        @nav_menu("Logout", endpoint="AuthLogin:logout", order=100)
        def _(self):
            pass

        @nav_menu("Account Info", order=1)
        def account_info(self):
            page_meta(title="Account Info")

        @nav_menu("Edit Account Info", visible=False)
        @get()
        @post()
        def edit_account_info(self):
            page_meta(title="Edit Account Info")

            if request.method == "POST":
                try:
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
                    current_user.update(**data)

                    flash_success("Account info updated successfully!")

                except AppError as ae:
                    flash_error(ae.message)
                return redirect(self.account_info)

        @nav_menu("Change Login", order=2)
        @get()
        @post()
        def change_email(self):
            page_meta(title="Change Login Email")

            user_login = current_user.user_login("email")
            if not user_login:
                abort(400, "Require and Email account login to continue")

            if request.method == "POST":
                try:
                    self._confirm_password()

                    email = request.form.get("email")
                    if utils.is_email_valid(email):
                        user_login.change_email(email)
                        flash_success("Login Email changed successfully!")
                        return redirect(self.account_info)
                    else:
                        raise AppError("Invalid email")
                except AppError as ex:
                    flash_error("Error: %s" % ex)
                    return redirect(self.change_email)

            return {
                "user_login": user_login
            }

        @nav_menu("Change Password", order=3)
        @get()
        @post()
        def change_password(self):
            page_meta(title="Change Password")

            user_login = current_user.user_login("email")
            if not user_login:
                abort(400, "Require and Email account login to continue")

            if request.method == "POST":
                try:
                    self._confirm_password()
                    password = request.form.get("password")
                    password2 = request.form.get("password2")
                    if password != password2:
                        raise AppError("Passwords don't match")
                    elif utils.is_password_valid(password):
                        user_login.change_password(password.strip())
                        session_set_require_password_change(False)
                        flash_success("Password updated successfully!")
                        return redirect(self.account_info)
                    else:
                        raise AppError("Invalid password")
                except AppError as ex:
                    flash_error("Error: %s" % ex)
                    return redirect(self.change_password)

        @nav_menu("Change Profile Image", order=4)
        @get()
        @post()
        def change_profile_image(self):
            page_meta(title="Change Profile Image")

            if request.method == "POST":
                file = request.files.get("file")
                if file:
                    name = "%s" % uuid.uuid4().hex
                    extensions = ["jpg", "jpeg", "png", "gif"]
                    my_photo = storage.upload(file,
                                              name=name,
                                              prefix="profile-images/",
                                              allowed_extensions=extensions)
                    if my_photo:
                        url = my_photo.url
                        current_user.update(profile_image_url=url)
                        flash_success("Profile Picture updated successfully!")
                return redirect(self.account_info)

        @nav_menu("Setup Login", visible=False)
        @get()
        @post()
        def setup_login(self):
            user_login = current_user.user_login("email")
            if user_login:
                return redirect(self.account_info)

            if request.method == "POST":
                try:
                    email = request.form.get("email")
                    password = request.form.get("password")
                    password2 = request.form.get("password2")

                    if not password.strip() or password.strip() != password2.strip():
                        raise AppError("Passwords don't match")
                    else:
                        new_login = models.AuthUserLogin.new(login_type="email",
                                                         user_id=current_user.id,
                                                         email=email,
                                                         password=password.strip())
                        if verify_email:
                            send_mail_signup_welcome(new_login)
                            flash_success("A welcome email containing a confirmation link has been sent to %s" % email)
                            return redirect(self.account_info)
                except AppError as ex:
                    flash_error(ex.message)
                return redirect(self.setup_login)

    return AuthAccount



