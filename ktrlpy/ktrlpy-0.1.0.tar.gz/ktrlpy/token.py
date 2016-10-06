import jwt


def ParseClaims(token, validate=True):
    '''
    parses the claims out of the given json web token

    Args:
        token (str): the raw token string
        validate (bool): if False, do not validate the token signature
    Returns:
        a dictionary of claims from the jwt
    '''
    return jwt.decode(token, verify=validate)
