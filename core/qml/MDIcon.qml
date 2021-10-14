import QtQuick 2.15
import QtQuick.Controls.Material 2.15
import "MDIconGlyphs.js" as MaterialGlyphs

Item {
    property int size: 24
    property string icon
    property color color: Material.foreground

    width: size
    height: size

    Text {
        anchors.fill: parent

        color: parent.color

        font.family: materialFont.name
        font.pixelSize: parent.height

        text: MaterialGlyphs.glyphs[parent.icon]
    }

    FontLoader {
        id: materialFont
        source: "./materialdesignicons-webfont.ttf"
    }

    Component.onCompleted: console.assert(MaterialGlyphs.glyphs[icon], "Icon with name '" + icon + "' not found")
}
