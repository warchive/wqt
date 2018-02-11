"""@package templates
This file helps perform operations on toolchain files
"""

from distutils.dir_util import copy_tree
from wqt.utils.helper import (
    get_platform,
    OS,
    get_wqt_path
)


def copy_toolchain_files(path):
    """Copies the toolchain files based on OS"""
    os = get_platform()
    toolchain_path = get_wqt_path() + '/toolchain'

    if os == OS.mac:
        copy_tree(toolchain_path + '/osx/cmake', path + '/wqt/cmake')
    else:
        copy_tree(toolchain_path + '/others/cmake', path + '/wqt/cmake')
