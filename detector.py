#!/usr/bin/env python3
# TBH-PhishDetector v1.1 - + IDN Homograph Detection
# Tulungagung Black Hat - uchil404

import re
import argparse
from urllib.parse import urlparse
import sys

BANNER = """\033[91m╔════════════════════════════════════╗
\033[91m║ \033[97mTBH-PhishDetector v1.1 \033[91m- + IDN Homograph\033[91m║
\033[91m║ \033[90mTulungagung Black Hat | uchil404 \033[91m║
\033[91m╚════════════════════════════════════╝\033[0m"""

SUSPICIOUS_TLDS = ['.tk','.ml','.ga','.cf','.gq']
SHORTENERS = ['bit.ly','tinyurl','goo.gl','t.me','shorturl']
BRANDS = ['google','facebook','instagram','paypal','bank','bca','bri','mandiri']

def analyze(url):
    score = 0
    reasons = []
    parsed = urlparse(url if url.startswith("http") else "https://"+url)
    domain = parsed.netloc
    path = parsed.path
    full = url

    if re.match(r"^\d+\.\d+\.\d+\.\d+", domain):
        score += 3; reasons.append("Menggunakan IP address bukan domain")
    if len(full) > 75:
        score += 1; reasons.append(f"URL sangat panjang ({len(full)} char)")
    if "@" in full:
        score += 2; reasons.append("Mengandung '@' (redirect trick)")
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 2; reasons.append(f"TLD mencurigakan {tld}")
    for s in SHORTENERS:
        if s in domain:
            score += 1; reasons.append(f"URL shortener {s}")
    if domain.count('.') > 3:
        score += 1; reasons.append(f"Banyak subdomain ({domain.count('.')})")
    if "-" in domain and any(b in domain for b in BRANDS):
        score += 2; reasons.append("Brand + hyphen")
    if not full.startswith("https"):
        score += 1; reasons.append("Tidak pakai HTTPS")
    keywords = ['login','verify','secure','account','update','confirm']
    for kw in keywords:
        if kw in path.lower() or kw in domain.lower():
            score += 1; reasons.append(f"Keyword phising '{kw}'")
            break
    # NEW v1.1 - IDN Homograph
    # Punycode xn-- or non-ascii
    if "xn--" in domain:
        score += 3; reasons.append("IDN Punycode xn-- (homograph phising, misal xn--pple-... = apple palsu)")
    # Non-ASCII chars
    try:
        domain.encode('ascii')
    except:
        score += 3; reasons.append("Karakter non-ASCII (homograph, misal а bukan a)")
    # Mixed script sneaky: paypal with Cyrillic 'а'
    if re.search(r"[а-яА-Я]", domain):  # Cyrillic
        score += 2; reasons.append("Mengandung huruf Cyrillic (homograph)")

    if score >= 5:
        verdict = "\033[91m[PHISHING ⛔]\033[0m"; risk = "Tinggi"
    elif score >= 3:
        verdict = "\033[93m[MENCURIGAKAN ⚠️]\033[0m"; risk = "Sedang"
    else:
        verdict = "\033[92m[AMAN ✅]\033[0m"; risk = "Rendah"
    return score, risk, verdict, reasons

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="TBH-PhishDetector v1.1")
    parser.add_argument("-u","--url", required=True, help="URL")
    parser.add_argument("-b","--bulk", help="File list URL")
    args = parser.parse_args()
    urls = []
    if args.bulk:
        try:
            with open(args.bulk) as f:
                urls = [l.strip() for l in f if l.strip()]
        except:
            print("\033[91m[!] File tidak ditemukan\033[0m"); sys.exit(1)
    else:
        urls = [args.url]
    for url in urls:
        print(f"\n\033[96m[*] Analisis: {url}\033[0m")
        print("\033[90m" + "="*50 + "\033[0m")
        score, risk, verdict, reasons = analyze(url)
        print(f"Score: {score}/10 | Risiko: {risk} {verdict}")
        if reasons:
            print("\033[93mAlasan:\033[0m")
            for r in reasons:
                print(f"  - {r}")
        else:
            print("\033[92mTidak ada indikator\033[0m")
        print("\033[90m" + "="*50 + "\033[0m")
    print("\n\033[92m[✓] Selesai v1.1 - Waspada homograph!\033[0m")

if __name__ == "__main__":
    main()
