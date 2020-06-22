from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from wtforms.fields.html5 import DateField
from app.sqlquery import Database

'''This is where the FlaskForm base class is imported from at the top of app/forms.py.
by Julie'''

class NoSessionsForm(FlaskForm):
    ''' No session form ie dates campus closed
    by Julie '''
    DB_object = Database()
    sql = "SELECT cast(campusID as char) campusID, campusName from campus;"
    campus_list = list(DB_object.sql_query(sql,False))
    campusID = SelectField('Campus', choices=campus_list , validators=[DataRequired()]) 
    startDate = DateField('Start Date', format='%Y-%m-%d', validators=[DataRequired()]) 
    endDate = DateField('End Date', format='%Y-%m-%d', validators=[DataRequired()]) 
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    """ login form
    fields defined in LoginForm class know how to render themselves as HTML
    by Julie"""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')  
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    """registration form for staff
    by Julie"""
    DB_object = Database()
    sql = "SELECT cast(campusID as char) campusID, campusName from campus;"
    campus_list = list(DB_object.sql_query(sql,False))
    #print(campus_list)
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    campusID = SelectField('campusID', choices=campus_list , validators=[DataRequired()]) #[('1', 'Hornby'), ('2', 'Ricarton'), ('3', 'Rangiora')])
    submit = SubmitField('Register')
    #state = SelectField('State:', validators=[DataRequired()], id='select_state')
    

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')