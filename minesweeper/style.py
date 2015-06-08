# coding=utf8


class ButtonStyle(object):
    """ 按钮风格
    """

    @staticmethod
    def grid_swept_style(number):
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
        return {'relief': 'sunken', 'text': number or ' ', 'bg': '#DDDDDD', 'fg': colors[number]}

    grid_unknown_style = {'relief': 'raised', 'text': '', 'bg': '#DDDDDD', 'fg': '#000000'}

    grid_marked_style = {'relief': 'raised', 'text': '?', 'bg': '#DDDDDD', 'fg': '#000000'}

    grid_mine_style = {'relief': 'sunken', 'text': 'X', 'bg': '#D71A23', 'fg': '#FFFFFF'}