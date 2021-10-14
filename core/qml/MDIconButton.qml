import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import "MDIconGlyphs.js" as MaterialGlyphs

Item {
    property int size: 24
    property string icon
    property color color: Material.foreground

    signal clicked()

    id: root
    width: size
    height: size

    RoundButton {
        width: root.size
        height: root.size
        
        contentItem: MDIcon { icon: root.icon; color: root.color; size: root.size}
        onPressed: root.clicked()
    }
}