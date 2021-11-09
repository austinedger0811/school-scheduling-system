
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

    def enroll_into_class(self, student_id: str, course_id: str, semester: str, year: int) -> list[dict]: # need to be tested
        '''
        enroll a student into a course by inserting into takes table in the database.
        '''
        query = "SELECT %s FROM %s" % args
        conn = self.connect()
        cursor = conn.execute(query)
        self.close(conn)

    def update_student_course_grade(self, student_id: str, course_id: str, semester: str, year: int, grade: str) -> list[dict]: # need to be tested
        '''
        updates a student grade in a giving course.
        '''
        args = grade, student_id, course_id, semester, year
        query = " UPDATE Takes  SET grade = %s WHERE sid = %s and cid = %s and semester = %s and year = %s;" % args
        conn = self.connect()
        cursor = conn.execute(query)
        #result = [row._asdict() for row in cursor]
        self.close(conn)
        #return result

    def update_num_credits(self, student_id:str): # need to be tested
        '''
        retrive the number of credits the studnet completed successfully.
        '''

        query = """SELECT count(*)
           FROM Takes T, Student S
           WHERE S.student_id = T.sid and S.student_id = %s and T.grade not in (SELECT Distinct T1.grade
            																	FROM Takes T1
																	            WHERE T1.grade='F')
        """ % student_id

        conn = self.connect()
        cursor = conn.execute(query)
        credits = [row._asdict()['count'] for row in cursor][0]

        updatequery = " UPDATE Student SET num_completed_credits = %s WHERE sid = %s;" % (credits, student_id)
        cursor = conn.execute(updatequery)

        self.close(conn)



    def update_student_grade(self, student_id:str): # need to be tested
        '''
        Update the student grade by increasing it by one
        '''
        query1 = """SELECT S.grade
           FROM  Student S
           WHERE S.student_id = %s """ % student_id
        conn = self.connect()
        cursor = conn.execute(query)
        grade = [row._asdict()['grade'] for row in cursor][0]

        updatequery = " UPDATE Student SET grade = %s WHERE sid = %s;" % (grade+1, student_id)
        cursor = conn.execute(updatequery)

        self.close(conn)

    def get_student_ids_without_full_schedule(self, semester: str,year: int) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        and studnets newly enrolled and have not been enrolled into classes
        '''
        args = (semester, year)
        query = """
            SELECT S.student_id
            FROM Student S, Takes T
            WHERE S.student_id = T.sid and T.semester = %s and T.year = %s
            GROUP BY S.student_id
            HAVING COUNT(S.student_id) < 5
            UNION
            SELECT S.student_id
            FROM Student S
            WHERE S.student_id not in (SELECT S.student_id
                                       FROM Student S, Takes T
                                       WHERE S.student_id = T.sid)
        """ % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict()['student_id'] for row in cursor]
        self.close(conn)
        return result

    def get_student_requirements_status(self, student_id: str) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        '''
        query = """
            SELECT  C.requirement_type, count(*)
            FROM Student S, Takes T, Course C
            WHERE S.student_id = T. sid and T.cid = C.course_id and S.student_id = %s
            group by C.requirement_type
        """ % student_id
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_student_schdule(self, student_id: str, semester: str,year: int) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        '''
        args = (semester, year, student_id)
        query = """
        SELECT  DISTINCT S.student_id, S.first_name, S.last_name, C.name, C.course_id, A.classroom, A.day_of_week, A.start_time, A.end_time
        FROM Student S, Takes T, Course C, Assigned_to A
        WHERE S.student_id = T. sid and T.cid = C.course_id and A.cid = C.course_id and T.semester = %s and T.year = %s and S.student_id = %s
        ORDER BY A.day_of_week, A.start_time;
        """ % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_student_emergency_contact(self, student_id: str) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        '''
        query = """
        SELECT  S.student_id, S.first_name As student_first_name , S.last_name As student_last_name, H.relation, E.first_name As contact_first_name, E.last_name As contact_last_name, E.phone_number
        FROM Student S, has H, Emergency_Contact E
        WHERE S.student_id = %s and E.ssn = H.ecid;
        """ % student_id
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result


    def get_student_ids_not_enrolled_in_semester(self, semester: str, year: int) -> list[str]:
        '''
        Returns all studnet ids for students that are not enrolled in a specific semester.
        '''
        args = (semester, year)

        query = """
            SELECT S.student_id
            FROM Student S
            WHERE S.student_id not in (SELECT S1.student_id
                        FROM Student S1, Takes T
                        WHERE S1.student_id = T.sid and semester = %s and year = %s)
        """ % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_course_ids_with_capacity(self) -> list[str]:
        '''
        Returns all course ids for Fall 2021 (current academic semester) where the capacity is greater than
        the number of students enrolled.
        '''
        # TODO FIX THIS QUERY
        query = """
            SELECT T.cid
            FROM takes T
            Group by  T.cid
            Having count(*) < (SELECT Distinct R.capacity
            FROM  Classroom R, assigned_to A
            Where T.cid = A.cid and  R.cla
        """
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_completed_courses(self, student_id: str) -> list[str]:
        '''
        Returns a list of all courses from every academic semester that the student has completed(has letter grade)
        '''
        query = """
        Select T.cid, T.grade
        From Takes T
        Where  T.sid= %s  and T.grade is not NULL;
        """ % student_id

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_prerequisites(self, course_id: str) -> list[str]:
        '''
        Returns a list of course_ids that are prerequisites for the given course.
        '''

        query = """
        SELECT P.prerequisite
        FROM prerequire P
        WHERE P.cid = %s """ % course_id

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_course_timeslot(self, course_id: str, semester: str,year: int) -> list[str]:
        '''
        Returns a the start_time of a given course at a specifed semester
        '''
        args = (semester, year, course_id)

        query = """
        SELECT Distinct A.start_time
        FROM   Course C, Assigned_to A
        WHERE A.cid = C.course_id and A.semester = %s and A.year = %s and C.course_id = %s
        """ % args

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def check_time_conflict(self, student_id: str ,course_id: str, semester: str,year: int) -> list[str]:
        '''
        Returns an empty list if there is no conflict, otherwise, it returns a table of course names that have a time conflict with.
        '''

        args = (semester, year, student_id, semester, year, course_id)
        query = """
        SELECT  C.name
        FROM Student S, Takes T, Course C, Assigned_to A
        WHERE S.student_id = T. sid and T.cid = C.course_id
        and A.cid = C.course_id and T.semester = %s
        and T.year = %s and S.student_id = %s and A.start_time in (
        SELECT Distinct A1.start_time
        FROM   Course C1, Assigned_to A1
        WHERE A1.cid = C1.course_id and A1.semester = %s and A1.year = %s and C1.course_id = %s)

        """ % args

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_list_possible_courses_to_enroll(self, student_id: str ) -> list[str]:
        '''
        Returns an list of all possible courses that the student can take keeping in mind classroom capacity and prerequisites.
        '''

        args = (student_id, student_id, student_id, student_id)
        query = """
        SELECT C.course_id, C.requirement_type
        FROM Course C
        WHERE C.course_id not in ( Select T.cid
                                   From Takes T
                                   Where  T.sid = %s )
        UNION
        SELECT C.course_id, C.requirement_type
        FROM Course C
        WHERE C.course_id in ( Select T.cid
                                   From Takes T
                                   Where  T.sid = %s and T.grade = 'F')
        EXCEPT
        SELECT P.cid, C.requirement_type
        FROM prerequire P, Course C
        WHERE P.cid = C.course_id and  P.prerequisite not in (Select T.cid
                                 From Takes T
                                 Where  T.sid = %s)
        EXCEPT
        SELECT Distinct P.cid, C.requirement_type
        FROM prerequire P, Course C
        WHERE P.cid = C.course_id and P.prerequisite in (Select T.cid
                                 From Takes T
                                 Where  T.sid = %s and T.grade ='F')

        INTERSECT
        SELECT Distinct  C.course_id, C.requirement_type
        FROM Course C
        Where C.course_id in
        (SELECT Distinct T.cid
        FROM takes T
        Group by  T.cid
        Having count(*) < (SELECT Distinct R.capacity
        FROM  Classroom R, assigned_to A
        Where T.cid = A.cid and  R.classroom_id = A.classroom ))""" % args

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
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
