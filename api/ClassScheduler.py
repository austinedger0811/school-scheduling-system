
from Database import Database
import random

class ClassScheduler:

    def __init__(self):
        self.db = Database()


    def schedule_students(self, semester: str, year:int): # need to be tested
        '''
        Schedules all students who currently do not have full schedules.
        '''
        student_ids = self.db.get_student_ids_without_full_schedule(semester, year)
        for id in student_ids:
            self.schedule_student(id, semester, year)
        #return student_ids

    def add_semester(self, semester: str, year:int):
        '''
        add the add a new semester with all its offersings.
        '''
        #- add to academic_semester
        self.db.insert_values(['semester','year','start_date','end_date'],[semester, year, '1/18/2022','5/13/2022'],'Academic_Semester')
        #- add to taught_in table
        taught_in_table = self.db.get_table_where('*','taught_in','semester = \'fall\' and year = 2021')
        for i in taught_in_table:
            self.db.insert_values(['cid','semester','year'],[i['cid'], semester, year],'taught_in')

        #- add to teachs
        teach_table = self.db.get_table_where('*','teach','semester = \'fall\' and year = 2021')

        for i in teach_table:
            self.db.insert_values(['cid','tid','semester','year'],[i['cid'],i['tid'], semester, year],'teach')

        assigned_to = self.db.get_table_where('*','assigned_to','semester = \'fall\' and year = 2021')
        #- add to assigned_to
        for i in assigned_to:
            self.db.insert_values(['cid','semester','year','classroom','day_of_week','start_time','end_time'],[i['cid'], semester, year,i['classroom'],i['day_of_week'], str(i['start_time']), str(i['end_time'])],'assigned_to')
        self.update_studnet_info_after_semester_ends('Spring',2022) # how can we better represent the previous semester


    def get_list_of_fullfilled_requirements(self, student_requirements):
        '''
        Return a list of fullfilled requirement types.
        '''

        fullfilled = []

        for r in student_requirements:
            req_type = r['requirement_type'].strip('                                           ')

            if r['requirement_type'] == 'english':
                if r['count'] >= 4:
                    fullfilled.append(r['requirement_type'])

            elif r['requirement_type'] == 'health and physical education':
                if r['count'] >= 1:
                    fullfilled.append(r['requirement_type'])

            elif r['requirement_type'] == 'math':
                if r['count'] >= 4:
                    fullfilled.append(r['requirement_type'])

            elif r['requirement_type'] == 'science':
                if r['count'] >= 3:
                    fullfilled.append(r['requirement_type'])

            elif r['requirement_type'] == 'socal studies':
                if r['count'] >= 3:
                    fullfilled.append(r['requirement_type'])

            elif r['requirement_type'] == 'fine arts':
                if r['count'] >= 1:
                    fullfilled.append(r['requirement_type'])

            elif r['requirement_type'] == 'world language':
                if r['count'] >= 2:
                    fullfilled.append(r['requirement_type'])

            elif r['requirement_type'] == 'elective':
                if r['count'] >= 4:
                    fullfilled.append(r['requirement_type'])

        return fullfilled


    def schedule_student(self, student_id: str, semester: str,year: int) -> None:
        '''
        Schedules a student in 5 classes.
        '''

        all_possible_course_ids_with_reqs=['placeholder']

        while (student_id in self.db.get_student_ids_without_full_schedule(semester, year) and len(all_possible_course_ids_with_reqs)!=0): # less than 5 courses, more testing with requierments
            all_possible_course = self.db.get_list_possible_courses_to_enroll(student_id)
            all_possible_course_ids = [all_possible_course[i]['course_id'] for i in range(len(all_possible_course))]
            while (self.db.get_number_of_courses(student_id, semester, year) < 5) and len(all_possible_course_ids_with_reqs)!=0:
                requirements = self.db.get_student_requirements_status(student_id)

                all_possible_course_ids_with_reqs = []
                for c in all_possible_course:
                    if c['requirement_type'] not in self.get_list_of_fullfilled_requirements(requirements):
                       all_possible_course_ids_with_reqs.append(c['course_id'])

                selected_course = random.choice(all_possible_course_ids_with_reqs)
                timeconflict = True;
                while(timeconflict and len(all_possible_course_ids_with_reqs)!=0):
                    val = self.db.check_time_conflict(student_id, selected_course, semester, year)
                    if val == []:
                        timeconflict = False
                        all_possible_course_ids_with_reqs.remove(selected_course)

                    else:
                        timeconflict = True
                        all_possible_course_ids_with_reqs.remove(selected_course)
                        if len(all_possible_course_ids_with_reqs) !=0:
                            selected_course = random.choice(all_possible_course_ids_with_reqs)



                #insert to takes table
                if timeconflict == False:
                    self.db.enroll_into_class(student_id, selected_course , semester, year)


    def grade_value(self, grade):
        '''
        Returns the grade value for a letter grade
        '''
        if grade == 'A':
            return 4
        elif grade == 'B':
            return 3
        elif grade == 'C':
            return 2
        elif grade == 'D':
            return 1
        else:
            return 0


    def calculate_gpa(self, sid):
        '''
        calculate the GPA for a student and updates it in the database
        '''
        total_credit = 0
        total_grade_values = 0
        credits_grads = self.db.get_table_where('S.num_completed_credits, T.grade','Takes T, Student S', 'T.sid = S.student_id and T.sid = %s'%(sid))

        for r in credits_grads:
            credit = r['num_completed_credits']
            grade = r['grade']
            total_grade_values += self.grade_value(grade)
            total_credit = credit
        if total_credit!=0:
            gpa = total_grade_values / total_credit
            self.db.update_student_gpa(sid, gpa)



    def update_studnet_info_after_semester_ends(self, semester, year): # should we call it in add_semester ?
        all_sids  = self.update_studnet_grade_in_courses(semester, year) # how to get grades and fill each course, uploaded sheet (sid,cid,grade)?  #random assigement
        for sid in all_sids:
            self.db.update_num_credits(sid)
            self.calculate_gpa(sid)
        #self.db.update_student_grade(student_id) # after a year
        # GPA? create a method?

    def update_studnet_grade_in_courses(self, semester: str, year: int):
        '''
        Updates all students grades in all enrolled courses at a given semester by randomly chosen grade.
        '''

        sid_cids = self.db.get_table_where('sid, cid','Takes', 'semester= \'%s\' and year = %s'%(semester,year))
        grades = ['A','B','C','D','F']
        all_sids = []
        for r in sid_cids:
            sid = r['sid']
            cid = r['cid']
            grade = random.choice(grades)
            self.db.update_student_course_grade(sid, cid, semester, year, grade)
            all_sids.append(sid)
        return all_sids

    def remove_completed_courses(self, avalible_course_ids: str, completed_course_ids) -> list[str]:
        return list(set(avalible_course_ids) - set(completed_course_ids))

    def get_schedule(self, sid) -> list[dict]:
        return self.db.get_schedule(sid)

    def get_students(self) -> list[dict]:
        '''
        Returns all students.
        '''
        return self.db.get_table('*', 'Student')

    def remove_course(self, student_id: str, course_id: str, semester: str,year: int ) -> list[dict]:
        '''
        remove a course from student's schedule.
        '''
        return self.db.remove_course(student_id, course_id, semester,year)

    def add_course(self, student_id: str, course_id: str, semester: str,year: int ) -> list[dict]:
        '''
        adds a course to student's schedule after checking if the student has fullfilled any prerequisites and has not taken the course previously.
        '''
        list_of_prerequisites = self.db.get_prerequisites(course_id)
        list_of_completed_courses = self.db.get_completed_courses(student_id)
        list_of_current_courses = self.db.get_student_schdule(student_id, semester,year)
        list_of_current_courses = [r['course_id'] for r in list_of_current_courses]
        not_fullfilled = False
        if (course_id not in list_of_completed_courses):
            if (course_id not in list_of_current_courses):
                if list_of_prerequisites != [] :
                    for p in list_of_prerequisites:
                        if p in list_of_completed_courses:
                            continue
                        else:
                            not_fullfilled = True
                if not not_fullfilled:
                     self.db.enroll_into_class(student_id, course_id, semester, year)
                     print('The course has been added successfully.')

                     return True
                else:
                    print('Error: Prerequisites not fullfilled.')
                    return False
            else:
                    print('Error: the student is taking the course.')
                    return False
        else:
                print('Error: the student has already taken the course.')
                return False

    def get_courses(self) -> list[dict]:
        '''
        Returns all courses.
        '''
        return self.db.get_table('*', 'Course')

    def get_takes(self) -> list[dict]:
        return self.db.get_table('*', 'Takes')

    def clear_schedule(self):
        '''
        This method should clear the schedule of all students.
        '''
        self.db.clear_schedule()
