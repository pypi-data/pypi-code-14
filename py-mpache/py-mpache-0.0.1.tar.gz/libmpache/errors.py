"""
This file is part of py-mpache.

py-mpache is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

py-mpache is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with py-sonic.  If not, see <http://www.gnu.org/licenses/>
"""

class mpacheError(Exception):
    pass

class ParameterError(mpacheError):
    pass

class VersionError(mpacheError):
    pass

class CredentialError(mpacheError):
    pass

class AuthError(mpacheError):
    pass

class LicenseError(mpacheError):
    pass

class DataNotFoundError(mpacheError):
    pass

class ArgumentError(mpacheError):
    pass

class InvalidInputError(mpacheError):
    pass

class HandshakeError(mpacheError):
    pass

class ACLrestrictedError(mpacheError):
    pass

class MethodError(mpacheError):
    pass

class ACLaccessError(mpacheError):
    pass

# This maps the error code numbers from the Ampache server to their
# appropriate Exceptions see: https://github.com/ampache/ampache/wiki/XML-API-ERRORS
# NB subsonic errors left intact coz reasons
ERR_CODE_MAP = {
    0: mpacheError ,
    10: ParameterError ,
    20: VersionError ,
    30: VersionError ,
    40: CredentialError ,
    50: AuthError ,
    60: LicenseError ,
    70: DataNotFoundError ,
    400: InvalidInputError ,
    401: HandshakeError ,
    403: ACLrestrictedError ,
    405: MethodError ,
    501: ACLaccessError ,    
}

def getExcByCode(code):
    code = int(code)
    if code in ERR_CODE_MAP:
        return ERR_CODE_MAP[code]
    return mpacheError
