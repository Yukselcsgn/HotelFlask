document.addEventListener('DOMContentLoaded', function() {
    const slides = document.querySelectorAll('.carousel-slide');
    const prevBtn = document.getElementById('carouselPrev');
    const nextBtn = document.getElementById('carouselNext');
    let current = 0;
    let timer = null;

    function showSlide(idx) {
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === idx);
        });
        current = idx;
    }
    function nextSlide() {
        showSlide((current + 1) % slides.length);
    }
    function prevSlide() {
        showSlide((current - 1 + slides.length) % slides.length);
    }
    nextBtn.addEventListener('click', () => {
        nextSlide();
        resetTimer();
    });
    prevBtn.addEventListener('click', () => {
        prevSlide();
        resetTimer();
    });
    function resetTimer() {
        if (timer) clearInterval(timer);
        timer = setInterval(nextSlide, 5000);
    }
    showSlide(0);
    timer = setInterval(nextSlide, 5000);
}); 