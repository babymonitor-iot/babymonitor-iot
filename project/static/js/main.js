var socket = io.connect('http://localhost:5000');
var disconnect_bm = false;
var data_bm = false;
var text_observe = "You can only define the observer before starting some of the applications"
var button_obs = false;

document.querySelector('#btn-babymonitor').onclick = function () {
    /*if (!button_obs) {
        document.querySelector("#adaptation").disabled= true;
        document.querySelector(".adaptation").style.color = "#839192"
    }*/
    data_bm = !data_bm
    if (data_bm) {
        socket.emit('babymonitorConnect');
        document.querySelector('#btn-babymonitor').innerHTML = 'Stop';
        disconnect_bm = false;
        changeColor("#17a2b8", "white", ".bm");
        setTimeout(function () {
            changeColor("white", "black", ".bm");
        }, 1000);
    } else {
        disconnect_bm = true;
        socket.emit('babymonitorDisconnect');
        document.querySelector('#btn-babymonitor').innerHTML = 'Start';
        changeColor("#CD5C5C", "white", ".bm")
        setTimeout(function () {
            changeColor("white", "black", ".bm")
            document.querySelector("#babymonitor-sent").innerHTML = '';
            document.querySelector("#babymonitor-receive").innerHTML = '';
            document.querySelector("#babymonitor-information").innerHTML = '';
        }, 1000);
    }
};

function chengeOrder(msg){
    if (msg['time_no_breathing'] == 0) {
        var newMsg = {
            time_no_breathing: msg['time_no_breathing'],
            sleeping: msg['sleeping'],
            type: msg['type'],
            breathing: msg['breathing'],
            crying: msg['crying'],
        }
        return newMsg
    }
    return msg
}

socket.on('BabyMonitorSent', function (msg) {
    msg = chengeOrder(msg);
    document.querySelector("#babymonitor-sent").innerHTML = '';
    if (!disconnect_bm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#babymonitor-sent").appendChild(p);
        }
    } else {
        document.querySelector("#babymonitor-sent").innerHTML = '';
    }
});

socket.on('BabyMonitorReceive', function (msg) {
    document.querySelector("#babymonitor-receive").innerHTML = '';
    if (!disconnect_bm) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#babymonitor-receive").appendChild(p);
            setTimeout(function () {
                document.querySelector("#babymonitor-receive").innerHTML = '';
                document.querySelector("#tv-sent").innerHTML = '';
                document.querySelector("#tv-receive").innerHTML = '';
                document.querySelector("#from-sm").innerHTML = '';
                document.querySelector(".from-tv").innerHTML = '';
                document.querySelector("#smartphone-sent").innerHTML = '';
                document.querySelector("#smartphone-information").innerHTML = '';
                document.querySelector("#from-tv-information").innerHTML = ''; 
            }, 1000);
        }
    } else {
        document.querySelector("#babymonitor-receive").innerHTML = '';
    }
});

socket.on('successAdapter', function (msg) {
    changeColor("#148F77", "white", "#block");
});

// document.querySelector('#restart').onclick = function () {
//    socket.emit('restart');
// };