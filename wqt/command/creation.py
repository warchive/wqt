"""
Handle creation, and update of WQt projects
"""

import json
import os
import sys
from distutils.dir_util import copy_tree
from shutil import copyfile

from colorama import Fore
from utils.helper import (
    create_folder,
    linux_path,
    get_working_directory,
    get_wqt_path

)
from utils.output import (
    writeln,
    write
)


def get_platform():
    """Returns the operating system"""

    platforms = {
        'linux1': 'Linux',
        'linux2': 'Linux',
        'darwin': 'OS X',
        'win32': 'Windows'
    }
    if sys.platform not in platforms:
        return sys.platform

    return platforms[sys.platform]


def create_folders(project_path, override=False):
    """Creates required folders (src, bin, lib and res) in the project directory"""

    create_folder(project_path + '/src', override)
    create_folder(project_path + '/src/app', override)
    create_folder(project_path + '/lib', override)
    create_folder(project_path + '/res', override)

    if get_platform() == 'OS X':
        create_folder(project_path + "/res/icons")


def verify_path(path):
    """check if the project path is correct"""

    if not os.path.exists(path) or not os.path.isdir(path):
        writeln('\nPath specified for project creation does not exist or is not a directory', color=Fore.RED)
        quit(2)


def copy_cmake_template_file(template_path, copy_path):
    """copy cmake template file to the project created"""

    if get_platform() == 'OS X':
        copyfile(template_path + '/CMakeLists-Apple.txt.tpl', copy_path + '/CMakeLists.txt')
    else:
        copyfile(template_path + '/CMakeLists.txt.tpl', copy_path + '/CMakeLists.txt')


def copy_config_template_file(template_path, copy_path):
    """copy config template file to the project created"""

    if get_platform() == 'OS X':
        copyfile(template_path + '/config-apple.json.tpl', copy_path + '/config.json')
    else:
        copyfile(template_path + '/config.json.tpl', copy_path + '/config.json')


def create(path):
    """Creates WQt project from scratch"""

    if path is None:
        path = get_working_directory()
    else:
        path = linux_path(os.path.abspath(path))

    verify_path(path)

    templates_path = linux_path(get_wqt_path() + '/templates')
    toolchain_path = linux_path(get_wqt_path() + '/toolchain')

    write('Creating Qt work environment - ', color=Fore.CYAN)

    create_folders(path, True)
    writeln('done')

    write('Copying required files - ', color=Fore.CYAN)
    copy_tree(toolchain_path + '/cmake', path + "/cmake")
    copy_cmake_template_file(templates_path, path)
    copy_config_template_file(templates_path, path)
    writeln('done')

    write('Applying configurations - ', color=Fore.CYAN)
    # load config file as json
    with open(path + "/config.json") as f:
        config_data = json.load(f)

    # fill the template
    # cmake.parse_update(path + "/CMakeLists.txt", config_data)
    writeln('done')
    writeln('Qt project created', color=Fore.YELLOW)


def update(path):
    pass
