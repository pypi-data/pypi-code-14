from model import user_data
from view import user_profile,success

class user_page:
    def user_prof(master,top_profile,username):
        detail=[]
        count=0
        user_details=user_data.get_user_data(username)
        for data in user_details[count]:
            count+=1
            if(count>2 and count<16):
                detail.append(data)

        user_profile.user_details.user_detail_page(master,top_profile,username,detail)

    def del_user(master,top_profile,username):
        user_data.del_userdetail(username)
        success.success.del_msg(master,top_profile)