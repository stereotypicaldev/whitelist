<h1 align="center">Whitelist</h1>
<br>

This repository auto-backs up the **allowlist (whitelist)** for a Pi-hole instance, organized by service category for easier management and restoration.

---

## 🗂️ Repository Structure

```
.
├── backup.sh
├── categories/
│   ├── streaming.txt
│   ├── analytics.txt
│   ├── dev-tools.txt
│   ├── social.txt
│   └── ...
└── README.md
```
---

## 🛠️ Prerequisites

- Linux environment (e.g. Debian/Raspbian)  
- `pihole` CLI tool installed and configured  
- (Optional) `jq`, `grep`, `awk`

---

## 🧩 Categories

- `streaming.txt` – Domains related to streaming services (e.g., Netflix, Hulu)  
- `analytics.txt` – Tracking and analytics domains (e.g., Google Analytics)  
- `dev-tools.txt` – Dev‑related domains (e.g., GitHub, Docker)  
- `social.txt` – Social media domains (e.g., Facebook, Twitter)  
- Add as many custom categories as your use-case dictates.

---

## 🧠 Usage

1. Clone this repo onto your Pi-hole host (or a cron‑enabled host).  
2. Make `backup.sh` executable:  
   ```bash
   chmod +x backup.sh
   ```  
3. (Optional) Schedule in cron to run nightly:  
   ```bash
   0 2 * * * /path/to/backup.sh >> /var/log/pihole-backup.log 2>&1
   ```  
4. Inspect `categories/` for domain lists—useful for auditing or editing.  
5. To restore, feed the desired allowlist back into Pi-hole:  
   ```bash
   xargs -a categories/streaming.txt -r pihole -w
   ```

---

## ✅ License

[MIT License](LICENSE) – do whatever you want with this. Just don’t sue me.

---
