function Generate(network) {
    var $myCanvas = $('#MainCanvas');
    var nodes = network.nodes;
    var channels = network.channels;

    $myCanvas.removeLayers();
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
            groups: ["node_and_text" + i],
            dragGroups: ["node_and_text" + i],
            name: "name_" + i,
            fillStyle: "steelblue",
            x: nodes[i].X,
            y: nodes[i].Y,
            radius: 30,
            shadowX: -1, shadowY: 3,
            shadowBlur: i,
            shadowColor: 'rgba(0, 0, 0, 0.5)',
            drag: function(layer) {
                var layerName = layer.name;
                nodes[parseInt(layer.name.split('_').pop())].X = layer.x;
                nodes[parseInt(layer.name.split('_').pop())].Y = layer.y;
                nodes[parseInt(layer.name.split('_').pop())].channels.forEach(function (channel) {
                    var channelName = "channel" + channel.start_node_id + channel.end_node_id;
                    $myCanvas.getLayer(channelName).x1 = find_node(nodes, channel.start_node_id).X;
                    $myCanvas.getLayer(channelName).y1 = find_node(nodes, channel.start_node_id).Y;
                    $myCanvas.getLayer(channelName).x2 = find_node(nodes, channel.end_node_id).X;
                    $myCanvas.getLayer(channelName).y2 = find_node(nodes, channel.end_node_id).Y;
                });
            }
        }).drawText({
            layer: true,
            groups: ["node_and_text" + i],
            text: nodes[i].id,
            fontSize: 20,
            name: "node_number" + i,
            x: nodes[i].X, y: nodes[i].Y,
            fillStyle: 'white',
            strokeStyle: 'white',
            strokeWidth: 1
        });
    }

}

function find_node(nodes, id) {
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].id == id)
            return nodes[i];
    }
}