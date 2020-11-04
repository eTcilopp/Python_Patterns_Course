from jinja2 import FileSystemLoader
from jinja2 import Environment


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)


if __name__ == '__main__':
    output_test = render('about.html', object_list=[
        {'name': 'Leo'}, {'name': 'Kate'}])
    print(output_test)
