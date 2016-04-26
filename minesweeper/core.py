# coding=utf8
"""
@author:kinegratii(kinegratii@yeah.net)
@Version:1.0.1
Update on 2014.05.04
"""
from __future__ import unicode_literals

try:
    import queue
except ImportError:
    import Queue as queue


class Map(object):
    # the mine flag in distribute map
    MINE_FLAG = -1

    def __init__(self, height, width, mine_pos_list):
        self._height = height
        self._width = width
        self._mine_number = 0
        self._mine_list = list(set(mine_pos_list))
        self._generate_distribute_map()

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def map_size(self):
        return self._height * self._width

    @property
    def mine_list(self):
        return self._mine_list

    @property
    def mine_number(self):
        return len(self._mine_list)

    @property
    def distribute_map(self):
        return self._distribute_map


    # Some base functions.Use self.height instead of self._height etc.

    def _generate_distribute_map(self):
        self._distribute_map = [[0 for _ in range(0, self.width)] for _ in range(0, self.height)]
        offset_step = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for t_x, t_y in self.mine_list:
            self._distribute_map[t_x][t_y] = Map.MINE_FLAG
            for o_x, o_y in offset_step:
                d_x, d_y = t_x + o_x, t_y + o_y
                if self.is_in_map((d_x, d_y)) and self._distribute_map[d_x][d_y] != Map.MINE_FLAG:
                        self._distribute_map[d_x][d_y] += 1

    def is_in_map(self, pos, offset=None):
        if offset:
            x, y = pos[0] + offset[0], pos[1] + offset[1]
        else:
            x, y = pos
        return x in range(0, self.height) and y in range(0, self.width)

    def is_mine(self, pos):
        return pos in self.mine_list

    def get_near_mine_number(self, pos):
        x, y = pos
        return self._distribute_map[x][y]


class Game(object):
    STATE_PLAY = 1
    STATE_SUCCESS = 2
    STATE_FAIL = 3

    def __init__(self, mine_map):
        self._mine_map = mine_map
        self._init_game()

    def _init_game(self):
        self._swept_state_map = [[False for _ in range(0, self._mine_map.width)] for _ in
                                 range(0, self._mine_map.height)]
        self._not_swept_number = self._mine_map.map_size
        self._cur_step = 0
        self._sweep_trace = []
        self._state = Game.STATE_PLAY

    def reset(self):
        self._init_game()


    @property
    def cur_step(self):
        return self._cur_step

    @property
    def sweep_trace(self):
        return self._sweep_trace

    @property
    def state(self):
        return self._state

    @property
    def not_swept_number(self):
        return self._not_swept_number

    @property
    def swept_state_map(self):
        return self._swept_state_map

    @property
    def height(self):
        return self._mine_map.height

    @property
    def width(self):
        return self._mine_map.width

    @property
    def mine_number(self):
        return self._mine_map.mine_number

    @property
    def mine_map(self):
        return self._mine_map

    def _sweep(self, click_pos):
        if self._state == Game.STATE_SUCCESS or self._state == Game.STATE_FAIL:
            # success or fail is the end state of game.
            return self._state
        self._cur_step += 1
        self._sweep_trace.append(click_pos)
        cx, cy = click_pos
        if self._swept_state_map[cx][cy]:
            # click the position has been clicked,pass
            self._state = Game.STATE_PLAY
            return self._state

        near_mine_number = self._mine_map.get_near_mine_number(click_pos)

        if near_mine_number == Map.MINE_FLAG:
            # click the mine,game over.
            self._not_swept_number -= 1
            self._swept_state_map[cx][cy] = True
            return Game.STATE_FAIL
        elif near_mine_number > 0:
            self._not_swept_number -= 1
            self._swept_state_map[cx][cy] = True
            if self._not_swept_number == self._mine_map.mine_number:
                self._state = Game.STATE_SUCCESS
            else:
                self._state = Game.STATE_PLAY
            return self._state
        else:
            scan_step = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            assert near_mine_number == 0
            q = queue.Queue()
            q.put(click_pos)
            self._not_swept_number -= 1
            self._swept_state_map[cx][cy] = True
            while not q.empty():
                c_x, c_y = q.get()
                for o_x, o_y in scan_step:
                    d_x, d_y = c_x + o_x, c_y + o_y
                    if self._mine_map.is_in_map((d_x, d_y)) and not self._swept_state_map[d_x][d_y]:
                        near_mine_number = self._mine_map.get_near_mine_number((d_x, d_y))
                        if near_mine_number == Map.MINE_FLAG:
                            pass
                        elif near_mine_number == 0:
                            q.put((d_x, d_y))
                            self._swept_state_map[d_x][d_y] = True
                            self._not_swept_number -= 1
                        else:
                            self._swept_state_map[d_x][d_y] = True
                            self._not_swept_number -= 1
            assert self._not_swept_number >= self._mine_map.mine_number
            if self._not_swept_number == self._mine_map.mine_number:
                self._state = Game.STATE_SUCCESS
            else:
                self._state = Game.STATE_PLAY
            return self._state

    def play(self, click_pos):
        state = self._sweep(click_pos)
        if state == Game.STATE_SUCCESS or state == Game.STATE_FAIL:
            self._sweep_all_map()
        return state

    def _sweep_all_map(self):
        self._swept_state_map = [[True for _ in range(0, self.width)] for _ in range(0, self.height)]
        self._not_swept_number = self.mine_map.map_size - self.mine_map.mine_number
