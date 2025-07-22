import usb.core

# Bağlı tüm USB cihazlarını bul
devices = usb.core.find(find_all=True)

if not devices:
    print("Bağlı USB cihazı bulunamadı.")
else:
    print("Bağlı USB cihazlarının Vendor ID ve Product ID'leri:")
    for device in devices:
        print(f"Vendor ID: {hex(device.idVendor)}, Product ID: {hex(device.idProduct)}")
