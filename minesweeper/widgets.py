# coding=utf8

from __future__ import unicode_literals

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    from tkinter import messagebox
except ImportError:
    import tkMessageBox as messagebox
from io import open


class CounterLabel(tk.Label):
    """可计数的标签
    """

    def __init__(self, parent, init_value=0, step=1, **kwargs):
        self._count_value = tk.IntVar()
        self._count_value.set(init_value)
        tk.Label.__init__(self, parent, textvariable=self._count_value, **kwargs)
        self._step = step

    def increase(self, step=None):
        step = step or self._step
        self._count_value.set(self._count_value.get() + step)

    def decrease(self, step=None):
        step = step or self._step
        self._count_value.set(self._count_value.get() - step)

    def set_counter_value(self, value=0):
        self._count_value.set(value)

    @property
    def count_value(self):
        return self._count_value.get()


class TimerLabel(CounterLabel):
    """可自动计数的标签控件，默认一秒一次
    """

    def __init__(self, parent, **kwargs):
        CounterLabel.__init__(self, parent, **kwargs)
        self._state = False
        self._timer_id = None

    def _timer(self):
        if self._state:
            self.increase()
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


class MapParamsInputDialog(tk.Toplevel):
    def __init__(self, parent, modal=True, callback=None, initial=None):
        tk.Toplevel.__init__(self, parent)
        initial = initial or {'width': 10, 'height': 10, 'mine_number': 10}
        self.height = tk.IntVar(value=initial['height'])
        self.width = tk.IntVar(value=initial['width'])
        self.mine_number = tk.IntVar(value=initial['mine_number'])
        self.validate_msg = tk.StringVar()

        self.create_widgets()
        self.parent = parent
        self.title('请输入新地图的参数')

        self.bind('<Return>', self.bind_quit)  # dismiss dialog
        self.bind('<Escape>', self.bind_quit)  # dismiss dialog
        self.callback = callback

        if modal:
            self.geometry("=%dx%d+%d+%d" % (200, 130, parent.winfo_rootx() + 10, parent.winfo_rooty() + 10))
            self.transient(parent)
            self.grab_set()
            self.wait_window()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        tk.Label(frame, text='地图高度').grid(column=0, row=0)
        tk.Entry(frame, textvariable=self.height).grid(column=1, row=0)
        tk.Label(frame, text='地图宽度').grid(column=0, row=1)
        tk.Entry(frame, textvariable=self.width).grid(column=1, row=1)
        tk.Label(frame, text='地雷数目').grid(column=0, row=2)
        tk.Entry(frame, textvariable=self.mine_number).grid(column=1, row=2)
        tk.Entry(frame, fg='#FF0000', textvariable=self.validate_msg, state=tk.DISABLED).grid(column=0, row=3,
                                                                                              columnspan=2)
        tk.Button(frame, text='确定', command=self.ok).grid(column=0, row=4, ipadx=10)
        tk.Button(frame, text='取消', command=self.quit).grid(column=1, row=4, ipadx=10)

    def quit(self):
        self.destroy()

    def bind_quit(self, event):
        self.quit()

    def ok(self):

        if self.callback:
            try:
                height, width, mine_number = int(self.height.get()), int(self.width.get()), int(self.mine_number.get())
            except ValueError:
                self.validate_msg.set('请输入整数！')
                return
            if height < 3 or width < 3:
                self.validate_msg.set('地图长度必须大于等于3！')
                return
            if mine_number < 0 or height * width <= mine_number:
                self.validate_msg.set('地图数目范围不正确！')
                return
            self.validate_msg.set('')
            map_params_dict = {
                'height': height,
                'width': width,
                'mine_number': mine_number
            }
            self.destroy()
            self.callback(self.parent, map_params_dict)


class MessageLabel(tk.Label):
    def splash(self, text):
        self.config({'text': text})
        self.after(700, self._clear)

    def _clear(self):
        self.config({'text': ''})


class TextViewer(tk.Toplevel):
    def __init__(self, parent, title, text, modal=True):
        tk.Toplevel.__init__(self, parent)
        self.configure(borderwidth=5)
        self.geometry("=%dx%d+%d+%d" % (625, 500, parent.winfo_rootx() + 10, parent.winfo_rooty() + 10))
        self.bg = '#ffffff'
        self.fg = '#000000'
        self.title(title)
        self.protocol("WM_DELETE_WINDOW", self.ok)
        self.parent = parent
        self.bind('<Return>', self.ok)
        self.bind('<Escape>', self.ok)
        # create widgets
        frame_text = tk.Frame(self, relief=tk.SUNKEN, height=700)
        frame_text.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)

        scroll_view = tk.Scrollbar(frame_text, orient=tk.VERTICAL, takefocus=tk.FALSE, highlightthickness=0)
        self.text_view = tk.Text(frame_text, wrap=tk.WORD, highlightthickness=0, fg=self.fg, bg=self.bg)
        scroll_view.config(command=self.text_view.yview)
        self.text_view.config(yscrollcommand=scroll_view.set)
        scroll_view.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_view.pack(side=tk.LEFT, expand=tk.TRUE, fill=tk.BOTH)

        frame_buttons = tk.Frame(self)
        tk.Button(frame_buttons, text='确定', command=self.ok, takefocus=tk.FALSE).pack()
        frame_buttons.pack(side=tk.BOTTOM, fill=tk.X)

        # init text
        self.text_view.focus_set()
        self.text_view.insert(0.0, text)
        self.text_view.config(state=tk.DISABLED)

        if modal:
            self.transient(parent)
            self.grab_set()
            self.wait_window()

    def ok(self, event=None):
        self.destroy()


def view_file(parent, title, filename, modal=True):
    try:
        text_file = open(filename, 'r', encoding='utf-8')
    except IOError:
        messagebox.showerror(title='File Load Error', message='Unable to load file %r .' % filename, parent=parent)
    else:
        return TextViewer(parent, title, text_file.read(), modal)

