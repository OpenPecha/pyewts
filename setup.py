#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
import sys
from setuptools import setup, find_packages
import pypandoc

def read(fname):
    rst = pypandoc.convert_file(os.path.join(os.path.dirname(__file__), fname), 'rst', format='md')
    return rst

setup(
    name="pyewts",
    version="0.1.0",  #edit version in __init__.py
    author="Esukhia development team",
    author_email="esukhiadev@gmail.com",
    description="Python utils for EWTS conversion from / to Unicode",
    license="Apache2",
    keywords="tibetan",
    url="https://github.com/eroux/pyewts",
    packages=find_packages(),
    long_description=read('README.md'),
    project_urls={
        'Source': 'https://github.com/eroux/pyewts',
        'Tracker': 'https://github.com/eroux/pyewts/issues',
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Text Processing :: Linguistic",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: Tibetan"
    ],
    python_requires='>=3',
)
