from datetime import datetime
from my_framework.tempalator import render

from models import categories_list, courses_list


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
                f'Method from {cls.__name__} was called at {datetime.now().strftime("%H:%M:%S")}')
            result = fn(*args, **kwargs)
            return result
        return new_call

    cls.__call__ = decorated_call(cls.__call__)
    return cls

@debug
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


@debug
class AboutView:
    def __call__(self, request):
        title = 'About'
        output = render('about.html',
                        title=title,
                        object_list=[])
        return '200 OK', [bytes(output, 'utf-8')]

@debug
class CategoriesView:
    def __call__(self, request):
        title = 'Categories'
        output = render('categories.html',
                        title=title,
                        object_list=categories_list)
        return '200 OK', [bytes(output, 'utf-8')]

@debug
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
class CourseView:
    def __call__(self, request):
        title = 'Course!'
        course = request['path'][8:-1]
        print(request)  # TODO - remove Print
        output = render('course.html',
                        title=title,
                        object_list={'course': course})
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
