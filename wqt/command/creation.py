"""@package command
Handle creation, and update of WQt projects
"""

from colorama import Fore

from wqt.utils.helper import (
    any_folders_exist,
    get_files,
    get_dirs,
    get_valid_path,
)
from wqt.utils.output import (
    writeln,
    write
)
from wqt.templates.operations import (
    fill_and_copy_config,
    parse_and_copy_cmake,
    copy_application_files,
    copy_other_files,
    verify_project_structure
)
from wqt.toolchain.operations import (
    copy_toolchain_files
)
from wqt.command.resource import (
    get_qt_type
)


def create(path, application):
    """Creates WQt project from scratch"""

    path = get_valid_path(path)

    # check if there are files in the folder
    if get_dirs(path) or get_files(path):
        if any_folders_exist([path + '/src', path + '/lib', path + '/res']):
            writeln('There is already a src/lib/res folder in this directory. Use wqt update instead',
                    color=Fore.RED)
            quit(2)

    writeln('Creating Qt ' + application + ' project', color=Fore.YELLOW)
    write('Copying required files and applying configuration - ', color=Fore.CYAN)

    verify_project_structure(path, application, True)
    fill_and_copy_config(application, path)
    parse_and_copy_cmake(application, path)
    copy_application_files(application, path)
    copy_toolchain_files(path)
    copy_other_files(path)

    writeln('done')
    writeln('Qt project created', color=Fore.YELLOW)


def update(path):
    """Updates existing WQt project"""

    path = get_valid_path(path)
    qt_type = get_qt_type(path)

    if qt_type is None:
        writeln('Cannot determine project Qt type, recreate the project!', Fore.RED)
        quit(2)

    writeln('Updating Wqt ' + qt_type + ' project', color=Fore.YELLOW)
    write('Updating Qt work environment - ', color=Fore.CYAN)

    verify_project_structure(path, qt_type, False)
    fill_and_copy_config(qt_type, path, True)
    parse_and_copy_cmake(qt_type, path)
    copy_toolchain_files(path)

    writeln('done')
    writeln('Qt project updated', color=Fore.YELLOW)
