"""@package templates
Parses and completes the cmake templates
"""

from utils import helper


def parse_update(tpl_path, project_data):
    """reads the cmake template file and completes it using project data"""
    with open(tpl_path) as f:
        tpl_str = f.readlines()

    new_str = ''
    index = 0
    while index < len(tpl_str):
        curr_line = tpl_str[index]
        new_str += helper.fill_template(curr_line, project_data)
        index += 1

    # link libraries
    libraries = project_data['libraries-qt']
    link_str = ''

    for library in libraries:
        link_str += 'PUBLIC Qt5::'
        link_str += library
        link_str += ' '

    link_str = link_str.strip(' ')
    new_str = new_str.replace('{{link-libraries}}', link_str)

    with open(tpl_path, 'w') as f:
        f.write(new_str)
