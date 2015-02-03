#coding=utf8

import Tkinter as tk


class ButtonStyle(object):
    """ the style for buttons on condition.
    """
    @staticmethod
    def invisual_btn_css(text=None):
        text = text or ''
        return {'relief':tk.RAISED, 'text':text,'bg':'#DDDDDD','fg':'#000000'}
    
    @staticmethod
    def tip_btn_css(number):
        if number == 0:
            text = ''
        else:
            text = str(number)
        colors = ['#BBBBBB','#0000FF','#191970','#CC0000','#FF00FF','#B22222','#FFFF00','#FFBBCC','#DDCC00']
        return {'text':text, 'fg':colors[number], 'relief':tk.SUNKEN, 'bg':'#DDDDDD'}
    
    @staticmethod
    def mine_clicked_css():
        return {'text':'X', 'bg':'#FF6347', 'relief':tk.RAISED,'fg':'#000000'}