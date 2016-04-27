# coding=utf8
"""
由Tkinter实现的扫雷GUI
"""
from __future__ import unicode_literals
import webbrowser

try:
    import tkinter as tk
except ImportError:
    import Tkinter as tk
try:
    from tkinter import messagebox
except ImportError:
    import tkMessageBox as messagebox

from core import Game
from helpers import GameHelpers
from helpers import level_config
import widgets
import static


class App(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.master.title(static.APP_NAME)
        self.master.resizable(False, False)
        self.master.iconbitmap(static.images('mine.ico'))
        self.pack(expand=tk.NO, fill=tk.BOTH)
        self.map_frame = None
        mine_map = level_config.map('primary')
        self._create_map_frame(mine_map)
        self.create_top_menu()

    def create_top_menu(self):
        top = self.winfo_toplevel()
        menu_bar = tk.Menu(top)
        top['menu'] = menu_bar

        game_menu = tk.Menu(menu_bar)
        game_menu.add_command(label='开始', command=self.map_frame.start)
        game_menu.add_command(label='重置', command=self.map_frame.reset)
        game_menu.add_separator()
        game_menu.add_command(label='退出', command=self.exit_app)
        menu_bar.add_cascade(label='游戏', menu=game_menu)

        map_menu = tk.Menu(menu_bar)
        self.level = tk.StringVar()
        self.level.set('primary')
        for level, label in level_config.choices:
            map_menu.add_radiobutton(label=label,
                                     variable=self.level,
                                     value=level,
                                     command=self.select_map_level)
        map_menu.add_separator()
        map_menu.add_command(label='自定义...', command=self.create_custom_map)
        menu_bar.add_cascade(label='地图', menu=map_menu)

        about_menu = tk.Menu(menu_bar)
        about_menu.add_command(label='主页', command=lambda: webbrowser.open_new_tab(static.HOME_URL))
        about_menu.add_command(label='关于...', command=self.show_about_info)
        menu_bar.add_cascade(label='关于', menu=about_menu)

    def select_map_level(self):
        level = self.level.get()
        mine_map = level_config.map(level)
        self._create_map_frame(mine_map)

    def _create_map_frame(self, mine_map):
        if self.map_frame:
            self.map_frame.pack_forget()
        self.map_frame = GameFrame(mine_map)
        self.map_frame.pack(side=tk.TOP)

    def create_custom_map(self):
        params = {
            'width': self.map_frame.game.width,
            'height': self.map_frame.game.height,
            'mine_number': self.map_frame.game.mine_number
        }
        return widgets.MapParamsInputDialog(self, callback=App.get_map_params, initial=params)

    def get_map_params(self, params_dict):
        new_map = GameHelpers.create_from_mine_number(**params_dict)
        self._create_map_frame(new_map)

    def exit_app(self):
        self.quit()

    def show_about_info(self):
        widgets.view_file(self, '关于', static.static_file('project.txt'))


class GameFrame(tk.Frame):
    def __init__(self, mine_map):
        tk.Frame.__init__(self)
        self._create_controller_frame()
        self.map_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
        self.map_frame.pack(side=tk.TOP, expand=tk.YES, padx=10, pady=10)
        self.game = Game(mine_map)
        height, width = mine_map.height, mine_map.width
        self.bt_map = [[None for _ in range(0, width)] for _ in range(0, height)]
        for x in range(0, height):
            for y in range(0, width):
                self.bt_map[x][y] = tk.Button(self.map_frame, text='', width=3, height=1,
                                              command=lambda px=x, py=y: self.sweep_mine(px, py))
                self.bt_map[x][y].config(static.style('grid.unknown'))

                def _mark_mine(event, self=self, x=x, y=y):
                    return self.mark_grid_as_mine(event, x, y)

                self.bt_map[x][y].bind('<Button-3>', _mark_mine)
                self.bt_map[x][y].grid(row=x, column=y)
        self._create_info_frame()

    def _create_controller_frame(self):
        self.controller_bar = tk.LabelFrame(self, text='控制', padx=5, pady=5)
        self.controller_bar.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=10, pady=2)
        self.start_bt = tk.Button(self.controller_bar, text='开始', relief=tk.GROOVE, command=self.start)
        self.start_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.reset_bt = tk.Button(self.controller_bar, text='重置', relief=tk.GROOVE, command=self.reset)
        self.reset_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)
        self.map_info_bt = tk.Button(self.controller_bar, text='查看', relief=tk.GROOVE, command=self._show_map_info)
        self.map_info_bt.pack(side=tk.LEFT, expand=tk.NO, padx=4)

    def _show_map_info(self):
        map_info_str = '当前地图大小：%d X %d\n地雷数目：%d' % (self.game.height, self.game.width, self.game.mine_number)
        messagebox.showinfo('当前地图', map_info_str, parent=self)

    def _create_info_frame(self):
        self.info_frame = tk.Frame(self, relief=tk.GROOVE, borderwidth=2)
        self.info_frame.pack(side=tk.TOP, fill=tk.X, expand=tk.YES, padx=10, pady=5)
        self.step_text_label = tk.Label(self.info_frame, text='步数')
        self.step_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.step_count_label = widgets.CounterLabel(self.info_frame, init_value=0, step=1)
        self.step_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.timer_text_label = tk.Label(self.info_frame, text='时间')
        self.timer_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.timer_count_label = widgets.TimerLabel(self.info_frame)
        self.timer_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.flag_text_label = tk.Label(self.info_frame, text='标记')
        self.flag_text_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.flag_count_label = widgets.CounterLabel(self.info_frame, init_value=0, step=1)
        self.flag_count_label.pack(side=tk.LEFT, fill=tk.X, expand=tk.NO)
        self.msg_label = widgets.MessageLabel(self.info_frame)
        self.msg_label.pack(side=tk.RIGHT)

    def start(self):
        mine_map = GameHelpers.create_from_mine_number(self.game.height, self.game.width, self.game.mine_number)
        self.game = Game(mine_map)
        self._draw_map()
        self.step_count_label.set_counter_value()
        self.flag_count_label.set_counter_value()
        self.timer_count_label.reset()
        self.msg_label.splash('新游戏已就绪')

    def reset(self):
        self.game.reset()
        self._draw_map()
        self.step_count_label.set_counter_value()
        self.flag_count_label.set_counter_value()
        self.timer_count_label.reset()
        self.msg_label.splash('游戏已经重置')

    def sweep_mine(self, x, y):
        if self.game.swept_state_map[x][y]:
            return
        if not self.timer_count_label.state:
            self.timer_count_label.start_timer()
        state = self.game.play((x, y))
        self.step_count_label.set_counter_value(str(self.game.cur_step))
        self._draw_map()
        if state == Game.STATE_SUCCESS:
            self.timer_count_label.stop_timer()
            self.msg_label.splash('恭喜你，游戏通关了')
            messagebox.showinfo('提示', '恭喜你通关了！', parent=self)
        elif state == Game.STATE_FAIL:
            self.timer_count_label.stop_timer()
            self.msg_label.splash('很遗憾，游戏失败')
            messagebox.showerror('提示', '很遗憾，游戏失败！', parent=self)

    def mark_grid_as_mine(self, event, x, y):
        if self.game.state == Game.STATE_PLAY and not self.game.swept_state_map[x][y]:
            cur_text = self.bt_map[x][y]['text']
            if cur_text == '?':
                cur_text = ''
                self.flag_count_label.decrease()
            elif cur_text == '':
                cur_text = '?'
                self.flag_count_label.increase()
            self.bt_map[x][y]['text'] = cur_text

    def _draw_map(self):
        # 重画地图
        for i in range(0, self.game.height):
            for j in range(0, self.game.width):
                if self.game.swept_state_map[i][j]:
                    if self.game.mine_map.is_mine((i, j)):
                        self.bt_map[i][j].config(static.style('grid.mine'))
                    else:
                        tmp = self.game.mine_map.distribute_map[i][j]
                        self.bt_map[i][j].config(static.style('grid.swept', num=tmp))
                else:
                    if self.bt_map[i][j]['text'] == '?':
                        self.bt_map[i][j].config(static.style('grid.marked'))
                    else:
                        self.bt_map[i][j].config(static.style('grid.unknown'))


def main():
    app = App()
    app.mainloop()


if __name__ == '__main__':
    main()
