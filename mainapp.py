from views import *

routes = {
    '/': IndexView(),
    '/about/': AboutView()
}

fronts = [SecretFront(), OtherFront()]


class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        """
        Callable object для вызова
        :param environ: словарь данных от сервера
        :param start_response: функция для ответа серверу
        :return:
        """

        path = environ['PATH_INFO']
        view = NotFound404()

        if path[-1] != '/':
            path += '/'

        if path in self.routes:
            view = self.routes[path]

        request = {}

        for front in self.fronts:
            front(request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes, fronts)
