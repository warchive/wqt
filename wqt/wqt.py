"""
Main Script that calls other scripts to make WQt work
"""

from __future__ import absolute_import

import argparse

from command import creation, handle


def parse():
    """Adds command line arguments and returns the options"""

    parser = argparse.ArgumentParser(description='WQt creates and builds Qt projects through CMake')

    parser.add_argument(
        'action',
        help='action to perform (create, update, build, listqml, and showqml')
    parser.add_argument(
        '--path',
        help='path where the project is or will be created'
    )
    parser.add_argument(
        '--name',
        help='name of the qml file to be shown'
    )

    return parser.parse_args()


def provided(*args):
    """checks if give flags are specified during command line usage"""

    if any(flag is not None for flag in args):
        return True


def main():
    options = parse()

    path = None
    name = None

    if provided(options.path):
        path = str(options.path)

    if provided(options.name):
        name = str(options.name)

    # based on the action call scripts
    if options.action == 'create':
        creation.create(path)
    elif options.action == "update":
        creation.update(path)
    elif options.action == "build":
        handle.build(path)
    elif options.action == "listqml":
        handle.listqml(path)
    elif options.action == "showqml":
        handle.showqml(path, name)


if __name__ == '__main__':
    main()
