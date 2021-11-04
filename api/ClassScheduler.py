
from Database import Database


class ClassScheduler:

    def __init__(self):
        self.db = Database()

    def get_students(self):
        '''
        This method returns all students
        '''
        return self.db.get_students()
