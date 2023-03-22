function startTimer(duration, display) {
    var timer = duration, minutes, seconds;
    let timerId = setInterval(function () {
        minutes = parseInt(timer / 60, 10);
        seconds = parseInt(timer % 60, 10);

        minutes = minutes < 10 ? "0" + minutes : minutes;
        seconds = seconds < 10 ? "0" + seconds : seconds;

        display.textContent = minutes + ":" + seconds;

        if (--timer < 0) {
            clearInterval(timerId)
            window.location.href = '/choose';
        }
    }, 1000);
}

window.onload = function () {
    var minutes = 30,
        display = document.querySelector('#time');
    startTimer(minutes, display);
};