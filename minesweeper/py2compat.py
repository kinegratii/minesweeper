# coding=utf8

import sys

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    range = xrange
    import Queue as queue
    from io import open
    import Tkinter as tkinter
    import tkMessageBox
    tkinter.messagebox = tkMessageBox