#coding=utf8
"""
This module contains some hard-coding data for level map.
"""
from minesweeper import Map


class LevelMapConfig(object):
    
    LEVEL_BEGINNER = 1
    LEVEL_PLAYER = 4
    LEVEL_ESCIALER = 9
    
    CHOICES = ((LEVEL_BEGINNER, '新手'), (LEVEL_PLAYER, '老手'), (LEVEL_ESCIALER, '专家'))    
    
    LEVEL_MAP_DICT = {
        LEVEL_BEGINNER:{
            'height': 10,
            'width': 10,
            'mine_number':10
        },
        LEVEL_PLAYER:{
            'height': 20,
            'width': 30,
            'mine_number':100
        },
        LEVEL_ESCIALER:{
            'height': 25,
            'width': 40,
            'mine_number':200
        }        
    }
    
    @staticmethod
    def level_map(level):
        map_config = LevelMapConfig.LEVEL_MAP_DICT[level]
        return Map(**map_config)
