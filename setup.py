from setuptools import setup

setup(
    name='lantern-tcp',
    version='0.1.1',
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
