# !/usr/bin/env python
# coding: utf-8

__author__ = 'winkidney'

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'django>=1.8',
]

setup(
    name='storygear',
    version='0.0.1',
    packages=find_packages('.', exclude=[]),
    url='',
    license='',
    author='kidney',
    author_email='winkidney@gmail.com',
    description='Gear to make stories by muliti-person.',
    install_requires=requires,
)
