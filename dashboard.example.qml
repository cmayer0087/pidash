import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow {
    Material.theme: Material.Dark
    Material.accent: Material.Purple

    title: "PiDash"
    width: 800
    height: 480

    Column {
        anchors.fill: parent
        padding: 10

        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "PiDash"
            font.pixelSize: 100
        }

        Label {
            anchors.horizontalCenter: parent.horizontalCenter
            text: "PiDash is intended for creating a dashboard for a raspberry pi.\n"
                + "You can use connectors to display and control remote devices.\n"
                + "e.g. For Home Assisntant use the homeassistnat connector\n"
                + "\n"
                + "There is also a local 'connector' to display and control local stuff.\n"
                + "Like which time it is or wich hostname this machine has:\n"
                + "  - Time: " + cons.local.dateTime.toLocaleTimeString("hh:MM") + "\n"
                + "  - Hostname: " + cons.local.hostname + "\n"
                + "\n"
                + "This is all about creating a custom dashboard, so this small helptext is all the gui this is shipped with.\n"
                + "To customize this copy the dashboard.example.qml to dashboard.qml and write your very own dashboard.\n"
                + "This is a qml file from qt5 so see https://doc.qt.io/Qt-5/qmltypes.html for more informations.\n"
                + "\n"
                + "The configured connectors can be accessed through cons.<NAME> like cons.local.dateTime.\n"
                + "Configuration values can be accessed by their name directly like key1 in this example:\n"
                + "  - Key1: " + key1 + "\n"
                + "  - Key2: " + key2 + "\n"
        }
    }
}