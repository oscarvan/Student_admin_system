from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin # allows us to add properties and methods, generic implementations appropriate for most user model classes
from app import login
from app.sqlquery import Database
from datetime import date, timedelta, datetime #used to calc start end dates for calendar
from app.noschooldayinyearrange import no_school_years

class NoSession(db.Model):
    """NoSession class inherits from db.Model, a base class for all models from Flask-SQLAlchemy. 
    This class defines several fields as class variables.
    by: Julie"""
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
        #self.noSessionID = noSessionID
        self.startDate = startDate
        self.endDate = endDate
        self.campusID = campusID
    


class User(UserMixin, db.Model):
    """User class created above inherits from db.Model, a base class for all models from Flask-SQLAlchemy. 
    This class defines several fields as class variables.
    by: Julie"""
    #id = db.Column(db.Integer, primary_key=True)
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    campusID = db.Column(db.Integer)
    
    def __repr__(self):
        """tells Python how to print objects of this class"""
        return '<User {}>'.format(self.username)
    
    #Password hashing implemented in 2 methods of user model
    def set_password(self, password):
       # print("set_password")
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        #print("check_password")
        return check_password_hash(self.password_hash, password)

@login.user_loader
def load_user(id):
    """called to load a user given the ID as Flask doesnt know anything about db 
    argument id Flask-Login passes to the functionis a string, 
    so if db use numeric IDs need to convert the string to integer
    by: Julie"""
   # print("load_user")
    return User.query.get(int(id))


def get_sessions(ecampusID, edatepicked=None, ReturnIDs = False, esessionPeriod=False):
    ''' gets sessions AM, PM. EVE for a campus on a day of week like Mon
    argument 1: campus id
    argument 2: date   
                used on front page to populate session list after selecte date
    argument 3: optional 
                used on available session page
    argument 4: optional session period such as afternoon P or morning A
                used on available sessions page
    returns: list of sessions 
    by: Julie'''
    
    DB_object = Database()
    if ReturnIDs:
        # uses Argument campusID and return all sessions isactive true and false
        # this is used on session_schedule page to load AM or PM session on schedule
        sql = "SELECT * FROM cSession WHERE sessionPeriod = %s AND campusID = %s"  
       # print("returnID get_session") 
        sqllist_of_sessions = DB_object.sql_query_fetchall(sql, (esessionPeriod, ecampusID))
        return sqllist_of_sessions
    else: #ReturnIDs == False and edatepicked!=None: #and esessionPeriod == False) and edatepicked!=None:
        #return only active sessions uses Arguments emapusID, dayofweek from passed date
        #print( "returnid", ReturnIDs , "datepicked", edatepicked, "campus", ecampusID)
        sql= "SELECT sessionID, left(sessionPeriod,1) as sessionPeriod FROM cSession WHERE campusid = %s AND SessionDay = %s AND isActive = 1" 
        dayofweek =datetime.strptime(edatepicked, '%d-%m-%Y').strftime('%a')
        dayofweek = dayofweek[:2].upper() # have to change to upper 2 letters as stupidly stored in db as this
        #print("day", dayofweek)
        sqllist_of_sessions = DB_object.sql_query_fetchall(sql, (ecampusID, dayofweek), True) # dont want dictionary ba
    # this data should have a lookup table but too hard at mo to change db
    #print("sql sessions", sqllist_of_sessions)
    
    list_of_sessions=[]
    for session in sqllist_of_sessions:
        inner_list=[]
        #print(session['sessionPeriod'])f
        session_code = session['sessionPeriod']
        if session_code == 'A':
            session_name = 'Morning Session'
        elif session_code == 'P':
            session_name = 'Afternoon Session'
        elif session_code == 'E':
            session_name = 'Evening Session'
        inner_list = [session['sessionID'], session_name]
        list_of_sessions.append(inner_list)
    
    return list_of_sessions     

def daterange(date1, date2):
    '''function to subtract startdate from enddate to know how many days disable on calendar
    argument 1: from date
    argument 2: to date 
    by: Julie'''
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)


def get_disabled_dates(ecampusID=0):
    ''' gets dates that location is closed
    argument 1: campus id  optional
    returns: list of dates 
    if no campusID then only get statatory hols
    by: Julie'''
    DB_object = Database()  #nitialize db obj
    disabled_dates=[]        #initialize empty list
    
    if ecampusID != 0:
        sql='''SELECT noSessionID, campusID, startDate, endDate FROM nosession WHERE campusID = %s'''
    # print(sql)
        no_sesion_rows = DB_object.sql_query_fetchall(sql, (ecampusID, ))
        #print(no_sesion_rows)
        for no_session in no_sesion_rows:                       
            #loop through list and pull out start and end dates from dictionary item
            start_dt =(no_session.get("startDate"))
            end_dt= no_session.get("endDate")
            #loop through start and end date for this dictionary
            for dt in daterange(start_dt, end_dt):
                #append to disabled date list
                disabled_dates.append(dt.strftime("%d-%m-%Y"))
        
    # get statutory holidays from func-----------------------------------------------------------
    no_school_day = no_school_years(2018,2019)                                     
    #append statutory list to noSessions list
    i= 0    
    while i < len(no_school_day):
        for day in no_school_day[i]:
            disabled_dates.append(day.strftime("%d-%m-%Y"))
           # print(type(day.strftime("%Y-%m-%d")))
        i = i + 1

    return disabled_dates
def get_campus_list():
    '''gets a list of all campus 
    by: Julie'''
    DB_object = Database()
    sql_all_branches = "SELECT campusName, campusID from campus;"
    campus_list = DB_object.sql_query(sql_all_branches)
    return campus_list
    
def get_students(enrolled=False):
    '''returns list of students 
    ARgument: enrolled shows only students enrolled in a course
    by: Julie'''
    DB_object = Database()
    if enrolled:
        sql= "SELECT student.*\
            FROM student\
            INNER JOIN enrolment ON student.studentID=enrolment.studentID"
    else: # show all students
        sql= "select * from student"

    #should only show students enrolled  sql = "select * from student inner join enrolment on enrolment.studentID =student.studentID ;"
    list_of_students = DB_object.sql_query(sql)
    return list_of_students