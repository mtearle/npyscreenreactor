#!/usr/bin/env python

# setp.py

# Copyright (c) 2015 Mark Tearle <mark@tearle.com>
# See LICENSE for details.

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4

from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Framework :: Twisted',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Natural Language :: English',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

setup(
    name='npyscreenreactor',
    version='1.3',
    license='MIT',
    classifiers=classifiers,
    author='Mark Tearle',
    author_email='mark@tearle.com',
    description = 'Twisted reactor for npyscreen',
    long_description = 'npyscreenreactor is a Twisted reactor for the npyscreen curses library',
    url='https://github.com/mtearle/npyscreenreactor',
    download_url='https://github.com/mtearle/npyscreenreactor/tarball/v1.3',
    packages=find_packages(),
    keywords=['npyscreen', 'twisted'],
    install_requires=['twisted', 'npyscreen']
)
