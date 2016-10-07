import mimetypes
from StringIO import StringIO
from boto.s3.key import Key
import boto.s3.connection


class S3Client(object):
    """A client that helps user to send and get files from S3"""
    s3_connection = None
    bucket = None

    def __init__(self, bucket):
        """
        Creates the logger and sets the bucket name that will be used throughout
        :param
            - bucket:   string - The name of the bucket you will be working with
        """
        self.bucket_name = bucket

    def connect(self):
        """Start the amazon connection using the system's boto.cfg file to retrieve the credentials"""
        if self.s3_connection:
            return

        try:
            #- Amazon S3 credentials will use Boto's fall back config, looks for boto.cfg then environment variables
            self.s3_connection = boto.s3.connection.S3Connection(
                is_secure=False)
            self.bucket = self.s3_connection.get_bucket(
                self.bucket_name, validate=False)

        except Exception as s3_connection_exception:
            #- Reset the variables on failure to allow a reconnect
            self.s3_connection = None
            self.bucket = None
            message = "Exception while connecting to S3: {0}".format(s3_connection_exception)
            raise S3ClientException(message)

    def store_file(self, s3_path, file_to_store, filename, return_url=False, mime_type=None):
        """
        Pushes the desired file up to S3 (e.g. log file).
        :param
            - s3_path:          string - The S3 path to the folder in which you'd like to store the file
            - file_to_store:    StringIO or string - The fileIO or file local file path for the file to be sent
            - filename:         string - The name the file will have when on S3. Should include the file extension
            - return_url:       boolean - Whether to return the path to the file on S3
            - mime_type:        string - the mime type the file should be saved as, ex: text/html or image/png
        :return
            - file_url:         string - The path to the file on S3. This is returned only is return_url is set to true
        """
        self.connect()

        try:
            s3_file = Key(self.bucket)
            s3_file.key = self._generate_file_path(s3_path, filename)
            #--- Set the Content type for the file being sent (so that it downloads properly)
            #- content_type can be 'image/png', 'application/pdf', 'text/plain', etc.
            mime_type = mimetypes.guess_type(filename) if mime_type is None else mime_type
            s3_file.set_metadata('Content-Type', mime_type)

            #- Determine whether the file_to_store is an object or file path/string
            file_type = type(file_to_store)
            if file_type == str:
                s3_file.set_contents_from_filename(file_to_store)
            else:
                s3_file.set_contents_from_file(file_to_store)

            if return_url:
                file_key = self.bucket.get_key(s3_file.key)
                file_key.set_acl('public-read')
                file_url = file_key.generate_url(0, query_auth=False)
                return file_url

        except Exception as store_file_exception:
            message = "Exception while storing file on S3: {0}".format(store_file_exception)
            raise S3ClientException(message)

    def get_file(self, s3_path, file_to_get):
        """
        Stores the desired file locally (e.g. configuration file).
        :param
            - s3_path:      string - The S3 path to the folder which contains the file
            - file_to_get:  string - The name of the file you are looking for in the folder
        :return
            - retrieved_file    StringIO - an IO object containing the content of the file retrieved from S3
        """
        self.connect()

        try:
            if self.verify_file(s3_path, file_to_get):
                retrieved_file = StringIO()
                s3_file = self.bucket.get_key(
                    self._generate_file_path(s3_path, file_to_get))
                s3_file.get_contents_to_file(retrieved_file)
                return retrieved_file
            else:
                raise S3ClientException("File not found in S3")

        except Exception as get_file_exception:
            message = "Exception while retrieving file from S3: {0}".format(get_file_exception)
            raise S3ClientException(message)

    def verify_file(self, s3_path, file_to_verify):
        """
        Verifies a file (e.g. configuration file) is on S3 and returns
        "True" or "False".
        :param
            - s3_path:          string - The S3 path to the folder which contains the file
            - file_to_verify:   string - The name of the file you are looking for in the folder
        :return
            - boolean:     True if .get_key returns an instance of a Key object and False if .get_key returns None:
        """
        self.connect()
        try:
            file_path = self._generate_file_path(s3_path, file_to_verify)
            s3_file = self.bucket.get_key(file_path)
            if s3_file:
                return True
            else:
                return False

        except Exception as verify_file_exception:
            message = "Exception while verifying file on S3: {0}".format(verify_file_exception)
            raise S3ClientException(message)

    def _generate_file_path(self, s3_path, file_to_store):
        """
        Ensures that the / situation creates a proper path by removing any double slash possibilities
        :param
            - s3_path:       string - The path to the folder you wish to store the file in
            - file_to_store: string - The name of the file you wish to store
        :return
            - string:    The concatenated version of the /folder/filename path
        """
        return "{0}/{1}".format(s3_path.strip("/"), file_to_store.strip("/"))

    def get_all_filenames_in_folder(self, path_to_folder):
        """
        Retrieves a list of the files/keys in a folder on S3
        :param
            - path_to_folder:   string - The path to the folder on S3. This should start after the bucket name
        :return
            - key_list: list - The list of keys in the folder
        """
        self.connect()

        s3_folder_path = str(path_to_folder)
        key_list = self.bucket.list(prefix=s3_folder_path)
        return key_list

    def get_most_recent_file_from_s3_key_list(self, key_list):
        """
        Sorts through the list of files in s3 key list object and returns the most recently modified file in the list
        :param
            - key_list:    list - The list of files returned from a s3.bucket.list() operation
        :return
            - key   boto.s3.Key - The most recently modified file in the key list
        """
        most_recent_key = None
        for key in key_list:
            if not most_recent_key or key.last_modified > most_recent_key.last_modified:
                most_recent_key = key
        return most_recent_key


class S3ClientException(Exception):
    def __init__(self, message):
        self.msg = message

    def __str__(self):
        return self.msg