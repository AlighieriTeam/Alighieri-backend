// ------------ socketIO signals for room-owner.html ------------





// ------------ JS functions for room-owner.html ------------

function startGame() {
    socketio.emit('start_game');
}

function addBot(b_key, b_val){    // b_val unused
    socketio.emit('add_bot', {name: b_key});
    console.log("bot sent: " + b_key);
}

function refreshPlayerList() {
    const playerList = document.getElementById("player-list");
    let content = "";
    for (const [id, name] of playerMap.entries()) {
        if(id != 0){
            content += `
                <div id="player_${id}" class="player_div player_gradient_${id}">
                    <div class="ls-player-name" onclick="copyToken(${id})">${name}</div>
                    <div class="ls-player-del">
                      <i class="bi bi-x-circle ls-icon-color"></i>
                      <i class="bi bi-x-circle-fill ls-icon-color" onclick="delPlayer(${id}, '${name}')"></i>
                    </div>
                </div>
            `
        }
        else{
            content += `
                <div id="player_${id}" class="player_div player_gradient_${id}">
                    <div class="ls-player-name" onclick="copyToken(${id})">${name}</div>
                    <div class="ls-player-del"></div>
                </div>
            `
        }
    }
    playerList.innerHTML = content;
}

function copyToken(playerId) {
    if (playerId === 0) {
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
function delPlayer(player_id, player_name){
    console.log("player was kicked: " + player_id + " " + player_name);
    const playerList = document.getElementById("player-list");
    playerList.innerHTML = "";
    playerMap.delete(player_id);
    playerTokens.delete(player_id);
    refreshPlayerList();
    socketio.emit('del_player', {id: player_id, name: player_name});
}
