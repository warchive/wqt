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
    setup_requires=['setuptools-markdown'],
    name='WQt',
    version='1.0.1',
    description='Create, Build, and Run Qt Projects',
    author='Deep Dhillon',
    author_email='deep@deepdhillon.ca',
    url='https://github.com/dhillondeep/wqt',  # use the URL to the github repo
    long_description_markdown_filename='README.md',
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
        'Development Status :: 4 - Beta'
    ],
    keywords=[
        'qt', 'c++', 'cmake', 'make', 'tool'
    ],
)
