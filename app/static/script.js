// let testbtn = document.getElementById('test')

// testbtn.addEventListener('click', (e) => {
//     console.log(e);
//     alert('button was clicked!')
// })

// let mysong=document.getElementById('mysong');
// function playSong() {
//     mysong.play();
// }
// function pauseSong() {
//     mysong.pause();
// }

// let pause = document.getElementById('pausebtn');
// pause.addEventListener('click', () => {
//     pauseSong()
//     pause.style.display = 'none'
//     play.style.display = 'flex'
// })

// let play = document.getElementById('playbtn');
// play.addEventListener('click', () => {
//     playSong()
//     play.style.display = 'none'
//     pause.style.display = 'flex'
// })

// playSong()

let songlist = document.querySelectorAll('.songObject');
console.log(songlist);
let player = document.getElementById('songtest');
// player.src = 'test'
// console.log(player)
for (let each in songlist) {
    console.log(songlist[each]);
    songlist[each].addEventListener('click', (e)=> {
        console.log(e, e.target);
        player.src = e.target.title
        player.play()
    })
}