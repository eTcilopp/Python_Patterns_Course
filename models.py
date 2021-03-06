import threading
from abc import ABCMeta, abstractmethod
import sqlite3
from sqlite3 import Error
from settings import db_file


# categories_list = [] #TODO - remove me!
courses_list = []


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def set_up_database():
    # creating/connecting to database
    # creating tables
    # creating table STUDENTS
    sql_create_students_table = """CREATE TABLE IF NOT EXISTS students (
                id integer PRIMARY KEY,
                first_name text NOT NULL,
                last_name text NOT NULL,
                dob text
            ); """

    sql_create_categories_table = """CREATE TABLE IF NOT EXISTS categories (
                id integer PRIMARY KEY AUTOINCREMENT,
                category text NOT NULL
            ); """

    sql_create_course_table = """ CREATE TABLE IF NOT EXISTS courses (
                id integer PRIMARY KEY AUTOINCREMENT,
                category_id integer NOT NULL,
                course_type text NOT NULL,
                course text NOT NULL,
                description TEXT,
                FOREIGN KEY (category_id) REFERENCES categories(id)
                ); """

    conn = create_connection(db_file)

    if conn is not None:
        create_table(conn, sql_create_students_table)
        create_table(conn, sql_create_categories_table)
        create_table(conn, sql_create_course_table)
    else:
        print("Error! cannot create the database connection.")

    return conn


db_connection = set_up_database()


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class UnitOfWork:
    """
    Паттерн UNIT OF WORK
    """

    current = threading.local()

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class Category:
    def __init__(self, category):
        self.category = category


class CategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    @property
    def get_categories_list(self):
        result = []
        cursor = self.cursor
        statement = "SELECT * FROM categories"
        cursor.execute(statement)
        query_result = self.cursor.fetchall()
        if query_result:
            for row in query_result:
                print(f'models 149 {row[1]}') #TODO - remove me!
                result.append(row[1])
        return result


    def insert(self, category):
        statement = "INSERT INTO categories (category) VALUES(?)"
        self.cursor.execute(statement, (category,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)



category_mapper = CategoryMapper(db_connection)
categories_list = category_mapper.get_categories_list

class User(metaclass=ABCMeta):
    def get_name(self):
        return f'First name: {self.first_name}, Last name: {self.last_name}'

    def notify(self, course, *args, **kwargs):
        print(f'Observer {self.first_name} received:', args, kwargs)


class DomainObject:

    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


class Instructor(User):
    instructor_id = 1
    instructor_list = []

    def __init__(self, first_name, last_name, dob):
        self.id = Instructor.instructor_id
        self.first_name = first_name
        self.last_name = last_name
        self.dob = dob
        Instructor.instructor_id += 1
        Instructor.instructor_list.append(self)


class Student(User, DomainObject):

    @staticmethod
    def student_list():
        result = []
        connection = sqlite3.connect(db_file)
        cursor = connection.cursor()
        print("Connected to SQLite")
        sqlite_select_query = """SELECT * from students"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        print("Total rows are:  ", len(records))
        print("Printing each row")
        for row in records:
            result.append(
                Student(
                    id=row[0],
                    first_name=row[1],
                    last_name=row[2],
                    dob=row[3]))
        cursor.close()
        return result

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class StudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_student):
        statement = f"SELECT id, first_name, last_name FROM students WHERE id=?"
        self.cursor.execute(statement, (id_student,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(
                f'record with id={id_student} not found')

    def insert(self, student):
        statement = f"INSERT INTO students (first_name, last_name, dob) VALUES (?, ?, ?)"
        self.cursor.execute(
            statement,
            (student.first_name,
             student.last_name,
             student.dob))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return StudentMapper(db_connection)


class UserFactory:
    @staticmethod
    def create_user(user_type, first_name, last_name, dob):
        try:
            if user_type == 'student':
                new_student = Student(
                    first_name=first_name, last_name=last_name, dob=dob)
                UnitOfWork.new_current()
                new_student.mark_new()
                UnitOfWork.get_current().commit()
                UnitOfWork.set_current(None)
                return new_student
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

    @property
    def get_enrolled_students_id_list(self):
        _enrolled_students_id_list = []
        for student in self.assignedStudents:
            _enrolled_students_id_list.append(student.id)
        return _enrolled_students_id_list

    def assign_student(self, student):
        if student not in self.assignedStudents:
            self.assignedStudents.append(student)


    def unassign_student(self, student):
        if student in self.assignedStudents:
            self.assignedStudents.remove(student)


    def notify(self, *args, **kwargs):
        for student in self.assignedStudents:
            student.notify(self, *args, kwargs)

class CourseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def insert(self, course):
        statement = f"INSERT INTO courses (category_id, course_type, course) VALUES (?, ?, ?)"
        self.cursor.execute(
            statement,
            (course.courseCategory,
             course.courseType,
             course.courseName))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def get_course_by_name(self, course_name):
        statement = f"SELECT courses.id, course_type, course, description, category FROM courses INNER JOIN categories ON categories.id = courses.category_id WHERE course = ?"
        self.cursor.execute(statement, (course_name,))
        result = self.cursor.fetchall()
        print('beeep')
        for row in result:
            print(row)
        # if result:
        #     print('beeeeeep')
        #     print(result)
        # else:
        #     raise RecordNotFoundException(
        #         f'record with name={course_name} not found')

course_mapper = CourseMapper(db_connection)

class OnlineCourse(Course):

    def __init__(self, courseName, courseCategory):
        self.courseType = 'Online'
        self.courseName = courseName  # TODO - сделай super()
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
                course_name = course_name.replace('+', '')
                course_category = course_category.replace('+', '')
                return OnlineCourse(course_name, course_category)
            if course_type == 'inclass':
                return InClassCourse(course_name, course_category)
            raise AssertionError('Course Category or Type not found')
        except AssertionError as _e:
            print(_e)


if __name__ == '__main__':
    # Getting list of students from the DB
    # connection = sqlite3.connect(db_file)
    # cursor = connection.cursor()
    # print("Connected to SQLite")
    # sqlite_select_query = """SELECT * from students"""
    # cursor.execute(sqlite_select_query)
    # records = cursor.fetchall()
    # print("Total rows are:  ", len(records))
    # print("Printing each row")
    # for row in records:
    #     print("Id: ", row[0])
    #     print("First Name: ", row[1])
    #     print("Last Name: ", row[2])
    #     print("Date of Birth: ", row[3])
    # cursor.close()

    for student in Student.student_list():
        print(student.first_name)
