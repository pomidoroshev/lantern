from setuptools import setup
from codecs import open
import os

here = os.path.abspath(os.path.dirname(__file__))

def get_packages(package):
    """
    Return root package and all sub-packages.
    """
    p = [dirpath for dirpath, dirnames, filenames in os.walk(package)
            if os.path.exists(os.path.join(dirpath, '__init__.py'))]

    print('####', p)
    return p

setup(
    name='lantern-tcp',
    version='0.0.1',
    description='Lantern TCP client and simple server',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],

    packages=['lantern_tcp'],

    install_requires=['xtermcolor'],

    entry_points={
        'console_scripts': [
            'lantern=lantern_tcp.lantern:main',
            'lantern_server=lantern_tcp.server:main',
        ],
    },
)
