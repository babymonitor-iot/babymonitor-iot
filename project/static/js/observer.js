document.querySelector('#adaptation').onchange = function () {
    button_obs = !button_obs;
    if(button_obs) {
        socket.emit('observerConnect');
    } else {
        socket.emit('observerDisconnect');
    }
};
