function Generate(network) {
    var $myCanvas = $('#MainCanvas');
    var nodes = network.nodes;
    var channels = network.channels;

    $myCanvas.clearCanvas();

    for (var i = 0; i < channels.length; i++) {
        var first_node = channels[i].start_node_id;
        var second_node = channels[i].end_node_id;
        $myCanvas.drawLine({
            layer: true,
            name: "channel" + first_node + second_node,
            strokeStyle: "black",
            strokeWidth: 3,
            draggable: true,
            x1: nodes[first_node].X, y1: nodes[first_node].Y,
            x2: nodes[second_node].X, y2: nodes[second_node].Y
        });
    }

    for(var i = 0; i < nodes.length; i++) {
        $myCanvas.drawArc({
            layer: true,
            draggable: true,
            bringToFront: true,
            name: "name" + i,
            fillStyle: "steelblue",
            x: nodes[i].X,
            y: nodes[i].Y,
            radius: 30,
            shadowX: -1, shadowY: 3,
            shadowBlur: i,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            drag: function(layer) {
                var layerName = layer.name;
                nodes[parseInt(layerName.slice(-1))].X = layer.x;
                nodes[parseInt(layerName.slice(-1))].Y = layer.y;
                nodes[parseInt(layerName.slice(-1))].channels.forEach(function (channel) {
                    var channelName = "channel" + channel.start_node_id + channel.end_node_id;
                    $myCanvas.getLayer(channelName).x1 = nodes[channel.start_node_id].X;
                    $myCanvas.getLayer(channelName).y1 = nodes[channel.start_node_id].Y;
                    $myCanvas.getLayer(channelName).x2 = nodes[channel.end_node_id].X;
                    $myCanvas.getLayer(channelName).y2 = nodes[channel.end_node_id].Y;
                });
                $myCanvas.getLayer("num"+parseInt(layerName.slice(-1))).x = layer.x;
                $myCanvas.getLayer("num"+parseInt(layerName.slice(-1))).y = layer.y
            }
        });
        $myCanvas.drawText({
          layer: true,
          name: "num" + i,
          fillStyle: '#9cf',
          strokeStyle: '#25a',
          strokeWidth: 2,
          x: nodes[i].X,
          y: nodes[i].Y,
          fontSize: 30,
          fontFamily: 'Verdana, sans-serif',
          text: i
        });
    }

}

$(document).ready(function() {

});