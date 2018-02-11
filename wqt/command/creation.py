"""@package command
Handle creation, and update of WQt projects
"""

import json
import os
from collections import OrderedDict
from distutils.dir_util import copy_tree
from shutil import copyfile

from colorama import Fore

from wqt.utils import cmake
from wqt.utils.helper import (
    any_folders_exist,
    get_files,
    get_dirs,
    get_valid_path,
    get_platform,
    get_qt_application,
)
from wqt.utils.output import (
    writeln,
    write
)
from wqt.templates.operations import (
    QType,
    fill_and_copy_config,
    parse_and_copy_cmake,
    copy_application_files,
    copy_other_files,
    verify_project_structure
)
from wqt.toolchain.operations import (
    copy_toolchain_files
)


def verify_path(path):
    """check if the project path is correct"""

    if not os.path.exists(path) or not os.path.isdir(path):
        writeln('Path specified for project creation does not exist or is not a directory', color=Fore.RED)
        quit(2)


def create(path, application):
    """Creates WQt project from scratch"""

    path = get_valid_path(path)

    writeln('Creating Qt ' + application + ' project', color=Fore.YELLOW)

    # check if there are files in the folder
    if get_dirs(path) or get_files(path):
        if any_folders_exist([path + '/src', path + '/lib', path + '/res']):
            writeln('There is already a src/lib/res folder in this directory. Use wqt update instead',
                    color=Fore.RED)
            quit(2)

    write('Copying required files and applying configuration - ', color=Fore.CYAN)

    verify_project_structure(path, application, True)
    fill_and_copy_config(application, path)
    parse_and_copy_cmake(application, path)
    copy_application_files(application, path)
    copy_toolchain_files(path)
    copy_other_files(path)

    writeln('done')
    writeln('Qt project created', color=Fore.YELLOW)


def update_config_file(app_path, toolchain_path):
    # get data from current config file
    with open(app_path + '/config.json') as f:
        app_config_data = json.load(f, object_pairs_hook=OrderedDict)

    # get data from the platform template path
    if get_platform() == 'OS X':
        template_config_path = toolchain_path + '/config/config.json'
    else:
        template_config_path = toolchain_path + '/config/config.json'

    with open(template_config_path) as f:
        template_config_data = json.load(f, object_pairs_hook=OrderedDict)

    # add the missing keys
    for key in template_config_data:
        if key not in app_config_data:
            app_config_data[key] = template_config_data[key]

    # write new config to the app config file
    with open(app_path + '/config.json', 'w') as f:
        json.dump(app_config_data, f, indent=2)

"""
def update(path):
    ""Updates existing WQt project""

    path = get_valid_path(path)

    project_name = os.path.basename(path)
    application = get_qt_application(path)

    writeln('Updating Qt ' + application + ' project', color=Fore.YELLOW)

    templates_path = linux_path(get_wqt_path() + '/templates')
    toolchain_path = linux_path(get_wqt_path() + '/toolchain')

    write('Updating Qt work environment - ', color=Fore.CYAN)

    create_folders(path, application, False)
    writeln('done')

    write('Copying required files - ', color=Fore.CYAN)
    copy_tree(toolchain_path + '/cmake', path + '/wqt/cmake')
    copy_tree(toolchain_path + '/helper', path + '/wqt/helper')
    copy_cmake_template_file(templates_path, path)

    if not os.path.exists(path + '/config.json'):
        copy_config_template_file(templates_path, path)
    else:
        update_config_file(path, templates_path)

    if not os.path.exists(path + '/gitignore'):
        copyfile(templates_path + '/gitignore.tpl', path + '/.gitignore')

    if not os.path.exists(path + '/src/app/README.mod'):
        copyfile(templates_path + '/readme/app-README.md.tpl', path + '/src/app/README.md')

    if not os.path.exists(path + '/lib/README.md'):
        copyfile(templates_path + '/readme/lib-README.md.tpl', path + '/lib/README.md')

    if get_platform() == 'OS X' and not os.path.exists(path + '/res/icons/icon.icns'):
        copyfile(templates_path + '/icon.icns', path + '/res/icons/icon.icns')

    writeln('done')

    write('Applying updated configurations - ', color=Fore.CYAN)

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
    writeln('Qt project updated', color=Fore.YELLOW)
"""
