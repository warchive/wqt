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
    version='1.0.0',
    description='Create, Build, and Run Qt Projects',
    author='Deep Dhillon',
    author_email='deep@deepdhillon.ca',
    # long_description=open('README.md').read(),
    license='MIT',
    packages=find_packages(),
    install_requires=install_requires,
    package_data={
        '': package_files('toolchain') + package_files('templates'),
        'wqt': ['*.json'],
    },
    entry_points={
        'console_scripts': [
            'wqt = wqt.wqt:main',
        ],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: MIT'
    ],
    keywords=[
        'qt', 'c++', 'cmake', 'make', 'tool'
    ],
)
