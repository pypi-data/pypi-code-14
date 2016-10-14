import logging

from datastore_layer.models.dated_model_base import DatedModelBase
from datastore_layer.models.property_types import PropertyTypes, create_property
from werkzeug.security import check_password_hash, generate_password_hash, _hash_internal, safe_str_cmp


class User(DatedModelBase):
    email = create_property(PropertyTypes.String)
    password = create_property(PropertyTypes.String, required=True)
    commerce_id = create_property(PropertyTypes.Integer)
    spree_token = create_property(PropertyTypes.String)
    bag_keys = create_property(PropertyTypes.Key, kind="Bag", repeated=True)

    # Password
    def set_password(self, secret):
        self.password = generate_password_hash(secret)

    def check_password(self, secret):
        if not self.password.startswith('pbkdf2'):
            return self.check_legacy_password(secret)

        return check_password_hash(self.password, secret)

    # passwords that originated on commerce site before user service creation use salted sha512 without pbkdf2
    def check_legacy_password(self, secret):
        if self.password.count('$') < 2:
            logging.error("Password hash for user %i is invalid" % self.key.id())
            return False
        method, salt, hashval = self.password.split('$', 2)

        if method.count(':') != 1:
            logging.error("Password hash for user %i is invalid" % self.key.id())
            return False
        method, iterations = method.split(':')

        generated_hash = secret + salt
        for i in range (0, int(iterations)):
            generated_hash = _hash_internal(method, None, generated_hash)[0]
        return safe_str_cmp(generated_hash, hashval)
