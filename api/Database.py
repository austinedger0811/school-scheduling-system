
from sqlalchemy import *


class Database:

    def __init__(self):
        self.DATABASEURI = 'postgresql://ame2194:5366@34.74.246.148/proj1part2'
        self.engine = create_engine(self.DATABASEURI)

    def get_students(self):
        '''
        This is an example query that gets all students.
        '''

        # Connect to the database
        conn = self.connect()

        # Run the query
        cursor = conn.execute("SELECT * From Student")

        # List to be returned
        students = []

        # retchall rows
        rows = cursor.fetchall()

        # Append each row to the list
        for row in rows:
            students.append(list(row))

        # Close database
        self.close(conn)

        return students

    def connect(self):
        '''
        Used to create a connection to the database.
        This method should be called BEFORE every database operation.
        '''
        try:
            return self.engine.connect()
        except Exception as e:
            print("Connection to database failed. " + e)

    def close(self, conn):
        '''
        Used to close connection to the database.
        This method should be called AFTER every database operation.
        '''
        try:
            conn.close()
        except Exception as e:
            pass
