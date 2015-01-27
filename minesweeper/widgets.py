#coding=utf8


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


class CustomMapDialog(tk.Toplevel):
    
    def __init__(self, parent, modal=True, callback=None):
        tk.Toplevel.__init__(self, parent)
        self.create_widgets()
        self.parent = parent
        self.title('请输入新地图的参数')
        
        self.bind('<Return>',self.quit) #dismiss dialog
        self.bind('<Escape>',self.quit) #dismiss dialog
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
        height_label = tk.Label(frame, text='地图高度')
        height_label.grid(column=0, row=0)
        self.height_entry = tk.Entry(frame, textvariable=self.height)
        self.height_entry.grid(column=1, row=0)
        width_label = tk.Label(frame, text='地图宽度')
        width_label.grid(column=0, row=1)
        self.width_entry = tk.Entry(frame, textvariable=self.width)
        self.width_entry.grid(column=1, row=1) 
        mine_num_label = tk.Label(frame, text='地雷数目')
        mine_num_label.grid(column=0, row=2)
        self.mine_num_entry = tk.Entry(frame, textvariable=self.mine_number)
        self.mine_num_entry.grid(column=1, row=2)
        self.validate_msg = tk.StringVar()
        self.validate_entry = tk.Entry(frame, fg='#FF0000', textvariable=self.validate_msg, state=tk.DISABLED)
        self.validate_entry.grid(column=0, row=3,columnspan=2)
        self.ok_btn = tk.Button(frame, text='确定', command=self.ok)
        self.ok_btn.grid(column=0, row=4)
        self.cancel_btn = tk.Button(frame, text='取消', command=self.quit)
        self.cancel_btn.grid(column=1, row=4)
    
    def quit(self):
        self.destroy()
    
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
            print height, width, mine_number
            map_params_dict = {
                'height':height,
                'width':width,
                'mine_number': mine_number
            }
            self.destroy()
            self.callback(self.parent, map_params_dict)
    