import os
basedir = os.path.abspath(os.path.dirname(__file__))



SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(os.path.join(basedir, 'db') , 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(os.path.join(basedir, 'db') , 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = True
