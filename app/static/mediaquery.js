function buffer() {
    let iframe = document.getElementById('iframe')
    let iframeDoc = iframe.contentDocument;
    let player = document.getElementById('songtest');
    let pause = document.getElementById('pausebtn');
    let play = document.getElementById('playbtn');
    let progressBar = document.getElementById('slider');
    let volumeBar = document.getElementById('volume');
    let currentDisplay = document.getElementById('current-time');
    let totalDisplay = document.getElementById('total-duration');
    let mute = document.getElementById('mutebtn');
    let skip = document.getElementById('nextbtn');
    let back = document.getElementById('prevbtn');
    let title = document.getElementById('playing-title');
    let artist = document.getElementById('playing-artist');
    let songlist = iframeDoc.querySelectorAll('.songObject')

    // let songlist = $('.songObject');
    // let iframe = document.querySelector('iframe');
    // let iframeDoc = iframe.contentDocument;
    // console.log(iframeDoc)
    // console.log(iframeDoc.getElementsByClassName('songObject'))
    let playlistbtn = iframeDoc.getElementById('playlistTest');

    let queue = [];
    let currentSong = '';

    function handlePlay() {
        player.play();
        play.style.display = 'none';
        pause.style.display = 'block';
    }

    function handlePause() {
        player.pause();
        pause.style.display = 'none';
        play.style.display = 'block';
    }

    function handleLoad() {
        handlePlay();
        play.classList.remove('inactive');
        pause.classList.remove('inactive');
        currentDisplay.innerText = '0:00';
        let minutes = Math.floor(player.duration / 60)
        let seconds = Math.floor(player.duration - minutes*60)
        totalDisplay.innerText = `${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;
    }

    function setVolume() {
        player.volume = volumeBar.value;
        document.getElementById('mutebtnimg').src = player.volume > .6 ? '/static/volume.png' : player.volume > .3 ? '/static/volume (1).png' : player.volume === 0 ? '/static/mute.png' : '/static/volume (2).png';
    }

    function handleMute() {
        volumeBar.value = volumeBar.value > 0 ? 0 : 1;
        setVolume()
    }

    player.onloadedmetadata = handleLoad

    volumeBar.onchange = setVolume

    volumeBar.onmousemove = setVolume

    pause.onclick = handlePause

    play.onclick = handlePlay

    mute.onclick = handleMute

    player.ontimeupdate = () => {
        progressBar.value = player.currentTime === 0 ? 0 : (player.currentTime / player.duration * 100);
        let minutes = Math.floor(player.currentTime / 60);
        let seconds = Math.floor(player.currentTime - minutes*60)
        currentDisplay.innerText = `${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;
        if (player.currentTime === player.duration && queue.length > queue.indexOf(currentSong)) {
            loadSong(queue[queue.indexOf(currentSong) + 1])
        }
    }

    function loadSong(songObject) {
        currentSong = songObject;
        player.src = songObject.title;
        title.innerText = songObject.innerText;
        artist.innerText = songObject.title;
        console.log(queue)
        queue.indexOf(currentSong) + 1 < queue.length ? skip.classList.remove('inactive') : skip.classList.add('inactive');
        queue.indexOf(currentSong) > 0 ? back.classList.remove('inactive') : back.classList.add('inactive');
    }

    playlistbtn.onclick = (e) => {
        queue = [...e.target.children];
        console.log(queue);
        loadSong(queue[0]);
    }

    songlist.forEach((song) => {
        song.addEventListener('click', (e)=> {
            queue = [song];
            loadSong(song);
        })
    })

    skip.onclick = () => {
        if (queue.indexOf(currentSong)+1 < queue.length) {
            loadSong(queue[queue.indexOf(currentSong)+1]);
        }
    }

    back.onclick = () => {
        if (queue.indexOf(currentSong) > 0) {
        loadSong(queue[queue.indexOf(currentSong)-1]);
        }
    }
}