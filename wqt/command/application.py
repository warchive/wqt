from shutil import copyfile


def copy_application_files(application, templates_path, path):
    if application == 'widgets':
        copy_widget_files(templates_path, path)
    elif application == 'quick':
        copy_widget_files(templates_path, path)
    elif application == 'console':
        copy_console_files(templates_path, path)


def copy_widget_files(templates_path, path):
    copyfile(templates_path + '/widgets/main.cpp', path + '/src/app/main.cpp')
    copyfile(templates_path + '/widgets/mainwindow.cpp', path + '/src/app/mainwindow.cpp')
    copyfile(templates_path + '/widgets/mainwindow.h', path + '/src/app/mainwindow.h')
    copyfile(templates_path + '/widgets/mainwindow.ui', path + '/res/ui/mainwindow.ui')


def copy_quick_files(templates_path, path):
    copyfile(templates_path + '/quick/main.cpp', path + '/src/app/main.cpp')
    copyfile(templates_path + '/quick/main.qml', path + '/res/qml/main.qml')


def copy_console_files(templates_path, path):
    copyfile(templates_path + '/console/main.cpp', path + '/src/app/main.cpp')

