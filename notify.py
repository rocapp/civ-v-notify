#!/usr/bin/env python
# encoding: utf-8
"""
screengrab.py

Created by Alex Snet on 2011-10-10.
Copyright (c) 2011 CodeTeam. All rights reserved.
"""

import sys
import os

from PIL import Image, ImageChops


class screengrab:
    def __init__(self):
        try:
            import gtk
        except ImportError:
            pass
        else:
            self.screen = self.getScreenByGtk

        try:
            import PyQt4
        except ImportError:
            pass
        else:
            self.screen = self.getScreenByQt

    def getScreenByGtk(self):
        print("Using Gtk...")
        import gtk.gdk
        w = gtk.gdk.get_default_root_window()
        sz = w.get_size()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        if (pb == None):
            return False
        else:
            width,height = pb.get_width(),pb.get_height()
            return Image.frombytes("RGB",(width,height),pb.get_pixels() )

    def getScreenByQt(self):
        print("Using Qt...")
        from PyQt4.QtGui import QPixmap, QApplication
        from PyQt4.Qt import QBuffer, QIODevice
        import StringIO
        app = QApplication(sys.argv)
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        QPixmap.grabWindow(QApplication.desktop().winId()).save(buffer, 'png')
        strio = StringIO.StringIO()
        strio.write(buffer.data())
        buffer.close()
        del app
        strio.seek(0)
        return Image.open(strio)

def run_check():
    S = screengrab() # initialize screengrab instance
    s0 = S.screen() # take a screenshot
    while True: # continuously...
        s1 = S.screen() # take another screenshot 
        diff = ImageChops.difference(s1, s0) # compare them
        bbox = diff.getbbox()
        if bbox is not None: # if they're different,
            s0 = s1
            s0.save('imgs/turn.png') # save the new one

if __name__ == '__main__':
    run_check()