from jinja2 import Environment, FileSystemLoader
import shutil
import os
from glob import glob
import json
import re


def build(root):
    config = {'metadata': {}, 'ignore': []}

    config_path = os.path.join(root, '.ljon/config.json')
    public_path = os.path.join(root, 'public')
    templates_path = os.path.join(root, '.ljon/templates')

    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        raise Exception("No configuration file found at '{}'".format(
            config_path))

    if not os.path.isdir(public_path):
        os.makedirs(public_path)

    for the_file in os.listdir(public_path):
        file_path = os.path.join(public_path, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            raise e

    j2 = Environment(loader=FileSystemLoader([root, templates_path]))

    content = []
    pathname = '*'

    while True:
        files = glob(os.path.join(root, pathname))

        if len(files) == 0: break

        content.extend(files)
        pathname = os.path.join(pathname, '*')

    for path in content:
        ignore = False

        for pattern in config['ignore']:
            if re.match(pattern, path):
                ignore = True
                break

        if ignore: continue

        if os.path.isdir(path): continue

        is_template, is_metadata = False, False

        try:
            extension = str(path.split('/')[-1]).split('.', maxsplit=1)[1]

            if extension.split('.')[-1] == 'j2':
                is_template = True
                real_extension = extension.split('.')[-2]

            if extension.split('.')[-1] == 'json' and \
                extension.split('.')[-2] == 'j2' and \
                len(extension.split('.')) >= 3:
                is_metadata = True

        except IndexError:
            pass
        if '/' in path:
            directories = '/'.join(path.split('/')[:-1])
            os.makedirs(os.path.join(public_path, directories), exist_ok=True)

        if is_template:
            template = j2.get_template(path)

            metadata = config['metadata'].copy()

            try:
                with open('{}.json'.format(path)) as metadata_file:
                    metadata.update(json.load(metadata_file))
            except FileNotFoundError:
                pass

            rendered = template.render(**metadata)

            destination_path = '.'.join(path.split('.')[0:-2])
            destination_path = '{destination}.{ext}'.format(
                                destination=destination_path,
                                ext=real_extension)
            destination_path = os.path.join(public_path, destination_path)

            with open(destination_path, 'w') as h:
                h.write(rendered)
        elif is_metadata:
            pass
        else:
            shutil.copy(path, os.path.join(public_path, path))


if __name__ == '__main__':
    build()
