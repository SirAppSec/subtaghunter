# subdomain-takeover-exploitation
Subdomain takeover vulnerabilities occur when a subdomain points to a hosting service without a valid site and can be taken over by attackers. SubTagHunter scans specified tags within a web page, such as <img> or <script> tags, and alerts users if the domain in those tags might be vulnerable.

# Features

* Scan multiple web pages in a single command.
* Detects domains within specified tags that might be vulnerable to subdomain takeover.
* Outputs results in YAML by default, with options for CSV or JSON formats.

# Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/subtaghunter.git
cd subtaghunter
```

Install the packages:
```bash
pip install -r requirements.txt
```

# Usage
Just run:
```bash
python subtaghunter.py TARGET_DOMAIN WEBPAGE_1 WEBPAGE_2 ... --output-format=FORMAT
```

Help:
```bash
python subtaghunter.py --help

```