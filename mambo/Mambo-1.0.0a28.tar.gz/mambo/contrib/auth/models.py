
import datetime
from mambo import db, utils
from mambo.exceptions import ModelError
from flask_login import UserMixin
import arrow


class AuthRole(db.Model):

    SUPERADMIN = "SUPERADMIN"  # ALL MIGHTY, RESERVED FOR SYS ADMIN
    ADMIN = "ADMIN"  # App/Site admin
    MANAGER = "MANAGER"  # Limited access, but can approve EDITOR Data
    EDITOR = "EDITOR"  # Rights to write, manage, publish own data
    CONTRIBUTOR = "CONTRIBUTOR"  # Rights to only write and read own data
    MODERATOR = "MODERATOR"   # Moderate content
    MEMBER = "MEMBER"  # Just a member

    # BASIC ROLES
    ROLES = [(99, SUPERADMIN),
               (89, ADMIN),
               (59, MANAGER),
               (49, EDITOR),
               (39, CONTRIBUTOR),
               (29, MODERATOR),
               (10, MEMBER)]

    name = db.Column(db.String(75), index=True)
    level = db.Column(db.Integer, index=True)

    @classmethod
    def _syncdb(cls):
        """
        Mambo specific
        To setup some models data after
        :return:
        """
        [cls.new(level=r[0], name=r[1]) for r in cls.ROLES]

    @classmethod
    def new(cls, name, level):
        name = utils.slugify(name)
        if not cls.get_by_name(name) and not cls.get_by_level(level):
            return cls.create(name=name, level=level)

    @classmethod
    def get_by_name(cls, name):
        name = utils.slugify(name)
        return cls.query().filter(cls.name == name).first()

    @classmethod
    def get_by_level(cls, level):
        return cls.query().filter(cls.level == level).first()

class AuthUser(db.Model, UserMixin):
    role_id = db.Column(db.Integer, db.ForeignKey(AuthRole.id))
    name = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    date_of_birth = db.Column(db.Date)
    profile_image_url = db.Column(db.String(255))
    contact_email = db.Column(db.String(75), index=True)
    address = db.Column(db.String(255))
    address_city = db.Column(db.String(255))
    address_state = db.Column(db.String(255))
    address_country = db.Column(db.String(255))
    address_zip_code = db.Column(db.String(255))
    telephone = db.Column(db.String(255))
    signup_method = db.Column(db.String(255))
    active = db.Column(db.Boolean, default=True, index=True)
    last_login = db.Column(db.DateTime)
    last_visited = db.Column(db.DateTime)
    locale = db.Column(db.String(10), default="en")
    role = db.relationship(AuthRole)

    DOB_FORMAT = "MM/DD/YYYY"

    # ------ FLASK-LOGIN REQUIRED METHODS ----------------------------------
    @property
    def is_active(self):
        return self.active

    # ---------- END FLASK-LOGIN REQUIREMENTS ------------------------------

    @classmethod
    def search_by_name(cls, query, name):
        query = query.filter(db.or_(cls.name.contains(name),
                             cls.first_name.contains(name),
                             cls.last_name.contains(name)))
        return query

    @property
    def email(self):
        user_login = self.user_login("email")
        return user_login.email if user_login else None

    @property
    def age(self):
        """
        Return the user's age
        :return:
        """
        return utils.how_old(self.date_of_birth) \
            if self.date_of_birth \
            else None

    @property
    def dob(self):
        """
        Return the DOB format
        :return: string
        """
        return arrow.get(self.date_of_birth).format(self.DOB_FORMAT) \
            if self.date_of_birth \
            else None

    @property
    def full_name(self):
        """
        Return the full name
        :return:
        """
        return "%s %s" % (self.first_name, self.last_name)

    def has_any_roles(self, *roles):
        """
        Check if user has any of the roles requested
        :param roles: tuple of roles string
        :return: bool
        """
        roles = map(utils.slugify, list(roles))

        return True \
            if AuthRole.query()\
            .join(AuthUser)\
            .filter(AuthRole.name.in_(roles))\
            .filter(AuthUser.id == self.id)\
            .count() \
            else False

    def user_login(self, login_type, social_provider=None):
        login = self.logins\
            .filter(AuthUserLogin.login_type == login_type)
        if social_provider:
            login = login.filter(AuthUserLogin.social_provider == social_provider)
        login = login.first()
        return login

    def has_login_type(self, login_type):
        return True if self.user_login(login_type) else False

    def get_email_login(self):
        """
        Get the active email login
        :return: AuthUserLogin
        """
        return self.user_login("email")

    def get_social_login(self, social_provider):
        """
        Get the action social login
        :param social_provider: the social networf
        :return: AuthUserLogin
        """
        return self.user_login("social", social_provider=social_provider)


class AuthUserLogin(db.Model):
    TYPE_EMAIL = "email"
    TYPE_SOCIAL = "social"
    PROVIDER_FACEBOOK = "facebook"
    PROVIDER_TWITTER = "twitter"
    PROVIDER_EMAIL = "email"

    user_id = db.Column(db.Integer, db.ForeignKey(AuthUser.id))
    login_type = db.Column(db.String(50), index=True)
    email = db.Column(db.String(255), index=True)
    email_verified = db.Column(db.Boolean, default=False)
    email_verified_token = db.Column(db.String(100), index=True)
    email_verified_expiration = db.Column(db.DateTime)
    password_hash = db.Column(db.String(255))
    require_password_change = db.Column(db.Boolean, default=False)
    social_provider = db.Column(db.String(255))
    social_user_id = db.Column(db.String(255))
    social_link = db.Column(db.String(255))
    access_token = db.Column(db.String(255))
    access_key_id = db.Column(db.String(255))
    access_secret_key = db.Column(db.String(255))
    has_temp_login = db.Column(db.Boolean, default=False)
    temp_login_token = db.Column(db.String(100), index=True)
    temp_login_expiration = db.Column(db.DateTime)
    user = db.relationship(AuthUser, backref=db.backref('logins', lazy='dynamic'))

    @classmethod
    def encrypt_password(cls, password):
        return utils.encrypt_string(password)

    @classmethod
    def new(cls, login_type, user_id=None, email=None, password=None,
            social_provider=None, social_user_id=None, access_token=None,
            access_key_id=None, access_secret_key=None, user_info={},
            random_password=True):
        """
        To create a new account
        :param login_type: email | social
        :param user_id: a user id if exists
        :param email: email to signup with
        :param password:
        :param social_provider:
        :param social_user_id:
        :param access_token:
        :param access_key_id:
        :param access_secret_key:
        :param user_info:
        :param random_password:
        :return:
        """

        if login_type not in [cls.TYPE_EMAIL, cls.TYPE_SOCIAL]:
            raise ModelError("Invalid login type '%s'" % login_type)

        data = {"login_type": login_type}

        if login_type == cls.TYPE_EMAIL:
            if not password and random_password:
                password = utils.generate_random_string()
            if not utils.is_email_valid(email):
                raise ModelError("Invalid email")
            if cls.get_by_email(email):
                raise ModelError("Email exists already!")
            if not utils.is_password_valid(password):
                raise ModelError("Password is required")
            data.update({
                "email": email,
                "email_verified": False,
                "password_hash": cls.encrypt_password(password)
            })

        elif login_type == cls.TYPE_SOCIAL:
            if not social_provider or not social_user_id:
                raise ModelError("Social Provider and ID are required")
            data.update({
                "social_provider": social_provider,
                "social_user_id": social_user_id,
                "access_token": access_token,
                "access_key_id": access_key_id,
                "access_secret_key": access_secret_key
            })

        if not user_id:
            role = user_info.get("role") or AuthRole.MEMBER
            role_ = AuthRole.get_by_name(role.upper())
            if role_:
                user_info.update(role=role_)
            data.update({"user": AuthUser(active=True,
                                          signup_method=login_type,
                                          **user_info)})
        else:
            data["user_id"] = user_id

        login = cls.create(**data)
        return login

    @classmethod
    def get_by_email(cls, email):
        """
        Return a User by email address
        """
        return cls.query().filter(cls.email == email).first()

    @classmethod
    def get_by_social(cls, provider, user_id):
        return cls.query() \
            .filter(cls.login_type == cls.TYPE_SOCIAL) \
            .filter(cls.social_provider == provider) \
            .filter(cls.social_user_id == user_id) \
            .first()

    @classmethod
    def get_by_temp_login(cls, token):
        """
        Return a User by temp_login_token
        temp_login_token allows a user to login with the token
        and reset the password
        """
        user = cls.query().filter(cls.temp_login_token == token).first()
        if user:
            now = datetime.datetime.now()
            if user.has_temp_login is True \
                    and user.temp_login_expiration > now:
                return user
            user.clear_temp_login()
        return None

    def set_temp_login(self, expiration=60):
        """
        Create temp login.
        It will allow to have change password on account
        :param expiration: in minutes the time for expiration
        """
        expiration = datetime.datetime.now() \
                     + datetime.timedelta(minutes=expiration)

        if self.login_type != self.TYPE_EMAIL:
            raise ModelError("Can't set temp login for non `email` account")

        token = None
        while True:
            token = utils.generate_random_string(32).lower()
            if not AuthUser.query().filter(AuthUserLogin.temp_login_token == token).first():
                break
        self.update(has_temp_login=True,
                    temp_login_token=token,
                    temp_login_expiration=expiration)
        return token

    def clear_temp_login(self):
        self.update(has_temp_login=False,
                    temp_login_token=None,
                    temp_login_expiration=None)

    @classmethod
    def get_by_email_verified_token(cls, token):
        """
        Return a User by email_conf_token
        temp_login_token allows a user to login with the token
        and reset the password
        """
        user = cls.query().filter(cls.email_verified_token == token).first()
        if user:
            now = datetime.datetime.now()
            if not user.email_verified \
                    and user.email_verified_expiration > now:
                return user
            user.clear_temp_login()
        return None

    def set_email_verified_token(self, expiration=60):
        """
        Create temp login.
        It will allow to have change password on account
        :param expiration: in minutes the time for expiration
        """
        expiration = datetime.datetime.now() \
                     + datetime.timedelta(minutes=expiration)

        if self.login_type != self.TYPE_EMAIL:
            raise ModelError("Can't set email confirmation for non `email` account")

        token = None
        while True:
            token = utils.generate_random_string(32).lower()
            if not AuthUser.query().filter(AuthUserLogin.email_verified_token == token).first():
                break
        self.update(email_verified=False,
                    email_verified_token=token,
                    email_verified_expiration=expiration)
        return token

    def clear_email_verified_token(self):
        self.update(email_verified=True,
                    email_verified_token=None,
                    email_verified_expiration=None)

    def password_matched(self, password):
        """
        Check if the password matched the hash
        :returns bool:
        """
        return utils.verify_encrypted_string(password, self.password_hash)

    def change_email(self, email):
        """
        Change account email
        :param email:
        :return:
        """
        if self.login_type != self.TYPE_EMAIL:
            raise ModelError("Invalid login type. Must be the type of email to change email")

        if not utils.is_email_valid(email):
            raise ModelError("Invalid email address '%s'" % email)
        if self.email != email:
            if self.get_by_email(email):
                raise ModelError("Email exists already '%s'" % email)
            self.update(email=email)
            return True

    def change_password(self, password=None):
        """
        To change a password
        :param password:
        :param random:
        :return:
        """
        if self.login_type != self.TYPE_EMAIL:
            raise ModelError("Invalid login type. Must be the type of email to change password")
        if not utils.is_password_valid(password):
            raise ModelError("Invalid password")
        self.update(password_hash=self.encrypt_password(password),
                    require_password_change=False)
        return password

    @property
    def active(self):
        return self.user.active

