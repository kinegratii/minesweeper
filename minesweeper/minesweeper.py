#coding=utf8
"""
@author:kinegratii(kinegratii@yeah.net)
@Version:1.0.1
Update on 2014.05.04
"""
import random
import Queue


class MapCreateError(Exception):
    """ Exception when creating map with invalid params.
    """
    INVALID_HEIGHT_OR_WIDTH = 'invalid height or width' 
    MINE_INDEX_INVALID = 'invalid mine index'
    MINE_INVALID_POS = 'invalid mine position'
    MINE_INVALID_NUMBER = 'invalid mine number'
    
    def __init__(self, message):
        super(MapCreateError, self).__init__(message)


class Map(object):
    """A map consist of some mine's position data.It is read-only so that you cannot motify
     its attributes after initing.
     Attributes:
        height: A integer,the height of the map.
        width:A integer,the width of the map.
        map_size:A integer,the amount of cells. map_size = height * width
        mine_list:A list,every element is a two-tuple like (x,y) stand for a mine's position.
        mine_number:A integer less or equal than map_size,the amount of mine
        distribute_map:A 2-d list,the distribute_map[x][y] is the amount of mines in near 8 cells
            if (x, y) is not a mine,otherwise will be -1
    """
    #the mine flag in distribute map
    MINE_FLAG = -1
    
    def __init__(self, height, width, mine_pos_list):
        """Create a map with mine postion list.
        @param height: the height of the map
        @param width: the width of the map
        @param mine_pos_list:the position list of mines
        """
        if type(height) != type(1) or type(width) != type(1) or height <= 0 or width <= 0:
            raise MapCreateError(MapCreateError.INVALID_HEIGHT_OR_WIDTH)
        self._height = height
        self._width = width
        self._mine_number = 0
        self._mine_list = []
        pos_set = set(mine_pos_list)
        for pos in pos_set:
            if not self.is_in_map(pos):
                raise MapCreateError(MapCreateError.MINE_INVALID_POS)
        self._mine_list = list(pos_set)
        self._mine_number = len(pos_set)
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
        return self._mine_number
    
    @property
    def distribute_map(self):
        return self._distribute_map

        
    #Some base functions.Use self.height instead of self._height etc.
    
    def _generate_distribute_map(self):
        """Generate the distribute map. 
        """
        self._distribute_map = [[0 for i in xrange(0,self.width)] for i in xrange(0,self.height)]
        offset_step = [(-1,-1),(-1,0),(-1,1),(0,1),(1,1),(1,0),(1,-1),(0,-1)]
        for t_x, t_y in self.mine_list:
            self._distribute_map[t_x][t_y] = Map.MINE_FLAG
            for o_x, o_y in offset_step:
                d_x, d_y = t_x + o_x, t_y + o_y
                if self.is_in_map((d_x, d_y)):
                    if self._distribute_map[d_x][d_y] != Map.MINE_FLAG:
                        self._distribute_map[d_x][d_y] += 1
    
    def is_in_map(self, pos, offset=None):
        """return the given postion is in the map.
        """
        if offset:
            x, y = pos[0] + offset[0], pos[1] + offset[1]
        else:
            x, y = pos
        return x in xrange(0, self.height) and y in xrange(0, self.width)
    
    def is_mine(self, pos):
        return pos in self.mine_list
    
    def get_near_mine_number(self, pos):
        """Return the mine number near the given position,if the position is mine return -1
        @param pos:a tuple like (x, y) 
        """
        x, y = pos
        return self._distribute_map[x][y]
    
    def create_new_map(self):
        """
        @warn:the method will be deprecated in futrue version.
        """
        return Map.create_from_mine_number(self.height, self.width, self.mine_number)
    
    @staticmethod
    def create_from_mine_number(height, width, mine_number):
        """Create a map with mine number.
        @param height: the height of the map
        @param width: the width of the map
        @param mine_number: the number of all mines.
        """
        map_size = height * width
        if mine_number not in xrange(0, map_size + 1):
            raise MapCreateError(MapCreateError.MINE_INVALID_NUMBER)
        mine_index_list = random.sample(xrange(0, map_size), mine_number)
        return Map.create_from_mine_index_list(height, width, mine_index_list)
    
    @staticmethod
    def create_from_mine_index_list(height, width, mine_index_list):
        """Create a map with mine index list
        @param height: the height of the map
        @param width: the width of the map
        @param mine_index_list: the mine position index list.
        """
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
    """A state machine for playing minesweeper.There are some attributes and actions as usual machine.
    Const attributes(will not change when running):
        mine_map:The map object the game is playing on.As convience,the game extends map attributes as
            its own attibutes.For examle, Game.height is for short to Game.mine_map.height
    Runtime attributes:
        cur_step:The steps that has already played.
        click_trace:The clicked position in playing. The expression len(click_trace) = cur_step is true.
        state:The state for this game.This game contains a no-end state namely playing, and two end state:
            success and fail.
        (Note:the above two attributes is for users' input)
        invisual_number:The number of invisual cells.
        visual_state_map: A 2-d list with bool flag which show the cell is visual or not.
    Actions:
        move:the core action.run to next state when accept a click position.
        play:the wrapper for move action.
        reset:reset to initial state.
    """
    STATE_PLAY = 1
    STATE_SUCCESS = 2
    STATE_FAIL = 3
    
    def __init__(self, mine_map):
        """
        Create a new game with map.
        @param mine_map:the map of mine
        """
        self._mine_map = mine_map
        self._init_game()
    
    def _init_game(self):
        """
        set state to init.
        """
        self._visual_state_map = [[False for i in xrange(0, self._mine_map.width)] for i in xrange(0, self._mine_map.height)]
        self._invisual_number = self._mine_map.map_size
        self._cur_step = 0
        self._click_trace = []
        self._state = Game.STATE_PLAY
    
    def reset(self):
        """
        Reset the game.
        """
        self._init_game()

    
    @property
    def cur_step(self):
        return self._cur_step
    
    @property
    def click_trace(self):
        return self._click_trace
    
    @property
    def state(self):
        return self._state
    
    @property
    def invisual_number(self):
        return self._invisual_number
    
    @property
    def visual_state_map(self):
        return self._visual_state_map
    
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
    
    def move(self, click_pos):
        """
        reflact on user's input
        @param click_pos:the position that user click
        @warn:You should use play instead of this method in app.
        """
        if self._state == Game.STATE_SUCCESS or self._state == Game.STATE_FAIL:
            # success or fail is the end state of game.
            return self._state
        self._cur_step += 1
        self._click_trace.append(click_pos)
        cx, cy = click_pos
        if self._visual_state_map[cx][cy]:
            #click the position has been clicked,pass
            self._state = Game.STATE_PLAY
            return self._state
        
        near_mine_number = self._mine_map.get_near_mine_number(click_pos)
        
        if near_mine_number == Map.MINE_FLAG:
            #click the mine,game over.
            self._invisual_number -= 1
            self._visual_state_map[cx][cy] = True
            return Game.STATE_FAIL
        elif near_mine_number > 0:
            self._invisual_number -= 1
            self._visual_state_map[cx][cy] = True
            if self._invisual_number == self._mine_map.mine_number:
                self._state = Game.STATE_SUCCESS
            else:
                self._state = Game.STATE_PLAY
            return Game.STATE_PLAY
        else:
            scan_step = [(-1, 0), (0, 1), (1, 0), (0, -1)]
            assert near_mine_number == 0
            q = Queue.Queue()
            q.put(click_pos)
            self._invisual_number -= 1
            self._visual_state_map[cx][cy] = True            
            while not q.empty():
                c_x, c_y = q.get()
                for o_x, o_y in scan_step:
                    d_x, d_y = c_x + o_x, c_y + o_y
                    if self._mine_map.is_in_map((d_x, d_y)) and not self._visual_state_map[d_x][d_y]:
                        near_mine_number = self._mine_map.get_near_mine_number((d_x, d_y))
                        if near_mine_number == Map.MINE_FLAG:
                            pass
                        elif near_mine_number == 0:
                            q.put((d_x, d_y))
                            self._visual_state_map[d_x][d_y] = True
                            self._invisual_number -= 1
                        else:
                            self._visual_state_map[d_x][d_y] = True
                            self._invisual_number -= 1
            assert self._invisual_number >= self._mine_map.mine_number
            if self._invisual_number == self._mine_map.mine_number:
                self._state = Game.STATE_SUCCESS
            else:
                self._state = Game.STATE_PLAY
            return self._state
    
    def play(self, click_pos):
        """
        Play a step
        @param click_pos:the position that user click
        """
        state = self.move(click_pos)
        if state == Game.STATE_SUCCESS or state == Game.STATE_FAIL:
            self._complete_game()
        return state
    
    def _complete_game(self):
        self._visual_state_map = [[True for i in xrange(0, self.width)] for i in xrange(0, self.height)]
        self._invisual_number = self.mine_map.map_size - self.mine_map.mine_number
    

def main():
    pass

if __name__ == '__main__':
    main()
