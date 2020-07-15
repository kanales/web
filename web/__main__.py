
from jinja2 import Environment, PackageLoader, select_autoescape, FileSystemLoader
import os
import shutil
import re

import markdown


BASE = os.path.dirname(__file__)
TEMPLATE_DIR = os.path.join(BASE, 'templates')
OUT_DIR = 'public'
STATIC_PATH = os.path.join(BASE, 'static')
RESOURCE_PATH = os.path.join(BASE, 'resources')

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    autoescape=select_autoescape(['html', 'xml']),
)


for root, dirs, files in os.walk(OUT_DIR):
    for dir in dirs:
        shutil.rmtree(os.path.join(root, dir))

    for file in files:
        if not file.startswith('.git'):
            os.remove(os.path.join(root, file))


class Data:
    def __init__(self, root: str, filename: str):
        stripped = filename[:filename.find('.')]
        self.name = stripped.replace('-', ' ').title()
        self.file = f'{stripped}.html'


# render templates
for root, dirs, files in os.walk(TEMPLATE_DIR):
    out_root = re.sub(TEMPLATE_DIR, OUT_DIR, root)
    for dir in dirs:
        os.makedirs(os.path.join(out_root, dir))

    files = [f for f in files if not f.startswith('_')]
    data = [
        Data(root, f) for f in files if f.endswith('.md')
    ]
    for file in files:
        if file.endswith('.md'):
            with open(os.path.join(root, file), 'r') as f:
                m = markdown.markdown(f.read())
            content = env.from_string('\n'.join([
                r'{% extends "_base.html" %}',
                r'{% block content %}',
                m,
                r'{% endblock %}'
            ])).render()
            file = re.sub('.md', '.html', file)
        elif file.endswith('.html'):
            o_root = re.sub(TEMPLATE_DIR, '', root)
            content = env.get_template(
                os.path.join(o_root, file)).render(filedata=data)
        else:
            break

        out_file = os.path.join(out_root, file)
        print('writing:', out_file)
        with open(out_file, 'w+') as f:
            f.write(content)

# Copy static files
for root, dirs, files in os.walk(STATIC_PATH):
    for dir in dirs:
        shutil.copytree(os.path.join(root, dir), os.path.join(OUT_DIR, dir))

# Copy resources
for name in os.listdir(RESOURCE_PATH):
    path = os.path.join(RESOURCE_PATH, name)
    if os.path.isdir(path):
        shutil.copytree(path, os.path.join(OUT_DIR, name))
    elif os.path.isfile(path):
        shutil.copyfile(path, os.path.join(OUT_DIR, name))
