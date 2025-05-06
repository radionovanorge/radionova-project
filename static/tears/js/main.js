document.addEventListener('DOMContentLoaded', function() {
    // Radio player functionality
    const player = document.getElementById('radio-player');
    const playButton = document.getElementById('play-button');
    const pauseButton = document.getElementById('pause-button');
    
    if (playButton && pauseButton && player) {
        // Play button click
        playButton.addEventListener('click', function() {
            player.play();
            playButton.classList.add('hidden');
            pauseButton.classList.remove('hidden');
        });
        
        // Pause button click
        pauseButton.addEventListener('click', function() {
            player.pause();
            pauseButton.classList.add('hidden');
            playButton.classList.remove('hidden');
        });
    }
    
    // Mobile menu toggle
    const menuToggle = document.getElementById('menu-toggle');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (menuToggle && mobileMenu) {
        menuToggle.addEventListener('click', function() {
            mobileMenu.classList.toggle('hidden');
        });
    }
}); 