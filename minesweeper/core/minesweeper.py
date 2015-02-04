# coding=utf8
"""
@author:kinegratii(kinegratii@yeah.net)
@Version:1.0.1
Update on 2014.05.04
"""
import random
import Queue


class MapCreateError(Exception):
    """ 创建过程中出现的异常.
    """
    INVALID_HEIGHT_OR_WIDTH = 'invalid height or width'
    MINE_INDEX_INVALID = 'invalid mine index'
    MINE_INVALID_POS = 'invalid mine position'
    MINE_INVALID_NUMBER = 'invalid mine number'

    def __init__(self, message):
        super(MapCreateError, self).__init__(message)


class Map(object):
    """一个描述地图的数据类，这是个只读类，在创建实例后就无法修改其上的任何属性
     Attributes:
        height: 整数，地图高度
        width:整数，地图宽度.
        map_size:整数，地图大小。
        mine_list:列表，地雷位置列表每个元素都是(x,y)的元组，表示该位置是地雷
        mine_number:：整数，地雷总数
        distribute_map:二维数组，附近地雷分布图，（x,y）的值表示该位置附近8个单元格中的地雷个数，如果本上
    """
    # the mine flag in distribute map
    MINE_FLAG = -1

    def __init__(self, height, width, mine_pos_list):
        """根据地图大小和地雷的位置创建地图
        @param height: 高度
        @param width: 宽度
        @param mine_pos_list:地雷位置
        """
        self._height = height
        self._width = width
        self._mine_number = 0
        self._mine_list = ()
        pos_set = set(mine_pos_list)
        for pos in pos_set:
            if not self.is_in_map(pos):
                raise MapCreateError(MapCreateError.MINE_INVALID_POS)
        self._mine_list = tuple(pos_set)
        self._mine_number = len(pos_set)
        self._generate_distribute_map()

    @property
    def height(self):
        """地雷高度
        """
        return self._height

    @property
    def width(self):
        """地图宽度
        """
        return self._width

    @property
    def map_size(self):
        """地图大小
        """
        return self._height * self._width

    @property
    def mine_list(self):
        """地雷位置列表
        """
        return self._mine_list

    @property
    def mine_number(self):
        """地雷个数
        """
        return self._mine_number

    @property
    def distribute_map(self):
        """地雷分布图
        """
        return self._distribute_map


    # Some base functions.Use self.height instead of self._height etc.

    def _generate_distribute_map(self):
        """生成地雷分布图
        """
        self._distribute_map = [[0 for i in xrange(0, self.width)] for i in xrange(0, self.height)]
        offset_step = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        for t_x, t_y in self.mine_list:
            self._distribute_map[t_x][t_y] = Map.MINE_FLAG
            for o_x, o_y in offset_step:
                d_x, d_y = t_x + o_x, t_y + o_y
                if self.is_in_map((d_x, d_y)):
                    if self._distribute_map[d_x][d_y] != Map.MINE_FLAG:
                        self._distribute_map[d_x][d_y] += 1

    def is_in_map(self, pos, offset=None):
        """某一个单元格是否在地图里
        """
        if offset:
            x, y = pos[0] + offset[0], pos[1] + offset[1]
        else:
            x, y = pos
        return x in xrange(0, self.height) and y in xrange(0, self.width)

    def is_mine(self, pos):
        """判断某一个位置是否是地雷
        """
        return pos in self.mine_list

    def get_near_mine_number(self, pos):
        """返回某个位置周围8个单元格中地雷数据，如果本身是地雷返回-1
        @param pos:a tuple like (x, y) 
        """
        x, y = pos
        return self._distribute_map[x][y]

    def create_new_map(self):
        return Map.create_from_mine_number(self.height, self.width, self.mine_number)

    @staticmethod
    def create_from_mine_number(height, width, mine_number):
        """Create a map with mine number.
        @param height: the height of the map
        @param width: the width of the map
        @param mine_number: the number of all mines.
        """
        # TODO 移到Game类
        map_size = height * width
        if mine_number not in xrange(0, map_size + 1):
            raise MapCreateError(MapCreateError.MINE_INVALID_NUMBER)
        mine_index_list = random.sample(xrange(0, map_size), mine_number)
        return Map.create_from_mine_index_list(height, width, mine_index_list)

    @staticmethod
    def create_from_mine_index_list(height, width, mine_index_list):
        """Create a map with mine index list as [3, 4, 7]
        @param height: the height of the map
        @param width: the width of the map
        @param mine_index_list: the mine position index list.
        """
        # TODO 移动到Game类
        index_set = set(mine_index_list)
        map_size = height * width
        mine_pos_list = []
        for index in index_set:
            if index in xrange(0, map_size):
                mine_pos_list.append((index / width, index % width))
            else:
                raise MapCreateError(MapCreateError.MINE_INDEX_INVALID)
        return Map(height, width, mine_pos_list)


class Game(object):
    """扫雷游戏类
    属性
        mine_map:地图类对象，扫雷所使用的地图
        cur_step:当前步数
        sweep_trace:扫雷路径
        state:状态，共有游戏中、成功、失败三种状态
        invisual_number:未扫到单元格
        visual_state_map: 扫到标记地图，二维数组，表示某一位置是否扫过
    动作:
        sweep:从某一位置开始扫雷
        reset:重置游戏状态
    """
    STATE_PLAY = 1
    STATE_SUCCESS = 2
    STATE_FAIL = 3

    def __init__(self, mine_map):
        """根据地图创建游戏
        @param mine_map:地图
        """
        self._mine_map = mine_map
        self._init_game()

    def _init_game(self):
        """初始化
        """
        self._swept_state_map = [[False for i in xrange(0, self._mine_map.width)] for i in
                                 xrange(0, self._mine_map.height)]
        self._not_swept_number = self._mine_map.map_size
        self._cur_step = 0
        self._sweep_trace = []
        self._state = Game.STATE_PLAY

    def reset(self):
        """重置
        """
        self._init_game()


    @property
    def cur_step(self):
        """当前步数
        """
        return self._cur_step

    @property
    def sweep_trace(self):
        """扫雷路径
        """
        return self._sweep_trace

    @property
    def state(self):
        """当前状态
        """
        return self._state

    @property
    def not_swept_number(self):
        """未扫到个数
        """
        return self._not_swept_number

    @property
    def swept_state_map(self):
        """已扫过的地图
        """
        return self._swept_state_map

    @property
    def height(self):
        """地图高度
        """
        return self._mine_map.height

    @property
    def width(self):
        """地图宽度
        """
        return self._mine_map.width

    @property
    def mine_number(self):
        """地雷总数目
        """
        return self._mine_map.mine_number

    @property
    def mine_map(self):
        """地图对象
        """
        return self._mine_map

    def _sweep(self, click_pos):
        """从某一个位置开始扫雷动作
        """
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
            return Game.STATE_PLAY
        else:
            scan_step = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            assert near_mine_number == 0
            q = Queue.Queue()
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
        """
        Play a step
        @param click_pos:the position that user click
        """
        state = self._sweep(click_pos)
        if state == Game.STATE_SUCCESS or state == Game.STATE_FAIL:
            self._sweep_all_map()
        return state

    def _sweep_all_map(self):
        """完成游戏后全部打开
        """
        self._swept_state_map = [[True for i in xrange(0, self.width)] for i in xrange(0, self.height)]
        self._not_swept_number = self.mine_map.map_size - self.mine_map.mine_number
