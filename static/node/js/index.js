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
                draggable: false,
                x1: find_node(nodes, first_node).X, y1: find_node(nodes, first_node).Y,
                x2: find_node(nodes, second_node).X, y2: find_node(nodes, second_node).Y,
                contextmenu: function (layer) {
                    var node_1 = layer.name.match(/\d+/g)[0];
                    var node_2 = layer.name.match(/\d+/g)[1];
                    var channel = find_channel(channels, node_1, node_2);
                    var modal_window = $('#modal_form');

                    modal_window.find('#weight').text(channel.weight);
                    modal_window.find('#error_prob').text(channel.error_prob);
                    modal_window.find('#type').text(channel.type);
                    $('#overlay').fadeIn(100, function() {
                     $('#modal_form')
                         .css('display', 'block')
                         .animate({opacity: 1, top: '50%'}, 100);
                    });

                },
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
                contextmenu: function (layer) {
                    var modal_window = $('#modal_form_node');
                    var node_id = layer.name.match(/\d+/g)[0];
                    var node = find_node(nodes, node_id);
                    modal_window.find('#id_node').text(node.id);
                    modal_window.find('#table_node').text(JSON.stringify(node.table.metric,null,4));
                    modal_window.find('#table_node_path').text(JSON.stringify(node.table.path,null,4));
                    modal_window.find('#address_node').text(node.address);
                    $('#overlay_node').fadeIn(100, function() {
                     $('#modal_form_node')
                         .css('display', 'block')
                         .animate({opacity: 1, top: '50%'}, 100);
                    });

                },
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
                },

            }).drawText({
                layer: true,
                groups: ["node_and_text" + i],
                text: nodes[i].address,
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
function find_node_by_address(nodes, address) {
    for (var i = 0; i < nodes.length; i++) {
        if (nodes[i].address == address)
            return nodes[i];
    }
}
function find_channel(channels, first_node, second_node) {
    for (var i = 0; i < channels.length; i++) {
        if (channels[i].start_node_id == first_node && channels[i].end_node_id == second_node)
            return channels[i];
    }
}
function close_modal_window() {
    $('#modal_form').animate({opacity: 0, top: '45%'}, 100,
        function() {
            $(this).css('display', 'none');
            $('#overlay').fadeOut(200);
        }
    );
}
function close_modal_window_node() {
    $('#modal_form_node').animate({opacity: 0, top: '45%'}, 100,
        function() {
            $(this).css('display', 'none');
            $('#overlay_node').fadeOut(200);
        }
    );
}

function add_node() {
    var address = document.getElementById('add_node_address').value;
    $.ajax({
        url: 'node/add',
        type: 'POST',
        data: JSON.stringify({'address':address}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
    location.reload();
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
    var address = document.getElementById('remove_node_address').value;
    var id = find_node_by_address(network.nodes,address).id
    $.ajax({
        url: 'node/remove/'+id,
        type: 'POST',
        data: JSON.stringify(id),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
}

function add_channel() {
    var start_node_id = find_node_by_address(network.nodes,
    document.getElementById('add_start_node_id').value).id;
    var end_node_id = find_node_by_address(network.nodes,
    document.getElementById('add_end_node_id').value).id;

    $.ajax({
        url: 'channel/add',
        type: 'POST',
        data: JSON.stringify({'start_node_id':start_node_id,'end_node_id':end_node_id}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
}
function remove_channel() {
    var start_node_id = find_node_by_address(network.nodes,
    document.getElementById('remove_start_node_id').value).id;
    var end_node_id = find_node_by_address(network.nodes,
    document.getElementById('remove_end_node_id').value).id;
    $.ajax({
        url: 'channel/remove',
        type: 'POST',
        data: JSON.stringify({'start_node_id':start_node_id,'end_node_id':end_node_id}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
}
function regenerate() {
    var average_nums_id = document.getElementById('average_nums_id').value;
    var node_nums_id = document.getElementById('node_nums_id').value;
    $.ajax({
        url: 'regenerate',
        type: 'POST',
        data: JSON.stringify({'average_nums':average_nums_id,'node_nums':node_nums_id}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
    location.reload();
}

function send_datagram() {
    var start_node_id = document.getElementById('datagram_start_node_id').value;
    var end_node_id = document.getElementById('datagram_end_node_id').value;
    var info_size = document.getElementById('datagram_info_size_id').value;

    $.ajax({
        url: 'message/datagram',
        type: 'POST',
        data: JSON.stringify({'start_node_address':start_node_id, 'end_node_address':end_node_id,
        'info_size':info_size}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
}
function next_step() {
    $.ajax({
        url: 'message/step',
        type: 'POST',
        data: "",
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
    location.reload();
}
function run() {
    $.ajax({
        url: 'message/run',
        type: 'POST',
        data: "",
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
    location.reload();
}
function save_nodes() {
    $.ajax({
        url: 'jsonsave',
        type: 'POST',
        data: JSON.stringify({'filename':"dump.json"}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
    location.reload();
}
function load_nodes() {
    $.ajax({
        url: 'load',
        type: 'POST',
        data: JSON.stringify({'filename':"dump.json"}),
        contentType: 'application/json; charset=utf-8',
        dataType: 'json',
        async: true,
    });
    location.reload();
}

$(document).ready(function() {
//    var network = $('#network').data('networkObj');
//    Generate(network);

    $('.dropdown-menu').on('click', function(event) {
        event.stopPropagation();
    });

    $('#modal_close, #overlay').click(close_modal_window);
    $('#modal_close_node, #overlay_node').click(close_modal_window_node);
});