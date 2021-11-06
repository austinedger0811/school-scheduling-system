
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

    def schedule_student(self, id: str) -> None:
        '''
        Schedules a student in 5 classes.
        '''
        course_ids = self.db.get_course_ids_with_capacity()

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
