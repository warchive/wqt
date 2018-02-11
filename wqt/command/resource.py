"""@package command
Resource helps read resources from the Wqt created project
"""

import os
import sys

from colorama import Fore

from wqt.templates.files import QType
from wqt.utils.output import writeln

if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser


def get_configuration(path, tag, key):
    """Get configuration from the configuration file"""

    if not os.path.exists(path + '/properties.ini'):
        writeln('Configuration file does not exist', Fore.RED)
        quit(2)

    config = configparser.ConfigParser()
    config.read(path + '/properties.ini')

    return config.get(tag, key)


def set_configuration(path, tag, key, value):
    """Set configuration for the configuration file"""

    if not os.path.exists(path + '/properties.ini'):
        writeln('Configuration file does not exist', Fore.RED)
        quit(2)

    config = configparser.ConfigParser()
    config.read(path)

    return config.set(tag, key, value)


def get_qt_type(path):
    """Finds the type of qt project the given path is"""

    # check if there is config file
    if os.path.exists(path + '/properties.ini'):
        return get_configuration(path + '/properties.ini', 'project', 'type')

    # check the res folder
    if os.path.exists(path + '/res/ui'):
        return QType.WIDGETS
    elif os.path.exists(path + '/res/qml'):
        return QType.QUICK
    elif not os.path.exists(path + '/res'):
        return QType.CONSOLE
    else:
        return None
