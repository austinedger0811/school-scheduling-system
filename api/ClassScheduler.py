
from Database import Database


class ClassScheduler:

    def __init__(self):
        self.db = Database()

    def schedule_students(self):
        '''
        Schedules all students who currently do not have full schedules.
        '''
        student_ids = self.db.get_student_ids_without_full_schedule()
        for id in student_ids:
            self.schedule_student(id)
        return student_ids

    def schedule_student(self, student_id: str) -> None:
        '''
        Schedules a student in 5 classes.
        '''
        avalible_course_ids = self.db.get_course_ids_with_capacity()
        completed_course_ids = self.db.get_completed_courses(student_id)

        # Remove completed courses from avalible courses
        course_ids = self.remove_completed_courses(
            avalible_course_ids, completed_course_ids)

        # Remove coures where the student does not have the prereques

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
        return self.db.get_table('*', 'Tasks')

    def clear_schedule(self):
        '''
        This method should clear the schedule of all students.
        '''
        self.db.clear_schedule()
