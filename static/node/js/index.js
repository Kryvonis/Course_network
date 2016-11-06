function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');
var network = 0;
function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie != '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) == (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        }
    }
});

function Generate(local_net){
    network = local_net;
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
                name: first_node + "channel" + second_node,
                groups: ["channel_and_text" + i],
                dragGroups: ["channel_and_text" + i],
                strokeStyle: "black",
                strokeWidth: 2,
                draggable: true,
                x1: find_node(nodes, first_node).X, y1: find_node(nodes, first_node).Y,
                x2: find_node(nodes, second_node).X, y2: find_node(nodes, second_node).Y,
                // contextmenu: function (layer) {
                //     var node_1 = layer.name.match(/\d+/g)[0];
                //     var node_2 = layer.name.match(/\d+/g)[1];
                //     var channel = find_channel(channels, node_1, node_2);
                //     var modal_window = $('#modal_form');
                //
                //     modal_window.find('#weight').val(channel.weight);
                //     modal_window.find('#error_prob').val(channel.error_prob);
                //     modal_window.find('#type').val(channel.type);
                //     $('#overlay').fadeIn(100, function() {
                //         $('#modal_form')
                //             .css('display', 'block')
                //             .animate({opacity: 1, top: '50%'}, 100);
                //     });
                //
                //     $('#update_channel').on("click", function() {
                //         close_modal_window();
                //         update_channel(channel);
                //         location.reload();
                //     });
                // },
                mouseover: function (layer) {
                    $myCanvas.getLayer(layer.name).strokeWidth = 8;
                },
                mouseout: function (layer) {
                    $myCanvas.getLayer(layer.name).strokeWidth = 2;
                }
            })
        }

        for(var i = 0; i < nodes.length; i++) {
            $myCanvas.drawArc({
                layer: true,
                draggable: true,
                // bringToFront: true,
                name: "name" + i,
                groups: ["node_and_text" + i],
                dragGroups: ["node_and_text" + i],
                fillStyle: "steelblue",
                x: nodes[i].X, y: nodes[i].Y,
                radius: 30,
                shadowX: -1, shadowY: 8,
                shadowBlur: i,
                shadowColor: 'rgba(0, 0, 0, 0.8)',
                drag: function(layer) {
                    var layerName = layer.name;
                    nodes[layerName.match(/\d+/)[0]].X = layer.x;
                    nodes[layerName.match(/\d+/)[0]].Y = layer.y;
                    nodes[layerName.match(/\d+/)[0]].channels.forEach(function (channel) {
                        var channelName = channel.start_node_id + "channel" + channel.end_node_id;
                        var channelWeight = channel.start_node_id + "channel_weight" + channel.end_node_id;
                        $myCanvas.getLayer(channelName).x1 = find_node(nodes, channel.start_node_id).X;
                        $myCanvas.getLayer(channelName).y1 = find_node(nodes, channel.start_node_id).Y;
                        $myCanvas.getLayer(channelName).x2 = find_node(nodes, channel.end_node_id).X;
                        $myCanvas.getLayer(channelName).y2 = find_node(nodes, channel.end_node_id).Y;
                        // $myCanvas.getLayer(channelWeight).x = ($myCanvas.getLayer(channelName).x1 +
                        //                                         $myCanvas.getLayer(channelName).x2) / 2;
                        // $myCanvas.getLayer(channelWeight).y = ($myCanvas.getLayer(channelName).y1 +
                        //                                         $myCanvas.getLayer(channelName).y2) / 2;
                    });
                },
                dragstop: function() {
                    save_network_state();
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
    // for (var i = 0; i < channels.length; i++) {
    //     var first_node = channels[i].start_node_id;
    //     var second_node = channels[i].end_node_id;
    //     $myCanvas.drawLine({
    //         layer: true,
    //         name: "channel" + first_node + second_node,
    //         strokeStyle: "black",
    //         strokeWidth: 3,
    //         draggable: true,
    //         x1: nodes[first_node].X, y1: nodes[first_node].Y,
    //         x2: nodes[second_node].X, y2: nodes[second_node].Y
    //     });
    // }
    //
    // for (var i = 0; i < nodes.length; i++) {
    //     $myCanvas.drawArc({
    //         layer: true,
    //         draggable: true,
    //         groups: ["node_and_text" + i],
    //         dragGroups: ["node_and_text" + i],
    //         name: "name_" + i,
    //         fillStyle: "steelblue",
    //         x: nodes[i].X,
    //         y: nodes[i].Y,
    //         radius: 30,
    //         shadowX: -1, shadowY: 3,
    //         shadowBlur: i,
    //         shadowColor: 'rgba(0, 0, 0, 0.5)',
    //         drag: function (layer) {
    //             var layerName = layer.name;
    //             nodes[parseInt(layer.name.split('_').pop())].X = layer.x;
    //             nodes[parseInt(layer.name.split('_').pop())].Y = layer.y;
    //             nodes[parseInt(layer.name.split('_').pop())].channels.forEach(function (channel) {
    //                 var channelName = "channel" + channel.start_node_id + channel.end_node_id;
    //                 $myCanvas.getLayer(channelName).x1 = find_node(nodes, channel.start_node_id).X;
    //                 $myCanvas.getLayer(channelName).y1 = find_node(nodes, channel.start_node_id).Y;
    //                 $myCanvas.getLayer(channelName).x2 = find_node(nodes, channel.end_node_id).X;
    //                 $myCanvas.getLayer(channelName).y2 = find_node(nodes, channel.end_node_id).Y;
    //             });
    //         },
    //         dragstop: function (layer) {
    //             $.ajax({
    //                 url: 'save',
    //                 type: 'POST',
    //                 data: JSON.stringify(network),
    //                 contentType: 'application/json; charset=utf-8',
    //                 dataType: 'json',
    //                 async: false,
    //             });
    //         }
    //     }).drawText({
    //         layer: true,
    //         groups: ["node_and_text" + i],
    //         text: nodes[i].id,
    //         fontSize: 20,
    //         name: "node_number" + i,
    //         x: nodes[i].X, y: nodes[i].Y,
    //         fillStyle: 'white',
    //         strokeStyle: 'white',
    //         strokeWidth: 1,
    //     });
    // }

// }

function find_node(nodes, id) {
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].id == id)
            return nodes[i];
    }
}
function add_node() {
    $.ajax({
        url: 'node/add',
        type: 'POST',
        data: "",
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
}
function save_network_state() {
    $.ajax({
        url: 'save',
        type: 'POST',
        data: JSON.stringify(network),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: false,
    });
}
function remove_node() {
    var id = document.getElementById('remove_node_id').value;
    $.ajax({
        url: 'node/remove/'+id,
        type: 'POST',
        data: JSON.stringify(id),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
}