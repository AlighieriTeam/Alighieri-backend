let timerId;
function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    timerId = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0 ) {
            console.log('entered');
            socketio.emit('timerOut');
            clearInterval(timerId);
        }
    }, 1000);
}

window.onload = function () {
    var seconds = 3,
        display = document.querySelector('#time');
    startTimer(seconds, display);
};