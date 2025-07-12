// Tab sistemi
function showTab(tabName) {
    // Tüm tab içeriklerini gizle
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(content => {
        content.classList.remove('active');
    });
    
    // Tüm tab linklerini pasif yap
    const navTabs = document.querySelectorAll('.nav-tab');
    navTabs.forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Seçilen tabı aktif yap
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Fiyat düzenleme
function editPrice(roomType, currentPrice, currentDescription) {
    const newPrice = prompt(`${roomType} oda fiyatını güncelleyin:`, currentPrice);
    if (newPrice === null) return;
    
    const newDescription = prompt(`${roomType} oda açıklamasını güncelleyin:`, currentDescription);
    if (newDescription === null) return;
    
    // Form oluştur ve gönder
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = '/admin/prices/update';
    
    const roomTypeInput = document.createElement('input');
    roomTypeInput.type = 'hidden';
    roomTypeInput.name = 'room_type';
    roomTypeInput.value = roomType;
    
    const priceInput = document.createElement('input');
    priceInput.type = 'hidden';
    priceInput.name = 'price';
    priceInput.value = newPrice;
    
    const descInput = document.createElement('input');
    descInput.type = 'hidden';
    descInput.name = 'description';
    descInput.value = newDescription;
    
    form.appendChild(roomTypeInput);
    form.appendChild(priceInput);
    form.appendChild(descInput);
    
    document.body.appendChild(form);
    form.submit();
}

// Modal işlemleri
function viewReservation(reservationId) {
    // Bu fonksiyon gelecekte rezervasyon detaylarını göstermek için kullanılabilir
    alert('Rezervasyon ID: ' + reservationId + ' detayları görüntülenecek');
}

// Modal kapatma
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('reservationModal');
    const closeBtn = document.querySelector('.close');
    
    if (closeBtn) {
        closeBtn.onclick = function() {
            modal.style.display = "none";
        }
    }
    
    // Modal dışına tıklandığında kapatma
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }
});

// Tablo sıralama (gelecekte eklenebilir)
function sortTable(column) {
    // Tablo sıralama fonksiyonu
    console.log('Sıralama: ' + column);
} 