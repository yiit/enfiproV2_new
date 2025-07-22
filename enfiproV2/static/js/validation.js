// validation.js - Form alanlarını ve yazdırma öncesi kontrolleri içerir

export function validateFields(autoPrintWarningDisplayed = false) {
    const missingFields = [];
    const fieldMap = {
        'selected-customer-name': 'Müşteri Seçilmemiş',
        'selected-product-name': 'Ürün Seçilmemiş',
        // Diğer gerekli alanlar buraya eklenebilir
    };

    for (const [fieldId, label] of Object.entries(fieldMap)) {
        const fieldValue = document.getElementById(fieldId)?.value.trim();
        if (!fieldValue) {
            missingFields.push(label);
        }
    }

    if (missingFields.length > 0) {
        if (!autoPrintWarningDisplayed) {
            Swal.fire({
                icon: 'warning',
                title: 'Eksik Bilgiler',
                html: `Lütfen aşağıdaki alanları doldurun:<br><strong>${missingFields.join(', ')}</strong>`,
                confirmButtonText: 'Tamam',
                confirmButtonColor: '#3085d6',
                background: '#f7f7f7'
            });
        }
        return false;
    }
    return true;
}