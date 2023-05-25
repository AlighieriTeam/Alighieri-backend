const socketio = io();
socketio.emit('rejoin');

function test_me(){
    socketio.emit('draw_rectangle', 15, 15, 'blue', 5, 5);
    socketio.emit('draw_circle', 10, 10, 'yellow', 5);
    socketio.emit('draw_text', 20, 20, "Hello");
}

function leave_game(page) {
    socketio.emit("leave_game", {}, function() {
        // Server has acknowledged the event, navigate to new page
        window.location.href = page;
    });
}

var screen = document.getElementById('screen');
context = screen.getContext('2d');

// TODO board dimensions
var y_scale = screen.height / 14,
    x_scale = screen.width / 7;

socketio.on('drawRectangle', function(data){
    //console.log('drawRectangle called');
    context.fillStyle = data["color"];
    let x = Math.trunc((data["x"] - (data["width"] / 2)) * x_scale),
        y = Math.trunc((data["y"] - (data["height"]/2))* y_scale),
        width = Math.trunc(data["width"] * x_scale),
        height = Math.trunc(data["height"] * y_scale);
    context.fillRect(x, y, width, height);
})

socketio.on('drawCircle', function(data){
    //console.log('drawCircle called');
    let xp = Math.trunc((data["x"] - (data["width"] / 2)) * x_scale),
        yp = Math.trunc((data["y"] - (data["height"]/2))* y_scale),
        x = Math.trunc(data["x"] * x_scale),
        y = Math.trunc(data["y"] * y_scale),
        radius = Math.trunc(data["radius"] * y_scale);
    context.moveTo(xp, yp);
    context.beginPath();
    context.arc(x, y, radius, 0, 2 * Math.PI, false);
    context.fillStyle = data["color"];
    context.fill();
})

socketio.on('drawText', function(data){
    console.log('drawText called');
    context.fillStyle = "white";
    context.font = "30px Arial";
    context.fillText(data["text"], data["x"] * x_scale, data["y"] * y_scale);
})

socketio.on('clearAll', function(){
    console.log('clearAll called');
    context.fillStyle = "black";
    context.fillRect(0, 0, screen.width, screen.height);
})