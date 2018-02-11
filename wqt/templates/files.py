"""@package templates
This helps in getting template resources based on OS
"""

from wqt.utils.helper import (
    OS,
    get_wqt_path,
    get_platform,
    get_files_recursively
)


class QType:
    """Type of Qt application"""

    QUICK = 0
    WIDGETS = 1
    CONSOLE = 2


def __get_cmake_quick(os):
    """Based on the OS return the quick cmake template"""

    quick_path = get_wqt_path() + '/templates/cmake/quick'

    if os == OS.mac:
        return quick_path + '/osx/CMakeLists.txt'
    else:
        return quick_path + '/others/CMakeLists.txt'


def __get_cmake_widgets(os):
    """Based on the OS return the widgets cmake template"""

    widgets_path = get_wqt_path() + '/templates/cmake/widgets'

    if os == OS.mac:
        return widgets_path + '/osx/CMakeLists.txt'
    else:
        return widgets_path + '/others/CMakeLists.txt'


def __get_cmake_console():
    """Based on the OS return the console cmake template"""
    console_path = get_wqt_path() + '/templates/cmake/console'

    return console_path + '/CMakeLists.txt'


def get_cmake_file(qt_type):
    """Returns the path for cmake template file for the qt type specified"""

    os = get_platform()

    if qt_type == QType.QUICK:
        return __get_cmake_quick(os)
    elif qt_type == QType.WIDGETS:
        return __get_cmake_widgets(os)
    elif qt_type == QType.CONSOLE:
        return __get_cmake_console()
    else:
        raise ValueError('Type of Qt application not valid')


def __get_config_quick(os):
    """Based on the OS return the quick properties file"""

    quick_path = get_wqt_path() + '/templates/config/quick'

    if os == OS.mac:
        return quick_path + '/osx/properties.ini'
    else:
        return quick_path + '/others/properties.ini'


def __get_config_widgets(os):
    """Based on the OS return the widgets properties file"""

    widgets_path = get_wqt_path() + '/templates/config/widgets'

    if os == OS.mac:
        return widgets_path + '/osx/properties.ini'
    else:
        return widgets_path + '/others/properties.ini'


def __get_config_console():
    """Based on the OS return the console properties file"""

    console_path = get_wqt_path() + '/templates/config/console'
    return console_path + '/properties.ini'


def get_config_file(qt_type):
    """Returns the config file based on the OS"""

    os = get_platform()

    os = get_platform()

    if qt_type == QType.QUICK:
        return __get_config_quick(os)
    elif qt_type == QType.WIDGETS:
        return __get_config_widgets(os)
    elif qt_type == QType.CONSOLE:
        return __get_config_console()
    else:
        raise ValueError('Type of Qt application not valid')


def get_src_files(qt_type):
    """Returns the src files for the application type"""

    application_path = get_wqt_path() + '/templates/applications'

    if qt_type == QType.QUICK:
        return get_files_recursively(application_path + '/quick/src')
    elif qt_type == QType.WIDGETS:
        return get_files_recursively(application_path + '/widgets/src')
    elif qt_type == QType.CONSOLE:
        return get_files_recursively(application_path + '/console/src')
    else:
        raise ValueError('Type of Qt application not valid')


def get_res_files(qt_type, ext):
    """Returns the resource files for the application type"""

    application_path = get_wqt_path() + '/templates/applications'

    if qt_type == QType.QUICK:
        return get_files_recursively(application_path + '/quick/res', ext)
    elif qt_type == QType.WIDGETS:
        return get_files_recursively(application_path + '/widgets/res', ext)
    elif qt_type == QType.CONSOLE:
        return get_files_recursively(application_path + '/console/res', ext)
    else:
        raise ValueError('Type of Qt application not valid')
