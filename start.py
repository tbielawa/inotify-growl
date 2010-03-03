#!/usr/bin/env python
import pyinotify
import signal
from inotify_growl import MediaAddedQueue, GrowlTransport, EventWatcher, updown, QueueHandler
import sys
import threading
import functools
import os
import logging

__application__ = "inotify-growl"

args = sys.argv

if not len(args) >= 2:
    print "[-d] [start | stop | status]"
    sys.exit()

start = False
daemonize = False
for arg in args:
    if arg in ["--help", "-h", "help", "-help"]:
        print "[-d] [start | stop | status]"
        sys.exit()

    if arg == "stop":
        updown.stoprunning()
        sys.exit()

    if arg == "-d":
        daemonize = True
        continue

    if arg == "status":
        if updown.status() == updown.RUNNING:
            print "%s is running (%s)" % (__application__, updown.runningpid())
        else:
            print "%s is not running" % __application__
        sys.exit()

    if arg == "start":
        start = True

if not start:
    sys.exit()

print "Starting inotify-growl"

# Some constants
media_path = '/mnt/raid/Media/'
growl_app_name = "\"Media Sharepoint\""
remote_growls = ["192.168.1.11"]
growl_notes = ["Monitor Status", "Media Update"]

print "Creating the New-Media Queue."
media_queue = MediaAddedQueue.MediaAddedQueue()
EventWatcher.MediaWriteFilter.media_queue = media_queue

print "Starting and registering the Growl transport."
growl_transport = GrowlTransport.myGrowl(app=growl_app_name)
EventWatcher.MediaWriteFilter.growl_transport = growl_transport
    
for remote in remote_growls:
    growl_transport.addRemoteGrowl(remote)

for growl_note in growl_notes:
    growl_transport.addNote(growl_note)

growl_transport.register()
growl_transport.sendNote(
    noteName = "Monitor Status",
    noteTitle = "inotify-growl online",
    noteBody = "inotify-growl for " + growl_app_name + " is coming online!")

print "Starting the inotify watcher."

media_filter = EventWatcher.MediaWriteFilter()
updown.media_filter = media_filter
watch_manager = pyinotify.WatchManager()
watch_directory = watch_manager.add_watch(media_path, pyinotify.IN_CREATE, rec=True, auto_add=True)
watch_notifier = pyinotify.Notifier(watch_manager, default_proc_fun=media_filter)

updown.growl_transport = growl_transport
updown.watch_notifier = watch_notifier
signal.signal(signal.SIGTERM, updown.stop)

QueueHandler.QueueHandler.media_queue = media_queue
QueueHandler.QueueHandler.growl_transport = growl_transport
QueueHandler.QueueHandler.running = True

qh = QueueHandler.QueueHandler()
qh.start()

watch_notifier.loop(daemonize=daemonize, force_kill=True,
                    pid_file=updown.pid_file,
                    stderr='/tmp/stderr.txt',
                    stdout='/tmp/stdout.txt')
