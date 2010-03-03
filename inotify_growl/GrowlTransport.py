from socket import AF_INET, SOCK_DGRAM, socket
import netgrowl
import sys

class myGrowl:
    def __init__(self, app="media-watch", password="media"):
        self.password = password
        self.app = app
        self.remoteGrowls = []
        self.notes = []
        self.socket = self._growlSocket()
        self.registrationPacket = netgrowl.GrowlRegistrationPacket(
            password = self.password,
            application = self.app)

    def _growlSocket(self):
        """Give a working socket."""
        return socket(AF_INET, SOCK_DGRAM)

    def _rGrowl(self, ipHostNumber):
        """IP address to to a remote Growl daemon and the defined
        Growl UDP port"""
        return (ipHostNumber, netgrowl.GROWL_UDP_PORT)

    def register(self):
        """Send our notification list to each registered Growl"""
        print "Registering with:"
        for rg in self.remoteGrowls:
            print rg
            self.socket.sendto(self.registrationPacket.payload(), rg)

    def addRemoteGrowl(self, ipHostNumber):
        """Register a remote Growl daemon running on the
        GROWL_UDP_PORT"""
        remoteGrowl = self._rGrowl(ipHostNumber)
        self.remoteGrowls.append(remoteGrowl)
        
    def addNote(self, noteName, noteEnabled=True):
        """Add a notification to the list that will be sent to remote
        Growl daemons. Defining a notification multiple times is
        acceptable."""
        self.registrationPacket.addNotification(
            notification = noteName, enabled = noteEnabled)
        self.notes.append(noteName)

    def sendNote(self, noteName, noteTitle, noteBody):
        """Send a notification to all registered Growl daemons."""
        if not noteName in self.notes:
            print "There is no notification registered with that name."
            print self.notes
        else:
            print "Sending note to: "
            for rg in self.remoteGrowls:
                print rg
                # Assemble our payload
                note = netgrowl.GrowlNotificationPacket(
                    application = self.app,
                    notification = noteName,
                    title = noteTitle,
                    description = noteBody,
                    password = self.password)
                
                self.socket.sendto(note.payload(), rg)
                print "Note sent"

    def sendStatus(self, message):
        self.sendNote(noteName = "Monitor Status",
                      noteTitle = "Status Update",
                      noteBody = message)

    def stop(self):
        self.socket.close()
