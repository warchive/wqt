"""@package command
Resource helps read resources from the Wqt created project
"""

import os
import sys

from wqt.templates.files import QType

if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser


def get_configuration(path, tag, key):
    """Get configuration from the configuration file"""

    config = configparser.ConfigParser()
    config.read(path)

    return config.get(tag, key)


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
