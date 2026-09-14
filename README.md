# TBH-PhishDetector - Phishing URL Detector

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Purpose-Anti--Phishing%20%7C%20Educational-green?style=for-the-badge">
  <img src="https://img.shields.io/badge/Accuracy-Heuristik%209%20Rules-orange?style=for-the-badge">
</p>

> **⚠️ EDUCATIONAL ONLY** - Tool untuk edukasi & membantu deteksi URL phising. Bukan untuk menyerang. Gunakan untuk melindungi diri & orang lain.

Oleh **uchil404 | Tulungagung Black Hat**

---

### ✨ Features
- 🔍 **9 Heuristik** - IP, panjang URL, @ trick, TLD mencurigakan, shortener, hyphen+brand, HTTPS, keyword phising, banyak subdomain
- ⚡ **Tanpa dependency** - Pure Python, jalan di Termux
- 📋 **Bulk mode** - Scan banyak URL dari file
- 🎯 **Skor 0-10** - Aman / Mencurigakan / Phishing

### 📦 Install
```bash
git clone https://github.com/TulungagungBlackHat/TBH-PhishDetector
cd TBH-PhishDetector
python3 detector.py -u https://example.com
```

### 🚀 Usage
```bash
# Single URL
python3 detector.py -u https://paypal-secure-login.tk/verify

# Bulk dari file
echo "https://google.com" > urls.txt
echo "http://192.168.1.1/login@evil.com" >> urls.txt
python3 detector.py -u https://google.com --bulk urls.txt
```

**Contoh:**
```
[*] Analisis: https://paypal-secure-login.tk/verify
Score: 7/10 | Risiko: Tinggi [PHISHING ⛔]
Alasan:
  - TLD mencurigakan .tk
  - Brand + hyphen (paypal-secure.com)
  - Keyword phising 'verify'
```

### 🛡️ Tips Anti-Phising
1. Selalu cek domain asli (paypal.com bukan paypal-secure.tk)
2. Jangan klik link dari SMS/WA mencurigakan
3. Aktifkan 2FA
4. Ketik manual URL bank di browser

### 👥 Credits
uchil404 - Tulungagung Black Hat - Always Smile :)

### 📄 License
MIT
