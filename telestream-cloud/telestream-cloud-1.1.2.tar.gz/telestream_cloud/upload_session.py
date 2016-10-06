import requests
import json
import os
import threading

from .request import TelestreamCloudRequest, TelestreamCloudException

CHUNK_SIZE = 5 * 1024 * 1024


class UploadSession(object):

    def __init__(self, credentials, file_name, threads = 8, **kwargs):
        self.credentials = credentials
        self.file_name = file_name
        self.file_size = os.stat(file_name).st_size
        params = {
            "file_size": self.file_size,
            "file_name": file_name,
            "profiles": "h264",
            "multi_chunk": "true",
        }
        params.update(kwargs)

        data = TelestreamCloudRequest('POST', '/videos/upload.json',
                                      self.credentials, params).send()
        json_data = data.json()

        self.location = json_data['location']

        self.part_size = int(json_data["part_size"])
        self.parts = int(json_data["parts"])
        self.missing_parts = range(self.parts - 1, -1, -1)

        self.status = "initialized"
        self.video = None
        self.error_message = None

        self.n_threads = threads
        self.lock = threading.Lock()

    def read_chunks(self):
        while True:
            if not self.missing_parts:
                break

            self.lock.acquire()

            i = self.missing_parts.pop()

            self.file_object.seek(i * self.part_size)
            data = self.file_object.read(self.part_size)

            self.lock.release()

            if not data:
                break

            yield (data,i)

    def send_chunks(self):
        for chunk, i in self.read_chunks():
            if self.status == "aborted":
                break

            res = requests.post(self.location, headers={
                'Content-Type': 'application/octet-stream',
                'Cache-Control': 'no-cache',
                'X-Part' : str(i),
                'Content-Length' : str(min(self.part_size, len(chunk))), },
                                data = chunk)

            if res.text and json.loads(res.text)["status"] in ("processing"):
                self.status = "uploaded"
                from .models import Video
                self.video = Video(self.credentials, res.json())



    def start(self, pos=0):
        if self.status == "initialized":
            self.status = "uploading"

            self.file_object = open(self.file_name, "rb")

            if self.n_threads > 1:
                threads = []

                for i in range(0, self.n_threads):
                    thread = threading.Thread(target=self.send_chunks)
                    threads.append(thread)
                    thread.start()

                for thread in threads:
                    thread.join()
            else:
                self.send_chunks()

            self.missing_parts = []

            data = requests.get(self.location)

            if data.text:
                print (data.text)
                json_data = json.loads(data.text)
                if json_data.has_key('missing_parts'):
                    self.missing_parts = ['missing_parts']
                    self.missing_parts.reverse()
                    raise TelestreamCloudException('Failed to upload some parts, missing parts: %s' % self.missing_parts)
        else:
            raise KeyError("Already started")

    def resume(self):
        if self.status != 'uploaded':
            self.start()
        else:
            raise TelestreamCloudException('File already uploaded')

    def abort(self):
        if self.status != 'uploaded':
            self.status = 'aborted'
            self.error_message = None
            res = requests.delete(self.location)
        else:
            raise TelestreamCloudException('File already uploaded')
