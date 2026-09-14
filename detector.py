#!/usr/bin/env python3
# TBH-PhishDetector v2.0 Pro - CSV + API mode
import re, argparse, csv, json
from urllib.parse import urlparse
import sys

BANNER = """\033[91m╔════════════════════════════════════╗
\033[91m║ \033[97mTBH-PhishDetector v2.0 Pro \033[91m- CSV/API\033[91m║
\033[91m║ \033[90mTulungagung Black Hat | uchil404 \033[91m║
\033[91m╚════════════════════════════════════╝\033[0m"""

def analyze(url):
    score=0; reasons=[]
    parsed=urlparse(url if url.startswith("http") else "https://"+url)
    domain=parsed.netloc; path=parsed.path; full=url
    if re.match(r"^\d+\.\d+\.\d+\.\d+", domain): score+=3; reasons.append("IP address")
    if len(full)>75: score+=1; reasons.append(f"Long {len(full)}")
    if "@" in full: score+=2; reasons.append("@ trick")
    if any(domain.endswith(t) for t in ['.tk','.ml','.ga','.cf','.gq']): score+=2; reasons.append("Suspicious TLD")
    if "xn--" in domain: score+=3; reasons.append("Punycode xn--")
    try: domain.encode('ascii')
    except: score+=3; reasons.append("Non-ASCII")
    if re.search(r"[а-яА-Я]", domain): score+=2; reasons.append("Cyrillic")
    if not full.startswith("https"): score+=1; reasons.append("No HTTPS")
    if any(kw in domain.lower() for kw in ['login','verify','secure']): score+=1; reasons.append("Keyword")
    verdict="PHISHING" if score>=5 else "MENCURIGAKAN" if score>=3 else "AMAN"
    return {"url":url,"score":score,"verdict":verdict,"reasons":reasons}

def main():
    print(BANNER)
    parser=argparse.ArgumentParser(description="v2.0 Pro")
    parser.add_argument("-u","--url",help="Single URL")
    parser.add_argument("-b","--bulk",help="File list URL")
    parser.add_argument("--csv",help="Save CSV")
    parser.add_argument("--json",help="Save JSON")
    args=parser.parse_args()
    urls=[]
    if args.bulk:
        with open(args.bulk) as f: urls=[l.strip() for l in f if l.strip()]
    elif args.url: urls=[args.url]
    else: parser.error("need -u or -b")
    results=[analyze(u) for u in urls]
    for r in results:
        print(f"\n[*] {r['url']} -> {r['score']}/10 {r['verdict']} {r['reasons']}")
    if args.csv:
        with open(args.csv,'w',newline='') as f:
            w=csv.DictWriter(f, fieldnames=["url","score","verdict","reasons"]); w.writeheader()
            for r in results: w.writerow({"url":r["url"],"score":r["score"],"verdict":r["verdict"],"reasons":"|".join(r["reasons"])})
        print(f"[✓] CSV saved: {args.csv}")
    if args.json:
        open(args.json,'w').write(json.dumps(results,indent=2))
        print(f"[✓] JSON saved: {args.json}")

if __name__=="__main__": main()
