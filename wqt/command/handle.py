"""@package command
Handle building, listing, and showing WQt projects
"""

import json
import os
import shutil
import subprocess
from collections import OrderedDict

from colorama import Fore

from wqt.utils.finder import (
    get_cmake_program,
    get_generator_for,
    get_make_program,
    get_qmlscene_program,
    get_qmlviewer_program
)
from wqt.utils.helper import (
    get_files,
    get_files_recursively,
    get_dirs,
    get_valid_path,
    get_platform,
    get_qt_application
)
from wqt.utils.output import writeln, write
from . import creation


def get_usage(text, path):
    """Returns the code file where the resource is used"""

    list_usage = []
    for file in get_files_recursively(path + '/src/app'):
        with open(file) as f:
            for line in f:
                if text in line:
                    list_usage.append(file)

    return list_usage


def create_tracker(path):
    """Creates the tracker file"""

    tree_data = {}

    for i in get_files_recursively(path + '/res', ['.qml']):
        extension = os.path.splitext(i)[1]
        name_path = os.path.splitext(i)[0]

        tree_data[name_path + extension] = os.path.getmtime(name_path + extension)

    with open(path + '/wqt/tracker.json', 'w') as f:
        json.dump(tree_data, f, indent=2)


def update_tracker_and_action(path):
    """updates the tracker file and take actions"""

    if not os.path.exists(path + '/wqt/tracker.json'):
        created = True
        create_tracker(path)
    else:
        created = False

    with open(path + '/wqt/tracker.json') as f:
        tree_data = json.load(f)

    if os.path.exists(path + '/wqt/temp.txt'):
        os.remove(path + '/wqt/temp.txt')

    num_res_files = get_files_recursively(path + '/res', ['.qml'])
    num_entries = len(tree_data)

    if num_res_files != num_entries:
        create_tracker(path)
        created = True

    for key in tree_data:
        curr_last_modified = os.path.getmtime(key)
        last_modified = tree_data[key]

        if curr_last_modified > last_modified or created:
            usage_file_path = get_usage(os.path.basename(key), path)

            for file_path in usage_file_path:
                with open(file_path, 'a') as curr_file:
                    curr_file.write('#')

                with open(path + '/wqt/temp.txt', 'a') as temp_file:
                    temp_file.write(file_path)

            tree_data[key] = curr_last_modified

    with open(path + '/wqt/tracker.json', 'w') as f:
        json.dump(tree_data, f, indent=2)

    remove_action(path)

    return tree_data


def remove_action(path):
    """removes the extra action to trigger build"""

    if os.path.exists(path + '/wqt/temp.txt'):
        with open(path + '/wqt/temp.txt') as read_file:
            for line in read_file.readlines():
                print(line)
                with open(line) as read_code_file:
                    lines = read_code_file.readlines()

                with open(line, 'w') as write_code_file:
                    write_code_file.writelines([item for item in lines[:-1]])

        os.remove(path + '/wqt/temp.txt')


def build(path, generator=None, make=None, cmake=None):
    """build WQt project"""

    path = get_valid_path(path)

    writeln('WQt project build started', Fore.YELLOW)
    write('Verifying project structure - ', Fore.CYAN)

    application = get_qt_application(path)

    valid = False
    if os.path.exists(path + '/wqt') and os.path.exists(path + '/src') and os.path.exists(path + '/src/app') \
            and os.path.exists(path + '/res'):
        if application == 'widgets' and os.path.exists(path + '/res/ui'):
            valid = True
        elif application == 'quick' and os.path.exists(path + '/res/qml'):
            valid = True
        elif application == 'console':
            valid = True

    if valid:
        writeln('done')
    else:
        writeln('\nProject structure invalid, update the project', color=Fore.RED)
        quit(2)

    # check if build folder exists and if not make one
    if not os.path.exists(path + '/wqt/build'):
        os.mkdir(path + '/wqt/build')

    os.chdir(path + '/wqt/build')

    # check modifications to resource files
    update_tracker_and_action(path)

    cmake_program = cmake or get_cmake_program()
    make_program = make or get_make_program()

    write('Verifying cmake and make installs - ', Fore.CYAN)

    # check if cmake is in environment paths (unix/linux based systems)
    if not cmake_program:
        writeln('\ncmake does not exist, please install it or make sure it is in your environment PATH', Fore.RED)
        quit(2)

    # check if make is in environment paths (unix/linux based systems)
    if not make_program:
        writeln('\nmake does not exist, please install it or make sure it is in your environment PATH', Fore.RED)
        quit(2)

    writeln('done')

    if generator is None:
        generator = get_generator_for(make_program)

    writeln('Running the build using cmake and ' + str(generator), Fore.CYAN)
    cmake_code = subprocess.call(['cmake', '-G', str(generator), '../..'])

    if cmake_code != 0:
        writeln('Project build unsuccessful, cmake exited with error code ' + str(cmake_code), Fore.RED)
        quit(2)

    make_code = subprocess.call([make_program])

    if make_code != 0:
        writeln('Project build unsuccessful, make exited with error code ' + str(make_code), Fore.RED)
        quit(2)

    writeln('Project successfully built', Fore.YELLOW)


def clean(path):
    """clean WQt project's build folder"""

    path = get_valid_path(path)

    # confirm if bin folder/path exists
    if not os.path.exists(path + '/wqt/build'):
        writeln('No build files to clean', color=Fore.YELLOW)
        quit(2)

    # check if the current build files are for the current board
    # clean and build if boards are different
    try:
        write('Cleaning build files - ', Fore.CYAN)

        for folder in get_dirs(path + '/wqt/build'):
            shutil.rmtree(folder)

        for file in get_files(path + '/wqt/build'):
            os.unlink(file)
    except IOError:
        writeln('Error while cleaning build files', Fore.CYAN)

    shutil.rmtree(path + '/wqt/build')

    writeln('done')
    writeln('Project build files cleaned', color=Fore.YELLOW)


def list_types():
    """lists WQt application types supported"""

    writeln('Application types supported are: ', color=Fore.YELLOW)
    writeln('widgets', color=Fore.CYAN)
    writeln('quick', color=Fore.CYAN)
    writeln('console', color=Fore.CYAN)
    writeln('#################################')
    write('Example usage: ', color=Fore.YELLOW)
    writeln('wqt create widgets', color=Fore.YELLOW)


def add_lib(path, name):
    """add Qt library to the project"""

    path = get_valid_path(path)

    write('Adding library named ' + name + ' - ', color=Fore.CYAN)

    # load config file as json
    with open(path + '/config.json') as f:
        config_data = json.load(f, object_pairs_hook=OrderedDict)

    if not str(name) in config_data['libraries-qt']:
        config_data['libraries-qt'].append(str(name))
    else:
        writeln('\nLibrary already exist, libraries are: ' + ' '.join(config_data['libraries-qt']),
                color=Fore.YELLOW)
        quit(2)

    # write the project name to config file
    with open(path + '/config.json', 'w') as f:
        json.dump(config_data, f, indent=2)

    writeln('done')
    writeln('Libraries left are: ' + ' '.join(config_data['libraries-qt']), color=Fore.YELLOW)
    writeln('#################################################################################')
    writeln('Updating CMake files: ', color=Fore.CYAN)
    creation.update(path)


def rm_lib(path, name):
    """remove Qt library from the project"""

    path = get_valid_path(path)

    write('Removing library named ' + name + ' - ', color=Fore.CYAN)

    # load config file as json
    with open(path + '/config.json') as f:
        config_data = json.load(f, object_pairs_hook=OrderedDict)

    if str(name) in config_data['libraries-qt']:
        config_data['libraries-qt'].remove(str(name))
    else:
        writeln('\nNo such library to remove, libraries are: ' + ' '.join(config_data['libraries-qt']),
                color=Fore.YELLOW)
        quit(2)

    # write the project name to config file
    with open(path + '/config.json', 'w') as f:
        json.dump(config_data, f, indent=2)

    writeln('done')
    writeln('Libraries left are: ' + ' '.join(config_data['libraries-qt']), color=Fore.YELLOW)
    writeln('#################################################################################')
    writeln('Updating CMake files: ', color=Fore.CYAN)
    creation.update(path)


def list_libs(path):
    """list Qt library used for the project"""

    path = get_valid_path(path)

    writeln('Libraries used in the projects:', color=Fore.YELLOW)

    # load config file as json
    with open(path + '/config.json') as f:
        config_data = json.load(f, object_pairs_hook=OrderedDict)

    for lib in config_data['libraries-qt']:
        writeln(lib, color=Fore.CYAN)


def run(path, generator=None, cmake=None, make=None):
    """open the binary executable file"""

    path = get_valid_path(path)

    build(path, generator, cmake, make)

    with open(path + '/config.json') as f:
        config_data = json.load(f)

    executable = config_data['name-project']

    if get_platform() == 'OS X':
        subprocess.call(['open', path + '/bin/' + executable + '.app'])
    elif get_platform() == 'Windows':
        subprocess.call([path + '/bin/' + executable + '.exe'])
    else:
        subprocess.call([path + '/bin/' + executable])


def list_qml(path):
    """list qml files in the project"""

    path = get_valid_path(path)

    if get_qt_application(path) == 'quick':
        writeln('This project is not a Qt Quick project so no qml files', color=Fore.YELLOW)
        quit(2)

    writeln('Qml files for this project: ', color=Fore.YELLOW)
    files = get_files(path + '/res/qml')

    for file in files:
        if os.path.splitext(file)[1] == '.qml':
            writeln(os.path.basename(file), color=Fore.CYAN)


def preview_qml(path, name):
    """preview qml file"""

    path = get_valid_path(path)

    if not os.path.exists(path + '/wqt/quick'):
        writeln('This project is not a Qt Quick project so no qml preview :(', color=Fore.YELLOW)
        quit(2)

    qml_path = ''

    if os.path.exists(path + '/res/qml/' + name):
        qml_path = path + '/res/qml/' + name
    elif os.path.exists(path + '/res/qml/' + name + '.qml'):
        qml_path = path + '/res/qml/' + name + '.qml'

    if get_qmlscene_program():
        subprocess.call(['qmlscene', qml_path])
    elif get_qmlviewer_program():
        subprocess.call(['qmlviewer', qml_path])
    else:
        writeln('No Qml viewer program install please install qmlscene or qmlviewer', color=Fore.RED)
        quit(2)
