socket.on('TvSent', function (msg) {
    document.querySelector("#tv-sent").innerHTML = '';
    for (data in msg) {
        var p = document.createElement("p");
        var value = document.createTextNode(data + ": " + msg[data]);
        p.appendChild(value);
        document.querySelector("#tv-sent").appendChild(p);
    }
});