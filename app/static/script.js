/* ==={ Redirect User }=== */ 
if (window.self === window.top) {
    window.location.replace('/');
}

let playlistQuery = document.getElementsByClassName('playlist-icon');
let playlistNums = [...playlistQuery]

playlistNums.forEach((item) => {
    item.innerText = playlistNums.indexOf(item) + 1;
})

let playlists = document.getElementsByClassName('gridifier');
let playlistList = [...playlists];

playlistList.forEach((item) => {
    let shit = item.getElementsByClassName('playlist-song-count');
    shit[0].innerText = `${item.getElementsByTagName('song').length} songs`;
})
