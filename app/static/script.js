/* ==={ Redirect User }=== */ 
if (window.self === window.top) {
    window.location.replace('/');
}

let playlistQuery = document.getElementsByClassName('playlist-icon');
let playlistNums = [...playlistQuery]

playlistNums.forEach((item) => {
    item.innerText = playlistNums.indexOf(item) + 1;
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

let updatePlaylistBtn = document.getElementById('updateBtn');
try {
    updatePlaylistBtn.onclick = () => {
        document.getElementById('updatePlaylist').classList.remove('hidden');
    }
} catch {
    console.log('No Playlist Yet');
}

let addToPlaylistBtns = [...document.getElementsByClassName('ellipsis-box')]
addToPlaylistBtns.forEach((btn) => {
    btn.onclick = () => {
        btn.parentElement.querySelector('.playlistPopulationAnchor').classList.toggle('hidden');
        btn.parentElement.querySelector('.playlistPopulationAnchor').querySelector('.playlistPopulationClose').onclick = () => {
            btn.parentElement.querySelector('.playlistPopulationAnchor').classList.add('hidden');
        }
    }
})

let popForms = [...document.getElementsByClassName('playlistPopulationForm')];

popForms.forEach((form) => {
    form.querySelector('select').onchange = (e) => {
        if (e.target.value !== 'invalid') {
        e.target.parentElement.querySelector('.real').classList.remove('hidden')
        e.target.parentElement.querySelector('.dummy').classList.add('hidden')
        }
    }
})

let playlistFormBtn = document.getElementById('updateBtn');
let closePlaylistForm = document.getElementById('closeUpdatePlaylist');
let playlistViewHeader = document.getElementById('playlistViewHeader');
let playlistUpdateForm = document.getElementById('playlistViewFormWrapper');
try {
playlistFormBtn.onclick = () => {
    playlistViewHeader.classList.add('hidden');
    playlistUpdateForm.classList.remove('hidden');
    closePlaylistForm.onclick = () => {
        playlistViewHeader.classList.remove('hidden');
        playlistUpdateForm.classList.add('hidden');
    }
}
} catch {
    
}
