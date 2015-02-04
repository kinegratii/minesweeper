# coding=utf8


import Tkinter as tk


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
    def __init__(self, parent, modal=True, callback=None):
        tk.Toplevel.__init__(self, parent)
        self.create_widgets()
        self.parent = parent
        self.title('请输入新地图的参数')

        self.bind('<Return>', self.bind_quit)  # dismiss dialog
        self.bind('<Escape>', self.bind_quit)  # dismiss dialog
        self.callback = callback
        if modal:
            self.transient(parent)
            self.grab_set()
            self.wait_window()

    def create_widgets(self):
        frame = tk.Frame(self)
        frame.pack(side=tk.TOP, expand=tk.TRUE, fill=tk.BOTH)
        self.height = tk.IntVar(value=10)
        self.width = tk.IntVar(value=10)
        self.mine_number = tk.IntVar(value=10)
        self.validate_msg = tk.StringVar()

        tk.Label(frame, text='地图高度').grid(column=0, row=0)
        tk.Entry(frame, textvariable=self.height).grid(column=1, row=0)
        tk.Label(frame, text='地图宽度').grid(column=0, row=1)
        tk.Entry(frame, textvariable=self.width).grid(column=1, row=1)
        tk.Label(frame, text='地雷数目').grid(column=0, row=2)
        tk.Entry(frame, textvariable=self.mine_number).grid(column=1, row=2)
        tk.Entry(frame, fg='#FF0000', textvariable=self.validate_msg, state=tk.DISABLED).grid(column=0, row=3,
                                                                                              columnspan=2)
        tk.Button(frame, text='确定', command=self.ok).grid(column=0, row=4)
        tk.Button(frame, text='取消', command=self.quit).grid(column=1, row=4)

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
    