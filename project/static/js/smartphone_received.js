var disconnect_sm = false;
var data_sm = false;


document.querySelector('#btn-smartphone').onclick = function () {
    /*if (!button_obs) {
        document.querySelector("#adaptation").disabled= true;
        document.querySelector(".adaptation").style.color = "#839192"
    }*/
    data_sm = !data_sm
    if (data_sm) {
        socket.emit('smartphoneConnect');
        document.querySelector('#btn-smartphone').innerHTML = 'Stop';
        disconnect_sm = false;
        changeColor("#17a2b8", "white", ".sm");
        setTimeout(function () {
            changeColor("white", "black", ".sm");
        }, 1000);
    } else {
        disconnect_sm = true;
        socket.emit('smartphoneDesconnect');
        changeColor("#CD5C5C", "white", ".sm");
        document.querySelector('#btn-smartphone').innerHTML = 'Start';
        document.querySelector("#btn-smartphone-confirm").disabled = true;
        setTimeout(function () {
            changeColor("white", "black", ".sm");
            document.querySelector("#smartphone-sent").innerHTML = '';
            document.querySelector("#smartphone-receive").innerHTML = '';
            document.querySelector("#smartphone-information").innerHTML = '';
        }, 1000);
    }
};


socket.on('SmartphoneReceive', function (msg) {
    document.querySelector(".smartphone-receive").innerHTML = '';
    if (!disconnect_sm) {
        if (msg['type'] == 'notification') {
            document.querySelector("#btn-smartphone-confirm").disabled = false;
        } else {
            document.querySelector("#btn-smartphone-confirm").disabled = true;
        }
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector(".smartphone-receive").appendChild(p);
        }
    }
});

socket.on('FromTv', function (msg) {
    document.querySelector(".from-tv").innerHTML = '';
    if (!disconnect_sm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector(".from-tv").appendChild(p);
        }
    }
});


socket.on('SmartphoneInformation', function (msg) {
    document.querySelector("#smartphone-information").innerHTML = '';
    if (!disconnect_sm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#smartphone-information").appendChild(p);
        }
    }
});

socket.on('FromTvInformation', function (msg) {
    document.querySelector("#from-tv-information").innerHTML = '';
    console.log(disconnect_sm)
    console.log(msg)
    if (!disconnect_sm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#from-tv-information").appendChild(p);
        }
    }
});
