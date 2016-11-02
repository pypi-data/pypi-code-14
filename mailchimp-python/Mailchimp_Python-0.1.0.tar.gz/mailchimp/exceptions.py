# coding=utf-8


class ObjectNotFound(Exception):
    message = "Object not found"


class MCListNotFound(Exception):
    def __init__(self, list_id, *args, **kwargs):
        super(MCListNotFound, self).__init__(*args, **kwargs)
        self.message = "List not found with id: %s" % list_id


class MCMemberNotFound(Exception):
    def __init__(self, list_id, member_id, *args, **kwargs):
        super(MCMemberNotFound, self).__init__(*args, **kwargs)
        self.message = "Unable to find member %s from list with id: %s" % (member_id, list_id)
