#!/usr/bin/env python
# coding: utf-8

import os
from setuptools import setup, find_packages
import dbarc.authoring
from dbarc.version import get_version


def get_data_files(path):
    files = []
    path = os.path.abspath(path)
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            if os.path.splitext(filename)[1].lower() not in ['.py', '.pyc']:
                full_path = os.path.join(dirname, filename)
                files.append(os.path.relpath(full_path, path))
    return files


setup(
    name='dbarc',
    description='Dropbox archiver',
    version=get_version(),
    license=dbarc.authoring.__license__,
    author=dbarc.authoring.__author__,
    author_email=dbarc.authoring.__email__,
    url=dbarc.authoring.__url__,
    long_description=open('README.md').read(),
    platforms=['any'],
    packages=find_packages(),
    package_data={'dbarc': get_data_files('dbarc')},
    install_requires=[
        'docopt',
        'dropbox',
    ],
    entry_points={'console_scripts': ['dbarc = dbarc.dbarc:main']},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
       'Development Status :: 5 - Production/Stable',
       'Intended Audience :: Developers',
       'License :: OSI Approved :: MIT License',
       'Programming Language :: Python',
       'Programming Language :: Python :: 3.3',
    ],
)
