# CCF-student-admin-system-
For the project of SIGNAL's shift program 

liveversion running on testing server http://103.197.60.75:5000

BEFORE you CAN run the app you need to have 
lots of add-ins to Flask and python that allow secure password hashing

MySQL server needs to be running        run WAMP (windows)  run MAMP (MAC)
then run the below in the commandline
----------------------------------   
pip install -r requirements.txt


the main program to run is 
   computingforfree.py

to get a development debugging environment type at the command line 
(in MAC)
   EXPORT FLASK_ENV=development
   (in Windows)
   SET FLASK_ENV=development
   
to run in windows at command line type each command
   set FLASK_ENV=development
   flask run

to run on MAC at command line type each command
   EXPORT FLASK_APP=computingforfree.py
   flask run



