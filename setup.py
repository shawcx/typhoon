#!/usr/bin/env python3

import sys
import os

from setuptools import setup

exec(compile(open('typhoon/version.py').read(),'version.py','exec'))

setup(
    name             = 'typhoon',
    author           = __author__,
    author_email     = __email__,
    version          = __version__,
    license          = __license__,
    description      = 'Python code obfuscator',
    long_description = open('README.rst').read(),
    url              = 'https://github.com/moertle/typhoon',
    entry_points = {
        'console_scripts': [
            'typhoon = typhoon.main:main',
            ]
        },
    packages = setuptools.find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        ],
    zip_safe = False
    )
