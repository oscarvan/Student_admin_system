"""specify configuration options for app
define variables as keys in app.config
uses a dictionary style to work with variables"""
import os
#from app import app
# basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@localhost/computingforfree' # used for ORM for class forms like login 
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CFF_DB ='computingForFree'