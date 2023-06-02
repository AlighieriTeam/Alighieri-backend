// ------------ common socketIO signals for join.html and room.html ------------

const socketio = io();

socketio.on("connection", (player) => {
    console.log("[JS] user connected " + player["name"]);
    addPlayer(player);
});

socketio.on('disconnection', (player) => {
    console.log('[JS] user disconnected ' + player["name"]);
    const playerList = document.getElementById("player-list");
    playerList.innerHTML = "";
    playerMap.delete(player["id"]);
    refreshPlayerList();
});

socketio.on('redirect', function(destination) {
    window.location.href = destination;
});

socketio.emit('connected');



// ------------ common JS functions for join.html and room.html ------------

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
