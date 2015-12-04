from rolepermissions.roles import AbstractUserRole


class Student(AbstractUserRole):
    pass


class Teacher(AbstractUserRole):
    pass


class Supervisor(AbstractUserRole):
    pass
