import QtQuick
import QtQuick.Controls.Basic
ApplicationWindow {
    visible: true
    width: 360
    height: 600
    title: "HelloApp"
    property string currTime: "00:00:00"
    property QtObject backend
    Rectangle {
        anchors.fill: parent
        Image {
            sourceSize.width: parent.width
            sourceSize.height: parent.height
            source: "./images/bg.jpg"
            fillMode: Image.PreserveAspectFit
        }
        Text {
            anchors {
                bottom: parent.bottom
                bottomMargin: 12
                left: parent.left
                leftMargin: 12
            }
            text: currTime
            font.pixelSize: 48
            color: "white"
        }
    }

    Connections {
        target: backend
        function onUpdated(msg) {
            currTime = msg;
        }
    }
}