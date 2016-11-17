import os
from django.conf import settings

db_path = os.path.join(os.path.dirname(__file__), 'analysis.db')

settings.DATABASES['analysis_sqlite3'] = {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': db_path
}

if not os.path.exists(db_path):
    print('do init db')
    from .db import init_db
    init_db()
