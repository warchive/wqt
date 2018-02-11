"""@package templates
This file helps perform operations on template files
"""

import os
import sys
import pystache

from wqt.templates.files import (
    get_config_file,
    get_cmake_file
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

    config_file = get_config_file(qt_type)
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


def fill_and_copy_config(qt_type, path):
    """fills the essential config information and writes the config file"""

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
