import os

global settings
settings = {
    'settingsfile': str(os.path.join(os.path.expanduser("~"), ".golden-retriever.yaml")),
    'url': 'http://localhost:8080',
    'timeout': 60
}