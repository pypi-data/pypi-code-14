
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

    class ContactPage(Mambo):
        base_route = "/"
        decorators = Mambo.decorators + kwargs.get("decorators")

        @nav_menu(**navigation)
        @get("contact/")
        @post("contact/")
        def index(self):

            # Email to
            send_to = options.get("send_to", get_config("CONTACT_EMAIL", None))

            if not send_to:
                abort(500, "ContactPage missing email recipient")

            if request.method == "POST":
                email = request.form.get("email")
                subject = request.form.get("subject")
                message = request.form.get("message")
                name = request.form.get("name")

                success_message = options.get("success_message", "Message sent. Thank you!")
                return_to = options.get("return_to", None)
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
                                flash_data("emit_contact_page_email_sent")
                            except Exception as ex:
                                logging.exception(ex)
                                raise AppError("Unable to send email")
                    else:
                        raise AppError("Security code is invalid")
                except AppError as e:
                    flash_error(e.message)
                return redirect(return_to or self)

            title = options.get("title", "Contact Us")
            page_meta(title=title)


            return {
                "title": title,
                "email_sent_successful": True if "emit-contact-page-email-sent" in get_flash_data() else False
            }

    return ContactPage


