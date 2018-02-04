"""@package command
Handle building, listing, and showing WQt projects
"""

import os
import subprocess
import shutil

from utils.helper import (
    create_folder,
    linux_path,
    get_working_directory,
    get_wqt_path,
    get_files,
    get_dirs
)
from utils.finder import (
    get_cmake_program,
    get_generator_for,
    get_make_program,
)

from utils.output import writeln, write
from colorama import Fore


def verify_path(path):
    """check if the project path is correct"""

    if not os.path.exists(path) or not os.path.isdir(path):
        writeln('Path specified for project creation does not exist or is not a directory', color=Fore.RED)
        quit(2)


def build(path, generator=None, make=None, cmake=None):
    """build WQt project"""

    if path is None:
        path = get_working_directory()
    else:
        path = linux_path(os.path.abspath(path))

    verify_path(path)

    writeln('WQt project build started', Fore.CYAN)

    write('Verifying project structure', Fore.CYAN)

    if os.path.exists(path + '/wqt/console'):
        application = 'console'
    elif os.path.exists(path + '/wqt/quick'):
        application = 'quick'
    elif os.path.exists(path + '/wqt/widgets'):
        application = 'widgets'
    else:
        application = None

    valid = False

    if os.path.exists(path + '/wqt') and os.path.exists(path + '/src') and os.path.exists(path + '/src/app') \
            and os.path.exists(path + '/res'):
        if application == 'widgets' and os.path.exists(path + '/res/ui'):
            valid = True
        elif application == 'quick' and os.path.exists(path + '/res/qt'):
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

    pass


def clean(path):
    """clean WQt project's build folder"""

    if path is None:
        path = get_working_directory()
    else:
        path = linux_path(os.path.abspath(path))

    verify_path(path)

    path = str(path)

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
    writeln('Project build files cleaned')


def list_types():
    """lists WQt application types supported"""
    writeln('Application types supported are: ', color=Fore.YELLOW)
    writeln('widgets', color=Fore.CYAN)
    writeln('quick', color=Fore.CYAN)
    writeln('console', color=Fore.CYAN)
    write('Example usage: ', color=Fore.YELLOW)
    writeln('wqt create widgets', color=Fore.CYAN)


def add_lib(path, name):
    """add Qt library to the project"""


def rm_lib(path, name):
    """remove Qt library from the project"""


def list_qml(path):
    """list qml files in the project"""
    pass


def preview_qml(path, name):
    """preview qml file"""
    pass
