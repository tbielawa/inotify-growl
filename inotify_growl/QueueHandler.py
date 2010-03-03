import threading
import Queue
import time

class QueueHandler(threading.Thread):
    # Though timers aren't exact, it may be best to set this and
    # the cooldown on the queue to <> prime numbers
    def run(self):
        self.msg = QueueHandler.growl_transport.sendStatus
        self.msg("Launched Queue Handler")
        while QueueHandler.running:
            print "Entered the reducer"
            #self.msg("In the Queue Handler")
            if QueueHandler.media_queue.ready():
                #self.msg("Queue marked as ready, reducing")
                print "Queue ready, reducing"
                self.reduce()
                print "Reduced"
            print "Going to sleep again"
            time.sleep(5)
                
    def reduce(self):
        filesadded = 0
        sizeincreased = 0
        self.msg("Entered the reducer")
        try:
            while True:
                media = QueueHandler.media_queue.queue.get(block=False)
                #                QueueHandler.media_queue.note_modification()
                #self.msg("Processing %s" % media[0])
                filesadded += 1
                sizeincreased += media[1]
        except Queue.Empty:
            #self.msg("Reached end of queue")
            pass

        #self.msg("Generating status message")
        reportmessage = "%d new files totaling %2.2f MB have been added"\
            "to the media share!" % (filesadded, sizeincreased)
        #self.msg("Sending report")
        QueueHandler.growl_transport.sendNote(
            noteName = "Media Update",
            noteTitle = "New files added",
            noteBody = reportmessage)
