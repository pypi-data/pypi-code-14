import os
import tempfile
import requests

with open('./../storage/f/2/f2912edc0aa959aef81093442ec715f0.jpg', 'rb') as tempf:
    response = requests.post('http://127.0.0.1:8000/api/internal/file_upload', headers={"Authorization": "Token {0}".format('9cab57ce6ee3b275afd7d1893f448a31da68f3a7')},  files={'file': tempf})
    response.raise_for_status()