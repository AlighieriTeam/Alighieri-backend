const socketio = io();
socketio.emit('rejoin');

const playerMap = new Map();
function leave(destination){
    window.location.href=destination;
}

function addPlayer(player) {
    if (!playerMap.has(player.id) || playerMap.get(player.id) === "") {
        playerMap.set(player.id, player.name);
    }
    refreshPlayerList();
    console.log(player.id);
    console.log(player.name);
}

function refreshPlayerList() {
    console.log("refresh called")
    const playerList = document.getElementById("player-list");
    let content = "";
    for (const [id, name] of playerMap.entries()) {
        if (id === actual_player_id){
            content += `
                <div id="player_${id}" class="player_div" style="background-color: rgb${backgroundColor}">
                    <div class="ls-player-name">${name}</div>
                    <div class="ls-player-points"></div>
                </div>
            `
        }
        else{
             content += `
                <div id="player_${id}" class="player_div">
                    <div class="ls-player-name">${name}</div>
                    <div class="ls-player-points"></div>
                </div>
            `
        }
    }
    playerList.innerHTML = content;
}




socketio.on('showPopup', function(players) {
    let content = "";
    for (const player of players) {
        console.log(`Key: ${player["id"]}, Value: ${player["name"]}`);
        if(player["id"] === actual_player_id){
            content += `
                <div id='player_${player["id"]}' class="player_div" style="background-color: rgb${backgroundColor}">
                    <div class="ls-player-name">${player["name"]}</div>
                    <div class="ls-player-points">${player["points"]}</div>
                </div>
            `
        }
        else{
            content += `
                <div id='player_${player["id"]}' class="player_div">
                    <div class="ls-player-name">${player["name"]}</div>
                    <div class="ls-player-points">${player["points"]}</div>
                </div>
            `
        }
    }

    var popup_content = document.getElementsByClassName("modal-body")[0];
    popup_content.innerHTML = content;

    $('#endgame_popup').modal({backdrop: 'static', keyboard: false});
});

socketio.on('updateScores', function(players) {
    for (const player of players){
        console.log(`${player["id"]} -> ${player["points"][0]}`);
        playerScoreDivs[player["id"]].innerHTML = player["points"][0];
    }
});