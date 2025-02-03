document.querySelectorAll(".walkthrough .item").forEach(function(item){item.addEventListener("click",function(e){let wt=item.closest(".walkthrough")
let img=wt.querySelector(`.image-${item.dataset.item}`)
if(img){wt.querySelectorAll(".image").forEach(function(it){it.classList.remove("active");})
img.classList.add("active");}
wt.querySelectorAll(".item").forEach(function(it){it.classList.remove("active");})
item.classList.add("active")})})
function toggleRadio(){const radioPlayer=document.getElementById('radio-player');const playIcon=document.getElementById('play-radio-icon');if(radioPlayer.paused){radioPlayer.play();playIcon.className='fa fa-pause fa-xl';playIcon.innerHTML=' Playing...';}else{radioPlayer.pause();playIcon.className='fa fa-play fa-xl';playIcon.innerHTML=' Play';}}
(function($){$.fn.countdown=function(options,callback){var thisEl=$(this);var settings={date:null,format:null};var interval;if(options){$.extend(settings,options);}
function countdown_proc(){var eventDate=Date.parse(settings["date"])/1000;var currentDate=Math.floor($.now()/1000);if(eventDate<=currentDate){callback.call(this);clearInterval(interval);}
var seconds=eventDate-currentDate;var days=Math.floor(seconds/(60*60*24));seconds-=days*60*60*24;var hours=Math.floor(seconds/(60*60));seconds-=hours*60*60;var minutes=Math.floor(seconds/60);seconds-=minutes*60;if(days==1){thisEl.find(".timeRefDays").text("Day");}else{thisEl.find(".timeRefDays").text("Days");}
if(hours==1){thisEl.find(".timeRefHours").text("Hour");}else{thisEl.find(".timeRefHours").text("Hours");}
if(minutes==1){thisEl.find(".timeRefMinutes").text("Minute");}else{thisEl.find(".timeRefMinutes").text("Minutes");}
if(seconds==1){thisEl.find(".timeRefSeconds").text("Second");}else{thisEl.find(".timeRefSeconds").text("Seconds");}
if(settings["format"]=="on"){days=String(days).length>=2?days:"0"+days;hours=String(hours).length>=2?hours:"0"+hours;minutes=String(minutes).length>=2?minutes:"0"+minutes;seconds=String(seconds).length>=2?seconds:"0"+seconds;}
if(!isNaN(eventDate)){thisEl.find(".days").text(days);thisEl.find(".hours").text(hours);thisEl.find(".minutes").text(minutes);thisEl.find(".seconds").text(seconds);}else{alert("Invalid date. Here's an example: 12 Tuesday 2012 17:30:00");clearInterval(interval);}}
countdown_proc();interval=setInterval(countdown_proc,1000);};})(jQuery);$(".countdown").countdown({date:"28 July 2017 5:00:00",format:"on"},function(){$(".days").html("0");$(".timeRefDays").html("Days");$(".hours").html("0");$(".timeRefHours").html("Hours");$(".minutes").html("0");$(".timeRefMinutes").html("Minutes");$(".seconds").html("0");$(".timeRefSeconds").html("Seconds");$(".banner").html("Website going live soon!");});;