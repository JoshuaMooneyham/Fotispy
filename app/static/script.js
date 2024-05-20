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

let newPlaylist = document.getElementById('playlistBtn');
let hiddenPlaylist = document.getElementById('playlistHideToggle');
let playlistContainer = document.getElementById('playlistFormContainer');
let checklist = [document.getElementById('playlistFormWrapper'), document.getElementById('playlistForm'), document.getElementsByClassName('playlistNameInput')[0], document.getElementsByClassName('playlistDescInput')[0]]
try {
    newPlaylist.onclick = () => {
        try {
            hiddenPlaylist.classList.remove('hidden');
            playlistContainer.onclick = (e) => {
                checklist.includes(e.target) ? console.log('test') : hiddenPlaylist.classList.add('hidden');
            }
        } catch {
            console.log('not logged in')
            alert('You must be logged in to use this feature!')
        }
    }
} catch (err) {

}
