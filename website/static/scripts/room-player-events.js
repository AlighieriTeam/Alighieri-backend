// ------------ socketIO signals for room-player.html ------------

socketio.on('kick', function(json) {
    if(json["id"] == actual_player_id){
        window.location.href = json["dest"];
    }
    else{
        delPlayer(json["id"])
    }
});



// ------------ JS functions for room-player.html ------------

function refreshPlayerList() {
    const playerList = document.getElementById("player-list");
    let content = "";
    for (const [id, name] of playerMap.entries()) {
        content += `
            <div id="player_${id}" class="player_div">
                <div class="ls-player-name">${name}</div>
                <div class="ls-player-del"></div>
            </div>
        `
    }
    playerList.innerHTML = content;
}

function delPlayer(player_id){
    const playerList = document.getElementById("player-list");
    playerList.innerHTML = "";
    playerMap.delete(player_id);
    refreshPlayerList();
}
