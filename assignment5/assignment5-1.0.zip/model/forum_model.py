import pymysql
import datetime

def get_usertype(username):
    try:
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        mycursor.execute("Select UserTypeID from User WHERE Username=%s and Status=1",username)
        idtype = mycursor.fetchone()
        mycursor.close()
        con.close()
        return idtype
    except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT
        print("iderror")

def get_forum_id():
    try:
        connection = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = connection.cursor()
        #SELECT LIST OF ALL ACTIVE FORUMS ....................
        mycursor.execute("SELECT ForumID FROM forum WHERE WhenClosed is null")
        forum_list=mycursor.fetchall()
        return forum_list
    except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
        #raise RuntimeError("warning")
        print("select error")

def get_post_id(forumid):
    try:
        connection = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = connection.cursor()
        #SELECT LIST OF ALL ACTIVE posts ....................
        mycursor.execute("Select Username from post where ForumID=%s", forumid)
        post_list=mycursor.fetchall()
        return post_list
    except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
        #raise RuntimeError("warning")
        print("select error")

def get_post_entry(forumid):
    try:
        connection = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = connection.cursor()
        #SELECT LIST OF ALL ACTIVE posts entry ....................
        mycursor.execute("Select TextEntry from post where ForumID=%s", forumid)
        post_list=mycursor.fetchall()
        return post_list
    except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
        #raise RuntimeError("warning")
        print("select error")

def new_post(username, forumid, txt, photo, link, video):
    try:
        now = str(datetime.datetime.now())
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        # INSERTION INTO POST TABLE....................
        a = "insert into post (Username,TimeCreated,ForumID,TextEntry,PhotoLocation,LinkLocation,VideoLocation) " \
            "VALUES(%s,%s,%s,%s,%s,%s,%s) "
        mycursor.execute(a, (username, now, forumid, txt, photo, link, video))
        con.commit()
        mycursor.close()
        con.close()
    except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
        print("Input post error")


def new_forum(forum_id, topic, url, summary, username):
    try:
        now = str(datetime.datetime.now())
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        # INSERTION INTO FORUM WHENEVER A FORUM IS STARTED....................
        a = "Insert into forum (ForumID,Topic,URL,Summary,WhenCreated,CreatedByModerator_Username)" \
            " VALUES (%s,%s,%s,%s,%s,%s)"
        mycursor.execute(a, (forum_id, topic, url, summary, now, username))
        con.commit()
        print("Success")
        mycursor.close()
        con.close()
    except:
        print("start forum eroor")

def del_forum(forumid,username):
    try:
        now = str(datetime.datetime.now())
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        # UPDATE FORUM WHEN MODERATOR WISH TO CLOSE A FORUM....................
        mycursor.execute("update forum SET WhenClosed=%s and DeletedByModerator_Username=%s where ForumID=%s",
                         (now, username, forumid))
        con.commit()
        mycursor.close()
        con.close()
    except:  # TO THROW AWAY ERRORS DUE TO WRONG INPUT
        print("Invalid forumID entry")

def new_comment(username,forumid,post_sel,txt,photo,link,video):
    try:
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        now = str(datetime.datetime.now())
        #SELECT TIME FROM POST TABLE....................
        mycursor.execute("Select TimeCreated from post where ForumID=%s and Username=%s",(forumid,post_sel))
        post_time=mycursor.fetchone()
        #INSERT INTO COMMENT TABLE....................
        a= "insert into comment (Post_Username,Post_TimeCreated,Commenter_Username,CommentTime,CommentText," \
           "PhotoLocation,LinkLocation,VideoLocation) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) "
        mycursor.execute(a, (post_sel,post_time[0],username,now,txt,photo,link,video))
        con.commit()
        mycursor.close()
        con.close()
    except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT....................
        print("Input post error")

def new_rating(username,forumid,post_sel,user_star):
    try:
        con = pymysql.connect(user='root', password='1994', host='127.0.0.1', database='smarthealthdb')
        mycursor = con.cursor()
        #INSERTION INTO RATING TABLE....................
        mycursor.execute("Select TimeCreated from post where ForumID=%s and Username=%s",(forumid,post_sel))
        post_time=mycursor.fetchone()
        #INSERT INTO RATING TABLE....................
        a= "insert into rating (Post_Username,Post_TimeCreated,Rater_Username,Stars) VALUES(%s,%s,%s,%s) "
        mycursor.execute(a, (post_sel,post_time[0],username,user_star))
        con.commit()
        mycursor.close()
        con.close()
    except:#TO THROW AWAY ERRORS DUE TO WRONG INPUT
        print("Input post error")

