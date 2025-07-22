#!/bin/bash

# Hata olursa scripti durdur
set +e

echo "🚀 EnfiproV2 Kurulumu Başlıyor..."
read -p "Devam etmek için ENTER'a basın..."

#########################################
# 1. TEMEL SİSTEM GÜNCELLEME ve PAKETLER
#########################################
echo "📦 Linux sistem güncelleniyor ve temel paketler kuruluyor..."
sudo apt update
sudo apt install -y python3-evdev beep

TOUCH_NAME="ILITEK ILITEK-TP"
SERVICE_NAME="touch-beep"
BEEP_FREQ=500
BEEP_LEN=120

echo "==> pcspkr modülü etkinleştiriliyor …"
if ! lsmod | grep -q pcspkr; then
  sudo modprobe pcspkr
fi
echo "pcspkr" | sudo tee /etc/modules-load.d/pcspkr.conf >/dev/null

echo "==> /usr/bin/beep için yetenek veriliyor …"
sudo setcap 'cap_sys_tty_config+ep' /usr/bin/beep

echo "==> Dokunmatik event dosyası aranıyor …"
EVENT_PATH=$(grep -E -A5 "$TOUCH_NAME" /proc/bus/input/devices \
           | grep -Eo 'event[0-9]+' | head -n1 | xargs -I{} echo /dev/input/{})
if [ -z "$EVENT_PATH" ]; then
  echo "Aygıt bulunamadı! TOUCH_NAME doğru mu? Elle EVENT_PATH girip tekrar deneyin." >&2
  exit 1
fi
echo "  Bulundu: $EVENT_PATH"

echo "==> Python dinleyici oluşturuluyor …"
/usr/bin/sudo tee /usr/local/bin/touch_beep.py >/dev/null <<PY
#!/usr/bin/env python3
import subprocess
from evdev import InputDevice, list_devices, ecodes

# 🔍 Sadece "ILITEK ILITEK-TP Mouse" adını arıyoruz
TARGET_NAME = "ilitek ilitek-tp"

def find_ilitek_mouse():
    for path in list_devices():
        dev = InputDevice(path)
        if dev.name.lower() == TARGET_NAME:
            print(f"[INFO] Seçilen cihaz: {dev.name} ({path})")
            return path
    raise RuntimeError("❌ 'ILITEK ILITEK-TP' bulunamadı!")

# Cihazı bul
DEV_PATH = find_ilitek_mouse()
dev = InputDevice(DEV_PATH)
print(f"[INFO] Dinleniyor → {dev.path} ({dev.name})")

# 🔊 Dokunma olayını dinle
for ev in dev.read_loop():
    if ev.type == ecodes.EV_KEY and ev.code == ecodes.BTN_TOUCH and ev.value == 1:
        subprocess.Popen(["beep", "-f", "500", "-l", "120"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    elif ev.type == ecodes.EV_ABS and ev.code == ecodes.ABS_MT_TRACKING_ID and ev.value != -1:
        subprocess.Popen(["beep", "-f", "500", "-l", "120"],
                         stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

PY

sudo chmod +x /usr/local/bin/touch_beep.py

echo "==> Systemd servisi yazılıyor …"
/usr/bin/sudo tee /etc/systemd/system/${SERVICE_NAME}.service >/dev/null <<EOF
[Unit]
Description=Beep on ILITEK touchscreen touch
After=multi-user.target

[Service]
ExecStart=/usr/bin/python3 /usr/local/bin/touch_beep.py
WorkingDirectory=/usr/local/bin
User=pi
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

echo "==> Servis etkinleştiriliyor …"
sudo systemctl daemon-reload
sudo systemctl enable --now ${SERVICE_NAME}.service

echo "Kurulum tamamlandı! Ekrana dokunduğunuzda ${BEEP_FREQ} Hz, ${BEEP_LEN} ms bip duymalısınız."
read -p"Devam etmek için ENTER'a basın..."

sudo apt full-upgrade -y
sudo apt install -y wget git build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev \
  libsqlite3-dev curl libncurses5-dev libncursesw5-dev xz-utils tk-dev libffi-dev liblzma-dev \
  flex bison gnupg2 lsb-release gpg samba samba-common-bin libstdc++6
sudo apt install -y libstdc++6:amd64
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 2. GITHUB'DAN ENFIPROV2 KLONLAMA
#########################################
echo "📁 /home/pi/enfiproV2 klasörü hazırlanıyor ve GitHub'dan proje indiriliyor..."
git clone https://github.com/yiit/enfiproV2.git
cd enfiproV2
read -p "Devam etmek için ENTER'a basın..."

#########################################
# 3. PYTHON 3.13.1 KURULUMU
#########################################
echo "🐍 Python 3.13.1 indiriliyor ve kuruluyor..."
wget https://www.python.org/ftp/python/3.13.1/Python-3.13.1.tar.xz
rm -rf Python-3.13.1
tar -xf Python-3.13.1.tar.xz
cd Python-3.13.1
./configure --enable-optimizations --prefix=$HOME/enfiproV2/python3.13
make -j$(nproc)
make install
cd ..
read -p "Devam etmek için ENTER'a basın..."

#########################################
# 4. VENV OLUŞTURMA
#########################################
echo "🔧 Python venv oluşturuluyor..."
/home/pi/enfiproV2/python3.13/bin/python3.13 -m venv /home/pi/enfiproV2/venv
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 5. PIP GÜNCELLEME
#########################################
echo "⬆️ pip güncelleniyor..."
/home/pi/enfiproV2/venv/bin/pip install --upgrade pip
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 6. NODEENV + NODE.JS + NPM
#########################################
echo "🟢 nodeenv kuruluyor ve Node.js kuruluyor..."
/home/pi/enfiproV2/venv/bin/pip install nodeenv
/home/pi/enfiproV2/venv/bin/nodeenv -p
export PATH="$HOME/enfiproV2/venv/bin:$PATH"
/home/pi/enfiproV2/venv/bin/npm install -g npm@11.3.0
/home/pi/enfiproV2/venv/bin/npm install express serialport @serialport/parser-readline cors
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 7. POSTGRESQL 14 KURULUMU
#########################################
echo "🐘 PostgreSQL 14 indiriliyor ve kuruluyor..."
wget https://ftp.postgresql.org/pub/source/v14.11/postgresql-14.11.tar.gz
rm -rf postgresql-14.11
tar -xzf postgresql-14.11.tar.gz
cd postgresql-14.11
./configure --prefix=$HOME/enfiproV2/pgsql14
make -j$(nproc)
make install
cd ..
read -p "Devam etmek için ENTER'a basın..."

#########################################
# 8. POSTGRESQL DATA OLUŞTURMA
#########################################
echo "📂 PostgreSQL data klasörü hazırlanıyor..."
mkdir -p /home/pi/enfiproV2/pgsql14_data
/home/pi/enfiproV2/pgsql14/bin/initdb -D /home/pi/enfiproV2/pgsql14_data
sleep 5
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 9. DATABASE VE USER OLUŞTURMA
#########################################
echo "🛠 Systemd servisleri kuruluyor..."
sudo tee /etc/systemd/system/postgresql-enfipro.service > /dev/null <<EOL
[Unit]
Description=PostgreSQL 14 enfiproV2
After=network.target

[Service]
Type=forking
User=pi
Environment=PATH=/home/pi/enfiproV2/pgsql14/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin
ExecStart=/home/pi/enfiproV2/pgsql14/bin/pg_ctl -D /home/pi/enfiproV2/pgsql14_data -l /home/pi/enfiproV2/logfile start
ExecStop=/home/pi/enfiproV2/pgsql14/bin/pg_ctl -D /home/pi/enfiproV2/pgsql14_data stop
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable postgresql-enfipro
sudo systemctl start postgresql-enfipro

echo "🛠 PostgreSQL kullanıcısı ve veritabanı oluşturuluyor..."
/home/pi/enfiproV2/pgsql14/bin/psql -h localhost -d postgres -c "CREATE ROLE django_user WITH LOGIN PASSWORD '1';"
/home/pi/enfiproV2/pgsql14/bin/psql -h localhost -d postgres -c "CREATE DATABASE django_db OWNER django_user;"
/home/pi/enfiproV2/pgsql14/bin/psql -h localhost -d postgres -c "GRANT ALL PRIVILEGES ON DATABASE django_db TO django_user;"
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 10. DJANGO + GEREKLİ KÜTÜPHANELER
#########################################
echo "📦 Django ve requirements.txt kuruluyor..."
/home/pi/enfiproV2/venv/bin/pip install Django psycopg2-binary
/home/pi/enfiproV2/venv/bin/pip install -r /home/pi/enfiproV2/enfiproV2/requirements.txt
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 11. DJANGO MIGRATE ve SUPERUSER
#########################################
sudo tee /etc/systemd/system/django-enfipro.service > /dev/null <<EOL
[Unit]
Description=Django Server for enfiproV2
After=network.target postgresql-enfipro.service

[Service]
User=pi
WorkingDirectory=/home/pi/enfiproV2/enfiproV2
Environment="PATH=/home/pi/enfiproV2/venv/bin"
ExecStart=/home/pi/enfiproV2/venv/bin/python manage.py runserver 0.0.0.0:8000
Restart=always

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable django-enfipro
sudo systemctl start django-enfipro


echo "🔧 Django migrate ve superuser işlemleri..."
cd /home/pi/enfiproV2/enfiproV2
/home/pi/enfiproV2/venv/bin/python manage.py makemigrations
/home/pi/enfiproV2/venv/bin/python manage.py migrate
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.create_superuser('pi', 'pi@example.com', '1')" | /home/pi/enfiproV2/venv/bin/python manage.py shell
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 12. SYSTEMD SERVİSLERİ
#########################################
sudo tee /etc/systemd/system/serialjs-enfipro.service > /dev/null <<EOL
[Unit]
Description=Node.js Serial.js for enfiproV2
After=network.target postgresql-enfipro.service

[Service]
User=pi
WorkingDirectory=/home/pi/enfiproV2/enfiproV2
ExecStart=/home/pi/enfiproV2/venv/bin/node serial.js
Restart=always

[Install]
WantedBy=multi-user.target
EOL

sudo systemctl daemon-reload
sudo systemctl enable serialjs-enfipro
sudo systemctl start serialjs-enfipro
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 13. USB YAZICI / SERIAL AYARLARI
#########################################
echo "🔧 USB yazıcı ve serial port izinleri ayarlanıyor..."
sudo tee /etc/udev/rules.d/99-usblp.rules > /dev/null <<EOL
SUBSYSTEM=="usb", ATTR{idVendor}=="0fe6", ATTR{idProduct}=="8800", MODE="0666", GROUP="lp"
EOL

sudo tee /etc/udev/rules.d/99-serial-permissions.rules > /dev/null <<EOL
KERNEL=="ttyS0", MODE="0666"
KERNEL=="ttyS1", MODE="0666"
EOL

sudo udevadm control --reload-rules
sudo udevadm trigger
sudo usermod -aG lp $USER
sudo chmod 666 /dev/ttyS0
sudo chmod 666 /dev/ttyS1
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 14. SAMBA + GOOGLE CHROME
#########################################
echo "🌐 Chrome ve Samba kuruluyor..."
sudo apt install -y samba samba-common-bin
wget -O google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome.deb || sudo apt --fix-broken install -y
sudo apt autoremove -y
sudo apt remove -y chromium-browser
sudo systemctl restart smbd
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 15. ANYDESK
#########################################
echo "🌐 Anydesk..."
sudo apt update
sudo apt install wget gnupg2 lsb-release
wget -qO - https://keys.anydesk.com/repos/DEB-GPG-KEY | sudo apt-key add -
echo "deb http://deb.anydesk.com/ all main" | sudo tee /etc/apt/sources.list.d/anydesk.list
sudo apt update
sudo apt install anydesk
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 16. LXDE AUTOSTART
#########################################
echo "🖥 LXDE autostart yapılandırılıyor..."
mkdir -p /home/pi/.config/lxsession/LXDE-pi
sudo tee /home/pi/.config/lxsession/LXDE-pi/autostart > /dev/null <<EOL
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@xset s off
@xset -dpms
@xset s noblank
@/usr/bin/google-chrome --kiosk --force-device-scale-factor=0.65 http://localhost:8000
EOL

sudo chown pi:pi /home/pi/.config/lxsession/LXDE-pi/autostart
read -p "👉 Devam etmek için ENTER'a basın..."

sudo apt autoremove

#########################################
# 18. RASPAP KURULUMU (Kernel değiştirmez)
#########################################
echo "📡 RaspAP kurulumu başlatılıyor (kernel değişmeyecek)..."

# Gerekli bağımlılıkları yükle
sudo apt update
sudo apt install -y git lighttpd php7.4-cgi php7.4-cli php7.4-common php7.4-json php7.4-readline hostapd dnsmasq iptables-persistent

# RaspAP deposunu klonla
cd /home/pi
git clone https://github.com/RaspAP/raspap-webgui.git
cd raspap-webgui

# quick installer’ı çalıştır (kernel değiştirmez)
sudo bash quick-install.sh --yes

# RaspAP servislerini aktif et
sudo systemctl enable lighttpd
sudo systemctl restart lighttpd

# Not: quick-install.sh senin kernelini olduğu gibi bırakır.
echo "✅ RaspAP kurulumu tamamlandı. Arayüz: http://10.3.141.1/ (kullanıcı: admin / şifre: secret)"
read -p "👉 Devam etmek için ENTER'a basın..."

#########################################
# 19. RASPAP YEDEKTEN GERİ YÜKLEME SCRIPTİ
#########################################
echo "🗃️ raspap-restore.sh scripti hazırlanıyor..."
sudo tee /usr/local/bin/raspap-restore.sh > /dev/null <<'EOF'
#!/bin/bash
# raspap-restore.sh - RaspAP yedeğinden geri yükleme (seçmeli)

BACKUP_DIR="$PWD"
PATTERN="raspap-backup-*.tar.gz"

# Yedek dosyalarını bul
mapfile -t FILES < <(ls -1t $BACKUP_DIR/$PATTERN 2>/dev/null)

# Hiç dosya yoksa çık
if [ ${#FILES[@]} -eq 0 ]; then
  echo "❌ Hiç yedek dosyası bulunamadı ($BACKUP_DIR/$PATTERN)"
  exit 1
fi

# Eğer parametre verilmişse onu kullan
if [ -n "$1" ]; then
  BACKUP_FILE="$1"
else
  echo "🔎 Bulunan yedek dosyaları:"
  for i in "${!FILES[@]}"; do
    echo "$((i+1))) ${FILES[$i]}"
  done

  # Kullanıcıdan seçim al
  read -p "👉 Yüklemek istediğiniz yedeğin numarasını girin: " CHOICE
  INDEX=$((CHOICE-1))

  # Geçerli seçim mi kontrol et
  if [ -z "${FILES[$INDEX]}" ]; then
    echo "❌ Geçersiz seçim!"
    exit 1
  fi

  BACKUP_FILE="${FILES[$INDEX]}"
fi

# Dosya mevcut mu kontrol et
if [ ! -f "$BACKUP_FILE" ]; then
  echo "❌ Yedek dosyası bulunamadı: $BACKUP_FILE"
  exit 1
fi

# Geri yükle
echo "🔄 [RaspAP Geri Yükleme] $BACKUP_FILE yükleniyor..."
sudo tar xzvf "$BACKUP_FILE" -C /
echo "✅ Geri yükleme tamamlandı!"
echo "ℹ️ Değişikliklerin etkin olması için sistemi yeniden başlatmayı unutma."
EOF

# Çalıştırılabilir yap
sudo chmod +x /usr/local/bin/raspap-restore.sh

echo "✅ raspap-restore.sh başarıyla /usr/local/bin içine kopyalandı."
echo "ℹ️ Kullanım: 'cd /yedeklerin_bulunduğu_klasör && sudo raspap-restore.sh'"
read -p "👉 Devam etmek için ENTER'a basın..."


#########################################
# 17. TAMAMLANDI
#########################################
echo ""
echo "✅ Kurulum Başarıyla Tamamlandı!"
echo "🔔 İlk açılışta Virtual_Keyboard uzantısını manuel eklemeyi unutma!"
echo "♻️ 10 saniye sonra sistem yeniden başlatılacak..."
sleep 10
sudo reboot