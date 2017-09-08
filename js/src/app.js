// import "babel-polyfill";
const inView = require('in-view');
const pym = require('pym.js');
// const swiper = require('swiper.min.js');
// const boot = require('bootstrap.js');

// -------------------------------------------------------------------
// THIS APP.JS ONLY IS FOR CODE NEEDED FOR ALL STORIES!
// -------------------------------------------------------------------


function isMobile(){
    // returns true if I think we're on mobile.
    return window.innerWidth < 850 ? true : false;
}


if (document.getElementById('comments-button')){
    // If there is a comments button, then init comments on click. Otherwise, skip it. the sidebars 
    // have no comments thus no comments button.
    document.getElementById('comments-button').addEventListener('click', function(e){
        document.querySelector(`.trb_cm_so[data-role="cm_container"]`).style.maxHeight = "10000000vh";
        (window.registration || (registration = [])).push('solidopinion');
    }, false);
}

// Hide/show the mobile navigation menu
// document.getElementById('mobile-nav-toggle').addEventListener('click', function(e){
// 	const mobileNavButton = document.getElementById('nav-buttons-wrapper');
// 	mobileNavButton.classList.toggle('nav-buttons-wrapper--active');
// }, false);

// function pauseVideo(video){
//     pause.classList.toggle('video-control--visible');
//     play.classList.toggle('video-control--visible');
//     video.pause();
// }

// function playVideo(video){
//     pause.classList.toggle('video-control--visible');
//     play.classList.toggle('video-control--visible');
//     video.play();
// }

// Listen for the loaded event 
window.addEventListener('load', function() {  
    
    // Start by working around the dumb chrome bug that doesn't allow you to link to an ID on the page.
    // https://stackoverflow.com/questions/38588346/anchor-a-tags-not-working-in-chrome-when-using
    
        // const isChrome = /Chrome/.test(navigator.userAgent) && /Google Inc/.test(navigator.vendor);
        // if (window.location.hash && isChrome) {
        //     setTimeout(function () {
        //         var hash = window.location.hash;
        //         window.location.hash = "";
        //         window.location.hash = hash;
        //     }, 300);
        // }

    // First, let's load the not lazy graphics
    let pymParents = {};

    const graphics = document.querySelectorAll(".chart:not(.chart--lazy) .graphic-embed");
    
    for (var graphicCounter = 0; graphicCounter < graphics.length; graphicCounter++){
        const   graphic = graphics[graphicCounter],
                pymId = graphic.id,
                pymUrl = graphic.dataset.iframeUrl;
        
            pymParents[pymId] = new pym.Parent(pymId, pymUrl, {});
    }
    
    // Let's set our lazyload offset to 500px. The iframe should be loaded once it's 500px frmo being seen.
    inView.offset(-500);
    
    // Let's lazyload the pym
    inView('.chart--lazy')
        .on('enter', el => {
            const   chartContainer = el.querySelector('.graphic-embed'),
                    pymId = chartContainer.id,
                    pymUrl = chartContainer.dataset.iframeUrl;
            if (!pymParents[pymId]){
                pymParents[pymId] = new pym.Parent(pymId, pymUrl, {});
            }
        });

    // Also, let's lazyload the images
    inView('.image--lazy img')
        .on('enter', el => {
            const src = el.dataset.fullResSrc;
            el.setAttribute('src', src);
        });


    const mySwiper = new Swiper('.swiper-container', {
        speed: 400,
        spaceBetween: 100,
        slidesPerView: 1,
        pagination: '.swiper-pagination',
        nextButton: '.swiper-button-next',
        prevButton: '.swiper-button-prev',
        paginationClickable: true,
        spaceBetween: 30,
        loop: true


    });   
    // if (!isMobile() && document.createElement('video').canPlayType('video/mp4') != "" && document.querySelectorAll('.header-video').length > 0){
    //     // Prep the pause button, if video is supported and we are not on mobile and there is a video header on the page.
    //     const   play = document.getElementById('play'),
    //             pause = document.getElementById('pause'),
    //             video = window.innerWidth > 1100 ? document.querySelector('.header-video--large') : document.querySelector('.header-video--small');
        
    //     // // make the pause button appear
    //     pause.classList.add('video-control--visible');
    
    //     const controlButtons = document.querySelectorAll('.video-control');
    //     for (var buttonCounter= 0; buttonCounter < controlButtons.length; buttonCounter++){
    //         let button = controlButtons[buttonCounter];
    //         button.addEventListener('click', function(e){    
    //             if (e.target.id == "play"){
    //                 playVideo(video)
    //             } else {
    //                 pauseVideo(video)
    //             }
    //         })
    //     }
    //     // Also, let's kill the video after 30 seconds.
    //     var videoKill = setTimeout(function(){
    //         pauseVideo(video)
    //     }, 30000);
    // }
}, false);
