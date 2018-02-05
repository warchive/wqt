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
    create_folder,
    linux_path,
    get_wqt_path,
    get_files,
    get_dirs,
    get_valid_path,
    get_platform,
    get_qt_application
)
from wqt.utils.output import (
    writeln,
    write
)


def create_folders(project_path, application, override=False):
    """Creates required folders (src, bin, lib and res) in the project directory"""

    create_folder(project_path + '/src', override)
    create_folder(project_path + '/src/app', override)
    create_folder(project_path + '/lib', override)
    create_folder(project_path + '/wqt', override)

    if get_platform() == 'OS X':
        create_folder(project_path + "/res")
        create_folder(project_path + "/res/icons")

    if application == 'quick':
        if not os.path.exists(project_path + '/res'):
            create_folder(project_path + '/res', override)
        create_folder(project_path + '/res/qml', override)
    elif application == 'widgets':
        if not os.path.exists(project_path + '/res'):
            create_folder(project_path + '/res', override)
        create_folder(project_path + '/res/ui', override)


def verify_path(path):
    """check if the project path is correct"""

    if not os.path.exists(path) or not os.path.isdir(path):
        writeln('Path specified for project creation does not exist or is not a directory', color=Fore.RED)
        quit(2)


def copy_cmake_template_file(template_path, copy_path):
    """copy cmake template file to the project created"""

    if get_platform() == 'OS X':
        copyfile(template_path + '/cmake/CMakeLists-Apple.txt.tpl', copy_path + '/CMakeLists.txt')
    else:
        copyfile(template_path + '/cmake/CMakeLists.txt.tpl', copy_path + '/CMakeLists.txt')


def copy_config_template_file(template_path, copy_path):
    """copy config template file to the project created"""

    if get_platform() == 'OS X':
        copyfile(template_path + '/config/config-apple.json.tpl', copy_path + '/config.json')
    else:
        copyfile(template_path + '/config/config.json.tpl', copy_path + '/config.json')


def copy_application_files(application, templates_path, path):
    """copy Qt default files based on the application type"""

    if application == 'widgets':
        copy_widgets_files(templates_path, path)
    elif application == 'quick':
        copy_quick_files(templates_path, path)
    elif application == 'console':
        copy_console_files(templates_path, path)


def copy_widgets_files(templates_path, path):
    """copy widgets type files"""

    copyfile(templates_path + '/widgets/widgets', path + '/wqt/widgets')
    copyfile(templates_path + '/widgets/main.cpp', path + '/src/app/main.cpp')
    copyfile(templates_path + '/widgets/mainwindow.cpp', path + '/src/app/mainwindow.cpp')
    copyfile(templates_path + '/widgets/mainwindow.h', path + '/src/app/mainwindow.h')
    copyfile(templates_path + '/widgets/mainwindow.ui', path + '/res/ui/mainwindow.ui')


def copy_quick_files(templates_path, path):
    """copy quick type files"""

    copyfile(templates_path + '/quick/quick', path + '/wqt/quick')
    copyfile(templates_path + '/quick/main.cpp', path + '/src/app/main.cpp')
    copyfile(templates_path + '/quick/main.qml', path + '/res/qml/main.qml')


def copy_console_files(templates_path, path):
    """copy console type files"""

    copyfile(templates_path + '/console/console', path + '/wqt/console')
    copyfile(templates_path + '/console/main.cpp', path + '/src/app/main.cpp')


def create(path, application):
    """Creates WQt project from scratch"""

    path = get_valid_path(path)
    project_name = os.path.basename(path)

    writeln('Creating Qt ' + application + ' project', color=Fore.YELLOW)

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

    create_folders(path, application, True)
    writeln('done')

    write('Copying required files - ', color=Fore.CYAN)
    copy_tree(toolchain_path + '/cmake', path + '/wqt/cmake')
    copy_tree(toolchain_path + '/helper', path + '/wqt/helper')
    copy_cmake_template_file(templates_path, path)
    copy_config_template_file(templates_path, path)
    copyfile(templates_path + '/gitignore.tpl', path + '/.gitignore')
    copyfile(templates_path + '/readme/app-README.md.tpl', path + '/src/app/README.md')
    copyfile(templates_path + '/readme/lib-README.md.tpl', path + '/lib/README.md')

    if get_platform() == 'OS X':
        copyfile(templates_path + '/icon.icns', path + '/res/icons/icon.icns')

    copy_application_files(application, templates_path, path)

    writeln('done')

    write('Applying configurations - ', color=Fore.CYAN)

    # load config file as json
    with open(path + '/config.json') as f:
        config_data = json.load(f, object_pairs_hook=OrderedDict)

    config_data['name-project'] = project_name

    if application == 'quick':
        config_data['libraries-qt'].append(str('Gui'))
        config_data['libraries-qt'].append(str('Qml'))
    elif application == 'widgets':
        config_data['libraries-qt'].append(str('Gui'))
        config_data['libraries-qt'].append(str('Widgets'))

    # write the project name to config file
    with open(path + '/config.json', 'w') as f:
        json.dump(config_data, f, indent=2)

    # fill the template
    cmake.parse_update(path + "/CMakeLists.txt", config_data)
    writeln('done')
    writeln('Qt project created', color=Fore.YELLOW)


def update(path):
    """Updates existing WQt project"""

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
