
from Database import Database


class ClassScheduler:

    def __init__(self):
        self.db = Database()

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
