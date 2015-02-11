# coding=utf8
"""
This module contains some hard-coding data for level map.
"""

import random

from minesweeper import Map


def create_from_mine_index_list(height, width, mine_index_list):
    """根据地雷序号创建地图
    """
    return Map(height, width, ((index / width, index % width) for index in mine_index_list))


def create_from_mine_number(height, width, mine_number):
    """创建随机地图
    """
    map_size = height * width
    mine_index_list = random.sample(xrange(0, map_size), mine_number)
    return create_from_mine_index_list(height, width, mine_index_list)


class LevelMapConfig(object):
    LEVEL_BEGINNER = 1
    LEVEL_PLAYER = 4
    LEVEL_EXPERT = 9

    CHOICES = ((LEVEL_BEGINNER, '新手（10X10-10）'), (LEVEL_PLAYER, '老手（20X30-100）'), (LEVEL_EXPERT, '专家（25X40-200）'))

    LEVEL_MAP_DICT = {
        LEVEL_BEGINNER: {
            'height': 10,
            'width': 10,
            'mine_number': 10
        },
        LEVEL_PLAYER: {
            'height': 20,
            'width': 30,
            'mine_number': 100
        },
        LEVEL_EXPERT: {
            'height': 25,
            'width': 40,
            'mine_number': 200
        }
    }

    @staticmethod
    def level_map(level):
        map_config = LevelMapConfig.LEVEL_MAP_DICT[level]
        return create_from_mine_number(**map_config)
