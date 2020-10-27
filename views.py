from pathlib import Path
from my_framework.tempalator import render

template_folder = Path('templates/mainapp/')


class IndexView:
    def __call__(self, request):
        title = 'Index'
        output = render(
            template_folder / 'index.html',
            title=title,
            object_list=[
                'cat',
                'dog',
                'horse',
                'fish',
                'llama',
                'Polina'])
        return '200 OK', [bytes(output, 'utf-8')]


class AboutView:
    def __call__(self, request):
        title = 'About'
        output = render(
            template_folder / 'about.html',
            title=title,
            object_list=[
                1,
                2,
                3,
                4,
                5,
                6,
                7,
                8,
                9])
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
