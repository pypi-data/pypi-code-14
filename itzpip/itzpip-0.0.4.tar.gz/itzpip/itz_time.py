import time


class itz_time:
    now = time.time()
    
    def __init__(self):
        pass
    
    def get_timestamp_new(self):
        return int(self.now)

    def get_timestamp_today(self):
        return int(self.now//86400*86400-28800)
    
    def get_date_now(self):
        return time.strftime('%Y-%m-%d', time.localtime(self.now))
    
    def get_date_yestoday(self):
        return time.strftime('%Y-%m-%d', time.localtime(self.get_timestamp_today()-1))        
    

if __name__ == "__main__":
    it = itz_time()
    print (it.get_timestamp_new())
    print (it.get_date_now())
    print (it.get_timestamp_today())
    print (it.get_date_yestoday())