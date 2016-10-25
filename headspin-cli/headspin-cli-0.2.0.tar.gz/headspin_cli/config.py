import os
import json


config_dir = os.path.join(os.path.expanduser('~'), '.headspin')
auth_config = None


class AuthLease(object):
    def __init__(self, user_id, role, org_title, secret_api_key):
        self.user_id = user_id
        self.role = role
        self.org_title = org_title
        self.secret_api_key = secret_api_key


class AuthConfig(object):
    def __init__(self, default_lease_index, leases):
        self.default_lease_index = default_lease_index
        self.leases = leases

    @staticmethod
    def load_from_file():
        with open(os.path.join(config_dir, 'auth.json'), 'r') as auth_config:
            auth_json = json.loads(auth_config.read())
        default_lease_index = (
            auth_json['default_lease_index']
            if 'default_lease_index' in auth_json else None)
        leases = [
            AuthLease(lease['user_id'].encode('ascii'),
                      lease.get('role', None),
                      lease['org_title'].encode('ascii'),
                      lease['secret_api_key'].encode('ascii'))
            for lease in auth_json['leases']
        ]
        return AuthConfig(
            default_lease_index,
            leases
        )

    def has_lease(self, user_id, secret_api_key):
        for lease in self.leases:
            if lease.user_id == user_id and secret_api_key == lease.secret_api_key:
                return True
        return False

    def default_lease(self):
        return self.leases[self.default_lease_index]

    def write(self):
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(os.path.join(config_dir, 'auth.json'), 'w') as auth_config:
            auth_config.write(json.dumps(dict(
                default_lease_index=self.default_lease_index,
                leases=[
                    dict(
                        user_id=lease.user_id,
                        role=lease.role,
                        org_title=lease.org_title,
                        secret_api_key=lease.secret_api_key)
                    for lease in self.leases
                ]
            )))


def get_auth_or_die():
    """Read auth from ~/.headspin."""
    try:
        return AuthConfig.load_from_file()
    except:
        # traceback.print_exc()
        print("""
This user account is unauthorized to use the HeadSpin API. Please
contact HeadSpin at support@headspin.io to obtain an authorization token.
""")
        # exit for real
        os._exit(1)


def add_leases(leases):
    for lease in leases:
        add_lease(lease)


def add_lease(lease):
    user_id = lease['user_id']
    org_title = lease['key_org_title']
    role = lease['key_name']
    secret_api_key = lease['secret_api_key']

    try:
        auth_config = AuthConfig.load_from_file()
        if auth_config.has_lease(user_id, secret_api_key):
            print 'Already authorized'
            return
        auth_config.leases.append(AuthLease(
            user_id,
            role,
            org_title,
            secret_api_key
        ))
        auth_config.default_lease_index = len(auth_config.leases) - 1
        auth_config.write()
    except:
        leases = [AuthLease(user_id, role, org_title, secret_api_key)]
        auth_config = AuthConfig(0, leases)
        auth_config.write()

    print('Authorized')
