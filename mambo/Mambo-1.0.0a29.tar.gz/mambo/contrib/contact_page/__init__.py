
"""
Contact Page
"""
from mambo import (Mambo, page_meta, get_config, abort, get, post,
                    flash_success, flash_error, flash_data, get_flash_data,
                   register_package, redirect, request, url_for, send_mail,
                   recaptcha, nav_menu, route)
from mambo.exceptions import AppError
import mambo.utils as utils
import logging

# app_data
app_data = None
try:
    from mambo.contrib.app_data import AppData
    app_data = AppData("ContactPage")
except ImportError as e:
    pass


register_package(__package__)

__version__ = "1.0.0"

def main(**kwargs):
    """
        - config:
            - send_to
            - return_to
            - title
            - success_message
    """

    navigation = kwargs.get("nav_menu", {})
    navigation.setdefault("title", "Contact")
    navigation.setdefault("visible", True)
    navigation.setdefault("order", 100)

    options = kwargs.get("options", {})

    if app_data:
        if options.get("recipients") \
                and not app_data.has("recipients"):
            app_data.set(key="recipients",
                         value=options.get("recipients"),
                         description="Contact page recipients. Separated by comma")


    class ContactPage(Mambo):
        base_route = "/"
        decorators = Mambo.decorators + kwargs.get("decorators")

        @nav_menu(**navigation)
        @get("contact/")
        @post("contact/")
        def index(self):

            # Email to
            if app_data and app_data.get("recipients"):
                send_to = app_data.get("recipients")
            else:
                send_to = options.get("recipients", get_config("CONTACT_EMAIL", None))

            success_message = options.get("success_message", "Message sent. Thank you!")

            return_to = options.get("return_to", None)
            if return_to:
                if "/" not in return_to:
                    return_to = url_for(return_to)
            else:
                return_to = url_for(self)

            if not send_to:
                abort(500, "ContactPage missing email recipient")

            if request.method == "POST":
                email = request.form.get("email")
                subject = request.form.get("subject")
                message = request.form.get("message")
                name = request.form.get("name")

                try:
                    if recaptcha.verify():
                        if not email or not subject or not message:
                            raise AppError("All fields are required")
                        elif not utils.is_email_valid(email):
                            raise AppError("Invalid email address")
                        else:
                            try:
                                send_mail(to=send_to,
                                          reply_to=email,
                                          mail_from=email,
                                          mail_subject=subject,
                                          mail_message=message,
                                          mail_name=name,
                                          template=options.get("template", "contact-us.txt")
                                          )
                                flash_data("ContactPage:EmailSent")
                            except Exception as ex:
                                logging.exception(ex)
                                raise AppError("Unable to send email")
                    else:
                        raise AppError("Security code is invalid")
                except AppError as e:
                    flash_error(e.message)
                return redirect(self)

            title = options.get("title", "Contact Us")
            page_meta(title=title)

            fd = get_flash_data()
            return {
                "title": title,
                "email_sent": True if fd and "ContactPage:EmailSent" in fd else False,
                "success_message": success_message,
                "return_to": return_to
            }

    return ContactPage


