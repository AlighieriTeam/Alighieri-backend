const socketio = io();
socketio.emit('rejoin');

const playerMap = new Map();
function leave(destination){
    window.location.href=destination;
}

function addPlayer(player) {
    if (!playerMap.has(player.id) || playerMap.get(player.id) === "") {
        playerMap.set(player.id, {name: player.name, color: player.color[0]});
    }
    refreshPlayerList();
    console.log(player.id);
    console.log(player.name);
}

function refreshPlayerList(players) {
  const playerList = document.getElementById("player-list");
  let content = "";

  players.forEach((player) => {
    const id = player.id;
    const name = player.name;
    const points = player.points;
    const color = player.color[0];

    content += `
      <div id="player_${id}" class="player-div" style="background: var(--gradient-${color});">
        <div class="ls-player-name">${name}</div>
        <div class="ls-player-points">${points}</div>
      </div>
    `;
  });

  playerList.innerHTML = content;
}

socketio.on('showPopup', function(players) {
    let content = "";
    players.sort(function(a, b) {
    return b.points - a.points;
    });
    for (const player of players) {
        var color = player.color[0]
        content += `
            <div id='player_${player["id"]}' class="player-div" style="background: var(--gradient-${color});">
                <div class="ls-player-name">${player["name"]}</div>
                <div class="ls-player-points">${player["points"]}</div>
            </div>
        `
    }

    var popup_content = document.getElementsByClassName("modal-body")[0];
    popup_content.innerHTML = content;

    $('#endgame_popup').modal({backdrop: 'static', keyboard: false});
});

socketio.on('updateScores', function(players) {
   players.sort(function(a, b) {
    return b.points - a.points;
  });

  refreshPlayerList(players);
});
