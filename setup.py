#!/usr/bin/env python

from distutils.core import setup

setup(name = 'whisbert',
    version = '0.0.1',
    description = 'A BERT-RPC Interface for the Round Robin DB Whisper.',
    author = 'Andre Graf',
    author_email = 'andre@dergraf.org',
    url = 'https://github.com/dergraf/whisbert',
    classifiers = [
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires = [
        'eventlet',
        'python-bert',
        'python-ernie'],
    dependency_links = [
        'https://github.com/tylerneylon/python-ernie'
    ]
)
