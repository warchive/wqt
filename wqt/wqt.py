"""
Main Script that calls other scripts to make WQt work
"""

from __future__ import absolute_import

import argparse

from colorama import Fore

from wqt.command import creation, handle
from wqt.templates.files import QType
from wqt.utils.output import writeln


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


def verify_qt_application(qt_type):
    """verifies if the type of Qt application is supported"""

    if qt_type is None:
        writeln('Invalid Qt application specified', color=Fore.RED)
        quit(2)


def main():
    options = parse()

    path = None
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

        qt_type = QType.get_type(options.action[1])

        verify_qt_application(qt_type)
        creation.create(path, qt_type)
    elif 'update' in options.action:
        creation.update(path)
    elif 'build' in options.action:
        handle.build(path, generator, cmake, make)
    elif 'clean' in options.action:
        handle.clean(path)
    elif 'list-types' in options.action:
        handle.list_types()
    elif 'add-lib' in options.action:
        if len(options.action) < 2:
            writeln('Specify the name of the library to add', color=Fore.RED)
            quit(2)

        handle.add_lib(path, options.action[1])
    elif 'rm-lib' in options.action:
        if len(options.action) < 2:
            writeln('Specify the name of the library to remove', color=Fore.RED)
            quit(2)

        handle.rm_lib(path, options.action[1])
    elif 'run' in options.action:
        handle.run(path, generator, cmake, make)
    elif 'list-qml' in options.action:
        handle.list_qml(path)
    elif 'list-libs' in options.action:
        handle.list_libs(path)
    elif 'preview-qml' in options.action:
        if len(options.action) < 2:
            writeln('Specify the name of the qml file to preview', color=Fore.RED)
            quit(2)

        handle.preview_qml(path, options.action[1])


if __name__ == '__main__':
    main()
