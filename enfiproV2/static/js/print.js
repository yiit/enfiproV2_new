// 📦 printHandler.js
// Yazdırma işlemleri (otomatik ve manuel), veri toplama ve sayaçları yönetir

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
            paketSayisi = 0;
            $('#paket-sayisi').val('0');
            localStorage.setItem('paketSayisi', '0');

            pakettopnet = 0.000;
            $('#paket-top-net').text(pakettopnet.toFixed(3));
            localStorage.setItem('pakettopnet', pakettopnet.toFixed(3));

            await Swal.fire({
                icon: 'success',
                width: 700,
                padding: '2em',
                timer: 7000,
                showConfirmButton: false,
                html: `
                    <p style="color: #28a745; font-weight: bold; font-size: 28px;">Yazdırma Başarılı!</p>
                    <p style="font-size: 20px;">Toplam Etiketi Yazdırıldı.</p>
                    <div id="kapakAnim" style="width: 500px; height: 500px; margin: 0 auto;"></div>
                `,
                didOpen: () => {
                    lottie.loadAnimation({
                        container: document.getElementById('kapakAnim'),
                        renderer: 'svg',
                        loop: false,
                        autoplay: true,
                        path: "{% static 'animations/kapak-animasyonu.json' %}"
                    });
                }
            });

            await new Promise(resolve => setTimeout(resolve, 200));
        } else {
            if (!skipAutoAlert) {
                await Swal.fire({
                    icon: 'success',
                    width: 500,
                    timer: 1000,
                    showConfirmButton: false,
                    html: `
                    <p style="color: #28a745; font-weight: bold; font-size: 28px;">Yazdırma Başarılı!</p>
                    <p style="font-size: 20px;">Ürün Etiketi Yazdırıldı.</p>
                `,
                });

                await new Promise(resolve => setTimeout(resolve, 200));
            }
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

export async function doPrint(newWeight) {
    if (displayingWeight) {
        console.log("Yazdırma zaten devam ediyor...");
        return;
    }

    displayingWeight = true;
    console.log("✅ Yazdırılıyor:", newWeight, "kg");
    displayWeight(newWeight, true, false);

    lastPrintedWeight = newWeight;

    const formattedWeight = newWeight.toFixed(3);

    paketSayisi = parseInt($('#paket-sayisi').val()) || 0;
    paketSayisi++;
    $('#paket-sayisi').val(paketSayisi);
    localStorage.setItem('paketSayisi', paketSayisi);

    pakettopnet = parseFloat($('#paket-top-net').text()) || 0; 
    pakettopnet += newWeight;
    $('#paket-top-net').text(pakettopnet.toFixed(3));
    localStorage.setItem('pakettopnet', pakettopnet.toFixed(3));

    topnet += newWeight;
    $('#topnet').text(topnet.toFixed(3));
    localStorage.setItem('topnet', topnet.toFixed(3));

    await sendToPrinterWithData(collectFormData(formattedWeight), 'auto', false);

    await incrementPaketSayisi();
    displayingWeight = false;
}

export function collectFormData(weight) {
    const productAdetValue = parseFloat(document.getElementById('selected-product-adet').value) || 0;
    const paketSayisiValue = parseFloat(document.getElementById('paket-sayisi').value) || 0;

    return {
        weight: weight,
        customerName: document.getElementById('selected-customer-name').value,
        customerName2: document.getElementById('selected-customer-name2').value,
        customerAddress: document.getElementById('selected-customer-address').value,
        productName: document.getElementById('selected-product-name').value,
        productCode: document.getElementById('selected-product-code').value,
        productBarkod: document.getElementById('selected-product-barkodu').value,
        etiketText: document.getElementById('selected-product-etiket').value || 'eyz.prn',
        topetiketText: document.getElementById('selected-product-top-etiket').value,
        productMesaj1: document.getElementById('selected-product-mesaj1').value,
        productMesaj2: document.getElementById('selected-product-mesaj2').value,
        productMesaj3: document.getElementById('selected-product-mesaj3').value,
        productMesaj4: document.getElementById('selected-product-mesaj4').value,
        productMesaj5: document.getElementById('selected-product-mesaj5').value,
        productMesaj6: document.getElementById('selected-product-mesaj6').value,
        productMesaj7: document.getElementById('selected-product-mesaj7').value,
        productMesaj8: document.getElementById('selected-product-mesaj8').value,
        productMesaj9: document.getElementById('selected-product-mesaj9').value,
        producticerik: document.getElementById('selected-product-icerik').value,
        productstt: document.getElementById('selected-product-stt').value,
        paketSayisi: paketSayisiValue.toString(),
        pakettopnet: parseFloat(document.getElementById('paket-top-net').textContent || "0").toFixed(3),
        topnet: parseFloat(localStorage.getItem("topnet") || "0").toFixed(3),
        operator: document.getElementById('logged-in-username').value,
        topAdet: (productAdetValue * paketSayisiValue).toString()
    };
}

export async function incrementPaketSayisi() {
    const hedefDegeri = parseInt($('#selected-product-hedef').val()) || 0;

    if (hedefDegeri > 0 && paketSayisi >= hedefDegeri) {
        console.log("🎯 Hedefe ulaşıldı! Manuel yazdırma tetikleniyor...");

        let weightToPrint = lastPrintedWeight !== null ? lastPrintedWeight.toFixed(3) : '0.000';
        if (weightToPrint === '0.000') {
            const weightElement = document.getElementById('weight-display').querySelector('.value');
            if (weightElement) {
                weightToPrint = parseFloat(weightElement.textContent).toFixed(3);
            }
        }

        await sendToPrinterWithData(collectFormData(weightToPrint), 'manual', true);

        paketSayisi = 0;
        $('#paket-sayisi').val('0');
        localStorage.setItem('paketSayisi', '0');

        pakettopnet = 0.000;
        $('#paket-top-net').text(pakettopnet.toFixed(3));
        localStorage.setItem('pakettopnet', pakettopnet.toFixed(3));
    }
}
