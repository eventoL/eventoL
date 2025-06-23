document.addEventListener('DOMContentLoaded', function() {
    const track = document.querySelector('.slider-track');
    const images = track.querySelectorAll('img');
    let totalWidth = 0;
    
    images.forEach(img => {
        totalWidth += img.offsetWidth + 40; 
    });
    
    images.forEach(img => {
        const clone = img.cloneNode(true);
        track.appendChild(clone);
    });
    
    const duration = totalWidth * 0.05;
    track.style.animationDuration = `${duration}s`;
});