document.addEventListener('DOMContentLoaded', function() {
    const carouselSlide = document.querySelector('.carousel-slide');
    const slides = document.querySelectorAll('.slide-content');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    const indicatorsContainer = document.querySelector('.carousel-indicators');
    
    let currentIndex = 0;
    const slideCount = slides.length;
    
    // Crear indicadores
    slides.forEach((_, index) => {
        const indicator = document.createElement('div');
        indicator.classList.add('indicator');
        if(index === 0) indicator.classList.add('active');
        indicator.addEventListener('click', () => goToSlide(index));
        indicatorsContainer.appendChild(indicator);
    });
    
    const indicators = document.querySelectorAll('.indicator');
    
    // Función para actualizar el carrusel - VERSIÓN CORREGIDA
    function updateCarousel() {
        // Solo movemos el contenedor
        carouselSlide.style.transform = `translateX(-${currentIndex * 100}%)`;
        
        // Actualizar indicadores
        indicators.forEach((indicator, index) => {
            indicator.classList.toggle('active', index === currentIndex);
        });
    }
    
    // Ir a slide específico
    function goToSlide(index) {
        currentIndex = index;
        updateCarousel();
        resetAutoSlide();
    }
    
    // Siguiente slide
    function nextSlide() {
        currentIndex = (currentIndex + 1) % slideCount;
        updateCarousel();
        resetAutoSlide();
    }
    
    // Slide anterior
    function prevSlide() {
        currentIndex = (currentIndex - 1 + slideCount) % slideCount;
        updateCarousel();
        resetAutoSlide();
    }
    
    // Event listeners
    nextBtn.addEventListener('click', nextSlide);
    prevBtn.addEventListener('click', prevSlide);
    
    // Auto-desplazamiento
    let slideInterval;
    function startAutoSlide() {
        slideInterval = setInterval(nextSlide, 5000);
    }
    
    function resetAutoSlide() {
        clearInterval(slideInterval);
        startAutoSlide();
    }
    
    // Pausar al interactuar
    carouselSlide.addEventListener('mouseenter', () => {
        clearInterval(slideInterval);
    });
    
    carouselSlide.addEventListener('mouseleave', startAutoSlide);
    
    // Iniciar
    updateCarousel();
    startAutoSlide();
    
    // Touch events para móviles
    let touchStartX = 0;
    let touchEndX = 0;
    
    carouselSlide.addEventListener('touchstart', (e) => {
        touchStartX = e.changedTouches[0].screenX;
    }, {passive: true});
    
    carouselSlide.addEventListener('touchend', (e) => {
        touchEndX = e.changedTouches[0].screenX;
        handleSwipe();
    }, {passive: true});
    
    function handleSwipe() {
        const difference = touchStartX - touchEndX;
        if (difference > 50) {
            nextSlide(); // Swipe izquierda
        } else if (difference < -50) {
            prevSlide(); // Swipe derecha
        }
    }
});