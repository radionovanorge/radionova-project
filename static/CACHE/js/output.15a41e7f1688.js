document.querySelectorAll(".walkthrough .item").forEach(function(item){item.addEventListener("click",function(e){let wt=item.closest(".walkthrough")
let img=wt.querySelector(`.image-${item.dataset.item}`)
if(img){wt.querySelectorAll(".image").forEach(function(it){it.classList.remove("active");})
img.classList.add("active");}
wt.querySelectorAll(".item").forEach(function(it){it.classList.remove("active");})
item.classList.add("active")})})
function toggleRadio(){const radioPlayer=document.getElementById('radio-player');const playIcon=document.getElementById('play-radio-icon');if(radioPlayer.paused){radioPlayer.play();playIcon.className='fa fa-pause fa-xl';playIcon.innerHTML=' Pause';}else{radioPlayer.pause();playIcon.className='fa fa-play fa-xl';playIcon.innerHTML=' Play';}};