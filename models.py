from abc import ABCMeta, abstractmethod

categories_list = []
courses_list = []


class User(metaclass=ABCMeta):
    def get_name(self):
        return f'First name: {self.first_name}, Last name: {self.last_name}'


class Instructor(User):
    instructor_id = 1
    instructor_list = []

    def __init__(self, first_name, last_name, dob):
        self.id = Instructor.instructor_id
        self.firstName = first_name
        self.lastName = last_name
        self.yob = dob
        Instructor.instructor_id += 1
        Instructor.instructor_list.append(self)


class Student(User):
    student_id = 1
    student_list = []

    def __init__(self, first_name, last_name, dob):
        self.id = Student.student_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        Student.student_id += 1
        Student.student_list.append(self)


class UserFactory:
    @staticmethod
    def create_user(user_type, first_name, last_name, dob):
        try:
            if user_type == 'student':
                return Student(first_name, last_name, dob)
            else:
                return Instructor(first_name, last_name, dob)
        except AssertionError as _e:
            print(_e)


class Course(metaclass=ABCMeta):

    @property
    def get_courseName(self):
        return {'Course name': self.courseName}

    @property
    def get_courseType(self):
        return {'Course Type': self.courseType}

    @property
    def get_courseCategory(self):
        return {'Course Category': self.courseCategory}

    def assign_student(self, student):
        if student not in self.assignedStudents:
            self.assignedStudents.append(student)

    def unassign_student(self, student):
        if student in self.assignedStudents:
            self.assignedStudents.remove(student)



class OnlineCourse(Course):

    def __init__(self, courseName, courseCategory):
        self.courseType = 'Online'
        self.courseName = courseName #TODO - сделай super()
        self.courseCategory = courseCategory
        self.assignedStudents = []


class InClassCourse(Course):

    def __init__(self, courseName, courseCategory):
        self.courseType = 'In Class'
        self.courseName = courseName
        self.courseCategory = courseCategory
        self.assignedStudents = []


class CourseFactory:
    @staticmethod
    def get_course(course_type, course_name, course_category):
        """
        Функция создает класс заданного типа курса
        :param course_type: типы курса (Online, In Class)
        :param course_category: категория курса
        :param course_name: наименование курса
        :return: экземпляр класса соответствующего курса
        """
        try:
            if course_type == 'online':
                return OnlineCourse(course_name, course_category)
            if course_type == 'inclass':
                return InClassCourse(course_name, course_category)
            raise AssertionError('Course Category or Type not found')
        except AssertionError as _e:
            print(_e)


if __name__ == '__main__':
    course1 = CourseFactory.get_course(
        'online', 'How to get reach - fast', 'cat1')
    print(course1.get_courseName())

    course2 = CourseFactory.get_course(
        'inclass', 'How to lose weight- fast', 'cat2')
    print(course2.get_courseName())

    student1 = UserFactory.create_user(
        'student', 'Donald', 'Trump', '18/May/1974')
    student2 = UserFactory.create_user(
        'student', 'Donald', 'Trump', '18/May/1974')
    student3 = UserFactory.create_user(
        'student', 'Donald', 'Trump', '18/May/1974')
    print(student1.get_name())
    print(Student.student_list)

    for student in Student.student_list:
        print(f'Name: {student.first_name}, ID: {student.id}')
