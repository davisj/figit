#!/usr/bin/env python

from distutils.core import setup
#from setuptools import setup, find_packages
setup(
    name='Figit',
    version='0.1',
    packages=['Figit', 'Figit.channels', 'Figit.vcs'],
    scripts=['bin/figit.py'],
    #packages = find_packages(),

    # for SSH connections we use the paramiko library.
    #install_requires = ['paramiko>=1.6.4'],

    # Meta data for PyPI upload.
    author='Jake Davis',
    author_email='mrsalty0@gmail.com',
    description='Config file version control via ssh for the impatient',
    license = 'GPL',
    url='http://code.google.com/p/figit/',
)
