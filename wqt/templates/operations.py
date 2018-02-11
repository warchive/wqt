"""@package templates
This file helps perform operations on template files
"""

import sys
if sys.version_info < (3, 0):
    import ConfigParser as configparser
else:
    import configparser

import pystache


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


def parse_and_copy_cmake(cmake_file, path, config_file):
    """Parses template cmake files and fill them with info from config files"""

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

    with open(path, 'w') as f:
        f.write(filled_data)
