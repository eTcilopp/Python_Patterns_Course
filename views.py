from tempalator import render


class IndexView:
    def __call__(self, request):
        output = render('templates/mainapp/index.html', object_list=[])
        return '200 OK', [bytes(output, 'utf-8')]


class AboutView:
    def __call__(self, request):
        output = render('templates/mainapp/about.html', object_list=[])
        return '200 OK', [bytes(output, 'utf-8')]


class NotFound404:
    def __call__(self, request):
        return '404 OK', [b'404: page not fond']


class SecretFront:
    def __call__(self, request):
        request['secret'] = 'some secret'


class OtherFront:
    def __call__(self, request):
        request['key'] = 'key'
