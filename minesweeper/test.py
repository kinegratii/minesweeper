# coding=utf8
"""
Test cases for creating map and playing minesweeper game.
@author:kinegratii(kinegratii@yeah.net)
@Version:1.0.1
Update on 2014.05.04
"""
from __future__ import unicode_literals

import unittest
from core import Map
from core import Game
from helpers import GameHelpers


class MapCreateTestCase(unittest.TestCase):
    def setUp(self):
        self.height = 5
        self.width = 6
        self.valid_index_data = (
            {
                'mine_index_list': [0, 1, 5],
                'mine_number': 3
            },
            {
                'mine_index_list': [1, 23, 24, 15, 23, 1, 29],
                'mine_number': 5
            }
        )
        self.valid_pos_data = (
            {
                'mine_pos_list': [(0, 0), (3, 4), (2, 2)],
                'mine_number': 3
            },
            {
                'mine_pos_list': [(0, 0), (0, 0), (3, 5), (4, 5), (3, 4), (3, 5)],
                'mine_number': 4
            }
        )
        self.valid_number_data = [4, 10]

    def tearDown(self):
        pass

    def test_mine_valid_index(self):
        """Test creating map with valid mine index.
        """
        for data in self.valid_index_data:
            m = GameHelpers.create_from_mine_index_list(self.height, self.width, data['mine_index_list'])
            self.assertEqual(m.mine_number, data['mine_number'])

    def test_mine_valid_pos(self):
        """Test creating map with valid mine position.
        """
        for data in self.valid_pos_data:
            m = Map(self.height, self.width, data['mine_pos_list'])
            self.assertEqual(m.mine_number, data['mine_number'])

    def test_mine_valid_number(self):
        """Test creating map with valid mine number.
        """
        for data in self.valid_number_data:
            m = GameHelpers.create_from_mine_number(self.height, self.width, data)
            self.assertEqual(m.mine_number, data)


    def create_map(self, mine_pos_list):
        """convert constructing Map object to a callable function for self.assertRaises statement
        """
        m = Map(self.height, self.width, mine_pos_list)
        return m


class MapBaseFunctionTestCase(unittest.TestCase):
    def setUp(self):
        self.mine_map = GameHelpers.create_from_mine_number(5, 6, 6)

    def tearDown(self):
        self.mine_map = None

    def test_is_in_map(self):
        """Test function minesweeper.Map.is_in_map
        """
        # The mine created by random should be always in the map.
        mine_list = self.mine_map.mine_list
        for pos in mine_list:
            self.assertTrue(self.mine_map.is_in_map(pos))

    def test_near_mine_map(self):
        mine_pos_list = [(2, 5), (3, 2), (1, 3)]
        mine_map = Map(5, 6, mine_pos_list=mine_pos_list)
        for x, y in mine_pos_list:
            self.assertEqual(mine_map.distribute_map[x][y], -1)


class GamePlayTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_move_a(self):
        mine_map = Map(3, 4, mine_pos_list=[(0, 0)])
        test_data_cases = [
            {
                'click_trace': [(0, 1), (1, 0)],
                'state': 1,
                'cur_step': 2
            },
            {
                'click_trace': [(0, 1), (1, 0), (1, 1), (1, 2)],
                'state': 2,
                'cur_step': 4
            }
        ]
        for data in test_data_cases:
            game = Game(mine_map)
            self.batch_click(game, data['click_trace'])
            self.assertEqual(game.state, data['state'])
            self.assertEqual(game.cur_step, data['cur_step'])

    def test_move_one_step(self):
        """ This map can be done in one step.
        #####  01110
        ##@##  01@10
        #####  01110
        """
        mine_map = Map(5, 5, mine_pos_list=[(2, 2)])
        game = Game(mine_map)
        state = game._sweep((0, 0))
        self.assertEqual(state, 2)


    def batch_click(self, game, click_trace):
        for click_pos in click_trace:
            state = game._sweep(click_pos)
            if state > 1:
                return
        return


    def tearDown(self):
        pass


class BaseMapTestCase(unittest.TestCase):
    def setUp(self):
        """ This map can be done in one step.
        #####  01110
        ##@##  01@10
        #####  01110
        """
        self.mine_map = Map(5, 5, [(2, 2)])

    def test_one_step_success(self):
        click_list = [(0, 0), (0, 4), (4, 0), (4, 4)]
        for click_pos in click_list:
            game = Game(self.mine_map)
            state = game._sweep(click_pos)
            self.assertEqual(state, 2)


if __name__ == '__main__':
    unittest.main()
