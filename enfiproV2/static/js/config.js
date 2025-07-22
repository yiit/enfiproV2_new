// config.js
// Bu dosya global sabitler, ayarlar ve başlangıç değerlerini tutar

export const API = {
    PRINT_URL: '/sales/print/',
    CUSTOMER_INFO_URL: '/sales/get_customer_info/',
    NODE_SERVER_URL: 'http://localhost:3000/data',
};

export const TIMEOUTS = {
    STABLE_WEIGHT_DURATION: 1000,     // ms
    DISPLAY_DURATION: 1000,          // ms
    WEIGHT_TIMEOUT: 2000,            // ms
    LONG_PRESS_DURATION: 2000        // ms
};

export const RATIOS = {
    REPRINT_LOWER: 0.70,  // %30 az
    REPRINT_UPPER: 1.50   // %50 fazla
};

export const LOCAL_STORAGE_KEYS = {
    TOP_NET: 'topnet',
    PAKET_TOP_NET: 'pakettopnet',
    PAKET_SAYISI: 'paketSayisi',
    LAST_USERNAME: 'lastUsername',
    SELECTED_PRODUCT_ID: 'selectedProductId',
    SELECTED_CATEGORY: 'selectedCategory',
    PRODUCT_FILTER: 'productFilter',
    SELECTED_CUSTOMER_ID: 'selectedCustomerId'
};

export const DOM_IDS = {
    WEIGHT_DISPLAY: 'weight-display',
    WEIGHT_VALUE: '.value',
    UNIT_VALUE: '.unit',
    PAKET_SAYISI_INPUT: 'paket-sayisi',
    PAKET_TOP_NET_LABEL: 'paket-top-net',
    TOP_NET_LABEL: 'topnet',
    SELECTED_PRODUCT_MIN: 'selected-product-min',
    SELECTED_PRODUCT_MAX: 'selected-product-max',
    SELECTED_PRODUCT_HEDEF: 'selected-product-hedef',
    PRINT_BUTTON: 'print-button'
};

export const COLORS = {
    STABLE: 'green',
    UNSTABLE: 'red'
};

export const PRINT_MODE = {
    AUTO: 'auto',
    MANUAL: 'manual',
    COPY_PRODUCT: 'copy-product',
    COPY_TOTAL: 'copy-total'
};

export let globalState = {
    isAutoPrintMode: true,
    yazdirmaAktif: false,
    displayingWeight: false,
    lastPrintedWeight: null,
    stableStartTime: null,
    previousWeight: null,
    topn