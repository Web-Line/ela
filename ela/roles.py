from rolepermissions.roles import AbstractUserRole


class Admin(AbstractUserRole):
    available_permissions = {
        # 'edit_pacient_file': True,
    }


class Staff(AbstractUserRole):
    available_permissions = {

    }


class Student(AbstractUserRole):
    available_permissions = {

    }


class Teacher(AbstractUserRole):
    available_permissions = {

    }
