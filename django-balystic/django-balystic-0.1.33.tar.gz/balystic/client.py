import requests
from django.conf import settings


def _url(path):
    return ''


class Client(object):
    """
    Encapsulates all the logic to consume the services provided
    by the balystic API.
    """
    AUTH_ENDPOINT = 'authenticate/'
    SIGNUP_ENDPOINT = 'signup/'
    USER_ENDPOINT = 'users/'
    BLOG_ENDPOINT = 'blog/'
    QA_ENDPOINT = 'qa/'

    def __init__(self):
        """
        Token should be provided by the admin of the community.
        Root must be the full path to the api root
        i.e. http://sample.7dhub.com/api/
        """
        self.headers = {
            'Authorization': 'TOKEN ' + settings.BALYSTIC_API_TOKEN}
        self.root = settings.BALYSTIC_API_PATH

    def _make_request(self, path, method, data=None, params=None):
        """
        Encapsulates error handling. Sets an standard way to handle
        requests across the client.
        Path should end with slash.
        """
        if method == 'GET':
            request_method = requests.get
        elif method == 'POST':
            request_method = requests.post
        elif method == 'DELETE':
            request_method = requests.delete
        elif method == 'PUT':
            request_method = requests.put
        full_path = self.root + path
        try:
            response = request_method(full_path, headers=self.headers,
                                      data=data, params=params)
            if response.status_code != 200 and response.status_code != 400:
                return {'error': {'value': 'Wrong status code',
                                  'code': response.status_code}}
            return response.json()
        except requests.exceptions.MissingSchema:
            return {'error': 'The supplied API endpoint is missing the schema'}
        except requests.exceptions.ConnectionError:
            return {'error': 'Cannot communicate with server'}
        except requests.exceptions.Timeout:
            return {'error': 'Server is not responding'}

    def get_users(self, params=None):
        """
        Retrieves the list of users in the community.
        There are two kind of users, owners and regular users.
        """
        return self._make_request(self.USER_ENDPOINT, 'GET', params=params)

    def get_user_detail(self, username):
        """
        Retrieves an user detail.
        The user must be in the community for this to work.
        """
        return self._make_request(
            self.USER_ENDPOINT + username + '/', 'GET')

    def delete_user(self, username):
        """
        Removes an user from the community.
        """
        return self._make_request(
            self.USER_ENDPOINT + username + '/', 'DELETE')

    def add_user(self, username):
        """
        Adds an user to the community.
        """
        return self._make_request(
            self.USER_ENDPOINT + username + '/', 'POST')

    def update_user(self, username, data):
        """
        Update user details
        """
        return self._make_request(
            self.USER_ENDPOINT + username + '/', 'PUT', data=data)

    def get_blogs(self, page=1):
        """
        Retrieves the list of blog posts in the community
        """
        return self._make_request(
            self.BLOG_ENDPOINT + '?page=' + str(page), 'GET')

    def get_blog_detail(self, slug):
        """
        Retrieves a blog post detail
        """
        return self._make_request(
            self.BLOG_ENDPOINT + slug + '/', 'GET')

    def delete_blog(self, slug):
        """
        deletes a blog post
        """
        return self._make_request(
            self.BLOG_ENDPOINT + slug + '/', 'DELETE')

    def get_questions(self, page=1, noans_page=1):
        """
        retrieves the list of questions on a
        community
        """
        return self._make_request(
            self.QA_ENDPOINT + '?page=' + str(page) +
            '&noans_page=' + str(noans_page), 'GET')

    def create_question(self, data):
        """
        creates a question
        """
        return self._make_request(
            self.QA_ENDPOINT, 'POST', data=data)

    def get_question_detail(self, pk):
        """
        Retrieves a blog post detail
        """
        return self._make_request(
            self.QA_ENDPOINT + pk + '/', 'GET')

    def edit_question(self, pk, data):
        """
        edits a question
        """
        return self._make_request(
            self.QA_ENDPOINT + pk + '/', 'PUT', data=data)

    def vote_question(self, pk, data):
        """
        Create a vote for an question
        """
        return self._make_request(
            self.QA_ENDPOINT + 'vote/question/' + pk + '/', 'POST', data=data)

    def delete_question(self, pk, email):
        """
        Removes a question if the owner
        is related to the provided email
        """
        return self._make_request(
            self.QA_ENDPOINT + pk + '/', 'DELETE', data={'user_email': email})

    def close_question(self, pk, data):
        """
        closes a question
        """
        return self._make_request(
            self.QA_ENDPOINT + 'question/close/' + pk + '/',
            'POST', data=data)

    def create_answer(self, pk, data):
        """
        creates an answer for a question
        """
        return self._make_request(
            self.QA_ENDPOINT + pk + '/', 'POST', data=data)

    def select_answer(self, pk, data):
        """
        mark an answer as the best answer
        """
        return self._make_request(
            self.QA_ENDPOINT + 'question/answer/' + pk + '/',
            'POST', data=data)

    def create_comment(self, instance, pk, data):
        """
        creates a comment for an answer or a question
        """
        return self._make_request(
            self.QA_ENDPOINT + 'comment/' + instance + '/' +
            pk + '/', 'POST', data=data)

    def edit_comment(self, instance, pk, data):
        """
        edits a comment for an answer or a question
        """
        return self._make_request(
            self.QA_ENDPOINT + 'comment/' + instance + '/' +
            pk + '/', 'PUT', data=data)

    def delete_comment(self, instance, pk, email):
        """
        deletes a comment for an answer or a question
        """
        return self._make_request(
            self.QA_ENDPOINT + 'comment/' + instance + '/' +
            pk + '/', 'DELETE', data={'user_email': email})

    def edit_answer(self, pk, data):
        """
        edits an answer
        """
        return self._make_request(
            self.QA_ENDPOINT + 'answer/' + pk + '/', 'PUT', data=data)

    def vote_answer(self, pk, data):
        """
        Create a vote for an answer
        """
        return self._make_request(
            self.QA_ENDPOINT + 'vote/answer/' + pk + '/', 'POST', data=data)

    def delete_answer(self, pk, email):
        """
        Removes an answer if the owner is related
        to the provided email
        """
        return self._make_request(
            self.QA_ENDPOINT + 'answer/' + pk + '/',
            'DELETE', data={'user_email': email})

    def authenticate_user(self, email, password):
        """
        Verifies the credentials of an user on server
        """
        data = {'email': email, 'password': password}
        return self._make_request(
            self.AUTH_ENDPOINT, 'POST', data)

    def signup_user(self, **kwargs):
        """
        Wraps signup of users
        """
        return self._make_request(
            self.SIGNUP_ENDPOINT, 'POST', kwargs)
