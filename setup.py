from distutils.core import setup

setup(
    name='minesweeper',
    version='1.3.0',
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
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
