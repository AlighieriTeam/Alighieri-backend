const socketio = io();
socketio.emit('rejoin');

function test_me(){
    socketio.emit('draw_rectangle', 15, 15, 'blue', 5, 5);
    socketio.emit('draw_circle', 10, 10, 'yellow', 5);
    socketio.emit('draw_text', 20, 20, "Hello");
}

var screen = document.getElementById('screen'),
    context = screen.getContext('2d');
let scale = 100;

function set_scale(new_scale){
    scale = new_scale;
}

socketio.on('drawRectangle', function(data){
    context.fillStyle = data["color"];
    let x = Math.trunc((data["x"] - (data["width"] / 2)) * scale),
        y = Math.trunc((data["y"] - (data["height"]/2))* scale),
        width = Math.trunc(data["width"] * scale),
        height = Math.trunc(data["height"] * scale);
    context.fillRect(x, y, width, height);
})

socketio.on('drawCircle', function(data){
    let xp = Math.trunc((data["x"] - (data["width"] / 2)) * scale),
        yp = Math.trunc((data["y"] - (data["height"]/2))* scale),
        x = Math.trunc(data["x"] * scale),
        y = Math.trunc(data["y"] * scale),
        radius = Math.trunc(data["radius"] * scale);
    context.moveTo(xp, yp);
    context.beginPath();
    context.arc(x, y, radius, 0, 2 * Math.PI);
    context.fillStyle = data["color"];
    context.fill();
})

socketio.on('drawText', function(data){
    console.log('drawText called');
    context.fillStyle = "white";
    context.font = "30px Arial";
    context.fillText(data["text"], data["x"] * scale, data["y"] * scale);
})

socketio.on('clearAll', function(){
    console.log('clearAll called');
    context.fillStyle = "black";
    context.fillRect(0, 0, screen.width, screen.height);
})