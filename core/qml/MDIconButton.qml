import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import "MDIconGlyphs.js" as MaterialGlyphs

RoundButton {
    property string iconName
    property int size: 24
    property color color: Material.foreground

    width: size
    height: size

    contentItem: MDIcon { iconName: parent.iconName; color: parent.color; size: parent.size}
}