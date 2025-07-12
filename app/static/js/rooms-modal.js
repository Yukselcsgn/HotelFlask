// Oda modalında oda görselleri önce, ortak görseller (images ana klasörü) en sonda gösterilir.
const roomImages = {
    'standart': [
        '/static/images/standart/9091541f-bdec-4f78-b9c4-232473eaece0.jpg',
        '/static/images/standart/88905837-a54e-4e39-9e9f-1c177207159f.jpg'
    ],
    'deluxe': [
        '/static/images/deluxe/e12f74b8-fbe6-4e05-bde5-071da5dd079f.jpg',
        '/static/images/deluxe/a52dce7f-5201-4598-b77b-b93a56b38108.jpg',
        '/static/images/deluxe/WhatsApp Image 2025-06-30 at 17.09.38.jpeg'
    ],
    'suit': [
        '/static/images/suit/ec65c984-113b-42dc-87d9-06dcc1114d52.jpg',
        '/static/images/suit/a64d9336-499c-4d54-a068-5b06132e8a07.jpg',
        '/static/images/suit/411306cf-c4e8-4630-960c-a866d47d5b70.jpg'
    ]
};
const commonImages = [
    '/static/images/a688f843-02d6-4e5e-a1e6-9a5786f2be77.jpg',
    '/static/images/55044517-dfe9-4615-ad4b-b5e2d19b4208.jpg',
    '/static/images/761af1cf-a71b-4940-8028-c85964722a87.jpg',
    '/static/images/594e9ecf-771c-46ba-a1e9-c3b0c4306d01.jpg',
    '/static/images/100b6ac2-2993-434e-8a37-e57cef192f87.jpg',
    '/static/images/57e75f88-7aa1-40d7-aa13-860cad90f4fb.jpg',
    '/static/images/2a01acd5-4c3a-4f3c-937e-28eea8587114.jpg',
    '/static/images/ab0d7649-b2c0-457d-94df-f1ba32bc23aa.jpg',
    '/static/images/acb9b965-c63b-4d58-9419-7955a7258277.jpg',
    '/static/images/c009ac2d-ec8f-4eae-b6d1-070e9ee1eb15.jpg',
    '/static/images/e8a1bceb-69b8-472f-a1cd-595c23f3e0f4.jpg',
    '/static/images/WhatsApp-Image-2025-06-30-at-17.09.36.jpg',
    '/static/images/e25a5afb-da1c-4602-bb19-7b233e92de07.jpg',
    '/static/images/eb7be851-19e9-4211-b957-15108493bc73.jpg',
    '/static/images/WhatsApp-Image-2025-06-30-at-17.09.36-_1_.jpg'
];

let currentImages = [];
let currentIndex = 0;

function openLightbox(index) {
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    if (!currentImages.length) return;
    currentIndex = index;
    lightboxImg.src = currentImages[currentIndex];
    lightbox.style.display = 'flex';
}
function closeLightbox() {
    document.getElementById('lightbox').style.display = 'none';
}
function showPrev() {
    if (!currentImages.length) return;
    currentIndex = (currentIndex - 1 + currentImages.length) % currentImages.length;
    document.getElementById('lightbox-img').src = currentImages[currentIndex];
}
function showNext() {
    if (!currentImages.length) return;
    currentIndex = (currentIndex + 1) % currentImages.length;
    document.getElementById('lightbox-img').src = currentImages[currentIndex];
}

document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('roomModal');
    const modalImages = document.getElementById('modalImages');
    const closeBtn = modal.querySelector('.close');
    const cards = document.querySelectorAll('.room-card[data-room]');
    const lightbox = document.getElementById('lightbox');
    const lightboxImg = document.getElementById('lightbox-img');
    const lightboxClose = document.querySelector('.lightbox-close');
    const lightboxPrev = document.querySelector('.lightbox-prev');
    const lightboxNext = document.querySelector('.lightbox-next');

    cards.forEach(card => {
        card.addEventListener('click', function() {
            const room = card.getAttribute('data-room');
            // Oda görselleri + ortak görseller (ortaklar en sonda)
            const images = (roomImages[room] || []).concat(commonImages);
            currentImages = images;
            modalImages.innerHTML = images.map((src, i) => `<div class='modal-image-wrapper'><img src="${src}" loading="lazy" alt="Oda Fotoğrafı" data-index="${i}"></div>`).join('');
            modal.style.display = 'block';
            // Dikey (portrait) görsellere özel sınıf ekle
            setTimeout(() => {
                document.querySelectorAll('#modalImages img').forEach(img => {
                    img.onload = function() {
                        if (img.naturalHeight > img.naturalWidth) {
                            img.classList.add('portrait');
                        }
                    };
                    // Lightbox açma
                    img.onclick = function(e) {
                        e.stopPropagation();
                        openLightbox(Number(img.getAttribute('data-index')));
                    };
                });
            }, 50);
        });
    });

    // Lightbox kapatma
    lightboxClose.onclick = closeLightbox;
    lightboxImg.onclick = showNext;
    lightboxPrev.onclick = showPrev;
    lightboxNext.onclick = showNext;
    // Modal kapatılırsa lightbox da kapansın
    closeBtn.addEventListener('click', function() {
        closeLightbox();
    });
    window.addEventListener('click', function(e) {
        if (e.target === modal) {
            modal.style.display = 'none';
            closeLightbox();
        }
    });
    // Klavye ile gezinme
    document.addEventListener('keydown', function(e) {
        if (lightbox.style.display === 'flex') {
            if (e.key === 'ArrowLeft') showPrev();
            if (e.key === 'ArrowRight') showNext();
            if (e.key === 'Escape') closeLightbox();
        }
    });
    // Mobil swipe desteği
    let startX = null;
    lightboxImg.addEventListener('touchstart', function(e) {
        startX = e.touches[0].clientX;
    });
    lightboxImg.addEventListener('touchend', function(e) {
        if (startX === null) return;
        let endX = e.changedTouches[0].clientX;
        if (endX - startX > 40) showPrev();
        else if (startX - endX > 40) showNext();
        startX = null;
    });
}); 