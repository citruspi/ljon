import shutil
import os
from glob import glob
import json
import re

import ljon.processors


def build(root):
    config = {'metadata': {}, 'ignore': [], 'processors': {}}

    config_path = os.path.join(root, '.ljon/config.json')
    public_path = os.path.join(root, 'public')
    templates_path = os.path.join(root, '.ljon/templates')

    try:
        with open(config_path, 'r') as f:
            config = json.load(f, strict=False)
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

    content = []
    pathname = '*'

    while True:
        files = glob(os.path.join(root, pathname))

        if len(files) == 0:
            break

        content.extend(files)
        pathname = os.path.join(pathname, '*')

    for path in content:
        ignore = False

        for pattern in config['ignore']:
            if re.match(pattern, path):
                ignore = True
                break

        if ignore:
            continue

        if os.path.isdir(path):
            os.makedirs(os.path.join(public_path, path), exist_ok=True)
            continue

        processed = False

        for pattern in config['processors']:
            matched = re.match(pattern, path)

            if matched:
                processed = True

                if config['processors'][pattern]['processor'] == 'jinja':
                    ljon.processors.jinja(path,
                                          os.path.join(public_path,
                                                       matched.groups()[0]),
                                          root,
                                          templates_path,
                                          config)
        if not processed:
            shutil.copy(path, os.path.join(public_path, path))
