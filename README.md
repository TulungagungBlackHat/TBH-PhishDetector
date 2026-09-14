# TBH-PhishDetector v1.1 - + IDN Homograph

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python">
  <img src="https://img.shields.io/badge/Version-v1.1-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/New-IDN%20Homograph-orange?style=for-the-badge">
</p>

> **v1.1 Update** - Tambah deteksi **IDN Homograph** (phising pakai huruf mirip).

## ✨ v1.1 vs v1.0
- ✅ **Punycode `xn--`** - misal `xn--pple-43d.com` (apple palsu)
- ✅ **Non-ASCII** - deteksi `а` Cyrillic vs `a` Latin
- ✅ **Cyrillic** - `paypal` pakai `а` Rusia

## 🚀 Usage
```bash
python3 detector.py -u https://xn--pple-43d.com
# Score: 3/10 | Mencurigakan - Punycode xn--

python3 detector.py -u https://google.com  # Aman
python3 detector.py -u https://paypal-secure.tk/login  # Phishing
```

## 🛡️ Edukasi Homograph
Penyerang pakai huruf mirip: `а` (Cyrillic) bukan `a` (Latin). Cek punycode `xn--`.

## 👥 TBH
uchil404 - Tulungagung Black Hat

## 📄 License
MIT
