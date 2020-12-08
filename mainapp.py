import logging
from views import *
from models import CourseFactory, UserFactory, db_connection, category_mapper

# simple logging setup
# to log an event do: logging.info(f'Event {variable}')
logging.basicConfig(
    filename=f'logs/{__name__}.log',
    format='%(levelname)-10s %(asctime)s %(message)s',
    level=logging.INFO
)
logging.info('Started Logging')

fronts = [SecretFront(), OtherFront()]


def parse_input_data(data):
    """
    Функция чтения содержимого GET запроса
    :param data: запрос
    :return: словарь с расшифрованным текстом запроса
    """
    result = {}
    if data:
        params = data.split('&')
        for item in params:
            key, value = item.split('=')
            result[key] = value
    return result


def get_wsgi_input_data(env):
    """
    Извлечение запроса, отправленного методом POST
    :param env: запрос
    :return: словарь с текстом запроса
    """
    content_length_data = env.get('CONTENT_LENGTH')
    content_length = int(content_length_data) if content_length_data else 0
    data = env['wsgi.input'].read(
        content_length) if content_length > 0 else b''
    return data


def parse_wsgi_input_data(data: bytes) -> dict:
    result = {}
    if data:
        data_str = data.decode(encoding='utf-8')
        result = parse_input_data(data_str)
    return result


class Application:
    def __init__(self, routes, fronts, db_connection):
        self.routes = routes
        self.fronts = fronts
        self.connection = db_connection


    def __call__(self, environ, start_response):
        """
        Callable object для вызова
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        :return:
        """

        path = environ['PATH_INFO']

        method = environ['REQUEST_METHOD']

        if method == 'GET':
            print('method: ', method)
            query_string = environ['QUERY_STRING']
            request_params = parse_input_data(query_string)
            print(request_params)
        else:
            print('method: ', method)
            data = get_wsgi_input_data(environ)
            data = parse_wsgi_input_data(data)
            if 'createcategory' in data and data['createcategory'] not in categories_list:
                category_mapper.insert(data['createcategory'])
                categories_list.append(data['createcategory'])
                logging.info(f'Created new category: {data["createcategory"]}')
            if 'newcoursename' in data:
                newCourse = CourseFactory.get_course(
                    data['newcoursetype'],
                    data['newcoursename'],
                    data['newcoursecategory']
                )
                courses_list.append(newCourse)
                logging.info(f'Created new course: {newCourse.courseName}')
            if 'addstfirstname' in data and 'addstlastname' in data and 'addstdob' in data:
                if len(
                        data['addstfirstname'] +
                        data['addstlastname'] +
                        data['addstdob']) > 5:
                    new_student = UserFactory.create_user(
                        'student', data['addstfirstname'], data['addstlastname'], data['addstdob'])
                    logging.info(
                        f'Created new student: {new_student.get_name()}')
                    del new_student
            if 'assigning_student_id' in data and 'course' in data:
                student = find_student(int(data['assigning_student_id']))
                course = find_course(data['course'])
                course.assign_student(student)
                logging.info(
                    f'Student: {student.last_name}, {student.first_name}'
                    f'enrolled into the course {course.get_courseName["Course name"]}')
            if 'student_notification_message' in data and 'course' in data:
                course = find_course(data['course'])
                course.notify(
                    'Hello, Observers',
                    data['student_notification_message'])
                logging.info(
                    f'Notification was sent to all users of a course: {data["course"]}')
            if 'unassign_student_id' in data and 'course' in data:
                course = find_course(data['course'])
                student = find_student(int(data['unassign_student_id']))
                course.unassign_student(student)
                logging.info(
                    f'Student {student.first_name} unenrolled from the course: {data["course"]}')

            print(data)  # TODO - remove

        view = NotFound404()

        if path[-1] != '/':
            path += '/'

        for route in self.routes:
            rex = re.compile(route)
            if rex.match(path):
                view = self.routes[route]
                logging.info(f'Processed path: {path}')
                break

        request = {'path': path}

        for front in self.fronts:
            front(request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes, fronts, db_connection)
