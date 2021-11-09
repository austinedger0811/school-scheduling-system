
from Database import Database
import random

class ClassScheduler:

    def __init__(self):
        self.db = Database()
        # self.semester = X
        # self.year = Y
        # add course offersings to the database.


    def schedule_students(self):
        '''
        Schedules all students who currently do not have full schedules.
        '''
        student_ids = self.db.get_student_ids_without_full_schedule()
        for id in student_ids:
            self.schedule_student(id)
        return student_ids

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

        while (student_id in self.db.get_student_ids_without_full_schedule( '\''+semester+'\'', year)): # less than 5 courses
            requirements = self.db.get_student_requirements_status(student_id)
            all_possible_course = self.db.get_list_possible_courses_to_enroll(student_id)
            all_possible_course_ids = [all_possible_course[i]['course_id'] for i in range(len(all_possible_course))]

            # requirement commponent (get course ids of courses of reqs to be completed)
            all_possible_course_ids_with_reqs = []
            for c in all_possible_course:
                if c['requirement_type'] not in get_list_of_fullfilled_requirements(requirements):
                   all_possible_course_ids_with_reqs.append(r['course_id'])

            selected_course = random.choice(all_possible_course_ids_with_reqs)
            timeconflict = True;

            while(timeconflict):
                val = self.db.check_time_conflict(student_id, '\''+selected_course+'\'', '\''+semester+'\'', year)
                print(val)
                if val == []:
                    timeconflict = False
                else:
                    timeconflict = True
                    selected_course = random.choice(all_possible_course_ids_with_reqs)


            #insert to takes table
            #self.db.enroll_into_class(student_id, selected_course: , semester, year) # need to be tested
            print(selected_course)



    def update_studnet_info_after_semester_ends(student_id: str): # need to be tested
        update_studnet_grade_in_course() # how to get grades and fill each course, uploaded sheet (sid,cid,grade)? # need to be tested
        self.db.update_num_credits(student_id) # need to be tested
        self.db.update_student_grade(student_id)# need to be tested
        # GPA? create a method

    def update_studnet_grade_in_course(self, student_id: str, course_id: str, grade: str, semester: str,year: int): # need to be tested
        self.db.get_student_requirements_status(student_id, course_id, semester, year, grade)

    def remove_completed_courses(self, avalible_course_ids: str, completed_course_ids) -> list[str]:
        return list(set(avalible_course_ids) - set(completed_course_ids))

    def get_students(self) -> list[dict]:
        '''
        Returns all students.
        '''
        return self.db.get_table('*', 'Student')

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
