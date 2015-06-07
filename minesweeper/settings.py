#coding=utf8

import os

DEBUG = True

APP_NAME = 'Minesweeper v1.1.1'

BASE_PATH = os.path.abspath(os.path.dirname(__file__))

STATIC_DIR = os.path.join(BASE_PATH, 'resource')

GITHUB_URL = 'http://github.com/kinegratii/minesweeper'

OSC_URL = 'http://git.oschina.net/kinegratii/minesweeper'


def static(file_path):
    return os.path.join(STATIC_DIR, file_path)

def images(img_path):
    return os.path.join(STATIC_DIR, 'images', img_path)
