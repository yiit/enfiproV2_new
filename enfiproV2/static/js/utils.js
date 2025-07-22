// utils.js → Genel yardımcı fonksiyonlar, formatlama işlemleri, debounce gibi yardımcılar

export function roundTo(n, digits = 0) {
    const multiplicator = Math.pow(10, digits);
    n = parseFloat((n * multiplicator).toFixed(11));
    return Math.round(n) / multiplicator;
}

// Debounce fonksiyonu (örneğin input değişimlerinde kullanmak için)
export function debounce(func, delay) {
    let timeout;
    return function (...args) {
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(this, args), delay);
    };
}

// Belirli bir sayının belirli bir aralıkta olup olmadığını kontrol eder
export function isBetween(value, min, max) {
    return value >= min && value <= max;
}

// Sayısal değeri, boşlukla doldurulmuş belirli uzunlukta bir string'e çevirir
export function padNumberToLength(value, length = 8) {
    const str = parseFloat(value).toFixed(1);
    return str.padStart(length, ' ');
}

// DOM'dan numeric değer çekici güvenli yöntem
export function getNumericInputValue(id) {
    const val = document.getElementById(id)?.value;
    return parseFloat(val) || 0;
}

// DOM'dan text değer çekici güvenli yöntem
export function getTextInputValue(id) {
    return document.getElementById(id)?.value.trim() || '';
}

// DOM'dan innerText olarak sayı çekici yöntem
export function getNumericTextContent(id) {
    const val = document.getElementById(id)?.textContent;
    return parseFloat(val) || 0;
}

// Sayfa altına otomatik kaydırma
export function scrollToBottom(containerSelector) {
    const container = document.querySelector(containerSelector);
    if (container) {
        container.scrollTop = container.scrollHeight;
    }
}