import QtQuick 2.9


Rectangle {
    width: 100
    height: 100
    color: "steelblue"
    Text{ text: "shape: " + expression.evaluate("\"shape\"") }

    Component.onCompleted: console.log(expression.evaluate(" @project_path "));

    MouseArea {
        anchors.fill: parent
        onClicked: {
            parent.color = "red"
        }
    }
}