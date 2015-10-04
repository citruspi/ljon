from jinja2 import Environment, FileSystemLoader
import json


def jinja(path, intended_path, root, templates_path, config):
    j2 = Environment(loader=FileSystemLoader([root, templates_path]))

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
