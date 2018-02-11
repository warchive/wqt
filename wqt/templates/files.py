"""This helps in getting template resources based on OS"""

from wqt.utils.helper import (
    OS,
    get_wqt_path,
    get_platform
)


class QType:
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


def get_cmake(qt_type):
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

