// events.js
// Global event dinleyicileri ve kullanıcı etkileşimleri burada yönetilir

import { handleShortPress, handleLongPress } from './product.js';
import { toggleAutoPrintMode } from './config.js';

let pressTimer;
const longPressDuration = 2000; // 2 saniye

export function registerGlobalEvents() {
    const printButton = document.getElementById('print-button');

    // Manuel yazdırma için tıklama
    printButton?.addEventListener('click', (e) => e.preventDefault());

    // Uzun basma işlemi ile otomatik yazdırma modunu aç/kapat
    printButton?.addEventListener('mousedown', startLongPress);
    printButton?.addEventListener('touchstart', startLongPress);
    printButton?.addEventListener('mouseup', cancelLongPress);
    printButton?.addEventListener('mouseleave', cancelLongPress);
    printButton?.addEventListener('touchend', cancelLongPress);
    printButton?.addEventListener('touchcancel', cancelLongPress);

    // Sağ tık menüsünü devre dışı bırak
    window.addEventListener('contextmenu', e => e.preventDefault());

    // Tüm ürün butonları için kısa ve uzun basma işlemleri
    $(document).on('mousedown touchstart', '#all-products .btn', handleProductPressStart);
    $(document).on('mouseup touchend touchcancel mouseleave', '#all-products .btn', handleProductPressEnd);
    $(document).on('mousemove touchmove', '#all-products .btn', handleProductPressMove);
}

// Uzun basma başlatılır
function startLongPress(e) {
    e.preventDefault();
    clearTimeout(pressTimer);
    pressTimer = setTimeout(() => toggleAutoPrintMode(), longPressDuration);
}

function cancelLongPress() {
    clearTimeout(pressTimer);
}

// Ürün seçimi için global etkileşim kontrolleri
let productPressTimer = null;
let productScrollDetected = false;
let startX = 0;
let startY = 0;
const SCROLL_THRESHOLD = 5;

function handleProductPressStart(e) {
    productScrollDetected = false;
    const $target = $(this);

    if (e.type === 'mousedown') {
        startX = e.clientX;
        startY = e.clientY;
    } else if (e.type === 'touchstart') {
        const touch = e.originalEvent.touches[0];
        startX = touch.clientX;
        startY = touch.clientY;
    }

    productPressTimer = setTimeout(() => {
        handleLongPress($target);
    }, longPressDuration);
}

function handleProductPressMove(e) {
    let currentX, currentY;
    if (e.type === 'mousemove') {
        currentX = e.clientX;
        currentY = e.clientY;
    } else if (e.type === 'touchmove') {
        const touch = e.originalEvent.touches[0];
        currentX = touch.clientX;
        currentY = touch.clientY;
    }

    const dx = currentX - startX;
    const dy = currentY - startY;
    if (Math.abs(dx) > SCROLL_THRESHOLD || Math.abs(dy) > SCROLL_THRESHOLD) {
        productScrollDetected = true;
        clearTimeout(productPressTimer);
    }
}

function handleProductPressEnd(e) {
    clearTimeout(productPressTimer);

    const $target = $(this);
    if (!productScrollDetected) {
        handleShortPress($target);
    }
}