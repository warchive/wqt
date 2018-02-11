#include <QGuiApplication>
#include <QQmlApplicationEngine>
#include <ResourceManager.h>

int main(int argc, char *argv[]) {
#if defined(Q_OS_WIN)
    QCoreApplication::setAttribute(Qt::AA_EnableHighDpiScaling);
#endif

    QGuiApplication app(argc, argv);

    auto literal = getResource("qml/main.qml");

    QQmlApplicationEngine engine;
    engine.load(QUrl(literal));
    if (engine.rootObjects().isEmpty())
        return -1;

    return app.exec();
}
