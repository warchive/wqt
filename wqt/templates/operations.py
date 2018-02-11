"""@package templates
This file helps perform operations on template files
"""

import os
import re
import sys

import pystache
import xmltodict

from wqt.command.resource import (
    get_qt_type
)
from wqt.templates.files import (
    QType,
    get_config_file,
    get_cmake_file,
    get_src_files,
    get_res_files
)
from wqt.utils.helper import (
    get_files,
    get_dirs_recursively,
    copyfile
)
from wqt.utils.helper import (
    get_wqt_path,
    get_platform,
    OS,
    create_folder
)

if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser


def __ini_to_dictionary(config_file):
    """converts ini file content to dictionary"""

    config = configparser.ConfigParser()
    config.read(config_file)

    dictionary = {}
    for section in config.sections():
        dictionary[section] = {}
        for option in config.options(section):
            dictionary[section][option] = config.get(section, option)

    return dictionary


def parse_and_copy_cmake(qt_type, path):
    """Parses template cmake files and fill them with info from config files"""

    config_file = path + '/properties.ini'
    cmake_file = get_cmake_file(qt_type)
    config_dict = __ini_to_dictionary(config_file)

    # update config with link library string
    qt_libraries = config_dict['library']['qt'].split()
    link_str = ''

    for library in qt_libraries:
        link_str += 'Qt5::'
        link_str += library
        link_str += ' '

    link_str = link_str.strip(' ')

    # TODO -> handle user libraries

    config_dict['library']['link'] = link_str

    with open(cmake_file) as f:
        template_data = ''.join(f.readlines())

    filled_data = pystache.render(template_data, config_dict)

    with open(path + '/CMakeLists.txt', 'w') as f:
        f.write(filled_data)


def fill_and_copy_config(qt_type, path, check=False):
    """fills the essential config information and writes the config file"""

    if check and os.path.exists(path + '/properties.ini'):
        config_file = path + '/properties.ini'
    else:
        config_file = get_config_file(qt_type)
    project_name = os.path.basename(path)

    config = configparser.ConfigParser()
    config.read(config_file)
    config.set('project', 'name', project_name)
    config.set('project', 'type', qt_type)

    with open(path + '/properties.ini', 'w') as f:
        config.write(f)

    # remove 2 extra spaces at the end
    with open(path + '/properties.ini') as f:
        data = ''.join(f.readlines())

    with open(path + '/properties.ini', 'w') as f:
        f.write(data.strip().strip('\n'))


def copy_application_files(qt_type, path):
    """Copy template application files to get user started"""

    # copy source files
    src_files = get_src_files(qt_type)

    for file in src_files:
        copyfile(file, path + '/src/' + os.path.basename(path), True)

    # copy res files
    res_files = get_res_files(qt_type, ['.qml', '.ui', '.qrc'])

    for file in res_files:
        if qt_type == QType.WIDGETS:
            copyfile(file, path + '/res/ui/', True)
        elif qt_type == QType.QUICK:
            copyfile(file, path + '/res/qml/', True)

    # copy icon files
    if get_platform() == OS.mac and (qt_type == QType.QUICK or qt_type == QType.WIDGETS):
        copyfile(get_wqt_path() + '/templates/applications/icon.icns', path + '/res/icons/', True)


def copy_other_files(path):
    """Copy left over files to complete the project"""

    # copy readme files
    copyfile(get_wqt_path() + '/templates/readme/app-README.md.tpl',
             path + '/src/' + os.path.basename(path) + '/README.md')
    copyfile(get_wqt_path() + '/templates/readme/lib-README.md.tpl',
             path + '/lib' + '/README.md')

    # copy gitignore file
    copyfile(get_wqt_path() + '/templates/applications/gitignore.tpl',
             path + '/.gitignore')


def verify_project_structure(project_path, qt_type, override):
    """Verify if project has a proper structure, otherwise make a proper structure"""

    create_folder(project_path + '/src', override)
    create_folder(project_path + '/src/' + os.path.basename(project_path), override)
    create_folder(project_path + '/lib', override)
    create_folder(project_path + '/wqt', override)

    if qt_type == QType.WIDGETS or qt_type == QType.QUICK:
        create_folder(project_path + '/res', override)

        if get_platform() == OS.mac:
            create_folder(project_path + '/res/icons', override)

        if qt_type == QType.WIDGETS:
            create_folder(project_path + '/res/ui', override)
        else:
            create_folder(project_path + '/res/qml', override)

    # if src is empty, get src files
    if len(get_files(project_path + '/src')) == 0:
        # copy source files
        src_files = get_src_files(qt_type)

        for file in src_files:
            copyfile(file, project_path + '/src/' + os.path.basename(project_path), True)

    # copy icon files
    if get_platform() == OS.mac and (qt_type == QType.QUICK or qt_type == QType.WIDGETS):
        copyfile(get_wqt_path() + '/templates/applications/icon.icns', project_path + '/res/icons/', True)


def update_qml_resources(path):
    qt_type = get_qt_type(path)

    if not qt_type == QType.QUICK:
        return

    get_dirs = get_dirs_recursively(path + '/res/qml')
    q_resources_dict = {}

    n = 0

    for directory in get_dirs:
        rel_path = os.path.relpath(directory, path + '/res/qml')
        q_resource = 'qresource!' + str(n) + '!'

        if rel_path == '.':
            q_resources_dict[q_resource] = {'@prefix': '/'}
        else:
            q_resources_dict[q_resource] = {'@prefix': '/' + rel_path}

        # add all the files under that prefix
        y = 0
        files = get_files(directory, ['.qml'])

        for file in files:
            name = os.path.basename(file)
            q_resources_dict[q_resource]['file!' + str(y) + '!'] = rel_path + '/' + name
            y += 1

        n += 1

    # check of qml.qrc file exists, if not, copy the template
    copyfile(get_wqt_path() + '/templates/applications/quick/res/qml.qrc', path + '/res/qml/', True)

    with open(path + '/res/qml/qml.qrc') as fd:
        doc = xmltodict.parse(fd.read())

    doc['RCC'] = q_resources_dict
    string = xmltodict.unparse(doc, pretty=True)
    string = re.sub(r'![0-9]+!', '', string)

    # write back to the line
    with open(path + '/res/qml/qml.qrc', 'w') as fd:
        str_list = string.split('\n')

        for i in range(1, len(str_list)):
            fd.write(str(str_list[i]) + '\n')
