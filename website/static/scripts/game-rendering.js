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
    console.log(players)
    for (const player of players) {
        console.log(`Key: ${player["id"]}, Value: ${player["name"]}`);
        content += `
            <div id='player_${player["id"]}' class="player_div player_gradient_1">
                <div class="ls-player-name">${player["name"]}</div>
                <div class="ls-player-points">${player["points"]}</div>
                <div class="ls-player-del"></div>
            </div>
        `
    }

    var popup = document.getElementById("popup")

    part1 = `
        <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalCenterTitle" aria-hidden="true">
          <div class="modal-dialog modal-dialog-centered" role="document">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="exampleModalLongTitle">Modal title</h5>
                <button type="button" class="close" data-dismiss="modal" aria-label="Close">
                  <span aria-hidden="true">&times;</span>
                </button>
              </div>
              <div class="modal-body">
    `

    part2 = `
              </div>
              <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
                <button type="button" class="btn btn-primary">Save changes</button>
              </div>
            </div>
          </div>
        </div>
    `
    var ss = part1 + content + part2
    popup.innerHTML = ss
    $('#exampleModal').modal('show');
    console.log('show_popup called');
});