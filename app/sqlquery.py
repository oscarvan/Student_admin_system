import os
from flask import Flask, render_template, redirect, request, url_for
#!/usr/bin/python3
import pymysql
import pymysql.cursors
from app import app

class Database:
    """" Sets up database connection class
    Argument: self
    by Julie """


    def connect(self,returnDict=True):
        if returnDict:
            cType = pymysql.cursors.DictCursor
        else:
            cType = pymysql.cursors.Cursor
        #print ("returnDict", returnDict)


        return pymysql.connect(host='localhost', user='cff_user',
        password=app.config['DB_password'] , db=app.config['CFF_DB'], 
        cursorclass=cType) 

    def sql_query(self, query, returnDict = True):
        """ function for running SQL queries
        Argument query:  sql query string,  NO WHERE clause  - should not hard code where clause
        Argument self: do not have to pass as it is only with class definition
        Returns:  dictionary/tuple with data that you can loop through
        by Julie"""
        # Open database connection
        #connect to DB and prepare cursor
        connection = Database.connect(self,returnDict )  #db.cursor(pymysql.cursors.DictCursor) #gives named columns like rowfactory sqlite
        cursor = connection.cursor()
        # row=[] # set empty   for testing
        try:
            cursor.execute(query)
            row = cursor.fetchall()
            #print("tryfetchall")
            return row

        except Exception as e:
            #db.rollback()
            msg = "Error in SQL select operation " + str(e)
            #print("rollback " + msg)
            return ()
        finally:
            connection.close()
            # disconnect from server
            #db.close()
            #return row

    def sql_update_insert(self, query, var):
        '''function for running SQL queries
        Argument query:  sql query string,    HAS WHERE clause  - should not hard code where clause
        Arument var: list of variables passing to update or insert
        Dont pass Argument self: do not have to pass as it is only with class definition
        Returns:  message to display success or error
        by Julie'''
        connection = Database.connect(self)
        cursor = connection.cursor()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, var)
                #print("before commit")
                connection.commit()
                msg = "Successful Update/Insert " # + query + str(var)
                #print(msg)
                return msg
        except Exception as e:
            #print("error before rollback")
            connection.rollback()
            msg = "Error in insert/update operation " + str(e)
           # print("error", msg)
            return msg
        finally:
            connection.close()

    # sql_query_fetchall where additional variables are passed
    def sql_query_fetchall(self, query, var, returnDict = True):
        ''' argument1: sql query
        argument2: in () comma delimited
                     # for WHERE clause, eg (esearch_box,efirst_name)
         do not pass self as can only do this from within class
         by Julie'''
        connection = Database.connect(self, returnDict )  #db.cursor(pymysql.cursors.DictCursor) #gives named columns like rowfactory sqlite
        cursor = connection.cursor()
        #print("4 try")
        try:
            #print("before cursor")
            cursor.execute(query, var)
            #print("success fetchall ", query + str(var))
            rows =cursor.fetchall()
            return rows
        except Exception as e:
            msg = e
            print(msg)
            return ()
        finally:
            connection.close()

    def sql_query_fetchone(self, query, var):
        '''fttches one record
        Argument: self u don't have to pass, as db object
        Argument2: query   is sql query string to execute
        Argument3:  var = variables  to pass to WHERE clause
        by julie'''
        connection = Database.connect(self)
        cursor = connection.cursor()
        try:
            cursor.execute(query, var)
            #print("success fetchone")
            return cursor.fetchone()
        except Exception as e:
            msg = e
            #print(msg)
            return ()
        finally:
            connection.close()


    # you probably shouldn't be using this method
    def sql_query_delete(self, query,var):
        '''deletes record(s)
        Argument: self u don't have to pass, as db object
        Argument2: query   is sql query string to execute
        Argument3:  var = variables  to pass to WHERE clause
        by julie'''
        connection  = Database.connect(self)
        cursor = connection.cursor()

        try:
            cursor.execute(query,var)
            connection.commit()
            msg = "Successfully Deleted " #+ query + str(var)
            return msg
        except Exception as e:
            print(query, ' ',var)
            connection.rollback()
            msg = "Error in Delete operation " + str(e)
            return msg
        finally:
            connection.close()


    def sql_update_novar(self, query):
        '''function for running SQL queries
        Argument query:  sql query string,  has WHERE clause  - should not hard code where clause
        Dont pass Argument self: do not have to pass as it is only with class definition
        Returns:  message to display success'''
        # Open database connection
        #connect to DB and prepare cursor
        connection = Database.connect(self)
        cursor = connection.cursor()
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                connection.commit()
                msg = "Successful Update/Insert " #+ query + str(var)
                return msg
        except Exception as e:
            connection.rollback()
            msg = "Error in insert/update operation " + str(e)
            return msg
        finally:
            connection.close()
