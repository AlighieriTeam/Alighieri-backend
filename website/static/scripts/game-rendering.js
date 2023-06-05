const socketio = io();
socketio.emit('rejoin');

function leave_game(page) {
    socketio.emit("leave_game", {}, function() {
        // Server has acknowledged the event, navigate to new page
        window.location.href = page;
    });
}

var screen = document.getElementById('screen'),
    context = screen.getContext('2d');
let scale = 100;


function set_scale(new_scale){
    scale = new_scale;
}

socketio.on('drawRectangle', function(data){
    context.fillStyle = data["color"];
    let x = Math.trunc((data["x"] - (data["width"]/2)) * scale),
        y = Math.trunc((data["y"] - (data["height"]/2)) * scale),
        width = Math.trunc(data["width"] * scale),
        height = Math.trunc(data["height"] * scale);
    context.fillRect(x, y, width, height);
})

socketio.on('drawCircle', function(data){
    let x = Math.trunc(data["x"] * scale),
        y = Math.trunc(data["y"] * scale),
        radius = Math.trunc(data["radius"] * scale);
    context.beginPath();
    context.arc(x, y, radius, 0, 2 * Math.PI);
    context.fillStyle = data["color"];
    context.fill();
})

socketio.on('drawGhost', function(data){
    let xp = Math.trunc((data["x"] - (data["width"]/2)) * scale),
        yp = Math.trunc((data["y"] - (data["height"]/2)) * scale),
        width = Math.trunc(data["width"] * scale),
        height = Math.trunc(data["height"] * scale);
    context.beginPath();
    context.arc(xp + width/2, yp + height/2, height/2, Math.PI, 2 * Math.PI, false);
    context.lineTo(xp + width, yp + height);
    context.lineTo(xp, yp + height);
    context.fillStyle = data["color"];
    context.fill();
})

socketio.on('drawText', function(data){
    context.fillStyle = "white";
    context.font = "30px Arial";
    context.fillText(data["text"], data["x"] * scale, data["y"] * scale);
})

socketio.on('clearAll', function(){
    console.log('clearAll called');
    context.fillStyle = "black";
    context.fillRect(0, 0, screen.width, screen.height);
})



socketio.on('showPopup', function(players) {
    let content = "";
    for (const player of players) {
        console.log(`Key: ${player["id"]}, Value: ${player["name"]}`);
        content += `
            <div id='player_${player["id"]}' class="player_div">
                <div class="ls-player-name">${player["name"]}</div>
                <div class="ls-player-points">${player["points"]}</div>
                <div class="ls-player-del"></div>
            </div>
        `
    }

    var popup_content = document.getElementsByClassName("modal-body")[0];
    popup_content.innerHTML = content;

    $('#endgame_popup').modal({backdrop: 'static', keyboard: false});
});


var pl0 = document.getElementById("player_0") != null ? document.getElementById("player_0").querySelector(".ls-player-points") : null;
var pl1 = document.getElementById("player_1") != null ? document.getElementById("player_1").querySelector(".ls-player-points") : null;
var pl2 = document.getElementById("player_2") != null ? document.getElementById("player_2").querySelector(".ls-player-points") : null;
var pl3 = document.getElementById("player_3") != null ? document.getElementById("player_3").querySelector(".ls-player-points") : null;
var arr = [pl0,pl1,pl2,pl3]
socketio.on('updateScores', function(players) {
    for (var i = 0; i < players.length; i++) {
      arr[i].innerHTML = players[i]["points"][0];
    }
});