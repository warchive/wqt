#!/usr/bin/env python

import os

from setuptools import find_packages, setup

install_requires = [
    'colorama',
    'six'
]


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


setup(
    name='WQt',
    version='1.0.9',
    description='Create, Build, and Run Qt Projects',
    author='Deep Dhillon',
    author_email='deep@deepdhillon.ca',
    url='https://github.com/dhillondeep/wqt',  # use the URL to the github repo
    long_description=open('doc/README.rst').read(),
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    package_data={
        '': package_files('toolchain') + package_files('templates') + package_files('doc'),
        'wqt': ['*.json'],
    },
    entry_points={
        'console_scripts': [
            'wqt = wqt.wqt:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta'
    ],
    keywords=[
        'qt', 'c++', 'cmake', 'make', 'tool'
    ],
)
