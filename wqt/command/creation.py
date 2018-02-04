"""
Handle creation, and update of WQt projects
"""

import json
import os
import sys
from distutils.dir_util import copy_tree
from shutil import copyfile
from utils import cmake
from collections import OrderedDict

from colorama import Fore
from utils.helper import (
    create_folder,
    linux_path,
    get_working_directory,
    get_wqt_path,
    get_files,
    get_dirs

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

    project_name = os.path.basename(path)

    templates_path = linux_path(get_wqt_path() + '/templates')
    toolchain_path = linux_path(get_wqt_path() + '/toolchain')

    write('Creating Qt work environment - ', color=Fore.CYAN)

    # check if there are files in the folder
    if get_dirs(path) or get_files(path):
        if os.path.exists(path + '/src') or os.path.exists(path + '/lib') or os.path.exists(path + '/res') or \
                os.path.exists(path + '/cmake'):
            writeln('\nThere is already a src/lib/res/cmake folder in this directory. Use wqt update instead',
                    color=Fore.RED)
            quit(2)
        else:
            writeln('\nDirectory is not empty, aborting ..', color=Fore.RED)
            quit(2)

    create_folders(path, True)
    writeln('done')

    write('Copying required files - ', color=Fore.CYAN)
    copy_tree(toolchain_path + '/cmake', path + "/cmake")
    copy_cmake_template_file(templates_path, path)
    copy_config_template_file(templates_path, path)
    copyfile(templates_path + '/.gitignore.tpl', path + '/.gitignore')
    copyfile(templates_path + '/app-README.md.tpl', path + '/src/app/README.md')
    copyfile(templates_path + '/lib-README.md.tpl', path + '/lib/README.md')
    writeln('done')

    write('Applying configurations - ', color=Fore.CYAN)

    # load config file as json
    with open(path + '/config.json') as f:
        config_data = json.load(f, object_pairs_hook=OrderedDict)

    config_data['name-project'] = project_name

    # write the project name to config file
    with open(path + '/config.json', 'w') as f:
        json.dump(config_data, f, indent=2)

    # fill the template
    cmake.parse_update(path + "/CMakeLists.txt", config_data)
    writeln('done')
    writeln('Qt project created', color=Fore.YELLOW)


def update(path):
    pass
