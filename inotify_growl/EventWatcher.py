import pyinotify
import re
import os

class MediaWriteFilter(pyinotify.ProcessEvent):
    def process_IN_CREATE(self, event):
        print "Media Write Filter called for inotify event"
        path = event.pathname

        p = re.compile('.*untitled folder.*')
        if p.match(path):
            return

        if not os.path.isdir(path):
            end_of_dir = len(os.path.dirname(path)) + 1
            # Don't react for "dot" files
            if path[end_of_dir] == ".":
                return

        print "File created: ", event.pathname
        print "Adding to processing queue"
        MediaWriteFilter.media_queue.add_file(event.pathname)
        # MediaWriteFilter.growl_transport.sendNote(
        #     noteName = "Media Update",
        #     noteTitle = "New Media!",
        #     noteBody = "New file added: %s" % self.basename(event.pathname))

    def basename(self, path):
        if not os.path.isdir(path):
            start = len(os.path.dirname(path)) + 1
            return path[start:]
        else:
            return path
