var screen = document.getElementById('screen'),
context = screen.getContext('2d');

function drawRectangle(x, y, color, width, height){
    context.fillStyle = color;
    context.fillRect(x, y, width, height);
}

function drawCircle(x, y, color, radius){
   context.moveTo(x, y);
   context.beginPath();
   context.arc(x, y, radius, 0, 2 * Math.PI, false);
   context.fillStyle = color;
   context.fill();
}

function drawText(x, y, text){
    context.fillStyle = "white";
    context.font = "30px Arial";
    context.fillText(text, x, y);
}

function clearAll(){
    context.fillStyle = "black";
    context.fillRect(0, 0, screen.width, screen.height);
}


clearAll();

drawRectangle(10, 10, 'blue', 40, 40);
drawCircle(100, 100, 'yellow', 20);
drawText(300, 300, "Hello");
