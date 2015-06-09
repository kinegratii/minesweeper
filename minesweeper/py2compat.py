# coding=utf8

import sys

__all__ = ('range', 'reduce', 'queue', 'open', 'tkinter', 'messagebox')

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

if PY2:
    range = xrange
    reduce = reduce
    import Queue as queue
    from io import open
    import Tkinter as tkinter
    import tkMessageBox
    messagebox = tkMessageBox

else:
    range = range
    from functools import reduce
    import queue
    from io import open
    import tkinter
    from tkinter import messagebox