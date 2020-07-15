document.querySelector('#btn-smartphone-confirm').onclick = function () {
    socket.emit('confirmUser');
};

socket.on('SmartphoneSent', function(msg) {
    document.querySelector("#smartphone-sent").innerHTML = '';
    if (!disconnect_bm) {
        for(data in msg){
            var p = document.createElement("p");
            var value = document.createTextNode(data + ": " + msg[data]);
            p.appendChild(value);
            document.querySelector("#smartphone-sent").appendChild(p);
        }
    }
});