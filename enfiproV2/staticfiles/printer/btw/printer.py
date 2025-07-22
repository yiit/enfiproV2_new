import usb.core
import usb.util

VENDOR_ID = 0x0fe6
PRODUCT_ID = 0x8800
OUT_ENDPOINT = 0x01

# Yazıcıyı bul
printer = usb.core.find(idVendor=VENDOR_ID, idProduct=PRODUCT_ID)

if printer is None:
    print("Yazıcı bulunamadı.")
else:
    # Kernel sürücüsünü serbest bırak (gerekirse)
    if printer.is_kernel_driver_active(0):
        printer.detach_kernel_driver(0)

    # Konfigürasyonu ayarla
    printer.set_configuration()

    # Yazdırma komutu (örnek TSPL kodu)
    tspl_command = b"SIZE 100 mm,100 mm\nGAP 2 mm,0\nPRINT 1\n"
    printer.write(OUT_ENDPOINT, tspl_command)

    print("TSPL komutu yazıcıya gönderildi!")
