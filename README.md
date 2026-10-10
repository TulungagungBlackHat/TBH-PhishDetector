# TBH-PhishDetector

<p align="center">
  <a href="https://github.com/TulungagungBlackHat/TBH-PhishDetector/actions/workflows/ci.yml"><img src="https://github.com/TulungagungBlackHat/TBH-PhishDetector/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <img src="https://img.shields.io/badge/license-MIT-red.svg" alt="License">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/heuristics-9-orange.svg" alt="Heuristics">
</p>

Heuristic phishing URL detector. Scores a URL against 9 signals — no external API, no URL sent to a third party.

Part of the [Tulungagung Black Hat](https://github.com/TulungagungBlackHat) toolset.

## How It Works

Each URL is scored 0–10 across 9 heuristics:

| Signal | What it looks for |
|--------|-------------------|
| URL length / entropy | Unusually long or random-looking URLs |
| Hostname tricks | `@` confusion, hyphens in brand domains, punycode |
| Subdomain abuse | `paypal.login.evil.com`-style nesting |
| Brand keywords | Known brand names in path or host |
| TLD risk | Suspicious or rarely-abused TLDs |
| IP hosts | Bare IP instead of a hostname |
| HTTPS absence | Plain `http://` login pages |
| Redirect chains | URL shorteners / open redirects |
| Path keywords | `login`, `verify`, `secure`, `account`, `update` |

All checks run locally — bulk lists never leave your machine.

## Install

```bash
git clone https://github.com/TulungagungBlackHat/TBH-PhishDetector
cd TBH-PhishDetector
pip install -r requirements.txt
```

## Usage

```
usage: detector.py [-h] [-u URL] [-b BULK] [--csv CSV] [--json JSON]

options:
  -u, --url URL     Check a single URL
  -b, --bulk BULK   Check a file of URLs (one per line)
  --csv CSV         Save results as CSV
  --json JSON       Save results as JSON
```

### Examples

Single URL:

```bash
python3 detector.py -u "http://paypal-secure-login.verify-account.ru/login"
```

Bulk scan with both export formats:

```bash
python3 detector.py -b urls.txt --csv results.csv --json results.json
```

## Sample Output

```
[*] http://paypal-secure-login.verify-account.ru/login -> 8/10 PHISHY ['brand-in-host', 'suspicious-tld', 'login-keyword', 'no-https']
[*] https://example.com -> 0/10 SAFE []
[✓] CSV saved: results.csv
[✓] JSON saved: results.json
```

Scoring is heuristic, not ground truth — a high score is a signal to investigate, not proof.

## Use Cases

- Triaging inbound mail queues or user reports
- Curating phishing samples for awareness training
- Feature in defensive dashboards (JSON/CSV is stable)

## Authorized Use Only

This is a defensive tool. Don't use it to validate phishing kits you intend to deploy. See [SECURITY.md](SECURITY.md).

## Related Tools

- [TBH-Recon](https://github.com/TulungagungBlackHat/TBH-Recon) — web recon companion
- [TBH-PassStrength](https://github.com/TulungagungBlackHat/TBH-PassStrength) — password strength checker

## License

[MIT](LICENSE) — Tulungagung Black Hat, East Java, Indonesia. Always Smile :)
