"""routes are the different URLs that the application implements.
In Flask, handlers for the application routes are written as Python functions,
aka view functions which are mapped to one or more route URLs so that Flask knows what logic to execute """
from flask import Flask, render_template, flash, redirect, request, url_for, make_response, send_from_directory, jsonify
from app import app
from app.forms import LoginForm, NoSessionsForm
from flask_login import current_user, login_user
from app.models import User, NoSession
from app import db
from app.forms import RegistrationForm
from flask_login import logout_user
from flask_login import login_required
from werkzeug.urls import url_parse
from datetime import date, timedelta, datetime #used to calc start end dates for calendar
#from app.sqlquery import sql_query_fetchone, sql_query_fetchall, sql_update_insert, Database ##, sql_query
from app.sqlquery import Database
from app.models import get_sessions, get_disabled_dates, get_students, get_campus_list
import os
import json
from flask import send_from_directory

@app.route('/', methods=['POST','GET'])
@app.route('/index', methods=['POST','GET'])
@login_required
def index(campusid=1): #defaults to AraCity, datepicked=(date.today())    , sessionid=None,  datetext=None
    #sessionid=esessionID, campusid=ecampusID , datetext=edate)
    """load main page
    by: Julie and worked with oscar on sql to load students in class"""

    DB_object = Database()
    #for search for students enrolled in a course datatable
    list_of_students= get_students(True)

    campus_list = get_campus_list()
    #print(campus_list)
    # get the campus ID from the dropdown.   default of 1 is passed

    ecampusID = request.args.get('campusid')
    esession = request.args.get('sessionid')
    if (ecampusID is None or ecampusID =='None'):
        #go back to home page as no class selected and nothing to return
        book_list=[]
        disabled_dates=[]
        list_of_sessions=[]
        return render_template('index.html', list_of_students=list_of_students, title='Home', campus_list=campus_list,list_of_sessions=list_of_sessions)
        #ecampusID=campusid
    elif ecampusID != None and  ecampusID !='None':
       # print("ecampusID index",ecampusID)
        ecampusID = int(ecampusID)

    edatepicked= request.args.get('datetext')
    if edatepicked is None:
       # print("date is none")
        list_of_sessions =[]
        #edatepicked=edatepicked.strftime("%d-%m-%Y")
    elif edatepicked is not None:
       # print("date not none")
        edatepicked = datetime.strptime(request.args.get('datetext'), '%d-%m-%Y').strftime("%d-%m-%Y")
        sqlDate =  datetime.strptime(edatepicked, '%d-%m-%Y').strftime("%Y-%m-%d")
        #get sessions AM, PM. EVE for day eg Mon
        list_of_sessions = get_sessions(ecampusID, edatepicked)
        #print("session list index", list_of_sessions)


    #-------get sessions --------------------------------------
    if (esession is None) or (ecampusID is None):
        # dont run query
        book_list = []
        list_of_sessions=[]
    else:
        sql= "SELECT attenbooking.attenbookingID, attenbooking.studentID,\
            enrolment.courseID, student.firstName, student.lastName, attenbooking.action, cSession.campusID\
            FROM attenbooking\
            INNER JOIN student ON attenbooking.studentID=student.studentID\
            INNER JOIN enrolment ON student.studentID=enrolment.studentID\
            INNER JOIN cSession ON attenbooking.sessionID = cSession.sessionID\
            WHERE cSession.campusID  =%s AND actionTime = %s AND attenbooking.sessionID =%s AND attenbooking.action = 'book' OR attenbooking.action = 'checkin'"

        print("session for sql", sql)
        print("variables", ecampusID, sqlDate, esession)
        book_list = DB_object.sql_query_fetchall(sql, (ecampusID, sqlDate, esession))
        print(book_list)


    #-select campus-------------------------------------
    disabled_dates=[]        #initialize empty list
    disabled_dates = get_disabled_dates(ecampusID)
    #print(list_of_sessions)
    #also sends back date, location, session to reselect items in controls

    return render_template('index.html', list_of_students=list_of_students, title='Home', book_list=book_list, disabled_dates=disabled_dates, ecampusID= ecampusID,  campus_list= campus_list, edatepicked=edatepicked, esession=esession, list_of_sessions=list_of_sessions)


@app.route('/check_in', methods=['GET'])
def check_in():
    DB_object = Database()
    attenbookingID = request.args.get('attenID')
    #print (attenbookingID)
    edate = request.args.get('datetext')
    esessionID = request.args.get('sessionMenu')
    ecampusID = request.args.get('campusid')

    if request.method == 'GET':

        check_in_sql = "UPDATE attenbooking SET attenbooking.action = 'checkin' WHERE attenbooking.attenbookingID = %s;"

        values = DB_object.sql_update_insert(check_in_sql, (attenbookingID,))

        redirect_to_index = redirect(url_for('index', campusid=ecampusID , sessionid=esessionID, datetext=edate))
        response = make_response( redirect_to_index)
        return response


@app.route('/cancel', methods=['GET'])
def cancel():
    DB_object = Database()
    attenbookingID = request.args.get('attenID')

    edate = request.args.get('datetext')
    esessionID = request.args.get('sessionMenu')
    ecampusID = request.args.get('campusid')

    if request.method == 'GET':

        cancel  = "UPDATE attenbooking SET attenbooking.action = 'cancel' WHERE attenbookingID = %s;"

        msg = DB_object.sql_update_insert(cancel, (attenbookingID,))

        redirect_to_index = redirect(url_for('index', campusid=ecampusID , sessionid=esessionID, datetext=edate))
        response = make_response( redirect_to_index)
        return response

#to add searched student to the selected branch, date and session above
@app.route('/book_student', methods=['GET'])
def book_student():
    DB_object = Database()
    #this grabs selected studentID from url and assigns to object studentID
    estudentID = request.args.get('studentID')
    edate = request.args.get('datetext')
    esessionID = request.args.get('sessionMenu')
    ecampusID = request.args.get('campusid')
    #these 'objects' are passed to sql insert statement below through the '%s'

    if request.method == 'GET':
        #if (edate !=None) and (esessionID !=None ):
        sqlDate =  datetime.strptime(edate, '%d-%m-%Y').strftime("%Y-%m-%d")
        book_SQL = "INSERT INTO attenbooking (studentID, actionTime ,sessionID, action)\
                    VALUES (%s, %s, %s, %s);"

        msg = DB_object.sql_update_insert(book_SQL, (estudentID, sqlDate, esessionID, 'book'))
        flash(msg)
        #else:
        #flash("Please Select Campus, Date & Session to Find a Class to Book-into")

        redirect_to_index = redirect(url_for('index', studentID=estudentID,campusid=ecampusID , sessionid=esessionID, datetext=edate))
        response = make_response( redirect_to_index)
        return response

#to add searched student to the selected branch, date and session above
'''@app.route('/book_student', methods=['GET'])
def book_student():
    DB_object = Database()
    #this grabs selected studentID from html and assigns to object studentID
    #, selected_date and selected_sessionID here
    estudentID = request.args.get('studentID')
    edate = request.args.get('datetext')
    ecampusID = request.args.get('campusid')
    esessionID = request.args.get('sessionMenu')
    #these 'objects' are passed to sql insert statement below through the '%s'
    print(estudentID)
    print(edate)
    print(esessionID)

    if request.method == 'GET':
        sqlDate =  datetime.strptime(edate, '%d-%m-%Y').strftime("%Y-%m-%d")
        book_SQL = "INSERT INTO attenbooking (studentID, actionTime ,sessionID, action)\
                    VALUES (%s, %s, %s, %s);"

        values = DB_object.sql_update_insert(book_SQL, (estudentID, sqlDate, esessionID, 'book'))

        #msg = 'session booked for ' estudentID
        redirect_to_index = redirect(url_for('index', studentID=estudentID,campusid=ecampusID , sessionid=esessionID, datetext=edate))
        response = make_response( redirect_to_index)
        return response

'''

@app.route('/student_search', methods=['GET', 'POST'])
def student_search():
    ''' search and select students
    with or without a WHERE clause depends on how Peter wants to restrict
    by Julie'''
    msg=""
    list_of_students=[]
    DB_object = Database()

    #request.args.get('studentID'):
    sql= """SELECT * FROM student """
    list_of_students = DB_object.sql_query(sql)
    #sql = '''SELECT * FROM student WHERE firstName like %s'''
    #sql = "SELECT * FROM student WHERE firstName = "
    #list_of_students=DB_object.sql_query_fetchall(sql, ('e%',))
    #list_of_students=DB_object.sql_query_fetchall(sql, ('Frances',))

    print(msg) # msg returned for update insert query as no data is

    return render_template('index_search.html', list_of_students=list_of_students)


@app.route('/login', methods=['GET', 'POST'])
def login():
    '''staff login and checks password using werkzeug.security  function
    DO NOT COPY as OO based form using SQLAlchemy
    by: Julie'''
    if current_user.is_authenticated:
        #current_user comes from Flask-Login can be used at any time during to get user
        # object that represents the client of the request comes from db
        print("authenticated")
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print("user", user)
        if user is None or not user.check_password(form.password.data):
            print("password/username invalid")
            flash('Invalid username or password')
            return redirect(url_for('login'))
        #login_user(user,False)
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    """logs out user
    by: Julie"""
    logout_user()
    return redirect(url_for('index'))


@app.route('/student_page')
def student_page():
    """student_page """
    return render_template('student_page.html')

@app.route('/register', methods=['GET', 'POST'])
#@login_required
def register():
    '''register a user - uses sqlalchemy classes forms.py and models.py
    DO NOT COPY as OO based form using SQLAlchemy
    by: Julie'''
    form = RegistrationForm()
    if form.validate_on_submit():
    #if request.method=="POST":
        user = User(username=form.username.data, email=form.email.data,campusID=form.campusID.data)
        user.set_password(form.password.data)
     #   print("in save")
      #  print(user)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    else:
        return render_template('register.html', title='Register', form=form)

@app.route('/staff', methods=['POST','GET'])
def staff():
    '''open add staff page
    by: Julie'''

    return render_template('staff.html')


# <!--  Kattia's Code -->
@app.route('/student', methods=['POST','GET'])
def student():
    '''open add_student page'''
    DB_object = Database()

    if request.method == 'POST':

        email = request.form ["email"]
        firstName = request.form ["firstName"]
        lastName = request.form ["lastName"]
        homePhoneNumber = request.form ["homePhoneNumber"]
        middleName = ""
        gender = ""
        MobileNumber = request.form ["MobileNumber"]
        studentID = request.form ["studentID"]

        sql= "INSERT INTO student (studentID, firstName, middleName, lastName, gender, homePhoneNumber, MobileNumber, emailAddress) VALUES (%s, %s, %s, %s, %s,%s, %s, %s)"
        msg = DB_object.sql_update_insert(sql, (studentID, firstName, middleName,lastName,gender,homePhoneNumber, MobileNumber,email,))
        #flash('Congratulations, you registered a Student!')
        #flash(msg)
    return render_template('student.html')
# <!--  Kattia's Code -->

# <!--  Oscars Code -->
@app.route('/edit_student', methods=['POST','GET'])
def edit_student():
    '''open edit_student page'''
    DB_object = Database()
    #this grabs selected studentID from html and assigns to object studentID
    #, selected_date and selected_sessionID here
    estudentID = request.args.get('studentID')
    print("estudent",estudentID)

    student_sql= """SELECT * FROM student WHERE studentID = %s """
    student_details = DB_object.sql_query_fetchone(student_sql, (estudentID,))

    # update student data if form data is posted
    if request.method == 'POST':

        studentID = request.form ["studentID"]
        firstName = request.form ["firstName"]
        lastName = request.form ["lastName"]
        MobileNumber = request.form ["MobileNumber"]
        homePhoneNumber =  request.form ["homePhoneNumber"]
        email = request.form ["email"]
        emoodle = request.form ["moodle"]
        enote = request.form ["notes"]

        edit_student_sql= "UPDATE student SET studentID = %s, firstName = %s, lastName = %s, mobileNumber = %s, homePhoneNumber= %s, emailAddress = %s, lastMoodleEngagement = %s, note =%s WHERE studentID = %s"
        msg = DB_object.sql_update_insert(edit_student_sql, (studentID, firstName, lastName, MobileNumber, homePhoneNumber, email, emoodle, enote, studentID,))

        flash(msg)
        student_sql= """SELECT * FROM student WHERE studentID = %s """
        student_details = DB_object.sql_query_fetchone(student_sql, (studentID,))
        return render_template('edit_student.html', student_details=student_details, )
        # redirect_to_index = redirect(url_for('edit_student', studentID=studentID))
        # response = make_response( redirect_to_index)
        # return response
        print("studen", student_details)

    return render_template('edit_student.html', student_details=student_details)
# <!--  Oscars Code -->

@app.route('/api/getsessions.html', methods=['POST','GET'])
def getsessions():
    '''uses javascript and ajax to get the sessions for a date onchange of datepicker
    from the db but
    doesnt load the page again
    by: Julie'''
    ecampusID = request.args.get('campusid')
    #print("campus", ecampusID)
    edateText = request.args.get('datetext')
    edateText = datetime.strptime(request.args.get('datetext'), '%d-%m-%Y').strftime("%Y-%m-%d") #format for MySQL
    DB_object = Database()
    #print("get sessions datepicker ", edateText)
    dayofweek =datetime.strptime(edateText, '%Y-%m-%d').strftime('%a')
    dayofweek=dayofweek[0:2].upper() #this is stupidly how we store in DB, if Id know about this function...
    sql= "SELECT sessionID, left(sessionPeriod,1) as sessionPeriod FROM cSession WHERE campusid = %s AND SessionDay = %s AND isActive=1"
    list_of_sessions = DB_object.sql_query_fetchall(sql, (ecampusID,dayofweek), True) # dont want dictionary back to load for dropdown list
   # list_of_sessions= get_sessions(ecampusID, edateText)
    #print("list",list_of_sessions)
    #print(list_of_sessions)
    option_str = "<option value='none'>Select Session</option>"
    for session in list_of_sessions:
        #print(session['sessionPeriod'])
        str_session = session['sessionPeriod']
        if str_session == 'A':
            session_name = 'Morning Session'
        elif str_session == 'P':
            session_name = 'Afternoon Session'
        elif str_session == 'E':
            session_name = 'Evening Session'
        option_str = option_str + '<option value="'+ str(session['sessionID']) +'">' + session_name + '</option>'
    #returns html to create select list options
    return option_str


@app.route('/session_schedule')
def session_schedule(campusid=None):
    '''opens session schedule    ie at Hornby   Mon am, Mon pm, Tues am etc
    by: Julie'''
    campus_list = get_campus_list()
    #print("campusid in session_schedule ", campusid)
    ecampusID = request.args.get('campusid')
    list_of_sessions = get_sessions(ecampusID,date.today, True, "A")
    list_of_PMsessions = get_sessions(ecampusID,date.today, True, "P")
    list_of_Evesessions = get_sessions(ecampusID,date.today, True, "E")
    #print("list_of_sessions",list_of_sessions)
    #print ("session campus", ecampusID)
    return render_template('sessions.html', title='Session Schedule', ecampusID=ecampusID, campus_list=campus_list, list_of_sessions=list_of_sessions, list_of_PMsessions=list_of_PMsessions, list_of_Evesessions=list_of_Evesessions)

@app.route('/save_weekly_sessions', methods=['POST','GET'])
def save_weekly_sessions():
    '''Save weekly sessions by location on sessions.html page
    by: Julie'''

    DB_object = Database()
    #if user has selected a course for the student to be enrolled in, insert the new record into the enrollment table
    if request.method == 'POST':
        campusid = request.form["campusID"]
       # print("campus from form" , campusid)
        #checkboxes = request.form.getlist("sesssionChkbox")
        #for checkbox in checkboxes:    bummer this just returned a list of 0s
        #update all sessions as inactive off for this campus, as dont know off unticked checkboxes as not returned
        sql="update cSession set isActive =0 where campusID=%s"
        #set sessions with checkbox off
        msg = DB_object.sql_update_insert(sql, (campusid,))

        keys = request.form
        f = request.form
        session_on_list =[]
        session_on_list=""
        for key in f.keys():
            for value in f.getlist(key):
                #nb only get on ticked checkboxes returned
                if "campusID" not in key: #only want checkboxes
                    #print( key,":",value, " " , str(key[6:]))   # shows as value=5 : on      value=3 : on
                    session_on_list = session_on_list + key[6:] + ", "
        session_on_list = session_on_list[:-2]  # take off comma
        #print(session_on_list)
        sql= "UPDATE cSession set isActive =1 WHERE campusID=" + campusid + " AND sessionID IN("+ session_on_list + ");"
        #sql = "UPDATE cSession set isActive =1 WHERE campusID=%s AND sessionID IN(%s)"
        #DB_object.sql_update_insert(sql, (campusID, session_on_list))
        norow= DB_object.sql_update_novar(sql)
       # print(sql)
        #print("norow", norow)

        flash(msg)
        #for ctr_tickboxs in request.:
         #   print(ctr_tickboxs)
    return redirect(url_for('session_schedule', title='Session Schedule', campusid=campusid))

@app.route('/favicon.ico')
def fav():
    """routes the favicon to show tabs in browser
    By: Julie"""
    return send_from_directory(os.path.join(app.root_path, 'static'),'favicon.ico')

@app.route('/icon.png')
def iconpng():
    ''' adds icon image
    by: Julie'''
    return send_from_directory(os.path.join(app.root_path, 'static'),'icon.png')


# <!--  Kattia's Code -->
# this is for enrolling student #working now!

@app.route('/enrol', methods=['POST','GET'])
def enrol():
    '''open enrol_student page'''

    DB_object = Database()
    estudentID=request.args.get('studentID')

    #if user has selected a course for the student to be enrolled in, insert the new record into the enrollment table
    programChosen = False
    list_of_available_courses = None
    if request.args.get('program_selected'):
        program_dict = request.args.get('program_selected')
        json_acceptable_string = program_dict.replace("'", "\"")
        d = json.loads(json_acceptable_string)
        estudentID = d["studentID"]
        programSelected = d["program"]
        sql_for_available_courses = "SELECT * FROM courseinfo WHERE courseinfo.courseID Not in (SELECT enrolment.courseID FROM enrolment WHERE enrolment.studentID= %s) AND courseinfo.program = %s"
        list_of_available_courses = DB_object.sql_query_fetchall(sql_for_available_courses, (estudentID, programSelected,))
        programChosen = True



    if request.method == 'POST':
        courseID = request.form["courseID"]
        studentID = request.form["studentID"]

        sql= """SELECT * FROM student Where studentID = %s"""
        student=DB_object.sql_query_fetchall(sql, (studentID,))[0]


        sql_student_historic= "SELECT courseinfo.courseName, courseinfo.courseID, courseinfo.program, enrolment.startDate,enrolment.lastWithdrawDate, enrolment.actualWithdrawDate,enrolment.studentID, enrolment.actualEndDate FROM courseinfo INNER JOIN enrolment on courseinfo.courseID= enrolment.courseID WHERE enrolment.studentID= %s"
        list_of_student_historic = DB_object.sql_query_fetchall(sql_student_historic, (studentID,))

        sql_for_available_courses = "SELECT * FROM courseinfo WHERE courseinfo.courseID Not in (SELECT enrolment.courseID FROM enrolment WHERE enrolment.studentID= %s)"
        list_of_available_courses = DB_object.sql_query_fetchall(sql_for_available_courses, (studentID,))

        Student_Enrolled = False
        if 'withdraw_button' in request.form:
            print("withdraw button clicked")
            sql_withdraw_date= "UPDATE enrolment SET actualWithdrawDate = %s WHERE studentID=%s AND courseID=%s"
            today_date = datetime.today().strftime("%Y-%m-%d")
            msg = DB_object.sql_update_insert(sql_withdraw_date, ( today_date, studentID, courseID,))
            list_of_student_historic = DB_object.sql_query_fetchall(sql_student_historic, (studentID,))
            list_of_available_courses = DB_object.sql_query_fetchall(sql_for_available_courses, (studentID,))
            return render_template('enrol_student.html', Student_Enrolled = Student_Enrolled, msg = msg,student=student, list_of_courses = list_of_available_courses, list_of_student_historic=list_of_student_historic,estudentID=studentID)

            # for actual End Date button
        if 'actualEndDate_button' in request.form:
            print("actualEndDate clicked")
            sql_actualEndDate= "UPDATE enrolment SET actualEndDate = %s WHERE studentID=%s AND courseID=%s"
            today_date = datetime.today().strftime("%Y-%m-%d")
            msg = DB_object.sql_update_insert(sql_actualEndDate, ( today_date, studentID, courseID,))
            print(msg)

            list_of_student_historic = DB_object.sql_query_fetchall(sql_student_historic, (studentID,))
            list_of_available_courses = DB_object.sql_query_fetchall(sql_for_available_courses, (studentID,))
            return render_template('enrol_student.html', Student_Enrolled = Student_Enrolled, msg = msg,student=student, list_of_courses = list_of_available_courses, list_of_student_historic=list_of_student_historic,estudentID=studentID)


        if 'enrol_button' in request.form:
            print("enrol button clicked")
            startDate = datetime.today()
            startDateAsString = datetime.today().strftime("%Y-%m-%d")

            #FIND THE DURATION OF THE SELECTED COURSE
            duration_sql= "Select durationInDay From courseinfo Where courseID=%s"
            duration= DB_object.sql_query_fetchone(duration_sql, (courseID))
            duration = duration.get('durationInDay')

            #CALCULATE THE ENDDATE (CURRENT DAY + DURATION OF THE COURSE)
            duration = timedelta(days = duration)
            end_date = (startDate + duration).strftime("%Y-%m-%d")
            print("date")
            print(end_date)

            #CALCULATE THE LASTWITHDATE (CURRENT DAY X 70% )
            lwd = startDate+ timedelta(days= round(70*0.1,0))
        #  print(lwd.strftime("%Y-%m-%d") + " line 390")

            #ENROL THE STUDENT INTO THE COURSE AND LAST WITH DRAW DATE
            sql= "INSERT INTO enrolment (courseID, studentID, startDate, endDate , lastWithdrawDate) VALUES (%s, %s, %s, %s, %s)"
            values =  (courseID, studentID, startDateAsString, end_date,lwd)
            msg = DB_object.sql_update_insert(sql, (courseID,studentID,startDateAsString,end_date,lwd))
            print("Enrol")
            print(msg)

            #check to see if the sql query was executed successfully, if not msg will be displayed to the user
            Student_Enrolled = False

            if "Successful"in msg:
                Student_Enrolled = True
            list_of_student_historic = DB_object.sql_query_fetchall(sql_student_historic, (studentID,))
            list_of_available_courses = DB_object.sql_query_fetchall(sql_for_available_courses, (studentID,))

            return render_template('enrol_student.html', Student_Enrolled = Student_Enrolled,end_date=end_date, msg = msg,student=student, list_of_courses = list_of_available_courses, list_of_student_historic=list_of_student_historic,estudentID=studentID)



    #check if a student has been chosen, if yes, return any courses that they are enrolled in
    if estudentID != None:
        sql= """SELECT * FROM student Where studentID = %s"""
        student=DB_object.sql_query_fetchall(sql, (estudentID,))[0]
        print(student)

     #test code to return all courses to allow the user to select one to enrol the student into
        sql_for_courses= "SELECT * FROM courseinfo"
        list_of_courses = DB_object.sql_query(sql_for_courses)


        sql_for_enrolled_courses= "SELECT * FROM enrolment Where studentID = %s"
        list_of_enrolled_courses = DB_object.sql_query_fetchall(sql_for_enrolled_courses, (estudentID,))


        sql_student_historic= "SELECT courseinfo.courseName, courseinfo.courseID, courseinfo.program, enrolment.startDate,enrolment.lastWithdrawDate, enrolment.actualWithdrawDate,enrolment.studentID, enrolment.actualEndDate FROM courseinfo INNER JOIN enrolment on courseinfo.courseID= enrolment.courseID WHERE enrolment.studentID= %s"
        list_of_student_historic = DB_object.sql_query_fetchall(sql_student_historic, (estudentID,))



        return render_template('enrol_student.html', student=student, list_of_courses = list_of_available_courses, list_of_enrolled_courses=list_of_enrolled_courses, list_of_student_historic=list_of_student_historic,estudentID=estudentID, programChosen = programChosen)
    else:
         return redirect(url_for('student_search'))



    return render_template('enrol_student.html', student=student)


# <!--  Kattia's Code -->


@app.route('/no_session', methods=['POST','GET'])
def no_session():
    ''' displays a list of Holidays and dates from and to By campus
    by Julie'''
    msg=""
    rows=[]
    DB_object = Database()

    #request.args.get('studentID'):
    #sql="SELECT * from nosession INNER JOIN campus ON nosession.campusID = campus.campusID;"
    sql="SELECT campus.*, noSessionID, DATE_FORMAT(startDate, '%d-%m-%Y') startDate, DATE_FORMAT(endDate, '%d-%m-%Y') endDate\
     from nosession INNER JOIN campus ON nosession.campusID = campus.campusID;"


    list_nosessions = DB_object.sql_query(sql)
    #print(list_no sessions)
    return render_template("no_session_list.html",list_nosessions=list_nosessions)

@app.route('/update_no_session', methods=['POST','GET'])
def update_no_session():
    '''update no_session record ie holidays and exclusions dates closed
    this doesnt use WTF forms if I have time I will migrate over otherwise leave it as it works
    by Julie'''
    row=[]
    DB_object = Database()
    disabled_dates = get_disabled_dates(0) #only get statatory dates

    campus_list = get_campus_list()

    if request.method == 'POST': #save the updates
        ecampusID = request.form['campus_no_session']
        eendDate = request.form['EndDatepicker']
        estartDate = request.form['StartDatepicker']
        enoSessionID = request.form['noSessionID']
        estartDate =  datetime.strptime(estartDate, '%d-%m-%Y').strftime("%Y-%m-%d")
        eendDate =  datetime.strptime(eendDate, '%d-%m-%Y').strftime("%Y-%m-%d")
        sql= "UPDATE nosession SET campusID = %s, startDate = %s, endDate = %s WHERE noSessionID = %s"
        msg = DB_object.sql_update_insert(sql, (ecampusID, estartDate, eendDate, enoSessionID))
        flash(msg)
        #sql = "SELECT * FROM nosession WHERE noSessionID =%s"
        #row = DB_object.sql_query_fetchone(sql, (enoSessionID,))
        #return render_template("no_session.html",row = row)
        response = make_response(redirect('/no_session'))
        return response
    elif request.method == "GET":
        enoSessionID = request.args.get('noSessionID')
   #     print("add_no_session", enoSessionID)
        row=[]
        sql =  "SELECT noSessionID, campusID, DATE_FORMAT(startDate, '%%d-%%m-%%Y') startDate, DATE_FORMAT(endDate, '%%d-%%m-%%Y') endDate  FROM noSession WHERE noSessionID = %s"
        #sql =  "SELECT *  FROM noSession WHERE noSessionID = %s"
        print(sql)
        row = DB_object.sql_query_fetchone(sql, (enoSessionID, ))
        print("row", row)
        return render_template("no_session_edit.html",row = row, campus_list=campus_list,disabled_dates=disabled_dates)

@app.route('/add_no_session', methods=['POST','GET'])
def add_no_session():
    '''add record to no_session ie holidays and excludsions
    open no_session page ie holidays and exclusions
    DO NOT COPY this CODE as uses WTF_Forms and SQLAchemy so different approach
    by Julie'''
    form = NoSessionsForm()
    if form.validate_on_submit():
        #print("in validate")
        #return form.startDate.data.strftime('%Y-%m-%d')
        no_session = NoSession(startDate=form.startDate.data, endDate=form.endDate.data,campusID=form.campusID.data)
        db.session.add(no_session)
        db.session.commit()
        flash('Saved Holiday/Closed Period!')
        return redirect(url_for('no_session'))
    return render_template('no_session.html', form=form)

    '''if request.method == 'GET': #load page
            enoSessionID = request.args.get('noSessionID')
            print("add_no_session", enoSessionID)
            row=[]
            sql =  "SELECT * FROM noSession WHERE noSessionID = %s"
            row = DB_object.sql_update_insert(sql, (enoSessionID, ))
            print("row". row)
            return render_template("no_session.html",row = row)
    elif request.method == 'POST': #insert new
            return render_template("no_session.html",row = row)
'''
@app.route('/delete_no_session', methods=['POST','GET'])
def delete_no_session():
    ''' deletes record from no_session holiday closed table
    from list of no_sessions
    by Julie'''
    DB_object = Database()

    enoSessionID = request.args.get('noSessionID')

    sql="DELETE FROM  nosession WHERE noSessionID = %s;"

    msg = DB_object.sql_query_delete(sql, (enoSessionID, ))
    flash(msg)
    response = make_response(redirect('/no_session'))
    return response


@app.route('/staff_list', methods=['POST','GET'])
def staff_list():
    ''' displays a list of staff with logins
    by Julie'''
    msg=""
    rows=[]
    DB_object = Database()

    sql="SELECT * from user;"

    list_staff = DB_object.sql_query(sql)
    #print(list_no sessions)
    return render_template("staff_list.html",list_staff=list_staff)


@app.route('/edit_staff', methods=['POST','GET'])
def edit_staff():
    ''' will edit a staff member logins
    by Julie'''
    list_staff = []

    return render_template("staff_list.html",list_staff=list_staff)


@app.route('/delete_staff', methods=['POST','GET'])
def delete_staff():
    ''' will edit a staff member logins
    by Julie'''
    list_staff = []
    DB_object = Database()
    euserID = request.args.get('userID')
    sql = "DELETE FROM user WHERE id = %s"
    DB_object.sql_query_delete(sql, (euserID,))

    redirect_to_index = redirect(url_for('staff_list'))
    response = make_response( redirect_to_index)
    return response

@app.route('/report_dashboard', methods=['POST','GET'])
def report_dashboard():
    '''open report dashboard page'''
    DB_object = Database()
    today = datetime.today().strftime('%Y-%m-%d')   #get today's date
    date = (datetime.today()-timedelta(7)).strftime('%Y-%m-%d') #used this date to count the last lastWithdrawDate
#    yesterday = (datetime.today()-timedelta(1)).strftime('%Y-%m-%d')
#    if yesterday is sunday:
#        last_school_day = (datetime.today()-timedelta(2)).strftime('%Y-%m-%d')
#    if yesterday is public_holiday:
#        last_school_day = (datetime.today()-timedelta(day_ph)).strftime('%Y-%m-%d')

    sql = '''SELECT COUNT(lastWithdrawDate)
             FROM enrolment
             WHERE lastWithdrawDate= %s and actualWithdrawDate is null;'''
    lsw_summary = DB_object.sql_query_fetchone(sql,(today))
    number_lsw_student = lsw_summary ['COUNT(lastWithdrawDate)']

    sql = '''SELECT COUNT(endDate)
             FROM enrolment
             WHERE endDate= %s and completed = %s;'''
    gf_student_summary = DB_object.sql_query_fetchone(sql,(today,'False'))
    number_gf_student = gf_student_summary ['COUNT(endDate)']

    sql = '''SELECT student.studentID, student.firstName, student.lastName, courseinfo.courseName, attenbooking.action, attenbooking.actionTime, student.lastMoodleEngagement
             From student
             INNER JOIN attenbooking ON student.studentID = attenbooking.studentID
             INNER JOIN enrolment ON attenbooking.studentID = enrolment.studentID
             INNER JOIN courseinfo ON enrolment.courseID = courseinfo.courseID
             WHERE actionTime = %s and (lastMoodleEngagement <= %s or lastMoodleEngagement is null);'''
    last_engagement_summary = DB_object.sql_query_fetchall(sql,(date,date))

    sql = '''SELECT COUNT(student.studentID)
           FROM student
           INNER JOIN attenbooking ON student.studentID = attenbooking.studentID
           INNER JOIN enrolment ON attenbooking.studentID = enrolment.studentID
           INNER JOIN courseinfo ON enrolment.courseID = courseinfo.courseID
           WHERE actionTime = %s and (lastMoodleEngagement <= %s or lastMoodleEngagement is null);'''
    inactive_student = DB_object.sql_query_fetchone(sql,(date,date))
    number_of_inactive_student = inactive_student['COUNT(student.studentID)']

    return render_template('report_dashboard.html',number_of_inactive_student = number_of_inactive_student, \
    number_lsw_student=number_lsw_student,number_gf_student = number_gf_student,last_engagement_summary=last_engagement_summary)

@app.route('/engagement_record', methods=['POST','GET'])
def engagement_record():
    DB_object = Database()
    today = datetime.today().strftime('%Y-%m-%d')   #get today's date
    date = (datetime.today()-timedelta(7)).strftime('%Y-%m-%d') #used this date to count the last lastWithdrawDate

    sql = '''SELECT student.studentID, student.firstName, student.lastName, courseinfo.courseName, attenbooking.action, attenbooking.actionTime, student.lastMoodleEngagement
                 From student
                 INNER JOIN attenbooking ON student.studentID = attenbooking.studentID
                 INNER JOIN enrolment ON attenbooking.studentID = enrolment.studentID
                 INNER JOIN courseinfo ON enrolment.courseID = courseinfo.courseID
                 WHERE actionTime = %s and (lastMoodleEngagement <= %s or lastMoodleEngagement is null);'''
    last_engagement_summary = DB_object.sql_query_fetchall(sql,(date,date))

    print(last_engagement_summary)

    return render_template('engagement_record.html', last_engagement_summary=last_engagement_summary)

@app.route('/student_profile', methods=['POST','GET'])
def student_profile():
    '''Will render a table of students who haven't finished their course before the course Endate'''
    DB_object = Database()
    today = datetime.today().strftime('%Y-%m-%d')
    sql = '''SELECT student.studentID, student.firstName, student.lastName, courseinfo.courseName, courseinfo.durationInDay, enrolment.startDate,enrolment.endDate,enrolment.actualEndDate
             FROM student
             INNER JOIN enrolment ON student.studentID = enrolment.studentID
             INNER JOIN courseinfo ON enrolment.courseID = courseinfo.courseID
             WHERE endDate <= %s and actualWithdrawDate is null and completed = %s;'''
    student_not_finish = DB_object.sql_query_fetchall(sql,(today,False))

    return render_template('student_profile.html',student_not_finish=student_not_finish)

@app.route('/update_end_date', methods=['POST'])
def update_end_date():
    '''Will receive the date and update the courseEndaDate'''
    DB_object = Database()
    if request.method == 'POST':
        sid = request.form["studentID"]#if [] not working try () request.args.get('userID')request.args.get
        print(sid)
        cname = request.form["courseName"]
        data = request.form.get['data']
        print(data['date'])
        print(type(date))
        sql = '''UPDATE enrolment SET endDate= %s WHERE studentID = %s;'''
        update = DB_object.sql_update_insert(sql,(date,sid))
        redirect_to_student_profile = redirect(url_for('student_profile'))
        response = make_response(redirect_to_student_profile)
        return response


@app.route('/facility_usage_record', methods=['POST','GET'])
def facility_usage_record():
    '''open report dashboard page'''


    return render_template('facility_usage_record.html')


# put in for testing
app.run(debug=True)
