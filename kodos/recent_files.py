# -*- coding: utf-8 -*-

import logging

from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QSettings

MAX_SIZE = 50 # max number of files to retain

class RecentFiles:
    def __init__(self, parent, numShown=5):
        self.log = logging.getLogger('kodos.recent_files')
        self.parent = parent
        self.numShown = int(numShown)
        self.__recent_files = []
        self.__indecies = []
        self.load()

    def load(self):
        settings = QSettings()
        cnt = settings.beginReadArray("RecentFiles")
        # PyQt bug: cnt is always 0, workaround with "None" test below
        i = -1
        while True:
            i += 1
            settings.setArrayIndex(i)
            try:
                s = settings.value("Filename")
                if s == None:
                    break
                self.__recent_files.append(str(s))
            except Exception as e:
                self.log.error('Loading of recent file entry %i failed: %s' %
                               (i, e))
                settings.remove("Filename")

        settings.endArray()

        self.log.debug("recent_files: %s" % self.__recent_files)

        self.addToMenu()

    def save(self):
        # truncate list if necessary
        self.__recent_files = self.__recent_files[:MAX_SIZE]
        s = QSettings()
        s.beginWriteArray("RecentFiles")
        cnt = 0
        for f in self.__recent_files:
            s.setArrayIndex(cnt)
            s.setValue("Filename", f)
            cnt += 1
        s.sync()

    def add(self, filename):
        try:
            self.__recent_files.remove(filename)
        except:
            pass

        self.__recent_files.insert(0, filename)
        self.save()
        self.addToMenu()


    def clearMenu(self):
        # clear each menu entry...
        for idx in self.__indecies:
            self.parent.fileMenu.removeAction(idx)

        # clear list of menu entry indecies
        self.__indecies = []


    def addToMenu(self, clear=1):
        if clear: self.clearMenu()

        # add applicable items to menu
        num = min(self.numShown, len(self.__recent_files))
        for i in range(num):
            filename = self.__recent_files[i]
            idx = self.parent.fileMenu.addAction(
                QIcon(QPixmap(":images/document-open-recent.png")),
                filename)

            self.__indecies.insert(0, idx)


    def setNumShown(self, numShown):
        ns = int(numShown)
        if ns == self.numShown: return

        # clear menu of size X then add entries of size Y
        self.clearMenu()
        self.numShown = ns
        self.addToMenu(0)


    def isRecentFile(self, menuid):
        return menuid in self.__indecies

