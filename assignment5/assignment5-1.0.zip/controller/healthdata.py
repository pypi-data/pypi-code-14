from model import healthdata
from view import success,health

class healthdata_control:
    def healthdata(healthdata_window,username,entries):
        healthdata.healthdata_model.healthdata_entry1(username,entries[0].get())
        healthdata.healthdata_model.healthdata_entry2(username,entries[1].get())
        success.success.success_msg(healthdata_window)

    def get_healthdata(friends_window,username):
        health_detail=[]
        data=healthdata.healthdata_view.get_health(username.get())
        if len(data)!=0:
            for i in data[0]:
                health_detail.append(i)
            for i in data[1]:
                health_detail.append(i)
        else:
            health_detail.append(0)
            health_detail.append(0)
        #print(health_detail)
        health.healthdata_class.print_health(friends_window,health_detail)

class friend_health_control:
    def get_friends(username):
        list1=[]
        data1=healthdata.health_friend.get_friends1(username)
        data2=healthdata.health_friend.get_friends2(username)
        if len(data1)!=0:
            for data in data1[0]:
                list1.append(data)
        elif len(data2) != 0:
            for data in data2[0]:
                list1.append(data)
        return list1