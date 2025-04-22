document.addEventListener('DOMContentLoaded', function() {
    const slider = document.querySelector('.slider-container');
    const slides = document.querySelectorAll('.slide');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    let currentIndex = 0;
    let slideWidth = slides[0].clientWidth;
    const gap = 16; // соответствует gap-4 (1rem = 16px)
    
    function updateSlider() {
        slideWidth = slides[0].clientWidth;
        console.log("Ширина слайда:", slideWidth);
        const offset = -(currentIndex * (slideWidth + gap));
        slider.style.transform = `translateX(${offset}px)`;
    }
    
    nextBtn.addEventListener('click', function() {
        currentIndex = (currentIndex + 1) % slides.length;
        updateSlider();
    });
    
    prevBtn.addEventListener('click', function() {
        currentIndex = (currentIndex - 1 + slides.length) % slides.length;
        updateSlider();
    });
    
    // Адаптация при изменении размера окна
    window.addEventListener('resize', function() {
        const newSlideWidth = slides[0].clientWidth;
        if (newSlideWidth !== slideWidth) {
            updateSlider();
        }
    });
});