# -*- coding: utf-8 -*-
from __future__ import unicode_literals  # support both Python2 and 3

""" lib.py

PyOTRS lib

This code implements the PyOTRS library to provide access to the OTRS API (REST)
"""

import os
import base64
import mimetypes
import copy
import json
import time
import datetime
import requests

OPERATION_MAPPING_DEFAULT = {
    'SessionCreate': {'RequestMethod': 'POST',
                      'Route': '/Session',
                      'Result': 'SessionID'},
    'TicketCreate': {'RequestMethod': 'POST',
                     'Route': '/Ticket',
                     'Result': 'TicketID'},
    'TicketGet': {'RequestMethod': 'GET',
                  'Route': '/Ticket/:TicketID',
                  'Result': 'Ticket'},
    'TicketGetList': {'RequestMethod': 'GET',
                      'Route': '/TicketList',
                      'Result': 'Ticket'},
    'TicketSearch': {'RequestMethod': 'GET',
                     'Route': '/Ticket',
                     'Result': 'TicketID'},
    'TicketUpdate': {'RequestMethod': 'PATCH',
                     'Route': '/Ticket/:TicketID',
                     'Result': 'TicketID'},
    'LinkAdd': {'RequestMethod': 'POST',
                'Route': '/LinkAdd',
                'Result': 'LinkAdd'},
    'LinkDelete': {'RequestMethod': 'DELETE',
                   'Route': '/LinkDelete',
                   'Result': 'LinkDelete'},
    'LinkDeleteAll': {'RequestMethod': 'DELETE',
                      'Route': '/LinkDeleteAll',
                      'Result': 'LinkDeleteAll'},
    'LinkList': {'RequestMethod': 'GET',
                 'Route': '/LinkList',
                 'Result': 'LinkList'},
    'PossibleLinkList': {'RequestMethod': 'GET',
                         'Route': '/PossibleLinkList',
                         'Result': 'PossibleLinkList'},
    'PossibleObjectsList': {'RequestMethod': 'GET',
                            'Route': '/PossibleObjectsList',
                            'Result': 'PossibleObject'},
    'PossibleTypesList': {'RequestMethod': 'GET',
                          'Route': '/PossibleTypesList',
                          'Result': 'PossibleType'}
}


class PyOTRSError(Exception):
    def __init__(self, message):
        super(PyOTRSError, self).__init__(message)
        self.message = message


class ArgumentMissingError(PyOTRSError):
    pass


class ArgumentInvalidError(PyOTRSError):
    pass


class ResponseParseError(PyOTRSError):
    pass


class SessionCreateError(PyOTRSError):
    pass


class SessionNotCreated(PyOTRSError):
    pass


class APIError(PyOTRSError):
    pass


class HTTPError(PyOTRSError):
    pass


class Article(object):
    """PyOTRS Article class """
    def __init__(self, dct):
        self.__dict__ = dct

        self.list_attachments = self._parse_attachments()
        self.list_dynamic_fields = self._parse_dynamic_fields()

    def __repr__(self):
        if hasattr(self, 'ArticleID'):
            _len = len(self.list_attachments)
            if _len == 0:
                return "<ArticleID: {1}>".format(self.__class__.__name__, self.ArticleID)
            elif _len == 1:
                return "<ArticleID: {1} (1 Attachment)>".format(self.__class__.__name__,
                                                                self.ArticleID)
            else:
                return "<ArticleID: {1} ({2} Attachments)>".format(self.__class__.__name__,
                                                                   self.ArticleID, _len)
        else:
            return "<{0}>".format(self.__class__.__name__)

    def to_dct(self):
        """represent as nested dict

        Returns:
            **dict**: Article represented as dict.

        """
        return {"Article": self.__dict__}

    def _parse_attachments(self):
        """parse Attachment objects from Article

        Returns:
            **list**: A list of Attachment objects.

        """
        if hasattr(self, 'Attachment'):
            lst = [Attachment(item) for item in self.Attachment]
            delattr(self, 'Attachment')
            return lst
        else:
            return []

    def _parse_dynamic_fields(self):
        """parse DynamicField objects from Article

        Returns:
            **list**: A list of DynamicField objects.

        """
        if hasattr(self, 'DynamicField'):
            lst = [DynamicField.from_dct(item) for item in self.DynamicField]
            delattr(self, 'DynamicField')
            return lst
        else:
            return []

    def validate(self, validation_map=None):
        """validate data against a mapping dict - if a key is not present
        then set it with a default value according to dict

        Args:
            validation_map (dict): A mapping for all Article fields that have to be set. During
            validation every required field that is not set will be set to a default value
            specified in this dict.

        .. note::
            There is also a blacklist (fields to be removed) but this is currently
            hardcoded to *list_dynamic_fields* and *list_attachments*.

        """
        if not validation_map:
            validation_map = {"Body": "API created Article Body",
                              "Charset": "UTF8",
                              "MimeType": "text/plain",
                              "Subject": "API created Article",
                              "TimeUnit": 0}

        dct = self.__dict__

        for key, value in validation_map.items():
            if not self.__dict__.get(key, None):
                dct.update({key: value})

        # TODO 2016-04-24 (RH): Check this
        # Article does not contain DynamicField or Attachment on TicketCreate and TicketUpdate!
        dct.pop("list_dynamic_fields", None)
        dct.pop("list_attachments", None)

        self.__dict__ = dct

    @classmethod
    def _dummy(cls):
        """dummy data (for testing)

        Returns:
            **Article**: An Article object.

        """
        return Article({"Subject": "Dümmy Subject",
                        "Body": "Hallo Bjørn,\n[kt]\n\n -- The End",
                        "TimeUnit": 0,
                        "MimeType": "text/plain",
                        "Charset": "UTF8"})

    @classmethod
    def _dummy_force_notify(cls):
        """dummy data (for testing)

        Returns:
            **Article**: An Article object.

        """
        return Article({"Subject": "Dümmy Subject",
                        "Body": "Hallo Bjørn,\n[kt]\n\n -- The End",
                        "TimeUnit": 0,
                        "MimeType": "text/plain",
                        "Charset": "UTF8",
                        "ForceNotificationToUserID": [1, 2]})


class Attachment(object):
    """PyOTRS Attachment class """
    def __init__(self, dct):
        self.__dict__ = dct

    def __repr__(self):
        if hasattr(self, 'Filename'):
            return "<{0}: {1}>".format(self.__class__.__name__, self.Filename)
        else:
            return "<{0}>".format(self.__class__.__name__)

    def to_dct(self):
        """represent AttachmentList and related Attachment objects as dict

        Returns:
            **dict**: Attachment represented as dict.

        """
        return self.__dict__

    @classmethod
    def create_basic(cls, Content=None, ContentType=None, Filename=None):
        """create a basic Attachment object

        Args:
            Content (str): base64 encoded content
            ContentType (str): MIME type of content (e.g. text/plain)
            Filename (str): file name (e.g. file.txt)


        Returns:
            **Attachment**: An Attachment object.

        """
        return Attachment({'Content': Content,
                           'ContentType': ContentType,
                           'Filename': Filename})

    @classmethod
    def create_from_file(cls, file_path):
        """save Attachment to a folder on disc

        Args:
            file_path (str): The full path to the file from which an Attachment should be created.

        Returns:
            **Attachment**: An Attachment object.

        """
        with open(file_path, 'rb') as f:
            content = f.read().encode('utf-8')

        content_type = mimetypes.guess_type(file_path)[0]
        if not content_type:
            content_type = "application/octet-stream"
        return Attachment({'Content': base64.b64encode(content),
                           'ContentType': content_type,
                           'Filename': os.path.basename(file_path)})

    def save_to_dir(self, folder="/tmp"):
        """save Attachment to a folder on disc

        Args:
            folder (str): The directory where this attachment should be saved to.

        Returns:
            **bool**: True

        """
        if not hasattr(self, 'Content') or not hasattr(self, 'Filename'):
            raise ValueError("invalid Attachment")

        file_path = os.path.join(os.path.abspath(folder), self.Filename)
        with open(file_path, 'wb') as f:
            f.write(base64.b64decode(self.Content))

        return True

    @classmethod
    def _dummy(cls):
        """dummy data (for testing)

        Returns:
            **Attachment**: A Attachment object.

        """
        return Attachment.create_basic("YmFyCg==", "text/plain", "dümmy.txt")


class DynamicField(object):
    """PyOTRS DynamicField class

    Args:
        name (str): Name of OTRS DynamicField (required)
        value (str): Value of OTRS DynamicField
        search_operator (str): Search operator (defaults to: "Equals")
            Valid options are:
            "Equals", "Like", "GreaterThan", "GreaterThanEquals",
            "SmallerThan", "SmallerThanEquals"
        search_patterns (list): List of patterns (str or datetime) to search for

    .. warning::
        **PyOTRS only supports OTRS 5 style!**
        DynamicField representation changed between OTRS 4 and OTRS 5.

    """

    SEARCH_OPERATORS = ("Equals", "Like", "GreaterThan", "GreaterThanEquals",
                        "SmallerThan", "SmallerThanEquals",)

    def __init__(self, name, value=None, search_patterns=None, search_operator="Equals"):
        self.name = name
        self.value = value

        if not isinstance(search_patterns, list):
            self.search_patterns = [search_patterns]
        else:
            self.search_patterns = search_patterns

        if search_operator not in DynamicField.SEARCH_OPERATORS:
            raise NotImplementedError("Invalid Operator: \"{0}\"".format(search_operator))
        self.search_operator = search_operator

    def __repr__(self):
        return "<{0}: {1}: {2}>".format(self.__class__.__name__, self.name, self.value)

    @classmethod
    def from_dct(cls, dct):
        """create DynamicField from dct

        Args:
            dct (dict):

        Returns:
            **DynamicField**: A DynamicField object.

        """
        return cls(name=dct["Name"], value=dct["Value"])

    def to_dct(self):
        """represent DynamicField as dict

        Returns:
            **dict**: DynamicField as dict.

        """
        return {"Name": self.name, "Value": self.value}

    def to_dct_search(self):
        """represent DynamicField as dict for search operations

        Returns:
            **dict**: DynamicField as dict for search operations

        """
        _lst = []
        for item in self.search_patterns:
            if isinstance(item, datetime.datetime):
                item = item.strftime("%Y-%m-%d %H:%M:%S")
            _lst.append(item)

        return {"DynamicField_{0}".format(self.name): {self.search_operator: _lst}}

    @classmethod
    def _dummy1(cls):
        """dummy1 data (for testing)

        Returns:
            **DynamicField**: A list of DynamicField objects.

        """
        return DynamicField(name="firstname", value="Jane")

    @classmethod
    def _dummy2(cls):
        """dummy2 data (for testing)

        Returns:
            **DynamicField**: A list of DynamicField objects.

        """
        return DynamicField.from_dct({'Name': 'lastname', 'Value': 'Doe'})


class Ticket(object):
    """PyOTRS Ticket class """
    def __init__(self, dct):
        for key, value in dct.items():
            if isinstance(value, dict):
                dct[key] = Ticket(value)
            self.__dict__ = dct

        self.list_articles = self._parse_articles()
        self.list_dynamic_fields = self._parse_dynamic_fields()

    def __repr__(self):
        if hasattr(self, 'TicketID'):
            return "<{0}: {1}>".format(self.__class__.__name__, self.TicketID)
        else:
            return "<{0}>".format(self.__class__.__name__)

    def _parse_articles(self):
        """parse Article objects from Ticket

        Returns:
            **list[Article]**: A list of Article objects.

        """
        if hasattr(self, 'Article'):
            lst = [Article(item) for item in self.Article]
            delattr(self, 'Article')
            return lst
        else:
            return []

    def _parse_dynamic_fields(self):
        """parse DynamicField objects from Ticket

        Returns:
            **list[DynamicField]**: A list of DynamicField objects.

        """
        if hasattr(self, 'DynamicField'):
            lst = [DynamicField.from_dct(item) for item in self.DynamicField]
            delattr(self, 'DynamicField')
            return lst
        else:
            return []

    def to_dct(self):
        """represent as nested dict

        Returns:
            **dict**: Ticket represented as dict.

        """
        return {"Ticket": self.__dict__}

    def article_get(self, article_id):
        """article_get

        Args:
            article_id (str): Article ID as either int or str

        Returns:
            **Article** or **None**

        """

        result = [x for x in self.list_articles if x.ArticleID == "{0}".format(article_id)]
        if result:
            return result[0]
        else:
            return None

    def dynamic_field_get(self, df_name):
        """dynamic_field_get

        Args:
            df_name (str): Name of DynamicField to retrieve

        Returns:
            **DynamicField** or **None**

        """

        result = [x for x in self.list_dynamic_fields if x.name == "{0}".format(df_name)]
        if result:
            return result[0]
        else:
            return None

    @classmethod
    def create_basic(cls,
                     Title=None,
                     QueueID=None,
                     Queue=None,
                     StateID=None,
                     State=None,
                     PriorityID=None,
                     Priority=None,
                     CustomerUser=None,
                     **kwargs):
        """create basic ticket

        Args:
            Title (str): OTRS Ticket Title
            QueueID (str): OTRS Ticket QueueID (e.g. "1")
            Queue (str): OTRS Ticket Queue (e.g. "raw")
            StateID (str): OTRS Ticket StateID (e.g. "1")
            State (str): OTRS Ticket State (e.g. "open" or "new")
            PriorityID (str): OTRS Ticket PriorityID (e.g. "1")
            Priority (str): OTRS Ticket Priority (e.g. "low")
            CustomerUser (str): OTRS Ticket CustomerUser
            **kwargs:

        Returns:
            **Ticket**: A new Ticket object.

        """
        if not Title:
            raise ArgumentMissingError("Title is required")

        if not Queue and not QueueID:
            raise ArgumentMissingError("Either Queue or QueueID required")

        if not State and not StateID:
            raise ArgumentMissingError("Either State or StateID required")

        if not Priority and not PriorityID:
            raise ArgumentMissingError("Either Priority or PriorityID required")

        if not CustomerUser:
            raise ArgumentMissingError("CustomerUser is required")

        dct = {u"Title": Title}

        if Queue:
            dct.update({"Queue": Queue})
        else:
            dct.update({"QueueID": QueueID})

        if State:
            dct.update({"State": State})
        else:
            dct.update({"StateID": StateID})

        if Priority:
            dct.update({"Priority": Priority})
        else:
            dct.update({"PriorityID": PriorityID})

        dct.update({"CustomerUser": CustomerUser})

        for key, value in dct.items():
            dct.update({key: value})

        return Ticket(dct)

    @classmethod
    def _dummy(cls):
        """dummy data (for testing)

        Returns:
            **Ticket**: A Ticket object.

        """
        return Ticket.create_basic(Queue=u"Raw",
                                   State=u"open",
                                   Priority=u"3 normal",
                                   CustomerUser="root@localhost",
                                   Title="Bäsic Ticket")

    @staticmethod
    def datetime_to_pending_time_text(datetime_object=None):
        """datetime_to_pending_time_text

        Args:
            datetime_object (Datetime)

        Returns:
            **str**: The pending time in the format required for OTRS REST interface.

        """
        return {
            "Year": datetime_object.year,
            "Month": datetime_object.month,
            "Day": datetime_object.day,
            "Hour": datetime_object.hour,
            "Minute": datetime_object.minute
        }


class SessionStore(object):
    """Session ID: persistently store to and retrieve from to file

    Args:
        file_path (str): Path on disc
        session_timeout (int): OTRS Session Timeout Value (to avoid reusing outdated session id
        value (str): A Session ID as str
        created (int): seconds as epoch when a session_id record was created
        expires (int): seconds as epoch when a session_id record expires

    Raises:
        ArgumentMissingError

    """
    def __init__(self, file_path=None, session_timeout=None,
                 value=None, created=None, expires=None):
        if not file_path:
            raise ArgumentMissingError("Argument file_path is required!")

        if not session_timeout:
            raise ArgumentMissingError("Argument session_timeout is required!")

        self.file_path = file_path
        self.timeout = session_timeout
        self.value = value
        self.created = created
        self.expires = expires

    def __repr__(self):
        return "<{0}: {1}>".format(self.__class__.__name__, self.file_path)

    def read(self):
        """Retrieve a stored Session ID from file

        Returns:
            **str** or **None**: Retrieved Session ID or None (if none could be read)

        """
        if not os.path.isfile(self.file_path):
            return None

        if not SessionStore._validate_file_owner_and_permissions(self.file_path):
            return None

        with open(self.file_path, "r") as f:
            content = f.read()
        try:
            data = json.loads(content)
            self.value = data['session_id']

            self.created = datetime.datetime.utcfromtimestamp(int(data['created']))
            self.expires = (self.created +
                            datetime.timedelta(minutes=self.timeout))

            if self.expires > datetime.datetime.utcnow():
                return self.value  # still valid
        except ValueError:
            return None
        except KeyError:
            return None
        except Exception as err:
            raise Exception("Exception Type: {0}: {1}".format(type(err), err))

    def write(self, new_value):
        """Write and store a Session ID to file (rw for user only)

        Args:
            new_value (str): if none then empty value will be writen to file
        Returns:
            **bool**: **True** if successful, False **otherwise**.

        """
        self.value = new_value

        if os.path.isfile(self.file_path):
            if not SessionStore._validate_file_owner_and_permissions(self.file_path):
                raise IOError("File exists but is not ok (wrong owner/permissions)!")

        with open(self.file_path, 'w') as f:
            f.write(json.dumps({'created': str(int(time.time())),
                                'session_id': self.value}))
        os.chmod(self.file_path, 384)  # 384 is '0600'

        # TODO 2016-04-23 (RH): check this
        if not SessionStore._validate_file_owner_and_permissions(self.file_path):
            raise IOError("Race condition: Something happened to file during the run!")

        return True

    def delete(self):
        """remove session id file (e.g. when it only contains an invalid session id

        Raises:
            NotImplementedError

        Returns:
            **bool**: **True** if successful, otherwise **False**.

        .. todo::
            (RH) implement this _remove_session_id_file
        """
        raise NotImplementedError("Not yet done")

    @staticmethod
    def _validate_file_owner_and_permissions(full_file_path):
        """validate SessionStore file ownership and permissions

        Args:
            full_file_path (str): full path to file on disc

        Returns:
            **bool**: **True** if valid and correct, otherwise **False**...

        """
        if not os.path.isfile(full_file_path):
            raise IOError("Does not exist or not a file: {0}".format(full_file_path))

        file_lstat = os.lstat(full_file_path)
        if not file_lstat.st_uid == os.getuid():
            return False

        if not file_lstat.st_mode & 0o777 == 384:
            """ check for unix permission User R+W only (0600)
            >>> oct(384)
            '0600' Python 2
            >>> oct(384)
            '0o600'  Python 3  """
            return False

        return True


class Client(object):
    """PyOTRS Client class - includes Session handling

    Args:
        baseurl (str): Base URL for OTRS System, no trailing slash e.g. http://otrs.example.com
        webservicename (str): OTRS REST Web Service Name
        username (str): Username
        password (str): Password
        session_id_file (str): Session ID path on disc, used to persistently store Session ID
        session_timeout (int): Session Timeout configured in OTRS (usually 28800 seconds = 8h)
        session_validation_ticket_id (int): Ticket ID of an existing ticket - used to perform
            several check - e.g. validate log in (defaults to 1)
        webservicename_link (str): OTRSGenericInterfaceLinkMechanism REST Web Service Name
        proxies (dict): Proxy settings - refer to requests docs for
            more information - default to no proxies
        https_verify (bool): Should HTTPS certificates be verified (defaults to True)
        ca_cert_bundle (str): file path - if specified overrides python/system default for
            Root CA bundle that will be used.
        operation_map (dict): A dictionary for mapping OTRS operations to HTTP Method, Route and
            Result string.

    """
    def __init__(self,
                 baseurl=None,
                 webservicename=None,
                 username=None,
                 password=None,
                 session_id_file=None,
                 session_timeout=None,
                 session_validation_ticket_id=1,
                 webservicename_link=None,
                 proxies=None,
                 https_verify=True,
                 ca_cert_bundle=None,
                 operation_map=None):

        if not baseurl:
            raise ArgumentMissingError("baseurl")
        self.baseurl = baseurl.rstrip("/")

        if not webservicename:
            raise ArgumentMissingError("webservicename")
        self.webservicename = webservicename

        # TODO 2016-30-10 (RH): check Name and Documentation
        if not webservicename_link:
            self.webservicename_link = "GenericLinkConnectorREST"

        if not session_timeout:
            self.session_timeout = 28800  # 8 hours is OTRS default
        else:
            self.session_timeout = session_timeout

        if not session_id_file:
            self.session_id_store = SessionStore(file_path="/tmp/.session_id.tmp",
                                                 session_timeout=self.session_timeout)
        else:
            self.session_id_store = SessionStore(file_path=session_id_file,
                                                 session_timeout=self.session_timeout)

        self.session_validation_ticket_id = session_validation_ticket_id

        if not proxies:
            self.proxies = {"http": "", "https": "", "no": ""}
        else:
            if not isinstance(proxies, dict):
                raise ValueError("Proxy settings need to be provided as dict!")
            self.proxies = proxies

        if https_verify:
            if not ca_cert_bundle:
                self.https_verify = https_verify
            else:
                ca_certs = os.path.abspath(ca_cert_bundle)
                if not os.path.isfile(ca_certs):
                    raise ValueError("Certificate file does not exist: {0}".format(ca_certs))
                self.https_verify = ca_certs
        else:
            self.https_verify = False

        if operation_map:
            self.operation_map = operation_map
        else:
            self.operation_map = OPERATION_MAPPING_DEFAULT

        # credentials
        self.username = username
        self.password = password

        # dummy initialization
        self.operation = None
        self.result_json = None
        self.result = []

    """
    GenericInterface::Operation::Session::SessionCreate
        * session_check_is_valid
        * session_create
        * session_restore_or_set_up_new  # try to get session_id from a (json) file on filesystem
    """
    def session_check_is_valid(self, session_id=None):
        """check whether session_id is currently valid

        Args:
            session_id (str): optional If set overrides the self.session_id

        Raises:
            ArgumentMissingError: if session_id is not set

        Returns:
            **bool**: **True** if valid, otherwise **False**.

        .. note::
            Uses HTTP Method: GET
        """
        self.operation = "TicketGet"

        if not session_id:
            raise ArgumentMissingError("session_id")

        # TODO 2016-04-13 (RH): Is there a nicer way to check whether session is valid?!
        payload = {"SessionID": session_id}

        response = self._send_request(payload, ticket_id=self.session_validation_ticket_id)
        return self._parse_and_validate_response(response)

    def session_create(self):
        """create new (temporary) session (and Session ID)

        Returns:
            **bool**: **True** if successful, otherwise **False**.

        .. note::
            Session ID is recorded in self.session_id_store.value (**non persistently**)

        .. note::
            Uses HTTP Method: POST

        """
        self.operation = "SessionCreate"

        payload = {
            "UserLogin": self.username,
            "Password": self.password
        }

        if not self._parse_and_validate_response(self._send_request(payload)):
            return False

        self.session_id_store.value = self.result_json['SessionID']
        return True

    def session_restore_or_set_up_new(self):
        """Try to restore Session ID from file otherwise create new one and save to file

        Raises:
            SessionCreateError
            SessionIDFileError

        .. note::
            Session ID is recorded in self.session_id_store.value (**non persistently**)

        .. note::
            Session ID is **saved persistently** to file: *self.session_id_store.file_path*

        Returns:
            **bool**: **True** if successful, otherwise **False**.
        """
        # try to read session_id from file
        self.session_id_store.value = self.session_id_store.read()

        if self.session_id_store.value:
            # got one.. check whether it's still valid
            try:
                if self.session_check_is_valid(self.session_id_store.value):
                    print("Using valid Session ID "
                          "from ({0})".format(self.session_id_store.file_path))
                    return True
            except APIError:
                """most likely invalid session_id so pass. Remove clear session_id_store.."""

        # got no (valid) session_id; clean store
        self.session_id_store.write("")

        # and try to create new one
        if not self.session_create():
            raise SessionCreateError("Failed to create a Session ID!")

        # save new created session_id to file
        if not self.session_id_store.write(self.result_json['SessionID']):
            raise IOError("Failed to save Session ID to file!")
        else:
            print("Saved new Session ID to file: {0}".format(self.session_id_store.file_path))
            return True

    """
    GenericInterface::Operation::Ticket::TicketCreate
        * ticket_create
    """
    def ticket_create(self,
                      ticket=None,
                      article=None,
                      attachment_list=None,
                      dynamic_field_list=None,
                      **kwargs):
        """Create a Ticket

        Args:
            ticket (Ticket): a ticket object
            article (Article): optional article
            attachment_list (list): *Attachment* objects
            dynamic_field_list (list): *DynamicField* object
            **kwargs: any regular OTRS Fields (not for Dynamic Fields!)

        Returns:
            **dict** or **False**: dict if successful, otherwise **False**.
        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "TicketCreate"

        payload = {"SessionID": self.session_id_store.value}

        if not ticket:
            raise ArgumentMissingError("Ticket")

        if not article:
            raise ArgumentMissingError("Article")

        payload.update(ticket.to_dct())

        if article:
            article.validate()
            payload.update(article.to_dct())

        if attachment_list:
            # noinspection PyTypeChecker
            payload.update({"Attachment": [att.to_dct() for att in attachment_list]})

        if dynamic_field_list:
            # noinspection PyTypeChecker
            payload.update({"DynamicField": [df.to_dct() for df in dynamic_field_list]})

        if not self._parse_and_validate_response(self._send_request(payload)):
            return False
        else:
            return self.result_json

    """
    GenericInterface::Operation::Ticket::TicketGet

        * ticket_get_by_id
        * ticket_get_by_list
        * ticket_get_by_number
    """
    def ticket_get_by_id(self,
                         ticket_id,
                         articles=False,
                         attachments=False,
                         dynamic_fields=True):
        """ticket_get_by_id

        Args:
            ticket_id (int): Integer value of a Ticket ID
            attachments (bool): will request OTRS to include attachments (*default: False*)
            articles (bool): will request OTRS to include all
                    Articles (*default: False*)
            dynamic_fields (bool): will request OTRS to include all
                    Dynamic Fields (*default: True*)

        Returns:
            **Ticket** or **False**: Ticket object if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "TicketGetList"

        payload = {
            "SessionID": self.session_id_store.value,
            "TicketID": "{0}".format(ticket_id),
            "AllArticles": int(articles),
            "Attachments": int(attachments),
            "DynamicFields": int(dynamic_fields)
        }

        if not self._parse_and_validate_response(self._send_request(payload)):
            return False
        else:
            return self.result[0]

    def ticket_get_by_list(self,
                           ticket_id_list,
                           articles=False,
                           attachments=False,
                           dynamic_fields=True):
        """ticket_get_by_list

        Args:
            ticket_id_list (list): List of either String or Integer values
            attachments (bool): will request OTRS to include attachments (*default: False*)
            articles (bool): will request OTRS to include all
                    Articles (*default: False*)
            dynamic_fields (bool): will request OTRS to include all
                    Dynamic Fields (*default: True*)

        Returns:
            **list**: Ticket objects (as list) if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "TicketGetList"

        # TODO 2016-09-11 (RH) should we silently catch and fix this "misusage" ?!
        # if isinstance(ticket_id_list, int):
        #     ticket_id_list = [ticket_id_list]

        if not isinstance(ticket_id_list, list):
            raise ArgumentInvalidError("Please provide list of IDs!")

        payload = {
            "SessionID": self.session_id_store.value,
            "TicketID": ','.join([str(item) for item in ticket_id_list]),
            "AllArticles": int(articles),
            "Attachments": int(attachments),
            "DynamicFields": int(dynamic_fields)
        }

        if not self._parse_and_validate_response(self._send_request(payload)):
            return False
        else:
            return self.result

    def ticket_get_by_number(self,
                             ticket_number,
                             articles=False,
                             attachments=False,
                             dynamic_fields=True):
        """ticket_get_by_number

        Args:
            ticket_number (str): Ticket Number as str
            attachments (bool): will request OTRS to include attachments (*default: False*)
            articles (bool): will request OTRS to include all
                    Articles (*default: False*)
            dynamic_fields (bool): will request OTRS to include all
                    Dynamic Fields (*default: True*)

        Raises:
            ValueError

        Returns:
            **Ticket** or **False**: Ticket object if successful, otherwise **False**.

        """
        if isinstance(ticket_number, int):
            raise ArgumentInvalidError("Provide ticket_number as str/unicode. "
                                       "Got ticket_number as int.")
        result_list = self.ticket_search(TicketNumber=ticket_number)

        if not result_list:
            return False

        if len(result_list) == 1:
            result = self.ticket_get_by_id(result_list[0],
                                           articles=articles,
                                           attachments=attachments,
                                           dynamic_fields=dynamic_fields)
            if not result:
                return False
            else:
                return result
        else:
            # TODO more than one ticket found for a specific ticket number
            raise ValueError("Found more than one result for "
                             "Ticket Number: {0}".format(ticket_number))

    """
    GenericInterface::Operation::Ticket::TicketSearch
        * ticket_search
        * ticket_search_full_text
    """
    def ticket_search(self, dynamic_fields=None, **kwargs):
        """Search for ticket

        Args:
            dynamic_fields (list): List of DynamicField objects for which the search
                should be performed
            **kwargs: Arbitrary keyword arguments (not for DynamicField objects).

        Returns:
            **list** or **False**: The search result (as list) if successful, otherwise
            **False**.

        .. note::
            If value of kwargs is a datetime object then this object will be
            converted to the appropriate string format for OTRS API.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "TicketSearch"
        payload = {
            "SessionID": self.session_id_store.value,
        }

        if dynamic_fields:
            for df in dynamic_fields:
                payload.update(df.to_dct_search())

        if kwargs is not None:
            for key, value in kwargs.items():
                if isinstance(value, datetime.datetime):
                    value = value.strftime("%Y-%m-%d %H:%M:%S")
                payload.update({key: value})

        if not self._parse_and_validate_response(self._send_request(payload)):
            return False
        else:
            return self.result

    def ticket_search_full_text(self, pattern):
        """Wrapper for search ticket for full text search

        Args:
            pattern (str): Search pattern (a '%' will be added to front and end automatically)

        Returns:
            **list** or **False**: The search result (as list) if successful, otherwise **False**.

        """
        self.operation = "TicketSearch"
        pattern_wildcard = "%{0}%".format(pattern)

        return self.ticket_search(FullTextIndex="1",
                                  ContentSearch="OR",
                                  Subject=pattern_wildcard,
                                  Body=pattern_wildcard)

    """
    GenericInterface::Operation::Ticket::TicketUpdate
        * ticket_update
        * ticket_update_set_pending
    """
    def ticket_update(self,
                      ticket_id,
                      article=None,
                      attachment_list=None,
                      dynamic_field_list=None,
                      **kwargs):
        """Update a Ticket

        Args:

            ticket_id (int): Ticket ID as integer value
            article (Article): **optional** one *Article* that will be add to the ticket
            attachment_list (list): list of one or more *Attachment* objects that will
                be added to ticket. Also requires an *Article*!
            dynamic_field_list (list): *DynamicField* objects
            **kwargs: any regular Ticket Fields (not for Dynamic Fields!)

        Returns:
            **dict** or **False**: A dict if successful, otherwise **False**.
        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "TicketUpdate"

        payload = {"SessionID": self.session_id_store.value}

        if article:
            article.validate()
            payload.update(article.to_dct())

        if attachment_list:
            if not article:
                raise ArgumentMissingError("To create an attachment an article is needed!")
            # noinspection PyTypeChecker
            payload.update({"Attachment": [att.to_dct() for att in attachment_list]})

        if dynamic_field_list:
            # noinspection PyTypeChecker
            payload.update({"DynamicField": [df.to_dct() for df in dynamic_field_list]})

        if kwargs is not None and not kwargs == {}:
            ticket_dct = {}
            for key, value in kwargs.items():
                ticket_dct.update({key: value})
            payload.update({"Ticket": ticket_dct})

        if not self._parse_and_validate_response(self._send_request(payload, ticket_id)):
            return False

        return self.result_json

    def ticket_update_set_pending(self,
                                  ticket_id,
                                  new_state="pending reminder",
                                  pending_days=1,
                                  pending_hours=0):
        """ticket_update_set_state_pending

        Args:
            ticket_id (int): Ticket ID as integer value
            new_state (str): defaults to "pending reminder"
            pending_days (int): defaults to 1
            pending_hours (int): defaults to 0

        Returns:
            **dict** or **False**: A dict if successful, otherwise **False**.

        .. note::
            Operates in UTC
        """
        datetime_now = datetime.datetime.utcnow()
        pending_till = datetime_now + datetime.timedelta(days=pending_days, hours=pending_hours)

        pt = Ticket.datetime_to_pending_time_text(datetime_object=pending_till)

        return self.ticket_update(ticket_id, State=new_state, PendingTime=pt)

    """
    GenericInterface::Operation::Link::LinkAdd
        * link_add
    """
    def link_add(self,
                 src_object_id,
                 dst_object_id,
                 src_object_type="Ticket",
                 dst_object_type="Ticket",
                 link_type="Normal",
                 state="Valid"):
        """link_add

        Args:
            src_object_id (int): Integer value of source object ID
            dst_object_id (int): Integer value of destination object ID
            src_object_type (str): Object type of source; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)
            dst_object_type (str): Object type of destination; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)
            link_type (str): Type of the link: "Normal" or "ParentChild" (*default: Normal*)
            state (str): State of the link (*default: Normal*)

        Returns:
            **True** or **False**: True if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "LinkAdd"

        payload = {
            "SessionID": self.session_id_store.value,
            "SourceObject": src_object_type,
            "SourceKey": int(src_object_id),
            "TargetObject": dst_object_type,
            "TargetKey": int(dst_object_id),
            "Type": link_type,
            "State": state
        }

        return self._parse_and_validate_response(self._send_request(payload))

    """
    GenericInterface::Operation::Link::LinkDelete
        * link_delete
    """
    def link_delete(self,
                    src_object_id,
                    dst_object_id,
                    src_object_type="Ticket",
                    dst_object_type="Ticket",
                    link_type="Normal"):
        """link_delete

        Args:
            src_object_id (int): Integer value of source object ID
            src_object_type (str): Object type of source; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)
            dst_object_id (int): Integer value of source object ID
            dst_object_type (str): Object type of source; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)
            link_type (str): Type of the link: "Normal" or "ParentChild" (*default: Normal*)

        Returns:
            **True** or **False**: True if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "LinkDelete"

        payload = {
            "SessionID": self.session_id_store.value,
            "Object1": src_object_type,
            "Key1": int(src_object_id),
            "Object2": dst_object_type,
            "Key2": int(dst_object_id),
            "Type": link_type
        }

        return self._parse_and_validate_response(self._send_request(payload))

    """
    GenericInterface::Operation::Link::LinkDeleteAll
        * link_delete_all
    """
    def link_delete_all(self,
                        object_id,
                        object_type="Ticket",):
        """link_delete_all

        Args:
            object_id (int): Integer value of source object ID
            object_type (str): Object type of source; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)

        Returns:
            **True** or **False**: True if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "LinkDeleteAll"

        payload = {
            "SessionID": self.session_id_store.value,
            "Object": object_type,
            "Key": int(object_id)
        }

        return self._parse_and_validate_response(self._send_request(payload))

    """
    GenericInterface::Operation::Link::LinkList
        * link_list
    """
    def link_list(self,
                  src_object_id,
                  src_object_type="Ticket",
                  dst_object_type=None,
                  state="Valid",
                  link_type=None,
                  direction=None):
        """link_list

        Args:
            src_object_id (int): Object type of source; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)
            src_object_type (str): Object type of destination; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)
            dst_object_type (str): Object type of destination; e.g. "Ticket", "FAQ"...
                Optional restriction of the object where the links point to. (*default: Ticket*)
            state (str): State of the link (*default: Valid*)
            link_type (str): Type of the link: "Normal" or "ParentChild" (*default: Normal*)
            direction (str): Optional restriction of the link direction ('Source' or 'Target').

        Returns:
            **Dict** or **None**: Dict if successful, if empty **None**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "LinkList"

        payload = {
            "SessionID": self.session_id_store.value,
            "Object": src_object_type,
            "Key": int(src_object_id),
            "State": state
        }

        if dst_object_type:
            payload.update({"Object2": dst_object_type})

        if link_type:
            payload.update({"Type": link_type})

        if direction:
            payload.update({"Direction": direction})

        return self._parse_and_validate_response(self._send_request(payload))

    """
    GenericInterface::Operation::Link::PossibleLinkList
        * link_possible_link_list
    """
    def link_possible_link_list(self):
        """link_possible_link_list

        Returns:
            **List** or **False**: List if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "PossibleLinkList"

        payload = {
            "SessionID": self.session_id_store.value,
        }

        if self._parse_and_validate_response(self._send_request(payload)):
            return self.result
        else:
            return False

    """
    GenericInterface::Operation::Link::PossibleObjectsList
        * link_possible_objects_list
    """
    def link_possible_objects_list(self,
                                   object_type="Ticket"):
        """link_possible_objects_list

        Args:
            object_type (str): Object type; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)

        Returns:
            **List** or **False**: List if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "PossibleObjectsList"

        payload = {
            "SessionID": self.session_id_store.value,
            "Object": object_type,
        }

        if self._parse_and_validate_response(self._send_request(payload)):
            return self.result
        else:
            return False

    """
    GenericInterface::Operation::Link::PossibleTypesList
        * link_possible_types_list
    """
    def link_possible_types_list(self,
                                 src_object_type="Ticket",
                                 dst_object_type="Ticket"):
        """link_possible_types_list

        Args:
            src_object_type (str): Object type of source; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)
            dst_object_type (str): Object type of destination; e.g. "Ticket", "FAQ"...
                (*default: Ticket*)

        Returns:
            **List** or **False**: List if successful, otherwise **False**.

        """
        if not self.session_id_store.value:
            raise SessionNotCreated("Call session_create() or "
                                    "session_restore_or_set_up_new() first")
        self.operation = "PossibleTypesList"

        payload = {
            "SessionID": self.session_id_store.value,
            "Object1": src_object_type,
            "Object2": dst_object_type,
        }

        if self._parse_and_validate_response(self._send_request(payload)):
            return self.result
        else:
            return False

    def _build_url(self, ticket_id=None):
        """build url for request

        Args:
            ticket_id (optional[int])

        Returns:
            **str**: The complete URL where the request will be send to.

        """
        route = self.operation_map[self.operation]["Route"]

        if not (route.startswith(("/Ticket", "/Session", "/Possible", "/Link"))):
            raise ValueError("Route misconfigured: {0}".format(route))

        if ":" in route:
            route_split = route.split(":")
            route = route_split[0]
            route_arg = route_split[1]

            if route_arg == "TicketID":
                if not ticket_id:
                    raise ValueError("TicketID is None but Route requires "
                                     "TicketID: {0}".format(route))
                self._url = ("{0}/otrs/nph-genericinterface.pl/Webservice/"
                             "{1}{2}{3}".format(self.baseurl,
                                                self.webservicename,
                                                route,
                                                ticket_id))
        else:
            if route.startswith(("/Link", "/Possible")):
                self._url = ("{0}/otrs/nph-genericinterface.pl/Webservice/"
                             "{1}{2}".format(self.baseurl,
                                             self.webservicename_link,
                                             route))
            else:
                self._url = ("{0}/otrs/nph-genericinterface.pl/Webservice/"
                             "{1}{2}".format(self.baseurl,
                                             self.webservicename,
                                             route))

        return self._url

    def _send_request(self, payload=None, ticket_id=None):
        """send the API request using the *requests.request* method

        Args:
            payload (dict)
            ticket_id (optional[dict])

        Raises:
            OTRSHTTPError:

        Returns:
            **requests.Response**: Response received after sending the request.

        .. note::
            Supported HTTP Methods: DELETE, GET, HEAD, PATCH, POST, PUT
        """
        if not payload:
            raise ArgumentMissingError("payload")

        self._result_type = self.operation_map[self.operation]["Result"]

        url = self._build_url(ticket_id)

        http_method = self.operation_map[self.operation]["RequestMethod"]

        if http_method not in ["DELETE", "GET", "HEAD", "PATCH", "POST", "PUT"]:
            raise ValueError("invalid http_method")

        headers = {"Content-Type": "application/json"}
        json_payload = json.dumps(payload)
        # ("sending {0} to {1} as {2}".format(payload, url, http_method.upper()))

        try:
            response = requests.request(http_method.upper(),
                                        url,
                                        headers=headers,
                                        data=json_payload,
                                        proxies=self.proxies,
                                        verify=self.https_verify)

            # store a copy of the request
            self._request = response.request

        # critical error: HTTP request resulted in an error!
        except Exception as err:
            # raise OTRSHTTPError("get http")
            raise HTTPError("Failed to access OTRS. Check Hostname, Proxy, SSL Certificate!\n"
                            "Error with http communication: {0}".format(err))

        if not response.status_code == 200:
            raise HTTPError("Received HTTP Error. Check Hostname and WebServiceName.\n"
                            "HTTP Status Code: {0.status_code}\n"
                            "HTTP Message: {0.content}".format(response))
        return response

    def _parse_and_validate_response(self, response):
        """_parse_and_validate_response

        Args:
            response (requests.Response): result of _send_request

        Raises:
            OTRSAPIError
            NotImplementedError
            ResponseJSONParseError

        Returns:
            **bool**: **True** if successful

        """

        if not isinstance(response, requests.models.Response):
            raise ValueError("requests.Response object expected!")

        if self.operation not in self.operation_map.keys():
            raise ValueError("invalid operation")

        # clear data from Client
        self.result = None
        self._result_error = False

        # get and set new data
        self.result_json = response.json()

        # TODO 2016-04-24 (RH) can this deep copy go?
        self._result_json_original = copy.deepcopy(self.result_json)
        self._result_status_code = response.status_code
        self._result_content = response.content

        # handle TicketSearch operation first. special: empty search result has no "TicketID"
        if self.operation == "TicketSearch":
            if not self.result_json:
                return True
            if self.result_json.get(self._result_type, None):
                self.result = self.result_json['TicketID']
                return True

        # handle Link operations; Add, Delete, DeleteAll return: {"Success":1}
        if self.operation in ["LinkAdd", "LinkDelete", "LinkDeleteAll"]:
            if self.result_json.get("Success", None) == 1:  # TODO 2016-10-30 (RH): enough?!
                return True

        # LinkList result can be empty
        if self.operation in "LinkList":
            _link_list = self.result_json.get("LinkList", None)
            if not _link_list:
                self.result = None
                return True
            else:
                self.result = _link_list
                return True

        # now handle other operations
        if self.result_json.get(self._result_type, None):
            self._result_error = False
            self.result = self.result_json[self._result_type]
        elif self.result_json.get("Error", None):
            self._result_error = True
        else:
            self._result_error = True
            # critical error: Unknown response from OTRS API - FAIL NOW!
            raise ResponseParseError("Unknown key in response JSON DICT!")

        # report error
        if self._result_error:
            raise APIError("Failed to access OTRS API. Check Username and Password! "
                           "Session ID expired?! Does Ticket exist?\n"
                           "OTRS Error Code: {0}\nOTRS Error Message: {1}"
                           "".format(self.result_json["Error"]["ErrorCode"],
                                     self.result_json["Error"]["ErrorMessage"]))

        # for operation TicketGet: parse result list into Ticket object list
        if self.operation == "TicketGet" or self.operation == "TicketGetList":
            self.result = [Ticket(item) for item in self.result_json['Ticket']]

        # TODO 2016-04-17 (RH): is this "extra net" needed?!
        # for operation TicketUpdate: if Article was updated, check that response contains
        #   new ArticleID.
        # if self.operation == "TicketUpdate":
        #     _request_body = json.loads(response.request.body)
        #     if "Article" in _request_body.keys():
        #         try:
        #             article_id = self.result_json.get('ArticleID', None)
        #             if not article_id:
        #                 raise ValueError("No new Article was created?!")
        #
        #         except Exception as err:
        #             raise ValueError("Unknown Exception: {0}".format(err))

        return True

# EOF
