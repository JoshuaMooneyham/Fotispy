let pause = document.getElementById('pausebtn');
let play = document.getElementById('playbtn');
let player2 = document.getElementById('songtest');
let progressBar = document.getElementById('slider');
let volumeBar = document.getElementById('volume');
let currentDisplay = document.getElementById('current-time');
let totalDisplay = document.getElementById('total-duration');
let mute = document.getElementById('mutebtn');
let playlistbtn = document.getElementById('playlistTest');
let playlist = [];

function handlePlay() {
    player2.play();
    play.style.display = 'none';
    pause.style.display = 'block';
}

function handlePause() {
    player2.pause();
    pause.style.display = 'none';
    play.style.display = 'block';
}

function handleLoad() {
    handlePlay();
    play.classList.remove('inactive');
    pause.classList.remove('inactive');
    currentDisplay.innerText = '0:00';
    let minutes = Math.floor(player2.duration / 60)
    let seconds = Math.floor(player2.duration - minutes*60)
    totalDisplay.innerText = `${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;
}

function setVolume() {
    player2.volume = volumeBar.value;
    document.getElementById('mutebtnimg').src = player2.volume > .6 ? '/static/volume.png' : player2.volume > .3 ? '/static/volume (1).png' : player2.volume === 0 ? '/static/mute.png' : '/static/volume (2).png';
}

function handleMute() {
    volumeBar.value = volumeBar.value > 0 ? 0 : 1;
    setVolume()
}

player2.onloadedmetadata = handleLoad

volumeBar.onchange = setVolume

volumeBar.onmousemove = setVolume

pause.onclick = handlePause

play.onclick = handlePlay

mute.onclick = handleMute

player2.ontimeupdate = () => {
    console.log(player.currentTime);
    progressBar.value = player.currentTime === 0 ? 0 : (player.currentTime / player.duration * 100);
    let minutes = Math.floor(player.currentTime / 60);
    let seconds = Math.floor(player.currentTime - minutes*60)
    currentDisplay.innerText = `${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;
}

function loadSong(songObject) {
    
}

playlistbtn.onclick = (e) => {
    playlist = [...e.target.children];
    console.log(playlist)
}