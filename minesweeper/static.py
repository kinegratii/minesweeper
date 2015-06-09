# coding=utf8
from __future__ import unicode_literals
from py2compat import reduce

import os


APP_NAME = 'Minesweeper v1.3.0'

OSC_URL = 'http://git.oschina.net/kinegratii/minesweeper'

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

STATIC_DIR = os.path.join(BASE_PATH, 'resource')


def static_file(file_path):
    return os.path.join(STATIC_DIR, file_path)


def images(img_path):
    return os.path.join(STATIC_DIR, 'images', img_path)


def style(style_name, **kwargs):
    """
    >>> style('grid.unknown')
    {'text': '', 'bg': '#DDDDDD', 'relief': 'raised', 'fg': '#000000'}
    >>> style('grid.swept', num=2)
    {'text': 2, 'bg': '#DDDDDD', 'relief': 'sunken', 'fg': '#00FF00'}
    """
    return _style_loader.style(style_name, **kwargs)


class GridStyle(object):
    """ 按钮风格
    """

    @staticmethod
    def swept(num):
        colors = ['#BBBBBB',
                  '#0000FF',
                  '#00FF00',
                  '#EE0000',
                  '#FF00FF',
                  '#B22222',
                  '#FFFF00',
                  '#FFBBCC',
                  '#DDCC00'
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

if __name__ == '__main__':
    import doctest

    doctest.testmod()