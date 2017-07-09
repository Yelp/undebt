# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

from setuptools import find_packages
from setuptools import setup

from undebt import __version__


setup(
    name="undebt",
    version=__version__,
    description="A fast, straightforward, reliable tool for performing massive, automated code refactoring",
    long_description="Check out Undebt on `GitHub <https://github.com/Yelp/undebt>`_!",
    license="Copyright Yelp, Inc. 2016",
    url="https://github.com/Yelp/undebt",
    packages=find_packages(exclude=[
        "tests",
        "docs",
    ]),
    install_requires=[
        'pyparsing',
    ],
    extras_require={
        "testing": [
            "flake8",
            "pytest",
            "mock",
            "coverage",
        ],
        "cPyparsing": [
            "cPyparsing",
        ],
    },
    entry_points={
        'console_scripts': [
            'undebt = undebt.__main__:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Developers",
        "Topic :: Software Development",
        "Topic :: Utilities",
        "Environment :: Console",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
    ]
)
