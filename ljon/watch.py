import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import ljon.build


class LjonFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, ctx):
        self.ctx = ctx

    def on_any_event(self, event):
        super().on_any_event(event)

        if not event.src_path.startswith(self.ctx.public_path):
            ljon.build(self.ctx.root)


def watch(ctx):
    event_handler = LjonFileSystemEventHandler(ctx)

    observer = Observer()

    observer.schedule(event_handler, ctx.root, recursive=True)

    print('Watching \'{}\' for changes'.format(ctx.root))

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
