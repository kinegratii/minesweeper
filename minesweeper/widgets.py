#coding=utf8
"""
This module contains some custom widget using in tkinter app.
@author:kinegratii(kinegratii@yeah.net)
"""
try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk

class CounterLabel(tk.Label):
    """A Label showing a integer.Change its value by calling functions.
    """
    def __init__(self, parent, init_value=0, step=1, **kw):
        tk.Label.__init__(self, parent, text=str(init_value), **kw)
        self._count_value = init_value
        self._step = step
    
    def inscrease(self, step=None):
        step = step or self._step
        self._count_value += step
        self.config({'text': str(self._count_value)})
    
    def descrease(self, step=None):
        step = step or self._step
        self._count_value -= step
        self.config({'text':str(self._count_value)})
    
    def set_counter_value(self, value=0):
        self._count_value = value
        self.config({'text':str(self._count_value)})
    
    @property
    def count_value(self):
        return self._count_value

class TimerLabel(CounterLabel):
    """A Counter label using timer.In tkinter you can use widget.after callback function to timer event,
    which is like setInterval function in Javascript.
    """
    def __init__(self, parent, **kw):
        CounterLabel.__init__(self, parent, **kw)
        self._state = False
        self._timer_id = None
    
    def _timer(self):
        if self._state:
            self.inscrease()
            self._timer_id = self.after(1000, self._timer)
            
    def start_timer(self):
        if not self._state:
            self._state = True
            self._timer()
    
    def stop_timer(self):
        self._state = False
        if self._timer_id:
            self.after_cancel(self._timer_id)
            self._timer_id = None
    
    def reset(self):
        self.stop_timer()
        self.set_counter_value()
    
    @property
    def state(self):
        return self._state
