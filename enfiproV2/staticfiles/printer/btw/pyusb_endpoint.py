import usb.core
import usb.util

# Bağlı tüm USB cihazlarını bul
device = usb.core.find(idVendor=0x0fe6, idProduct=0x8800)  # Vendor ID ve Product ID'yi burada belirtin

if device is None:
    print("Cihaz bulunamadı.")
else:
    print("Cihaz bulundu!")
    print(f"Vendor ID: {hex(device.idVendor)}, Product ID: {hex(device.idProduct)}")

    # Cihazdaki tüm yapılandırmaları listele
    for cfg in device:
        print(f"\nConfiguration {cfg.bConfigurationValue}:")
        for intf in cfg:
            print(f"  Interface {intf.bInterfaceNumber}, Alt Setting {intf.bAlternateSetting}")
            for ep in intf:
                print(f"    Endpoint Address: {hex(ep.bEndpointAddress)}")
                print(f"      Attributes: {hex(ep.bmAttributes)}")
                print(f"      Max Packet Size: {ep.wMaxPacketSize}")
                print(f"      Polling Interval: {ep.bInterval}")
