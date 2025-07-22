// Gerekli kütüphaneleri çağır
const express = require('express');
const { SerialPort } = require('serialport');
const { ReadlineParser } = require('@serialport/parser-readline');
const cors = require('cors');

const app = express();
const portNumber = 3000;

let latestData = ''; 
let lastReceivedTime = 0;

app.use(cors());

const SERIAL_PATH = '/dev/ttyS0';

console.log("[*] Seri port başlatılıyor...");

const serialPort = new SerialPort({ path: SERIAL_PATH, baudRate: 9600 }, (err) => {
    if (err) {
        return console.error(`⛔ Seri port açılamadı: ${err.message}`);
    }

    console.log(`✅ Seri port ${SERIAL_PATH} başarıyla açıldı.`);

    const parser = serialPort.pipe(new ReadlineParser({ delimiter: '\n' }));

    parser.on('data', (data) => {
        console.log(`📥 Veri alındı: ${data}`);
        latestData = data;
        lastReceivedTime = Date.now();
    });

    serialPort.on('error', (err) => {
        console.error(`⛔ Seri Port Hatası: ${err.message}`);
    });

    serialPort.on('close', () => {
        console.log("⚠ Seri port kapandı.");
    });
});

app.get('/data', (req, res) => {
    if (Date.now() - lastReceivedTime > 5000) {
        return res.json({ error: "Bağlantı hatası: Teraziden veri alınamıyor." });
    } else {
        return res.json({ data: latestData });
    }
});

app.listen(portNumber, '0.0.0.0', () => {
    console.log(`🚀 Server is running at http://0.0.0.0:${portNumber}`);
});
