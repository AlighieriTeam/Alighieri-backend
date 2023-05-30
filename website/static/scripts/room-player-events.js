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
            <div id="player_${id}" class="player_div player_gradient_${id}">
                <div class="ls-player-name" onclick="copyToken(${id})">${name}</div>
                <div class="ls-player-del"></div>
            </div>
        `
    }
    playerList.innerHTML = content;
}


function copyToken(playerId) {
    if (playerId === actual_player_id){
        const playerToken = playerTokens.get(playerId) || "";
        const tempInput = document.createElement('input');
        tempInput.value = playerToken;
        document.body.appendChild(tempInput);
        tempInput.select();
        document.execCommand('copy');
        document.body.removeChild(tempInput);
        alert('Token copied: ' + playerToken);
    }else{
       alert('Not your token');
    }
}

function delPlayer(player_id){
    const playerList = document.getElementById("player-list");
    playerList.innerHTML = "";
    playerMap.delete(player_id);
    playerTokens.delete(player_id);
    refreshPlayerList();
}
