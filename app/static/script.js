let songlist = document.querySelectorAll('.songObject');
console.log(songlist);
let player = document.getElementById('songtest');
let title = document.getElementById('playing-title');
let artist = document.getElementById('playing-artist')

songlist.forEach((song) => {
    song.addEventListener('click', (e)=> {
        player.src = e.target.title
        title.innerText = e.target.innerText;
        artist.innerText = e.target.title
    })
})