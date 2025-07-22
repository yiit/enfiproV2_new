// 📦 product.js
// Ürün seçimi, butonlar, kategori filtreleme, kısa ve uzun basma işlemleri

export function handleShortPress($button) {
    Swal.fire({
        title: 'Ürün Seç',
        text: 'Bu ürünü seçmek istediğinize emin misiniz?',
        icon: 'question',
        showCancelButton: true,
        confirmButtonText: 'Evet, Seç',
        cancelButtonText: 'Hayır, Vazgeç',
    }).then((result) => {
        if (result.isConfirmed) {
            $('#all-products .btn').removeClass('selected');
            $button.addClass('selected');

            const productData = extractProductData($button);
            updateProductFields(productData);
            localStorage.setItem('selectedProductId', productData.id);
        } else {
            console.log("Ürün seçimi iptal edildi.");
        }
    });
}

export function handleLongPress($button) {
    Swal.fire({
        title: '🛠️ Ürün Düzenleme',
        text: 'Bu ürünü düzenlemek için şifre girin:',
        input: 'password',
        inputPlaceholder: 'Yönetici şifresi',
        showCancelButton: true,
        confirmButtonText: 'Giriş Yap',
        cancelButtonText: 'İptal'
    }).then((result) => {
        if (result.isConfirmed) {
            const password = result.value;

            $.ajax({
                url: '/check-admin-password/',
                method: 'POST',
                data: {
                    password: password,
                    csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
                },
                success: function (response) {
                    if (response.success) {
                        const productId = $button.data('id');
                        window.location.href = `/products/update/${productId}`;
                    } else {
                        Swal.fire('❌ Hatalı Şifre', 'Erişim reddedildi.', 'error');
                    }
                },
                error: function () {
                    Swal.fire('⚠️ Hata', 'Sunucuya bağlanılamadı.', 'error');
                }
            });
        }
    });
}

export function extractProductData($button) {
    return {
        id: $button.data('id'),
        isim: $button.data('isim'),
        kod: $button.data('kod'),
        tip: $button.data('tip'),
        adetgramaj: $button.data('adetgramaj'),
        barkod: $button.data('barkod') || 'Barkod Yok',
        min: $button.data('min') || 0,
        max: $button.data('max') || 0,
        hedef: $button.data('hedef'),
        adet: $button.data('adet'),
        etiket: $button.data('etiket') || 'eyz.prn',
        topetiket: $button.data('topetiket'),
        mesaj1: $button.data('mesaj1'),
        mesaj2: $button.data('mesaj2'),
        mesaj3: $button.data('mesaj3'),
        mesaj4: $button.data('mesaj4'),
        mesaj5: $button.data('mesaj5'),
        mesaj6: $button.data('mesaj6'),
        mesaj7: $button.data('mesaj7'),
        mesaj8: $button.data('mesaj8'),
        mesaj9: $button.data('mesaj9'),
        icerik: $button.data('icerik'),
        stt: $button.data('stt'),
        resim: $button.data('resim'),
    };
}

export function updateProductFields(product) {
    $('#selected-product-name').val(product.isim).text(product.isim);
    $('#selected-product-code').val(product.kod);
    $('#selected-product-barkodu').val(product.barkod);
    $('#selected-product-etiket').val(product.etiket);
    $('#selected-product-top-etiket').val(product.topetiket);
    $('#selected-product-min').val(product.min);
    $('#selected-product-max').val(product.max);
    $('#selected-product-hedef').val(product.hedef);
    $('#hedef-sayisi').text(product.hedef);
    $('#selected-product-adet').val(product.adet);
    $('#selected-product-mesaj1').val(product.mesaj1).text(product.mesaj1);
    $('#selected-product-mesaj2').val(product.mesaj2);
    $('#selected-product-mesaj3').val(product.mesaj3);
    $('#selected-product-mesaj4').val(product.mesaj4);
    $('#selected-product-mesaj5').val(product.mesaj5);
    $('#selected-product-mesaj6').val(product.mesaj6);
    $('#selected-product-mesaj7').val(product.mesaj7);
    $('#selected-product-mesaj8').val(product.mesaj8);
    $('#selected-product-mesaj9').val(product.mesaj9);
    $('#selected-product-icerik').val(product.icerik);
    $('#selected-product-stt').val(product.stt);
}

export async function loadAllProducts() {
    const productsContainer = $('#all-products');
    const categoryFilter = $('#category-filter');

    try {
        const response = await $.ajax({
            url: "/sales/get_products/",
            method: 'POST',
            data: {
                all_products: true,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            }
        });

        const allProducts = response;
        productsContainer.empty();

        if (allProducts.length === 0) {
            productsContainer.append('<p>Hiç ürün bulunamadı.</p>');
            return;
        }

        allProducts.forEach(function (product) {
            const productResim = product.urun_resim ? '/media/products/' + product.urun_resim : null;
            const imageTag = productResim ? `<img src="${productResim}" class="product-image">` : '';

            const button = $(` <button class="btn btn-primary m-2"
                data-id="${product.id}"
                data-isim="${product.urun_ismi1}"
                data-kod="${product.urun_kod}"
                data-barkod="${product.urun_barkod || ''}"
                data-tip="${product.urun_tip || ''}"
                data-adet-gramaj="${product.urun_adet_gramaj || 0}"
                data-min="${product.urun_min || 0}"
                data-max="${product.urun_max || 0}"
                data-hedef="${product.urun_hedef || 0}"
                data-adet="${product.urun_adet || 1}"
                data-etiket="${product.urun_etiket || 'eyz.prn'}"
                data-topetiket="${product.urun_top_etiket || ''}"
                data-mesaj1="${product.urun_mesaj1 || ''}"
                data-mesaj2="${product.urun_mesaj2 || ''}"
                data-mesaj3="${product.urun_mesaj3 || ''}"
                data-mesaj4="${product.urun_mesaj4 || ''}"
                data-mesaj5="${product.urun_mesaj5 || ''}"
                data-mesaj6="${product.urun_mesaj6 || ''}"
                data-mesaj7="${product.urun_mesaj7 || ''}"
                data-mesaj8="${product.urun_mesaj8 || ''}"
                data-mesaj9="${product.urun_mesaj9 || ''}"
                data-icerik="${product.urun_icerik || ''}"
                data-stt="${product.urun_stt || ''}"
                data-resim="${product.urun_resim || ''}">
                <span>${product.urun_ismi1}</span>
                ${imageTag}
                <span class="badge">${product.urun_barkod}</span>
            </button>`);

            productsContainer.append(button);
        });

    } catch (error) {
        console.error('Ürünler yüklenemedi:', error);
        throw error; // main.js yakalasın diye dışarı fırlat
    }
}
