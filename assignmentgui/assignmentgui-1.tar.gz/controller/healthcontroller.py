from model.datum import Datum


# controller for health data
class HealthController:
    # display the health data
    def display_health(self,name):
        s=Datum()
        detail=s.display(name)
        return detail

    # insert new health data
    def insert_health(self,name, property_id, value,datum_id):
        s=Datum()
        message=s.datum(name, property_id, value,datum_id)
        return message

    # display the health data of friend
    def display_friend_health(self,name,friend):
        s=Datum()
        detail=s.display_friend_info(name,friend)
        return detail