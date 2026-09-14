#!/usr/bin/env python3
# TBH-PhishDetector - Phishing URL Detector (Educational)
# Tulungagung Black Hat - uchil404

import re
import argparse
from urllib.parse import urlparse
import sys

BANNER = """\033[91m╔════════════════════════════════════╗
\033[91m║ \033[97mTBH-PhishDetector \033[91m- v1.0            \033[91m║
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

    # 1. IP instead of domain
    if re.match(r"^\d+\.\d+\.\d+\.\d+", domain):
        score += 3; reasons.append("Menggunakan IP address bukan domain")

    # 2. Long URL
    if len(full) > 75:
        score += 1; reasons.append(f"URL sangat panjang ({len(full)} char)")

    # 3. @ symbol
    if "@" in full:
        score += 2; reasons.append("Mengandung '@' (redirect trick)")

    # 4. Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 2; reasons.append(f"TLD mencurigakan {tld}")

    # 5. Shortener
    for s in SHORTENERS:
        if s in domain:
            score += 1; reasons.append(f"URL shortener {s}")

    # 6. Many subdomains
    if domain.count('.') > 3:
        score += 1; reasons.append(f"Banyak subdomain ({domain.count('.')}) - typo-squatting?")

    # 7. Hyphen in domain (phish trick)
    if "-" in domain and any(b in domain for b in BRANDS):
        score += 2; reasons.append("Brand + hyphen (misal paypal-secure.com)")

    # 8. No HTTPS
    if not full.startswith("https"):
        score += 1; reasons.append("Tidak pakai HTTPS")

    # 9. Suspicious keywords
    keywords = ['login','verify','secure','account','update','confirm']
    for kw in keywords:
        if kw in path.lower() or kw in domain.lower():
            score += 1; reasons.append(f"Keyword phising '{kw}'")
            break

    # Verdict
    if score >= 5:
        verdict = "\033[91m[PHISHING ⛔]\033[0m"
        risk = "Tinggi"
    elif score >= 3:
        verdict = "\033[93m[MENCURIGAKAN ⚠️]\033[0m"
        risk = "Sedang"
    else:
        verdict = "\033[92m[AMAN ✅]\033[0m"
        risk = "Rendah"

    return score, risk, verdict, reasons

def main():
    print(BANNER)
    parser = argparse.ArgumentParser(description="TBH-PhishDetector - Educational Phishing Detector")
    parser.add_argument("-u","--url", required=True, help="URL untuk dianalisis")
    parser.add_argument("-b","--bulk", help="File berisi list URL (satu per baris)")
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
            print("\033[92mTidak ada indikator mencurigakan\033[0m")
        print("\033[90m" + "="*50 + "\033[0m")
    print("\n\033[92m[✓] Selesai. Edukasi: selalu cek domain asli sebelum login!\033[0m")

if __name__ == "__main__":
    main()
