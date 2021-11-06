
from sqlalchemy import *


class Database:

    def __init__(self):
        self.DATABASEURI = 'postgresql://ame2194:5366@34.74.246.148/proj1part2'
        self.engine = create_engine(self.DATABASEURI)

    def get_table(self, select: str, table: str) -> list[dict]:
        '''
        Queries the database for a specific table and returns the results as a list of dictionaries.
        '''
        args = (select, table)
        query = "SELECT %s FROM %s" % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_student_ids_without_full_schedule(self) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        '''
        query = """
            SELECT S.student_id
            FROM Student S, Takes T
            WHERE S.student_id = T.sid
            GROUP BY S.student_id
            HAVING COUNT(S.student_id) < 5
        """
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict()['student_id'] for row in cursor]
        self.close(conn)
        return result

    def get_course_ids_with_capacity(self) -> list[str]:
        '''
        Returns all course ids for Fall 2021 (current academic semester) where the capacity is greater than
        the number of students enrolled.
        '''
        # TODO FIX THIS QUERY
        query = """
            SELECT
            FROM 
            WHERE 
            GROUP 
            HAVING 
        """
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict()['course_id'] for row in cursor]
        self.close(conn)
        return result

    def clear_schedule(self):
        return

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
