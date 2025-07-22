// 📡 fetchWeight.js
// Node.js sunucusundan verileri alır, ağırlık kontrolü ve görüntüleme işlemleri yapar

import { extractNumericData } from './utils.js';
import { checkStabilityAndDisplay, displayWeight } from './fetchWeight.js';

const nodeServerIp = "http://localhost";
const url = `${nodeServerIp}:3000/data`;

let isFetching = false;

export async function fetchDataFromNode() {
    if (isFetching) return;
    isFetching = true;

    try {
        const response = await fetch(url, {
            method: 'GET',
            mode: 'cors',
            headers: { 'Accept': 'application/json' }
        });

        if (!response.ok) {
            throw new Error(`[HTTP ERROR] ${response.status} - ${response.statusText}`);
        }

        const data = await response.json();

        if (data && data.data) {
            const rawData = data.data;
            const numericData = extractNumericData(rawData);

            if (numericData !== null) {
                checkStabilityAndDisplay(numericData);
            } else {
                displayWeight('Veri Hatası', false, true);
            }
        } else {
            displayWeight('Bağlantı Yok', false, true);
        }
    } catch (error) {
        console.error("[CLIENT] Fetch error:", error);
        displayWeight('Bağlantı Hatası', false, true);
    } finally {
        isFetching = false;
    }
}

// Periyodik çağırmak için dışarıda setInterval yerine bu modül çağrılırken kullanılabilir.
// Örn: setInterval(fetchDataFromNode, 500);