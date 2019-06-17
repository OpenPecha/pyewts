#! /usr/bin/env python
# -*- coding: utf8 -*-

from __future__ import print_function

import os
import setuptools
from pkg_resources import parse_version

assert(parse_version(setuptools.__version__) >= parse_version("38.6.0"))

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name="pyewts",
    version="0.1.1",  #edit version in __init__.py
    author="Esukhia development team",
    author_email="esukhiadev@gmail.com",
    description="Python utils for EWTS conversion from / to Unicode",
    license="Apache2",
    keywords="tibetan",
    url="https://github.com/Esukhia/pyewts",
    packages=setuptools.find_packages(),
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    project_urls={
        'Source': 'https://github.com/Esukhia/pyewts',
        'Tracker': 'https://github.com/Esukhia/pyewts/issues',
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
    python_requires='>=3.4'
)
