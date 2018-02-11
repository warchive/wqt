"""@package command
Handle building, listing, and showing WQt projects
"""

import os
import shutil
import subprocess

from colorama import Fore

from wqt.command.resource import (
    get_configuration,
    set_configuration
)
from wqt.templates.files import QType
from wqt.utils.finder import (
    get_cmake_program,
    get_generator_for,
    get_make_program,
    get_qmlscene_program,
    get_qmlviewer_program
)
from wqt.utils.helper import (
    get_files,
    get_dirs,
    get_valid_path,
    get_platform,
    any_folders_exist,
    OS
)
from wqt.utils.output import writeln, write
from . import creation


def build(path, generator=None, make=None, cmake=None):
    """build WQt project"""

    path = get_valid_path(path)

    # verify there is a wqt folder
    if not any_folders_exist(path + '/wqt'):
        writeln("build files do not exist (wqt folder), aborting", Fore.RED)
        quit(2)

    writeln('WQt project build started', Fore.YELLOW)

    # check if build folder exists and if not make one
    if not any_folders_exist(path + '/wqt/build'):
        os.mkdir(path + '/wqt/build')

    os.chdir(path + '/wqt/build')

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

    # confirm if build folder/path exists
    if not any_folders_exist(path + '/wqt/build'):
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

    libraries = get_configuration(path, 'library', 'qt')

    if not str(name) in libraries.split():
        libraries += ' ' + name
        set_configuration(path, 'library', 'qt', libraries)
    else:
        writeln('\nLibrary already exist, libraries are: ' + libraries, color=Fore.RED)
        quit(2)

    writeln('done')
    string_libs = 'Libraries left are: ' + libraries
    writeln(string_libs, color=Fore.YELLOW)

    for i in range(0, len(string_libs)):
        write('#')
    writeln('')

    creation.update(path)


def rm_lib(path, name):
    """remove Qt library from the project"""

    path = get_valid_path(path)

    write('Removing library named ' + name + ' - ', color=Fore.CYAN)

    libraries = get_configuration(path, 'library', 'qt')
    libraries_list = libraries.split()

    if str(name) in libraries_list:
        libraries_list.remove(str(name))
        set_configuration(path, 'library', 'qt', ' '.join(libraries_list))
    else:
        writeln('\nNo such library to remove, libraries are: ' + libraries_list, color=Fore.YELLOW)
        quit(2)

    writeln('done')
    string_libs = 'Libraries left are: ' + ' '.join(libraries_list)
    writeln(string_libs, color=Fore.YELLOW)

    for i in range(0, len(string_libs)):
        write('#')
    writeln('')

    creation.update(path)


def list_libs(path):
    """list Qt library used for the project"""

    path = get_valid_path(path)

    writeln('Libraries used in the projects:', color=Fore.YELLOW)

    libraries = get_configuration(path, 'library', 'qt')
    libraries_list = libraries.split()

    for lib in libraries_list:
        writeln(lib, color=Fore.CYAN)


def run(path, generator=None, cmake=None, make=None):
    """open the binary executable file"""

    path = get_valid_path(path)

    build(path, generator, cmake, make)

    executable = get_configuration(path, 'project', 'name')
    qt_type = get_configuration(path, 'project', 'type')

    if get_platform() == OS.mac:
        if qt_type == QType.CONSOLE:
            os.system('cls' if os.name == 'nt' else 'clear')
            subprocess.call([path + '/bin/' + executable])
            quit(2)
        subprocess.call(['open', path + '/bin/' + executable + '.app'])
    elif get_platform() == OS.windows:
        subprocess.call([path + '/bin/' + executable + '.exe'])
    else:
        subprocess.call(['./' + path + '/bin/' + executable])


def list_qml(path):
    """list qml files in the project"""

    path = get_valid_path(path)

    if not get_configuration(path, 'project', 'type') == QType.QUICK:
        writeln('This project is not a Qt Quick project so no qml files', color=Fore.RED)
        quit(2)

    writeln('Qml files for this project: ', color=Fore.YELLOW)
    files = get_files(path + '/res/qml')

    for file in files:
        if os.path.splitext(file)[1] == '.qml':
            writeln(os.path.basename(file), color=Fore.CYAN)


def preview_qml(path, name):
    """preview qml file"""

    path = get_valid_path(path)

    if not get_configuration(path, 'project', 'type') == QType.QUICK:
        writeln('This project is not a Qt Quick project so no qml preview :(', color=Fore.RED)
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
