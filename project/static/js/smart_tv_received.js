var disconnect_tv = false;
var block_tv = false;
var data_tv = false;


document.querySelector('#btn-tv').onclick = function () {
    /*if (!button_obs) {
        document.querySelector("#adaptation").disabled= true;
        document.querySelector(".adaptation").style.color = "#839192"
    }*/
    data_tv = !data_tv
    if (data_tv) {
        socket.emit('tvConnect');
        document.querySelector('#btn-tv').innerHTML = 'Stop';
        document.querySelector("#btn-tv-block").disabled = false;
        disconnect_tv = false;
        changeColor("#17a2b8", "white", ".tv");
        setTimeout(function () {
            changeColor("white", "black", ".tv");
            document.querySelector('#tv-information').innerHTML = 'info: Tv unlock';
        }, 1000);
    } else {
        disconnect_tv = true;
        socket.emit('tvDisconnect');
        document.querySelector('#btn-tv').innerHTML = 'Start';
        document.querySelector("#btn-tv-block").disabled = true;
        document.querySelector('#btn-tv-block').innerHTML = 'Block'
        changeColor("#CD5C5C", "white", ".tv")
        setTimeout(function () {
            changeColor("white", "black", ".tv")
            document.querySelector("#tv-sent").innerHTML = '';
            document.querySelector("#tv-receive").innerHTML = '';
            document.querySelector("#tv-information").innerHTML = '';
        }, 1000);
    }
};

document.querySelector('#btn-tv-block').onclick = function () {
    block_tv = !block_tv;
    if (block_tv) {
        socket.emit('tvBlock', true);
        document.querySelector('#btn-tv-block').innerHTML = 'Unlock';
    } else {
        socket.emit('tvBlock', false);
        document.querySelector('#btn-tv-block').innerHTML = 'Block';
    }
};

socket.on('TvReceive', function (msg) {
    document.querySelector("#tv-receive").innerHTML = '';
    if (!disconnect_tv) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#tv-receive").appendChild(p);
        }
    }
});

socket.on('TvInformation', function (msg) {
    document.querySelector("#tv-information").innerHTML = '';
    if (!disconnect_tv) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#tv-information").appendChild(p);
        }
    }
});

socket.on('FromSmartphone', function (msg) {
    document.querySelector("#from-sm").innerHTML = '';
    if (!disconnect_tv) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#from-sm").appendChild(p);
        }
    }
});

socket.on('RedColor', function (msg) {
    document.querySelector("#block").style.backgroundColor = "#CD3333";
    document.querySelector("#block").style.color = "#ffff";
});

socket.on('NormalColor', function (msg) {
    document.querySelector("#block").style.backgroundColor = "white";
    document.querySelector("#block").style.color = "black";
});
