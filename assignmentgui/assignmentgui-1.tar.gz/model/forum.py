from model.connection import connection
import datetime
import pymysql
import uuid


class ForumModel(object):
    # init function calling object of connection class to create a cursor
    def __init__(self):
        connect = connection()
        self.insert = connect.initial()

    def forum(self, topic, url, summary, f_author, forum_id=None):
        # first author who is creating the function
        self.f_author = f_author
        self.topic = topic
        self.url = url
        self.summary = summary
        # self.when_created = datetime.datetime.utcnow()
        self.forum_id = uuid.uuid4().hex if forum_id is None else forum_id
        # self.forum_active = 1;

        connect =connection()
        self.insert = connect.initial()

        # Check if the user is moderator

        with self.insert.cursor() as cursor:
            sql = "SELECT Username from User WHERE Username=%s and UserTypeID = 2 "
            cursor.execute(sql, (self.f_author,))
            result = cursor.fetchone()
            #if the moderator exists
            if result is not None:
                try:
                    with self.insert.cursor() as cursor:
                        when_created = datetime.datetime.utcnow()
                        # now = datetime.datetime.now().date()
                        sql = "INSERT INTO Forum ( ForumID, Topic, URL, Summary, WhenCreated, " \
                              "CreatedByModerator_Username)" \
                              " VALUES ( %s,%s,%s,%s,%s,%s)"
                        cursor.execute(sql, (self.forum_id, self.topic, self.url, self.summary,
                                             when_created, self.f_author,))
                    self.insert.commit()
                    return "Forum has been created"

                except pymysql.err.IntegrityError:
                    return "Forum ID already exists!!!"
            #if it does not exists
            else:
                return "You don't have enough access to create a forum"

    # if user wants to close the forum
    def close_forum(self, s_author, id):
        # author who has closed the forum
        self.s_author = s_author
        self.when_closed = datetime.datetime.utcnow()
        # self.forum_active = 0

        connect = connection()
        self.insert = connect.initial()

        # cursor creation
        with self.insert.cursor() as cursor:
            sql = "SELECT ForumID from Forum WHERE ForumID=%s and WhenClosed IS NULL "
            cursor.execute(sql, (id,))
            result = cursor.fetchone()
            if result is not None:
                # exceuting the query
                sql = "UPDATE Forum SET DeletedByModerator_Username = %s, WhenClosed = %s WHERE ForumID= %s"
                cursor.execute(sql, (self.s_author, self.when_closed, id))
            else:
                return "Forum does not exists!!"

        # commit the changes
        self.insert.commit()
        return "Forum has been deleted!!"

    def show_forum(self, id):
        connect = connection()
        self.insert = connect.initial()

        with self.insert.cursor() as cursor:
            #retrieve data from Forum
            sql = "SELECT * from Forum WHERE ForumID=%s and WhenClosed IS NULL "
            cursor.execute(sql, (id))
            result_forum = cursor.fetchone()


            if result_forum  is not None:
                return result_forum
            else:
                return "Forum  does not exist"

    def showall_forum(self):
        with self.insert.cursor() as cursor:
            #retrieve data from Forum
            sql = "SELECT ForumID,Topic from Forum Where ForumID>0 and WhenClosed IS NULL"
            cursor.execute(sql)
            result_forum = cursor.fetchall()
            return result_forum



    # creating instance of post inside forum
    @staticmethod
    def new_post(text, p_link, v_link, link_loc, username, forum_id):
        post1 = PostModel(username)
        ret = post1.new_post(text, p_link, v_link, link_loc, forum_id)
        return ret

    def show_post(self,id):
        with self.insert.cursor() as cursor:
            sql = "SELECT TimeCreated,Username  FROM Forum,Post" \
                  " WHERE Forum.ForumID=Post.ForumID and Forum.ForumID=%s and WhenClosed IS NULL  "
            cursor.execute(sql,id)
            result = cursor.fetchall()

            if result is None:
                detail = "No Active Forum Available"
            else:
                detail = result
        self.insert.commit()
        return detail

# Post class to post on the forum
class PostModel():
    def __init__(self, author):
        self.author = author
        self.TimeCreated = datetime.datetime.utcnow()

        connect = connection()
        self.insert = connect.initial()

    def new_post(self, TextEntry, Photolocation, Videolocation, Linklocation, forum_id):
        connect = connection()
        self.insert = connect.initial()

        with self.insert.cursor() as cursor:
            sql = "SELECT ForumID from Forum WHERE ForumID=%s and WhenClosed IS NULL "
            cursor.execute(sql, forum_id)
            result = cursor.fetchone()
            if result is not None:
                with self.insert.cursor() as cursor:
                    sql = "INSERT INTO Post ( Username, TimeCreated, ForumID, TextEntry, PhotoLocation, " \
                          "LinkLocation, VideoLocation)" \
                          " VALUES ( %s,%s,%s,%s,%s,%s, %s)"
                    cursor.execute(sql, (self.author, self.TimeCreated, forum_id, TextEntry, Photolocation,
                                         Linklocation, Videolocation))
                self.insert.commit()
                return "Post has been added"

            elif result is None:
                return "Forum does not exists"

# function to post in the forum
    def show_postP(self,id):
        with self.insert.cursor() as cursor:
            sql = "SELECT Username, TimeCreated, ForumID, TextEntry, PhotoLocation FROM Post" \
                  " WHERE ForumID=%s and Username=%s "
            cursor.execute(sql,(id,self.author))
            result = cursor.fetchall()
            print(result)
            if result is None:
                detail = "No Active Forum Available"
            else:
                detail = result
        self.insert.commit()
        return detail

    # creating instance of comment inside post
    def new_comment(self, username, text, p_link, v_link, link_loc):
        com = Comment()
        ret = com.new_comment(self.author, username, text, p_link, v_link, link_loc)
        return ret

    # rate a post
    def rating(self, username, rating):
        rate = Rating()
        ret = rate.rating(self.author, username, rating)
        return ret
# comment in the forum
    def show_comment(self,Username,Timecreated):
        with self.insert.cursor() as cursor:
            sql = "SELECT * From Comment WHERE Post_Username=%s, Post_TimeCreated=%s"
            cursor.execute(sql,(Username, Timecreated))
            result = cursor.fetchone()
            if result is None:
                detail = "NO COMMENTS"
            else:
                detail = result
        self.insert.commit()
        return detail
# rate a comment in the forum
    def show_rating(self,Username,Timecreated):
        with self.insert.cursor() as cursor:
            sql = "SELECT * From Rating WHERE Post_Username=%s, Post_TimeCreated=%s"
            cursor.execute(sql,(Username, Timecreated))
            result = cursor.fetchone()
            if result is None:
                detail = "NO Rating"
            else:
                detail = result
        self.insert.commit()
        return detail


# class to comment in the forum
class Comment:
    def __init__(self):
        connect = connection()
        self.insert = connect.initial()

    def new_comment(self, post_username, commenter_username, comment_text, photo_location, video_location, link_location):
        self.Comment_Time = datetime.datetime.utcnow()

        connect = connection()
        self.insert = connect.initial()

        with self.insert.cursor() as cursor:

            sql = "SELECT TimeCreated from Post WHERE Username=%s "
            cursor.execute(sql, post_username)
            result = cursor.fetchone()
            time_created = (result["TimeCreated"])
            if time_created is not None:
                try:

                   sql = "INSERT INTO Comment (Post_Username, Post_TimeCreated, Commenter_Username, CommentTime , " \
                         "CommentText, PhotoLocation, LinkLocation,VideoLocation)" \
                      " VALUES ( %s,%s,%s,%s,%s,%s, %s, %s)"
                   cursor.execute(sql, (post_username, time_created, commenter_username, self.Comment_Time, comment_text,
                                        photo_location, link_location,  video_location))
                except pymysql.err.IntegrityError:
                    return 'already a comment exist by you'
            else:
                return "Post does not exists!!!"

        self.insert.commit()
        return "Comment has been added!!!"

    def disp_all_Comment(self,id,name):
        connect = connection()
        self.insert = connect.initial()

        with self.insert.cursor() as cursor:
            sql="select comment.commenter_Username,commentText from Comment,post " \
                "where post.Username=comment.post_username and post.forumID=%s and post.Username=%s"
            cursor.execute(sql, (id,name))
            result = cursor.fetchall()
            print(result)
            return result




# class to rate a comment in the forum
class Rating:
    def __init__(self):
        connect = connection()
        self.insert = connect.initial()

    def rating(self, post_username, username, rating):

        connect = connection()
        self.insert = connect.initial()

        with self.insert.cursor() as cursor:

            sql = "SELECT TimeCreated from Post WHERE Username=%s "
            cursor.execute(sql, post_username)
            result = cursor.fetchone()
            time_post = (result["TimeCreated"])
            if time_post is not None:
                try:
                    sql = "INSERT INTO Rating (Post_Username, Post_TimeCreated, Rater_Username, Stars)" \
                          " VALUES ( %s,%s,%s,%s)"
                    cursor.execute(sql, (post_username, time_post, username, rating))
                except pymysql.err.IntegrityError:
                    return "Rating already exist by you"

            else:
                return "Post does not exists!!!"

        self.insert.commit()
        return "Rating has been added!!!"

    def disp_all_rating(self,id,name):
        connect = connection()
        self.insert = connect.initial()

        with self.insert.cursor() as cursor:
            sql="select Rater_username,stars from rating,post where " \
                " post.Username=rating.post_username and post.forumID=%s and post.Username=%s"

            cursor.execute(sql, (id,name))
            result = cursor.fetchall()
            print(result)
            return result