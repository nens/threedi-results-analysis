import QtQuick 2.0

Rectangle {
    width: 400
    height: 400

    Canvas {
        anchors.fill: parent
        onPaint: {
            var ctx = getContext("2d");
            ctx.reset();

            var centreX = width / 2;
            var centreY = height / 2;

            ctx.beginPath();
            ctx.fillStyle = "black";
            ctx.moveTo(centreX, centreY);
            ctx.arc(centreX, centreY, width / 4, 0, Math.PI * 2, false);
            ctx.lineTo(centreX, centreY);
            ctx.fill();
        }
    }
}


// url: "/home/nens/.local/share/QGIS/QGIS3/profiles/default/python/plugins/ThreeDiToolbox/layer_styles/tools/circle.qml"