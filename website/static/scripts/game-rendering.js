const socketio = io();

function test_me(){
    socketio.emit('rejoin');    // necessary
    socketio.emit('draw_rectangle', 15, 15, 'blue', 5, 5);
    socketio.emit('draw_circle', 10, 10, 'yellow', 5);
    socketio.emit('draw_text', 20, 20, "Hello");
}

var screen = document.getElementById('screen');
context = screen.getContext('2d');

socketio.on('drawRectangle', function(data){
    context.fillStyle = data["color"];
    context.fillRect(data["x"], data["y"], data["width"], data["height"]);
})

socketio.on('drawCircle', function(data){
    context.moveTo(data["x"], data["y"]);
    context.beginPath();
    context.arc(data["x"], data["y"], data["radius"], 0, 2 * Math.PI, false);
    context.fillStyle = data["color"];
    context.fill();
})

socketio.on('drawText', function(data){
    context.fillStyle = "white";
    context.font = "30px Arial";
    context.fillText(data["text"], data["x"], data["y"]);
})

socketio.on('clearAll', function(){
    context.fillStyle = "black";
    context.fillRect(0, 0, screen.width, screen.height);
})