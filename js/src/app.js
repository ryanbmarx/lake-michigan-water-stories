// import "babel-polyfill";
const inView = require('in-view');
const pym = require('./pym.trib.js');
const Swiper = require('swiper.min.js');
// const boot = require('bootstrap.js');

// -------------------------------------------------------------------
// THIS APP.JS ONLY IS FOR CODE NEEDED FOR ALL STORIES!
// -------------------------------------------------------------------


function isMobile(){
    // returns true if I think we're on mobile.
    return window.innerWidth < 850 ? true : false;
}

// This is the nav window story toggle 
const   navMenuToggle = document.querySelector("#mobile-nav-toggle");

navMenuToggle.addEventListener('click', function(e){
    document.querySelector('.nav-buttons-wrapper').classList.toggle('nav-buttons-wrapper--visible')
});


if (document.getElementById('comments-button')){
    // If there is a comments button, then init comments on click. Otherwise, skip it. the sidebars 
    // have no comments thus no comments button.
    document.getElementById('comments-button').addEventListener('click', function(e){
        document.querySelector(`.trb_cm_so[data-role="cm_container"]`).style.maxHeight = "10000000vh";
        (window.registration || (registration = [])).push('solidopinion');
    }, false);
}

function pauseVideo(video){
    pause.classList.toggle('video-control--visible');
    play.classList.toggle('video-control--visible');
    video.pause();
}

function playVideo(video){
    pause.classList.toggle('video-control--visible');
    play.classList.toggle('video-control--visible');
    video.play();
}

// Listen for the loaded event 
window.addEventListener('load', function() {  

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

            let src = isMobile ? el.dataset.fullResSrc.replace('/1200', "/850") : el.dataset.fullResSrc ;
            console.log('adding', src);
            el.setAttribute('src', src);
        });

    const swipers = [].slice.call(document.querySelectorAll('.swiper-container'));
    if (swipers.length > 0){
        const slideshows = {};
        swipers.forEach((swiper, index) => {
            //if there are swipers, iterate over the containers array and init them.
            slideshows[index] = new Swiper('.swiper-container', {
                speed: 400,
                slidesPerView: 1,
                centeredSlides: true,
                pagination: '.swiper-pagination',
                nextButton: '.swiper-button-next',
                prevButton: '.swiper-button-prev',
                // scrollBar: '.swiper-scrollbar',
                paginationClickable: true,
                spaceBetween: 30,
                loop: true,
                // Disable preloading of all images
                // preloadImages: false,
                // // Enable lazy loading
                // lazyLoading: true,
                // watchSlidesProgress:true,
                // watchSlidesVisibility:true
            }); 

            console.log(slideshows, index)
            swiper.querySelector('.swiper-button-next').addEventListener('click', e => {
                console.log('click next')
                slideshows[index].slideNext();
            });

            swiper.querySelector('.swiper-button-prev').addEventListener('click', e => {
                console.log('click prev')
                slideshows[index].slidePrev();
            });            
        })

}

    if (!isMobile() && document.createElement('video').canPlayType('video/mp4') != "" && document.querySelectorAll('.header-video').length > 0){
        // Prep the pause button, if video is supported and we are not on mobile and there is a video header on the page.
        const   play = document.getElementById('play'),
                pause = document.getElementById('pause'),
                video = document.querySelector('.header-video');
        
        // // make the pause button appear
        pause.classList.add('video-control--visible');
    
        const controlButtons = document.querySelectorAll('.video-control');
        for (var buttonCounter= 0; buttonCounter < controlButtons.length; buttonCounter++){
            let button = controlButtons[buttonCounter];
            button.addEventListener('click', function(e){    
                if (e.target.id == "play"){
                    playVideo(video)
                } else {
                    pauseVideo(video)
                }
            })
        }
        // Also, let's kill the video after 30 seconds.
        var videoKill = setTimeout(function(){
            pauseVideo(video)
        }, 30000);
    }
}, false);
