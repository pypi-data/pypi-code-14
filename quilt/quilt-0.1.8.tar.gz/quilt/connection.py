import json
from getpass import getpass
import requests
import sys
import os

from mimetypes import MimeTypes
from multiprocessing import Pool

from .lib import *
from .table import *
from .util import *

def status_check(response):
    if response.status_code != requests.codes.ok:
        print("Warning: server responded with %s" % response.status_code)


class Connection(object):

    def __init__(self, username, url=QUILT_URL):
        self.url = url
        self.username = username
        self.password = os.environ.get('QUILT_PASSWORD') or getpass()
        self.auth = requests.auth.HTTPBasicAuth(self.username, self.password)
        self.status_code = None
        self.userid = None
        self.__tables = None
        self._files = None
        self._pool = None
        self._sqlengine = None
        response = requests.get("%s/users/%s/" % (self.url, username),
                                headers=HEADERS,
                                auth=requests.auth.HTTPBasicAuth(self.username, self.password))
        self.status_code = response.status_code
        if response.status_code == requests.codes.ok:
            userdata = response.json()
            self.userid = userdata['id']
            self.profile = userdata['profile']
            if SQLALCHEMY:
                self._sqlengine = sa.create_engine(userdata['odbc']['url'])
        else:
            print("Login Failed. Please check your credentials and try again.")

    def __del__(self):
        if self._pool:
            self._pool.close()
            self._pool.join()

    def get_thread_pool(self):
        if not self._pool:
            self._pool = Pool(processes=8)
        return self._pool

    def search(self, search):
        matches = []
        if isinstance(search, list):
            terms = search
        else:
            terms = [search]

        params = {'search' : ",".join(terms)}
        response = requests.get("%s/tables/" % (self.url),
                                headers=HEADERS,
                                params=params,
                                auth=self.auth)
        if response.status_code == 200:
            data = response.json()
            results = data.get('results', [])
            matches = [Table(self, d) for d in results]
        else:
            print("Oops, something went wrong.")
            print("response=%s" % response.status_code)

        return matches

    @property
    def tables(self):
        if not self.__tables:
            self.__tables = []
            next_link = "%s/tables/?owner__username=%s" % (self.url, self.username)
            while next_link:
                print("Fetching tables from %s" % next_link)
                response = requests.get(next_link,
                                        headers=HEADERS,
                                        auth=requests.auth.HTTPBasicAuth(self.username, self.password))
                self.status_code = response.status_code
                if response.status_code == requests.codes.ok:
                    userdata = response.json()
                    self.__tables += [Table(self, d) for d in userdata['results']]
                    next_link = userdata['next']
                else:
                    print("Oops, something went wrong.")
                    print("response=%s" % response.status_code)

        return self.__tables

    @property
    def files(self):
        if not self._files:
            response = requests.get("%s/files/" % (self.url),
                                    headers=HEADERS,
                                    auth=requests.auth.HTTPBasicAuth(self.username, self.password))
            self.status_code = response.status_code
            if response.status_code == requests.codes.ok:
                filedata = response.json()
                print(filedata)
                self._filedata = filedata
                self._files = [File(self, d) for d in filedata['results']]
            else:
                print("Oops, something went wrong.")
                print("response=%s" % response.status_code)
                self._files = []
        return self._files

    def get_table(self, table_id, branch=None, index=None):
        response = requests.get("%s/tables/%s/" % (self.url, table_id),
                                headers=HEADERS,
                                auth=self.auth)
        
        if response.status_code == requests.codes.ok:
            return Table(self, response.json(), branch=branch, index=index)
        else:
            print("Oops, something went wrong.")
            print(response.text)
            return None

    def create_table(self, name, description=None, columns=None, inputfile=None):
        data = { 'name' : name }
        if description:
            data['description'] = description
        if inputfile:
            if columns:
                print("Please specify either a set of columns or an input file, not both")
                return None

            if isinstance(inputfile, File):
                data['csvfile'] = inputfile.fullpath
            else:
                f = self.upload(inputfile)
                data['csvfile'] = f.fullpath
        elif columns:
            data['columns'] = columns

        response = requests.post("%s/tables/" % self.url,
                                 data = json.dumps(data),
                                 headers=HEADERS,
                                 auth=self.auth)

        if response.status_code == requests.codes.ok:
            return Table(self, response.json())
        else:
            print(response.text)
            return response.text

    def save_df(self, df, name, description=None):
        if not PANDAS:
            print("Install pandas to use DataFrames: http://pandas.pydata.org/")
            return None

        schema = { 'name' : name, 'columns' : [] }
        if description:
            schema['description'] = description

        for i, col in enumerate(df.columns):
            dt = df.dtypes[i]
            schema['columns'].append({'name' : col, 'sqlname' : col, 'dtype' : str(dt) }) 

        response = requests.post("%s/tables/" % self.url,
                                 data = json.dumps(schema),
                                 headers=HEADERS,
                                 auth=self.auth)

        if response.status_code == requests.codes.ok:
            table = Table(self, response.json())
        else:
            print(response.text)
            return None

        chunksz = 250
        maxreq = 40
        nrows = len(df.index)
        res = []

        for start in range(0, nrows, chunksz):
            end = start + chunksz

            while len(res) > maxreq:
                finished = [(r, b) for r, b in res if r.ready()]
                res[:] = [(r, b) for r, b in res if not r.ready()]
                for r, b in finished:
                    if not r.successful():
                        print("Retrying:")
                        print(b)
                        res.append((t.create_async(b, status_check), b))
                if len(res) > maxreq:
                    r, b = res[0]
                    r.wait()

            buffer = df[start:end].to_json(orient='records')
            res.append((table.create_json_async(buffer, callback=status_check), buffer))
        return table

    def upload(self, filepath):
        filename = filepath.split('/')[-1]
        mime = MimeTypes()
        mime_type = mime.guess_type(filename)
        data = { 'filename' : filename, 'mime_type' : mime_type }
        response = requests.post("%s/files/" % self.url,
                                 data = json.dumps(data),
                                 headers=HEADERS,
                                 auth=self.auth)

        if response.status_code == requests.codes.created:
            f = File(self, response.json())
            with open(filepath, 'rb') as localfile:
                response = requests.put(f.upload_url,
                                        data=localfile)
                return f
        else:
            print(response.text)
