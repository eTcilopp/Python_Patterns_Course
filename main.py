def index_view(request):
    print(request)
    return '200 OK', [b'Index']


def abc_view(request):
    print(request)
    return '200 OK', [b'ABC']


class Other:
    def __call__(self, request):
        print(request)
        return '200 OK', [b'<h1>Other</h1>']


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 PAGE Not Found']


class SecretFront:
    def __call__(self, request):
        request['secret'] = 'some secret'


class OtherFront:
    def __call__(self, request):
        request['key'] = 'key'


routes = {
    '/': index_view,
    '/abc/': abc_view,
    '/other/': Other()
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
        view = not_found_404_view
        if path[-1] != '/':
            path += '/'
        if path in self.routes:
            print(path)
            view = self.routes[path]

        request = {}

        for front in self.fronts:
            front(request)

        code, body = view(request)

        start_response(code, [('Content-Type', 'text/html')])
        return body


application = Application(routes, fronts)
