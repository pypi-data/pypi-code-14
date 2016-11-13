from model.forum import ForumModel, PostModel, Comment, Rating


# forum controller
class ForumController:
    # create forum
    def create_forum(self, topic, url, summary, username, forum_id):
        forum1 = ForumModel()
        ret = forum1.forum(topic, url, summary, username, forum_id)
        return ret

    # delete forum
    def delete_forum(self, username, id):
        forum1 = ForumModel()
        ret = forum1.close_forum(username, id)
        return ret

    # view forum
    def view_forum(self, forum_id):
        forum = ForumModel()
        ret = forum.show_forum(forum_id)
        return ret

    # view all in forum
    def view_allforum(self):
        forum = ForumModel()
        ret = forum.showall_forum()
        return ret

    # create forun
    def create_post(self, text, p_link, v_link, link_loc, username, forum_id):
        f = ForumModel
        msg = f.new_post(text, p_link, v_link, link_loc, username, forum_id)
        return msg

    # view the post
    def view_post(self, forum_id):
        f = ForumModel()
        detail = f.show_post(forum_id)
        return detail

    def view_postP(self, forum_id,user):
        f = PostModel(user)
        detail = f.show_postP(forum_id)
        return detail

    # new comment
    def create_comment(self, post_username, commenter_username, comment_text, photo_location, video_location,
                       link_location):
        f = Comment()
        detail = f.new_comment(post_username, commenter_username, comment_text, photo_location, video_location,
                               link_location)
        return detail

    # create rating
    def create_rating(self, post_username, username, rating):
        f = Rating()
        detail = f.rating(post_username, username, rating)
        return detail

    # dispaly all comments
    def display_comment(self,id,name):
        f=Comment()
        c=f.disp_all_Comment(id,name)
        return c

    # display all rating
    def display_rating(self,id,name):
        f=Rating()
        c=f.disp_all_rating(id,name)
        return c
