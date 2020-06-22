from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cff_user:geeknomads123@localhost/computingforfree' # used for ORM for class forms like login 
db = SQLAlchemy(app) # used for ORM for class forms like login and db access
class NoSession(db.Model):
    """NoSession class inherits from db.Model, a base class for all models from Flask-SQLAlchemy. 
    This class defines several fields as class variables.
    by: JS"""
    __tablename__= 'noSession'
    noSessionID = db.Column(db.Integer, primary_key=True)
    startDate = db.Column(db.DateTime)
    endDate = db.Column(db.DateTime)
    campusID = db.Column(db.Integer)

    '''def __repr__(self):
        """tells Python how to print objects of this class"""
        return '<User {}>'.format(self.username)
        '''
    def __init__(self, startDate, endDate, campusID):
        self.startDate = startDate
        self.endDate = endDate
        self.campusID = campusID
    

