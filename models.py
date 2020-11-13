from abc import ABCMeta, abstractmethod

categories_list = []
courses_list = []

class Course(metaclass=ABCMeta):

    @abstractmethod
    def get_courseName(self):
        pass

    @abstractmethod
    def get_courseCategory(self):
        pass

    @abstractmethod
    def get_courseType(self):
        pass


class OnlineCourse(Course):

    def __init__(self, courseName, courseCategory):
        self.courseType = 'Online'
        self.courseName = courseName
        self.courseCategory = courseCategory

    def get_courseName(self):
        return {'Course name': self.courseName}

    def get_courseType(self):
        return {'Course Type': self.courseType}

    def get_courseCategory(self):
        return {'Course Category': self.courseCategory}


class InClassCourse(Course):

    def __init__(self, courseName, courseCategory):
        self.courseType = 'In Class'
        self.courseName = courseName
        self.courseCategory = courseCategory

    def get_courseName(self):
        return {'Course name': self.courseName}

    def get_courseType(self):
        return {'Course Type': self.courseType}

    def get_courseCategory(self):
        return {'Course Category': self.courseCategory}

class CourseFactory:
    @staticmethod
    def get_course(courseType, courseName, courseCategory):
        """
        Функция создает класс заданного типа курса
        :param courseType: типы курса (Online, In Class)
        :param courseCategory: категория курса
        :param courseName: наименование курса
        :return: экземпляр класса соответствующего курса
        """
        try:
            if courseType == 'online':
                return OnlineCourse(courseName, courseCategory)
            if courseType == 'inclass':
                return InClassCourse(courseName, courseCategory)
            raise AssertionError('Course Category or Type not found')
        except AssertionError as _e:
            print(_e)


if __name__ == '__main__':
    course1 = CourseFactory.get_course('online', 'How to get reach - fast')
    print(course1.get_courseName())

    course2 = CourseFactory.get_course('inclass', 'How to lose weight- fast')
    print(course2.get_courseName())
