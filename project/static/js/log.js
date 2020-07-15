socket.on('Log', function (msg) {
    document.querySelector("#log").innerHTML = '';
    if (!disconnect_tv) {
        for (data in msg) {
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#log").appendChild(p);
        }
    } else {
        document.querySelector("#log").innerHTML = '';
    }
});