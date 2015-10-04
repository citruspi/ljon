import shutil
import os
from glob import glob
import re

import ljon.processors


def build(ctx):
    if not os.path.isdir(ctx.public_path):
        os.makedirs(ctx.public_path)

    for the_file in os.listdir(ctx.public_path):
        file_path = os.path.join(ctx.public_path, the_file)
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
        files = glob(os.path.join(ctx.root, pathname))

        if len(files) == 0:
            break

        content.extend(files)
        pathname = os.path.join(pathname, '*')

    for path in content:
        ignore = False

        for pattern in ctx.config['ignore']:
            if re.match(pattern, path):
                ignore = True
                break

        if ignore:
            continue

        if os.path.isdir(path):
            os.makedirs(os.path.join(ctx.public_path, path), exist_ok=True)
            continue

        processed = False

        for pattern in ctx.config['processors']:
            matched = re.match(pattern, path)

            if matched:
                processed = True

                if ctx.config['processors'][pattern]['processor'] == 'jinja':
                    ljon.processors.jinja(path,
                                          os.path.join(ctx.public_path,
                                                       matched.groups()[0]),
                                          ctx.root,
                                          ctx.templates_path,
                                          ctx.config)
                if ctx.config['processors'][pattern]['processor'] == 'shell':
                    command = ctx.config['processors'][pattern]['command']

                    ljon.processors.shell(command, path, ctx.root,
                                          ctx.public_path, ctx.templates_path,
                                          ctx.config)
        if not processed:
            shutil.copy(path, os.path.join(ctx.public_path, path))
