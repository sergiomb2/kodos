# -*- coding: utf-8 -*-
#  util.py: -*- Python -*-  DESCRIPTIVE TEXT.

import os
import os.path
import sys
import logging
import webbrowser

from PyQt4.QtGui import *
from PyQt4.QtCore import *

log = logging.getLogger('kodos.util')

# QT constants that should be defined
FALSE = 0
TRUE = 1

def getAppPath():
    "Convenience function so that we can find the necessary images"
    fullpath = os.path.abspath(os.path.join(sys.argv[0], '..'))
    path = os.path.dirname(fullpath)
    return path


def getPixmap(fileStr, fileType="PNG", dir="images"):
    """Return a QPixmap instance for the file fileStr relative
    to the binary location and residing in it's 'images' subdirectory"""

    image = getAppPath() + os.sep + dir + os.sep + fileStr
    pixmap = QPixmap(image, fileType)
    pixmap.setMask(pixmap.createHeuristicMask(1))

    return pixmap

def kodos_toolbar_logo(toolbar):
    # hack to move logo to right
    blanklabel = QLabel()
    blanklabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

    logolabel = QLabel("kodos_logo")
    logolabel.setPixmap(QPixmap(":/images/kodos_icon.png"))

    toolbar.addWidget(blanklabel)
    toolbar.addWidget(logolabel)

    return logolabel

def saveWindowSettings(window, filename):
    settings = QSettings()
    settings.setValue(window.objectName(), window.saveGeometry())

def restoreWindowSettings(window, filename):
    settings = QSettings()
    window.restoreGeometry(settings.value(window.objectName()).toByteArray())

def findFile(filename):
    dirs = [getAppPath(),
            os.path.join("/", "usr", "share", "kodos"),
            os.path.join("/", "usr", "local", "kodos")]

    for d in dirs:
        path = os.path.join(d, filename)
        if os.access(path, os.R_OK): return path

    return None

def launch_browser(url, caption=None, message=None):
    if not caption: caption = "Info"
    if not message: message = "Launch web browser?"

    button = QMessageBox.information(None, caption, message, QMessageBox.Ok | QMessageBox.Cancel)
    if button == QMessageBox.Cancel:
        return False
    try:
        webbrowser.open(url)
    except webbrowser.Error, e:
        log.error("Couldn't open URL %r: %s" % (url, e))
        return False
    return True
