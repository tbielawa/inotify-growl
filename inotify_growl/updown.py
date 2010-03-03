import os
import sys
import signal

pid_file = '/tmp/inotify-growl.pid'
RUNNING = int(1)
STOPPED = int(0)
from inotify_growl import QueueHandler

def start():
    #logger.info()
    print "Starting inotify-growl"
    print lol
    # is it running?
    # don't run, print PID

def status():
    if runningpid() == STOPPED:
        return STOPPED
    else:
        return RUNNING

def runningpid():
    if os.path.isfile(pid_file):
        return int(open(pid_file).read().strip())
    else:
        return STOPPED

def stop(one, two):
    QueueHandler.QueueHandler.running = False
    
    growl_transport.sendNote(
        noteName = "Monitor Status",
        noteTitle = "inotify-growl offline",
        noteBody = "inotify-growl for The Media Sharepoint is going offline!")
    growl_transport.stop()

    watch_notifier.stop()

def stoprunning():
    if status() == RUNNING:
        pid = runningpid()
        print "Stopping inotify-growl"
        os.kill(pid, signal.SIGTERM)

    else:
        print "inotify-growl is not running"
        sys.exit()
