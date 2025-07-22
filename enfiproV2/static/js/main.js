// static/js/main.js
import { sendToPrinterWithData } from './print.js';
import { checkStabilityAndDisplay, displayWeight } from './weight.js';
import { loadAllProducts, setupProductEvents } from './product.js';
import { saveSettingsToLocalStorage, loadSettingsFromLocalStorage } from './store.js';
import { config } from './config.js';
import { validateFields } from './validation.js';
import { extractNumericData } from './utils.js';
import { setupEventListeners } from './events.js';

document.addEventListener('DOMContentLoaded', async () => {
    loadSettingsFromLocalStorage();

    try {
        await loadAllProducts(); // şimdi await işe yarayacak
        setupProductEvents();
    } catch (err) {
        console.error("Ürünler yüklenirken hata oluştu:", err);
    }

    setupEventListeners();
});
