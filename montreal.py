from jinja2 import Environment, FileSystemLoader
import shutil
import os
from glob import glob
import json


if __name__ == '__main__':
    with open('.montreal.json', 'r') as f:
        config = json.load(f)

    try:
        shutil.rmtree('./public')
    except FileNotFoundError:
        pass

    os.makedirs('./public', exist_ok=True)

    j2 = Environment(loader=FileSystemLoader(['./.templates', './']))

    content = []

    pathname = '*'

    while True:
        files = glob(pathname)

        if len(files) == 0:
            break

        content.extend(files)
        pathname += '/*'

    for f in content:
        if os.path.isdir(f):
            continue

        extension = f.split('.', maxsplit=1)[1]
        path = f

        if '/' in path:
            directories = '/'.join(path.split('/')[:-1])
            os.makedirs('./public/{}'.format(directories), exist_ok=True)

        if extension == 'j2':
            template = j2.get_template(path)

            metadata = config.copy()

            if os.path.exists('{}.json'.format(f)):
                with open('{}.json'.format(f)) as metadata_file:
                    metadata.update(json.load(metadata_file))

            rendered = template.render(**metadata)

            with open('./public/{}'.format(path.replace('j2', 'html')), 'w') as h:
                h.write(rendered)
        elif extension == 'j2.json':
            pass
        else:
            shutil.copy(f, './public/{}'.format(path))
