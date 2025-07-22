// store.js → localStorage işlemleri ve kullanıcıya özel ayarların yönetimi

export function saveSettingsToLocalStorage() {
    const categoryValue = document.getElementById('category-filter')?.value || 'all';
    const productFilterValue = document.getElementById('product-filter')?.value || '';
    const paketSayisi = document.getElementById('paket-sayisi')?.value || '0';
    const selectedCustomerId = document.getElementById('searchbox_customers')?.value || '';
    const selectedProductId = localStorage.getItem('selectedProductId') || '';

    localStorage.setItem('selectedCategory', categoryValue);
    localStorage.setItem('productFilter', productFilterValue);
    localStorage.setItem('paketSayisi', paketSayisi);
    localStorage.setItem('selectedCustomerId', selectedCustomerId);
    localStorage.setItem('selectedProductId', selectedProductId);
}

export function loadSettingsFromLocalStorage() {
    const savedCategory = localStorage.getItem('selectedCategory');
    if (savedCategory) {
        const categoryFilter = document.getElementById('category-filter');
        if (categoryFilter) {
            categoryFilter.value = savedCategory;
            $('#category-filter').trigger('change');
        }
    }

    const savedProductFilter = localStorage.getItem('productFilter');
    if (savedProductFilter) {
        const productFilter = document.getElementById('product-filter');
        if (productFilter) {
            productFilter.value = savedProductFilter;
            $('#product-filter').trigger('input');
        }
    }

    const savedPaketSayisi = localStorage.getItem('paketSayisi');
    if (savedPaketSayisi !== null) {
        const paketInput = document.getElementById('paket-sayisi');
        if (paketInput) {
            paketInput.value = savedPaketSayisi;
        }
    }

    const savedCustomerId = localStorage.getItem('selectedCustomerId');
    if (savedCustomerId) {
        $('#searchbox_customers').val(savedCustomerId).trigger('change');
    }

    const savedProductId = localStorage.getItem('selectedProductId');
    if (savedProductId) {
        const productButton = $(`#all-products .btn[data-id="${savedProductId}"]`);
        if (productButton.length > 0) {
            productButton.trigger('click');
        }
    }

    const hedef = document.getElementById('selected-product-hedef')?.value;
    if (hedef) {
        document.getElementById('hedef-sayisi').textContent = hedef;
    }
}

export function resetStatsOnUserChange(currentUsername) {
    const savedUsername = localStorage.getItem('lastUsername');
    if (savedUsername && savedUsername !== currentUsername) {
        localStorage.setItem('topnet', '0.000');
        localStorage.setItem('pakettopnet', '0.000');
        localStorage.setItem('paketSayisi', '0');
        console.log(`👤 Kullanıcı değişti: ${savedUsername} ➜ ${currentUsername}, sayaçlar sıfırlandı.`);
    }
    localStorage.setItem('lastUsername', currentUsername);
}

export function updatePaketSayisiBeforeUnload() {
    const paketInput = document.getElementById('paket-sayisi');
    if (paketInput) {
        localStorage.setItem('paketSayisi', paketInput.value || '0');
    }
}