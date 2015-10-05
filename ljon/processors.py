from jinja2 import Environment, FileSystemLoader
import json
import subprocess
from PIL import Image
import os


def jinja(path, intended_path, root, templates_path, config):
    j2 = Environment(loader=FileSystemLoader([root, templates_path]),
                     extensions=['jinja2_highlight.HighlightExtension'])

    template = j2.get_template(path)

    metadata = config['metadata'].copy()

    try:
        with open('{}.json'.format(path)) as metadata_file:
            metadata.update(json.load(metadata_file))
    except FileNotFoundError:
        pass

    rendered = template.render(**metadata)

    with open(intended_path, 'w') as h:
        h.write(rendered)


def shell(command, path, root, public_path, templates_path, config):
    command = command.format(path=path, root=root, public_path=public_path,
                             templates=templates_path, config=config)

    subprocess.run(command.split(' '))


def pillow(filepath, pipeline, context):
    path, filename = os.path.split(filepath)
    filename, extension = os.path.splitext(filename)

    with Image.open(filepath) as image:
        for step in pipeline:
            if step['func'] == 'resize':
                width = step.get('width', None)
                height = step.get('height', None)

                if width is not None and height is not None:
                    image = image.resize((width, height))
                elif width is not None and height is None:
                    ratio = width / image.size[0]
                    height = int(image.size[1] * ratio)

                    image = image.resize((width, height))
                elif height is not None and width is None:
                    ratio = height / image.size[1]
                    width = int(image.size[0] * ratio)

                    image = image.resize((width, height))
                if not width and not height:
                    raise Exception('A width and/or height must be provided.')
            if step['func'] == 'write':
                name = step.get('name', None)

                if name is None:
                    name = os.path.join(context.public_path, filepath)
                else:
                    name = name.format(public_path=context.public_path,
                                       path=path, name=filename,
                                       width=image.size[0],
                                       height=image.size[1],
                                       extension=extension[1:])
                image.save(name)
