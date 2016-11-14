import falcon


class Resource(object):
    def __init__(self):
        pass
    def OK(self, met, req, res, ids=None):
        req.context['ret'] = met(req, ids)
        res.status = falcon.HTTP_OK

    def Doc(self, req):
        return req.context['doc']

    def Qry(self, req):
        return req.params

    def C(self, req, ids):
        return self.mod.C(ids, self.Doc(req))

    def Q(self, req, ids):
        return self.mod.Q(ids, self.Qry(req))

    def R(self, req, ids):
        return self.mod.R(ids)

    def U(self, req, ids):
        return self.mod.U(ids, self.Doc(req))

    def D(self, req, ids):
        return self.mod.D(ids)
