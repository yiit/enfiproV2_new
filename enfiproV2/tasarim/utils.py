# tasarim/utils.py
def tasarimi_tspl_cevir(tasarim):
    tspl_komutlari = []
    for eleman in tasarim.split(';'):
        if eleman:
            id, konum = eleman.split(':')
            x, y = konum.split(',')
            if id == 'barkod':
                tspl_komutlari.append(f'BARCODE {x},{y},"128",50,1,0,2,2,"123456789"')
            elif id == 'qrcode':
                tspl_komutlari.append(f'QRCODE {x},{y},"L",5,"A",0,"QR Code"')
    return '\n'.join(tspl_komutlari)