

class NoSuchEntity(Exception):
    code=1
    def __init__(self, id):
        self.id = id

    def __str__(self):
        return unicode(self).encode('utf8')

    def __unicode__(self):
        return 'No such entity: {0}'.format(self.id).decode('utf8')
