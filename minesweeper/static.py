# coding=utf8
from __future__ import unicode_literals

import os
import sys

from functools import reduce


APP_NAME = '简易扫雷 v1.4.0'

HOME_URL = 'http://github.com/kinegratii/minesweeper'

BASE_PATH = os.path.abspath(os.path.dirname(sys.argv[0]))

STATIC_DIR = os.path.join(BASE_PATH, 'resource')


def static_file(file_path):
    return os.path.join(STATIC_DIR, file_path)


def images(img_path):
    return os.path.join(STATIC_DIR, 'images', img_path)


def style(style_name, **kwargs):
    return _style_loader.style(style_name, **kwargs)


class GridStyle(object):
    """ 按钮风格
    """

    @staticmethod
    def swept(num):
        colors = ['#BBBBBB',
                  '#000000',
                  '#0602E7',
                  '#F52703',
                  '#6F3F17',
                  '#FFFE07',
                  '#FF12FF',
                  '#3EE8D3',
                  '#FDFCD6'
                  ]
        return {'relief': 'sunken', 'text': num or ' ', 'bg': '#DDDDDD', 'fg': colors[num]}

    unknown = {'relief': 'raised', 'text': '', 'bg': '#DDDDDD', 'fg': '#000000'}

    marked = {'relief': 'raised', 'text': '?', 'bg': '#DDDDDD', 'fg': '#000000'}

    mine = {'relief': 'sunken', 'text': 'X', 'bg': '#D71A23', 'fg': '#FFFFFF'}


class StyleLoader(object):
    def style(self, style_name, **kwargs):
        func = reduce(getattr, style_name.split('.'), self)
        return func(**kwargs) if callable(func) else func

    def register(self, style_pre, obj):
        setattr(self, style_pre, obj)


_style_loader = StyleLoader()
_style_loader.register('grid', GridStyle)
