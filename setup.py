from distutils.core import setup

setup(
    name='minesweeper',
    version='1.3.1',
    packages=['minesweeper',],
    url='http://github.com/kinegratii/minesweeper',
    license='GPLv2',
    author='kinegratii',
    author_email='kinegratii@gmail.com',
    description='A tkinter-based game for minesweeper.',
    data_files=[
        (
            'minesweeper/resource',
            [
                'minesweeper/resource/project.txt',
                'minesweeper/resource/images/mine.ico'
            ]
        )
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Games/Entertainment :: Board Games',
    ]
)
