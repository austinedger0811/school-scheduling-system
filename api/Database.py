
from sqlalchemy import *
from sqlalchemy import exc
import pandas as pd


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

    def get_table_where(self, select: str, table: str, where: str) -> list[dict]:
        '''
        Queries the database for a specific table and returns the results as a list of dictionaries.
        '''
        args = (select, table, where)
        query = "SELECT %s FROM %s WHERE %s" % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def insert_values(self, columns, vals, table: str):
        '''
        insert values to columns in a given table.
        '''

        q = "INSERT INTO "+table+" ("
        for i in columns[:len(columns)-1]:
            q += str(i) + ", "
        q += str(columns[-1])+") "

        v = "values ("
        for i in vals[:len(vals)-1]:
            if type(i) == str:
                v += "\'"+i+"\', "
            else:
                v += str(i)+", "
        if type(vals[-1]) == str:
            v += "\'"+str(vals[-1])+"\')"
        else:
            v += str(vals[-1])+")"

        insert_query = q+v
        conn = self.connect()
        cursor = conn.execute(insert_query)
        self.close(conn)

    # need to be tested
    def enroll_into_class(self, student_id: str, course_id: str, semester: str, year: int) -> list[dict]:
        '''
        enroll a student into a course by inserting into takes table in the database.
        '''
        args = (student_id, course_id, semester, year)
        query = "INSERT INTO Takes (sid, cid, semester, year) VALUES (%s, \'%s\', \'%s\', %s)" % args
        conn = self.connect()
        cursor = conn.execute(query)
        self.close(conn)

    # need to be tested
    def remove_course(self, student_id: str, course_id: str, semester: str, year: int) -> list[dict]:
        '''
        remove a course from student's schedule
        '''
        args = (student_id, course_id, semester, year)
        query = "DELETE FROM Takes WHERE (sid = %s and cid = \'%s\' and  semester = \'%s\' and year = %s)" % args
        conn = self.connect()
        cursor = conn.execute(query)
        self.close(conn)

    # need to be tested
    def add_new_student_with_EC(self, student_id: str, fname: str, lname: str, grade: int, email: str, ssn: int, ec_fname: str, ec_lname: str, ec_phone_number: int, ec_email: str, ec_relation: str) -> list[dict]:
        '''
        add a student to the school's database with is emergency contact info.
        '''
        students_args = (student_id, fname, lname, grade, email)
        query = "INSERT INTO Student (student_id, first_name, last_name, grade, email) VALUES (%s, \'%s\',\'%s\', \'%s\', \'%s\')" % students_args
        conn = self.connect()
        cursor = conn.execute(query)

        ec_args = (ssn, ec_fname, ec_lname, ec_phone_number, ec_email)
        ec_query = "INSERT INTO emergency_contact (ssn, first_name, last_name, phone_number, email) VALUES (%s, \'%s\',\'%s\' , %s, \'%s\')" % ec_args
        cursor = conn.execute(ec_query)

        S_has_EC = (student_id, ssn, ec_relation)
        has_query = "INSERT INTO Has (sid, ecid, relation ) VALUES (%s, %s, \'%s\')" % S_has_EC
        cursor = conn.execute(has_query)
        self.close(conn)

    def add_new_student(self, student_id: str, fname: str, lname: str, grade: int, email: str) -> list[dict]:
        '''
        add a student to the school's database.
        '''
        try:
            students_args = (student_id, fname, lname, grade, email)
            query = "INSERT INTO Student (student_id, first_name, last_name, grade, email) VALUES (%s, \'%s\',\'%s\', \'%s\', \'%s\')" % students_args
            conn = self.connect()
            cursor = conn.execute(query)
            self.close(conn)
            print('Student added successfully.')  # return True?
        except exc.IntegrityError:
            print('Error: Duplicated student id or email.')  # return False?
            self.close(conn)

    def update_student_course_grade(self, student_id: str, course_id: str, semester: str, year: int, grade: str) -> list[dict]:
        '''
        updates a student grade in a giving course.
        '''
        args = (grade, student_id, course_id, semester, year)
        query = " UPDATE Takes SET grade = \'%s\' WHERE sid = %s and cid = \'%s\' and semester = \'%s\' and year = %s" % args
        conn = self.connect()
        cursor = conn.execute(query)
        self.close(conn)

    def update_student_gpa(self, student_id: str, gpa: float) -> list[dict]:
        '''
        updates a student grade in a giving course.
        '''
        args = (gpa, student_id)
        query = " UPDATE Student SET gpa = %s WHERE student_id = %s" % args
        conn = self.connect()
        cursor = conn.execute(query)
        self.close(conn)

    def has_taken_course(self, student_id: str, course_id: str):
        '''
        retrive the number of credits the studnet completed successfully.
        '''
        args = (student_id, course_id, course_id)
        query = """SELECT  T.cid
           FROM Takes T, Student S
           WHERE S.student_id = T.sid and S.student_id = %s and T.cid = \'%s\' and T.grade not in (SELECT Distinct T1.grade
            																	FROM Takes T1
																	            WHERE T1.grade='F' and T1.cid = \'%s\')
        """ % args

        conn = self.connect()
        cursor = conn.execute(query)
        credits = [row._asdict() for row in cursor]
        self.close(conn)

        if credits == []:
            return False
        else:
            return True

    # need to be tested after adding new semester, tested before update works
    def update_num_credits(self, student_id: str):
        '''
        retrive the number of credits the studnet completed successfully.
        '''

        query = """SELECT count(*)
           FROM Takes T, Student S
           WHERE S.student_id = T.sid and S.student_id = %s and T.grade not in (SELECT Distinct T1.grade
            																	FROM Takes T1
																	            WHERE T1.grade='F' or T1.grade is NULL)
        """ % student_id

        conn = self.connect()
        cursor = conn.execute(query)
        credits = [row._asdict()['count'] for row in cursor][0]
        updatequery = " UPDATE Student SET num_completed_credits = %s WHERE student_id = %s" % (
            credits, student_id)
        cursor = conn.execute(updatequery)

        self.close(conn)

    # need to be tested after adding new semester, tested before update works
    def get_number_of_courses(self, student_id: str, semester: str, year):
        '''
        retrive the number of credits the studnet completed successfully.
        '''
        args = (student_id, semester, year)
        query = """SELECT count(*)
        FROM Takes T, Student S
        WHERE S.student_id = T.sid and  S.student_id = %s and semester = \'%s\' and year = %s
        """ % args

        conn = self.connect()
        cursor = conn.execute(query)
        num_courses = [row._asdict()['count'] for row in cursor][0]
        self.close(conn)
        return num_courses

    # need to be tested after adding new semester , tested before update works
    def update_student_grade(self, student_id: str):
        '''
        Update the student grade by increasing it by one
        '''
        query1 = """SELECT S.grade
           FROM  Student S
           WHERE S.student_id = %s """ % student_id
        conn = self.connect()
        cursor = conn.execute(query1)
        grade = [row._asdict()['grade'] for row in cursor][0]
        updatequery = " UPDATE Student SET grade = \'%s\' WHERE sid = %s" % (
            grade+1, student_id)
        cursor = conn.execute(updatequery)

        self.close(conn)

    def get_student_ids_without_full_schedule(self, semester: str, year: int) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        and studnets newly enrolled and have not been enrolled into classes
        '''
        args = (semester, year, semester, year)
        query = """
            SELECT T.sid
            FROM Takes T
            WHERE T.semester = \'%s\' and T.year = %s
            GROUP BY T.sid
            HAVING COUNT(T.sid) < 5
            UNION
            SELECT S.student_id
            FROM Student S
            WHERE S.student_id not in (SELECT T.sid
                                       FROM  Takes T
                                       WHERE T.semester = \'%s\' and T.year = %s)
        """ % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict()['sid'] for row in cursor]
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

    # add teacher name, office number
    def get_student_schdule(self, student_id: int, semester: str, year: int) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        '''

        args = (semester, year, student_id)
        query = """
        SELECT  DISTINCT S.student_id, S.first_name, S.last_name, C.name AS Course_Name, C.course_id, A.classroom, A.start_time, A.end_time, T1.first_name AS Teacher_First_Name, T1.last_name AS Teacher_Last_Name, T1.office_number
        FROM Student S, Takes T, Course C, Assigned_to A, Teacher T1, Teach T2
        WHERE S.student_id = T. sid and T.cid = C.course_id and A.cid = C.course_id and T.semester = \'%s\' and T.year = %s and S.student_id = %s and T2.tid= T1.teacher_id and C.course_id = T2.cid and T2.semester =T.semester and T2.year =T.year
        ORDER BY A.start_time""" % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        for res in result:
            start = res['start_time'].strftime("%H:%M")
            end = res['end_time'].strftime("%H:%M")
            res['start_time'] = start
            res['end_time'] = end
        self.close(conn)
        return result

    def get_student_emergency_contact(self, student_id: str) -> list[str]:
        '''
        Returns all studnet ids for students that are not in 5 classes.
        '''
        query = """
        SELECT  S.student_id, S.first_name As student_first_name , S.last_name As student_last_name, H.relation, E.first_name As contact_first_name, E.last_name As contact_last_name, E.phone_number
        FROM Student S, has H, Emergency_Contact E
        WHERE S.student_id = %s and E.ssn = H.ecid and H.sid = %s
        """ % (student_id, student_id)
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
                        WHERE S1.student_id = T.sid and semester = \'%s\' and year = %s)
        """ % args
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
            SELECT T.cid
            FROM takes T
            Group by  T.cid
            Having count(*) < (SELECT Distinct R.capacity
            FROM  Classroom R, assigned_to A
            Where T.cid = A.cid and  R.classroom_id=A.classroom)
        """
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict()['cid'] for row in cursor]
        self.close(conn)
        return result

    def get_completed_courses(self, student_id: str) -> list[str]:
        '''
        Returns a list of all courses from every academic semester that the student has completed(has letter grade)
        '''
        query = """
        Select T.cid, T.grade
        From Takes T
        Where  T.sid= %s  and T.grade is not NULL
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
        WHERE P.cid = \'%s\' """ % course_id

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict()['prerequisite'] for row in cursor]
        self.close(conn)
        return result

    def get_course_timeslot(self, course_id: str, semester: str, year: int) -> list[str]:
        '''
        Returns a the start_time of a given course at a specifed semester
        '''
        args = (semester, year, course_id)

        query = """
        SELECT Distinct A.start_time
        FROM   Course C, Assigned_to A
        WHERE A.cid = C.course_id and A.semester = \'%s\' and A.year = %s and C.course_id = \'%s\'
        """ % args

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def check_time_conflict(self, student_id: str, course_id: str, semester: str, year: int) -> list[str]:
        '''
        Returns an empty list if there is no conflict, otherwise, it returns a table of course names that have a time conflict with.
        '''

        args = (semester, year, student_id, semester, year, course_id)
        query = """
        SELECT  C.name
        FROM Student S, Takes T, Course C, Assigned_to A
        WHERE S.student_id = T. sid and T.cid = C.course_id
        and A.cid = C.course_id and T.semester = \'%s\'
        and T.year = %s and S.student_id = %s and A.start_time in (
        SELECT Distinct A1.start_time
        FROM   Course C1, Assigned_to A1
        WHERE A1.cid = C1.course_id and A1.semester = \'%s\' and A1.year = %s and C1.course_id = \'%s\')

        """ % args

        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def get_list_possible_courses_to_enroll(self, student_id: str) -> list[str]:
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

    def get_schedule(self, sid: int, semester: str, year: str) -> list[dict]:
        args = (sid)  # add semester and year
        # Add where T.semester=%s and T.year=%s
        query = """
            SELECT *
            FROM Takes T
            WHERE T.sid=%s
        """ % args
        conn = self.connect()
        cursor = conn.execute(query)
        result = [row._asdict() for row in cursor]
        self.close(conn)
        return result

    def clear_schedule(self, semester: str, year: str):
        '''
        reomve all the data from takes.
        '''
        args = (semester, year)
        query = """DELETE FROM Takes WHERE semester=\'%s\' AND year=%s;""" % args
        query 1= """DELETE FROM academic_semester WHERE semester=\'%s\' AND year=%s;""" % args

        conn = self.connect()
        cursor = conn.execute(query)
        cursor = conn.execute(query2)

        self.close(conn)

    def add_schedule_from_file(self):
        '''
        adds data from a csv file.
        '''

        # clear takes
        df = pd.read_csv('Takes.csv')
        df = df.drop('letter_grade', axis=1)
        cols = ", ".join([str(i) for i in df.columns.tolist()])

        conn = self.connect()

        for i, row in df.iterrows():
            query = "INSERT INTO Takes (" + cols + \
                ") VALUES (%s, \'%s\', \'%s\', %s)" % tuple(row)
            cursor = conn.execute(query)

        self.close(conn)

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
