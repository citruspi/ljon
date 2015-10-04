import time

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import ljon.build


class LjonFileSystemEventHandler(FileSystemEventHandler):
    def __init__(self, root, public_path):
        self.root = root
        self.public_path = public_path

    def on_any_event(self, event):
        super().on_any_event(event)

        if not event.src_path.startswith(self.public_path):
            ljon.build(self.root)


def watch(root, public_path):
    event_handler = LjonFileSystemEventHandler(root, public_path)

    observer = Observer()

    observer.schedule(event_handler, root, recursive=True)

    print('Watching \'{}\' for changes'.format(root))

    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
