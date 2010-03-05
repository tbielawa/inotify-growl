import Queue
import time
import os

"""Something launches the initial timer. Timer sleeps for blabla
seconds. Timer runs function. Function ends by starting another timer
calling itself."""


class MediaAddedQueue:
    """The point of this is to have a queue in some globally
    addressable space which gets filled up with new files as they are
    found. To prevent a flood of Growl alerts the queue maintains a
    last_modified attribute. A timer is triggered by inotify when new
    files are added to the media share. If the queue hasn't been idle
    for long enough it will sleep and a new timer will not be blocked
    from launching until the the existing timer has exited. When the
    idle_time() returned is above a certain value the timer will call
    a function to iterate over the items in the queue and calculate
    their combined disk usage, removing each item as it is processed
    until the queue is empty. Each item removed will increment the
    last_updated value to prevent other timers from interfering."""

    def __init__(self):
        self.queue = Queue.Queue(0)
        self.last_modified = time.time()

        # Minimum seconds required without udpates for the queue to be
        # considered idle
        self.cooldown = 5

    def add_file(self, new_file):
        """Add a file to the new media queue. Record the full path,
        size in megabytes, and the time the file was added. Update the
        queue's last_modified flag if successful."""
        if not os.path.isfile(new_file):
            return
        else:
            file_size = self.file_size(new_file)
            file_add_time = time.time()
            self.queue.put([new_file, file_size, file_add_time])
            self.note_modification()

    def b2mb(self, b):
        """Convert from bytes to megabytes."""
        return (float(b)/1024.0/1024.0)

    def b2kb(self, b):
        """Convert from bytes to kilobytes."""
        return (float(b)/1024.0)

    def file_size(self, in_file):
        """Return size of a file in kilobytes."""
        size = os.stat(in_file)[6]
        return self.b2kb(size)

    def idle(self):
        """Return a boolean value indicating the idle state of the
        queue. An idle state of True indicates the queue is ready to
        be processed."""
        if (time.time() - self.last_modified > self.cooldown):
            return True
        else:
            return False

    def note_modification(self):
        self.last_modified = time.time()

    def ready(self):
        if (not self.queue.empty()) and self.idle():
            return True
        else:
            return False
