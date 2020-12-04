import re
from datetime import datetime
from my_framework.tempalator import render

from models import categories_list, courses_list, Student

routes = {}


def app(url):
    if '<int>' in url:
        url = url.replace('<int>', r'\d*')
        url = re.compile(url)
    elif '<str>' in url:
        url = url.replace('<str>', r'\w*')
        url = re.compile(url)

    def decorator(cls):
        routes.update({url: cls()})
        return cls
    return decorator


def debug(cls):
    '''
    Функция-декоратор, принимает класс (View), переопределяет кго __call__ метод, добавляя в него вывод в консоль
    имени переданного класса, времени вызова
    :param cls: класс с функцией __call__: любой из имеющихся View
    :return: Возвращает класс с измененным (дополненным) методов __call__
    '''

    def decorated_call(fn):
        def new_call(*args, **kwargs):
            print(
                f'Method from {cls.__name__} has been called at {datetime.now().strftime("%H:%M:%S")}')
            result = fn(*args, **kwargs)
            return result

        return new_call

    cls.__call__ = decorated_call(cls.__call__)
    return cls


def find_student(student_id):
    for student in Student.student_list():
        if student.id == student_id:
            return student
    return f'Student with ID {student_id} not found'


def find_course(course_name):
    for course in courses_list:
        if course.get_courseName['Course name'] == course_name:
            return course



@debug
@app('^/$')
class IndexView:
    def __call__(self, request):
        title = 'Index'
        output = render('index.html',
                        title=title,
                        object_list=[
                            'cat',
                            'dog',
                            'horse',
                            'fish',
                            'llama',
                            'Polina'])
        return '200 OK', [bytes(output, 'utf-8')]


@app('/about/')
class AboutView:
    def __call__(self, request):
        title = 'About'
        output = render('about.html',
                        title=title,
                        object_list=[])
        return '200 OK', [bytes(output, 'utf-8')]


@app('/students/')
class StudentsView:
    def __call__(self, request):
        title = 'Student List'
        output = render('students.html',
                        title=title,
                        object_list=Student.student_list())
        return '200 OK', [bytes(output, 'utf-8')]


@debug
@app('/student/<int>')
class StudentView:
    def __call__(self, request):
        student_id = int(request['path'][9:-1])
        student = find_student(student_id)
        output = render(
            'student.html',
            title='Student page',
            object_list=student)
        return '200 OK', [bytes(output, 'utf-8')]


@debug
@app('/categories/')
class CategoriesView:
    def __call__(self, request):
        title = 'Categories'
        output = render('categories.html',
                        title=title,
                        object_list=categories_list)
        return '200 OK', [bytes(output, 'utf-8')]


@debug
@app('/courses/')
class CoursesView:
    def __call__(self, request):
        title = 'Courses'
        output = render(
            'courses.html',
            title=title,
            object_list={
                'courses_list': courses_list,
                'categories_list': categories_list})
        return '200 OK', [bytes(output, 'utf-8')]


@debug
@app(r'/course/<str>')
class CourseView:

    def get_available_students_list(self, enrolled_students_id_list):
        _available_students_list = []
        for student in Student.student_list():
            if student.id not in enrolled_students_id_list:
                _available_students_list.append(
                    {'id': student.id, 'first_name': student.first_name, 'last_name': student.last_name})
        return _available_students_list

    def __call__(self, request):
        title = 'Course!'
        course_name = request['path'][8:-1]
        course = find_course(course_name)
        _enrolled_students_id_list = course.get_enrolled_students_id_list
        _available_students_list=self.get_available_students_list(_enrolled_students_id_list)
        print(f'views 150 {_enrolled_students_id_list}')
        output = render(
            'course.html',
            title=title,
            object_list={
                'course': course,
                'available_students': _available_students_list})
        return '200 OK', [bytes(output, 'utf-8')]


@debug
class NotFound404:
    def __call__(self, request):
        return '404 OK', [b'404: page not fond']


class SecretFront:
    def __call__(self, request):
        request['secret'] = 'some secret'


class OtherFront:
    def __call__(self, request):
        request['course'] = 'key'
