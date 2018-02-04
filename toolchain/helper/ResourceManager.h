#ifndef RESOURCEMANAGER_H
#define RESOURCEMANAGER_H

#include <QGuiApplication>
#include <QString>
#include <QDir>

QString getResource(QString relativePath) {
    auto path = QDir(QGuiApplication::applicationDirPath());
    auto resourceDir = path.absolutePath() + "/Resources/";

#if defined(__APPLE__)
    return path.absolutePath() + "/../Resources/" + relativePath;
#endif

    return resourceDir + relativePath;
}


#endif //RESOURCEMANAGER_H
