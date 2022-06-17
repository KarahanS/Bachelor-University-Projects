from tkinter import N
import mysql.connector
from mysql.connector import Error
import json

class Connection():

    def __init__(self):
        db_config = None
        with open('db_config.json', 'r') as f:
            db_config = json.load(f)

        self.connection = None
        try:
            self.connection = mysql.connector.connect(**db_config)
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)

    def run_query(self, query, multi=False):
        try:
            cursor = self.connection.cursor()
            # The "multi" parameter is added specifically for R22. Query
            # in R22 was raising "Use multi=True when executing multiple
            # statements" error. We couldn't figure out why this was the
            # case since the query looked like it was a single statement.
            if multi:
                for result in cursor.execute(query, multi=True):
                    if result.with_rows:
                        response = result.fetchall()
                    else:
                        pass
                self.connection.commit()
                return response
            else:
                cursor.execute(query)
                response = cursor.fetchall()
                self.connection.commit()
                cursor.close()
                return response
        except mysql.connector.Error as error:
            print("Query failed: {}".format(error))

connection = Connection()