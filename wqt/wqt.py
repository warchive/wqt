"""
Main Script that calls other scripts to make WQt work
"""

from __future__ import absolute_import

import argparse

from command import creation, handle
from utils.output import writeln, write
from colorama import Fore


def parse():
    """adds command line arguments and returns the options"""

    parser = argparse.ArgumentParser(description='WQt creates and builds Qt projects through CMake')

    parser.add_argument(
        'action',
        nargs='+',
        help='action to perform (create, update, build, clean, list-types, add-lib, rm-lib, list_qml, and show_qml')
    parser.add_argument(
        '--path',
        help='path where the project is or will be created'
    )
    parser.add_argument(
        '--generator',
        help='makefile generator to use for build (default: Unix Makefiles)',
        type=str)
    parser.add_argument(
        '--make',
        help='path to make binary',
        type=str)
    parser.add_argument(
        '--cmake',
        help='path to cmake binary',
        type=str)

    return parser.parse_args()


def provided(*args):
    """checks if given flags are specified during command line usage"""

    if any(flag is not None for flag in args):
        return True


def verify_qt_application(name):
    if name != 'quick' and name != 'widgets' and name != 'console':
        writeln('Invalid Qt application specified', color=Fore.RED)
        quit(2)


def main():
    options = parse()

    path = None
    name = None
    cmake = options.cmake
    make = options.make
    generator = options.generator

    if provided(options.path):
        path = str(options.path)

    # based on the action call scripts
    if 'create' in options.action:
        if len(options.action) < 2:
            writeln('Specify a type of Qt application to create', color=Fore.RED)
            quit(2)

        verify_qt_application(options.action[1])
        creation.create(path, options.action[1])
    elif 'update' in options.action:
        creation.update(path)
    elif 'build' in options.action:
        handle.build(path, generator, cmake, make)
    elif 'clean' in options.action:
        handle.clean(path)
    elif 'list-types' in options.action:
        handle.list_types()
    elif options.action == 'add-lib':
        handle.add_lib(path)
    elif options.action == 'rem-lib':
        handle.rem_lib(path)
    elif options.action == 'list-qml':
        handle.list_qml(path)
    elif options.action == 'preview-qml':
        handle.preview_qml(path, name)


if __name__ == '__main__':
    main()
