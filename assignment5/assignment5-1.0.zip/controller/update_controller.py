from model import update_model
from view import update_view,success

class update_control:
    def get_usertype(master,top_profile,top_update,username):
        usertype=update_model.update_model.get_usertype(username)
        if(usertype[0]==1):
            update_view.update_view.make_form_enduser(master,top_profile,top_update,username)

        elif(usertype[0]==2):
            update_view.update_view.make_form_moderator(master,top_profile,top_update,username)

        elif(usertype[0]==3):
            update_view.update_view.make_form_admin(master,top_profile,top_update,username)

    def update_password(master,top_profile,top_update,password,username):
        update_model.update_model.update_Password(password.get(),username)
        success.success.login_again(master)
        top_update.destroy()
        top_profile.destroy()

    def update_Email1(master,Email1,username):
        update_model.update_model.update_Email1(Email1.get(),username)
        success.success.success_update(master)

    def update_Email2(master,Email2,username):
        update_model.update_model.update_Email2(Email2.get(),username)
        success.success.success_update(master)

    def update_FirstName(master,FirstName,username):
        update_model.update_model.update_FirstName(FirstName.get(),username)
        success.success.success_update(master)

    def update_LastName(master,LastName,username):
        update_model.update_model.update_LastName(LastName.get(),username)
        success.success.success_update(master)
