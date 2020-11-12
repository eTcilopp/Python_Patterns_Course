from abc import ABCMeta, abstractmethod


class Course(metaclass=ABCMeta):

    @abstractmethod
    def get_courseName(self):
        pass


class OnlineCourse(Course):

    def __init__(self, courseName):
        self.courseType = 'Online'
        self.courseName = courseName

    def get_courseName(self):
        return {'Course name': self.courseName, 'Course Type': self.courseType}


class InClassCourse(Course):

    def __init__(self, courseName):
        self.courseType = 'In Class'
        self.courseName = courseName

    def get_courseName(self):
        return {'Course name': self.courseName, 'Course Type': self.courseType}


class CourseFactory:
    @staticmethod
    def get_course(courseType, courseName):
        """
        Функция создает класс заданного типа курса
        :param courseType: типы курса (Online, In Class)
        :param courseName: наименование курса
        :return: экземпляр класса соответствующего курса
        """
        try:
            if courseType == 'online':
                return OnlineCourse(courseName)
            if courseType == 'inclass':
                return InClassCourse(courseName)
            raise AssertionError('CourseType not found')
        except AssertionError as _e:
            print(_e)


if __name__ == '__main__':
    course1 = CourseFactory.get_course('online', 'How to get reach - fast')
    print(course1.get_courseName())

    course2 = CourseFactory.get_course('inclass', 'How to lose weight- fast')
    print(course2.get_courseName())
