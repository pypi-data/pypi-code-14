from falcon import HTTP_409, HTTP_401, HTTP_403


def dupkey_handle(e, req, res, params):
    res.status = HTTP_409
    res.body = {
        'message': str(e)
    }


def jwt_decode_handle(e, req, res, params):
    res.status = HTTP_401
    res.body = {
        'message': str(e)
    }


def jwt_sign_handle(e, req, res, params):
    res.status = HTTP_401
    res.body = {
        'message': str(e)
    }


def unauthorized_handle(e, req, res, params):
    res.status = HTTP_401
    res.body = {
        'message': str(e)
    }


def forbidden_handle(e, req, res, params):
    res.status = HTTP_403
    res.body = {
        'message': str(e)
    }
