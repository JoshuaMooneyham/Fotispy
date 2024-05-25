// ==={ Independent Variables }===
let queue = [];
let currentSong = '';
let lastVolume = 1;
let playlingPlaylist = '';

function buffer() { // <== Necessary to wait for iframe content to load fully

    /* ==={ Iframe document setup }=== */
    let iframe = document.getElementById('iframe')
    let iframeDoc = iframe.contentDocument;

    /* ==={ Media Player }=== */
    let player = document.getElementById('songtest');

        /* ==={ Buttons }=== */
        let pause = document.getElementById('pausebtn');
        let play = document.getElementById('playbtn');
        let mute = document.getElementById('mutebtn');
        let skip = document.getElementById('nextbtn');
        let back = document.getElementById('prevbtn');

        /* ==={ Bars/Meters }=== */
        let progressBar = document.getElementById('slider');
        let volumeBar = document.getElementById('volume');
        let currentDisplay = document.getElementById('current-time');
        let totalDisplay = document.getElementById('total-duration');

        /* ==={ Song Data }=== */
        let title = document.getElementById('playing-title');
        let artist = document.getElementById('playing-artist');

    /* ==={ Song Objects }=== */ 
    let songlist = iframeDoc.querySelectorAll('.songPlayBtn');
    let playlistBtns = iframeDoc.querySelectorAll('.playlistBtn');

    /* ==={ Functions/Event Handlers }=== */ 
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
        lastVolume = player.volume;
        player.volume = volumeBar.value;
        document.getElementById('mutebtnimg').src = player.volume > .6 ? '/static/volume.png' : player.volume > .3 ? '/static/volume (1).png' : player.volume === 0 ? '/static/mute.png' : '/static/volume (2).png';
    }

    function handleMute() {
        volumeBar.value = volumeBar.value > 0 ? 0 : lastVolume < .2 ? .2 : lastVolume;
        setVolume()
    }

    function loadSong(songObject) {
        currentSong = songObject;
        player.src = songObject.title;
        title.innerText = songObject.innerText;
        artist.innerText = songObject.classList[0];
        queue.indexOf(currentSong) + 1 < queue.length ? skip.classList.remove('inactive') : skip.classList.add('inactive');
        queue.indexOf(currentSong) > 0 ? back.classList.remove('inactive') : back.classList.add('inactive');
    }

    function unloadSong() {
        player.src = '';
        currentSong = '';
        title.innerText = '';
        artist.innerText = '';
        queue = [];
        playlingPlaylist = '';
        currentDisplay.innerText = '-:--';
        totalDisplay.innerText = '-:--';
        skip.classList.add('inactive');
        back.classList.add('inactive');
        play.classList.add('inactive');
        pause.classList.add('inactive');
        pause.style.display = 'none';
        play.style.display = 'block';
    }

    /* ==={ Events/Listeners }=== */ 

    player.onloadedmetadata = handleLoad

    volumeBar.onchange = setVolume

    volumeBar.onmousemove = setVolume

    pause.onclick = handlePause

    play.onclick = handlePlay

    mute.onclick = handleMute

    testPlaylist = iframeDoc.getElementById('playlistPlayBtn');
   
    try {
        testPlaylist.onclick = () => {
            queue = [...testPlaylist.querySelectorAll('song')];
            playlingPlaylist = testPlaylist.parentElement.querySelector('#playlistViewTitle').innerText
            console.log(playlingPlaylist)
            loadSong(queue[0]);
        }
    } catch {
        console.log('play playlist broke')
    }
    
    deletePlaylist = iframeDoc.getElementById('deletePlaylist');
    try {
        console.log(deletePlaylist.parentElement.parentElement.parentElement.parentElement.parentElement.querySelector('#playlistViewTitle'))
        console.log(iframeDoc.getElementById('playlistViewTitle'))
        deletePlaylist.onclick = () => {
            if (iframeDoc.getElementById('playlistViewTitle').innerText == playlingPlaylist) {
                unloadSong()
            }
        }
    } catch {
        console.log('delete playlist broke')
    }

    iframe.onchange = () => {
        console.log('iframe refresh')
    }

    player.ontimeupdate = () => {
        progressBar.value = player.currentTime === 0 ? 0 : (player.currentTime / player.duration * 100);
        let minutes = Math.floor(player.currentTime / 60);
        let seconds = Math.floor(player.currentTime - minutes*60)
        currentDisplay.innerText = `${minutes}:${seconds < 10 ? '0'+seconds : seconds}`;
        if (player.currentTime === player.duration && queue.length > queue.indexOf(currentSong)) {
            loadSong(queue[queue.indexOf(currentSong) + 1])
        }
    }

    songlist.forEach((song) => {
        song.addEventListener('click', (e)=> {
            queue = [...e.target.querySelectorAll('song')];
            playlingPlaylist = '';
            loadSong(queue[0]);
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
