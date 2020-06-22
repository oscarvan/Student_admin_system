"""creates the application object as an instance of class Flask
imported from the flask package
 __name__ variable passed to the Flask class is a Python predefined variable, 
 which is set to the name of the module in which it is used.
 by Julie"""
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from datetime import timedelta
#from flask_bootstrap import Bootstrap


app = Flask(__name__)
app.config.from_object(Config) #use our config file
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=240)
#connection for user login 
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cff_user:geeknomads123@localhost/' + app.config['CFF_DB'] # used for ORM for class forms like login 
app.config['CFF_DB'] ='computingForFree'
app.config['DB_password'] = 'geeknomads123' 
db = SQLAlchemy(app) # used for ORM for class forms like login and db access
migrate = Migrate(app, db) # used for class forms like login and registration
#bootstrap = Bootstrap(app)

login = LoginManager(app)
login.login_view = 'login' # when login is required

#leave at bottom as this is a workaround to circular imports as routes needs to import app var defined above
from app import routes, models # models defines the structure of the database