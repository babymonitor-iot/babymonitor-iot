function changeColor(background, color, className){
    var components = document.querySelectorAll(className)
    for(var i = 0; i < components.length; i++){
        components[i].style.backgroundColor = background;
        components[i].style.color = color;
    }
}

function showData(className, data, msg){
    var p = document.createElement("p");
    var value = document.createTextNode(data + ": " + msg[data]);
    p.appendChild(value);
    document.querySelector(className).appendChild(p);
}

function deleteMessage(className, time) {
    setTimeout(function () {
        document.querySelector(className).innerHTML = '';
    }, time);
}