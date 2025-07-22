// 📦 printer.js
// Yazdırma işlemleri ve animasyonlar

import { showSuccessAnimation } from './uiHelpers.js';
import { collectFormData } from './formUtils.js';
import { validateFields } from './validation.js';

export async function sendToPrinterWithData(printData, printSource = 'auto', skipAutoAlert = false) {
    try {
        printData.printSource = printSource;

        const response = await fetch('/sales/print/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            },
            body: JSON.stringify(printData)
        });

        const data = await response.json();

        if (!response.ok) {
            console.error('Hata:', data.message);
            await Swal.fire({
                icon: 'error',
                title: 'Yazdırma Hatası!',
                text: `(${printSource}): ${data.message}`,
                timer: 3000,
                showConfirmButton: false
            });
            return;
        }

        console.log(`${printSource.toUpperCase()} yazdırma başarılı:`, data.message);

        if (printSource === 'manual') {
            await showSuccessAnimation(true);
        } else if (!skipAutoAlert) {
            await showSuccessAnimation(false);
        }

    } catch (error) {
        console.error('Yazdırma sırasında bir hata oluştu:', error.message);
        await Swal.fire({
            icon: 'error',
            title: 'Yazdırma Hatası!',
            text: `(${printSource}): Yazdırma sırasında bir hata oluştu.`,
            timer: 3000,
            showConfirmButton: false
        });
    }
}

export async function handlePrint(weightToPrint, isManual = true) {
    if (!validateFields()) return;

    const finalWeight = parseFloat(weightToPrint) || 0;
    if (finalWeight <= 0 && isManual) {
        await Swal.fire({
            icon: 'warning',
            title: 'Ağırlık Geçersiz!',
            text: 'Yazdırma işlemi için ağırlık 0 kg\'dan büyük olmalıdır.',
            timer: 3000,
            showConfirmButton: false
        });
        return;
    }

    await sendToPrinterWithData(collectFormData(finalWeight.toFixed(3)), isManual ? 'manual' : 'auto', !isManual);
}