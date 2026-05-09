# 🚀 Premium Shuterstock Asset Downloader Bot

> A professional Telegram bot built with **Python** to extract and download premium stock assets — including Photos, Vectors, PSDs, and 3D Models — with a real-time progress tracking UI.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🖼️ Multi-Asset Support | Download high-res Photos, PSDs, Vectors, and 3D Models |
| ⚡ Live Progress UI | Real-time extraction percentage bar + download progress bar |
| 🛡️ Smart Filtering | Auto-blocks Video/Audio links to save API/scraper usage |
| 💎 Premium System | Built-in license key activation via `/activate` |
| 📊 MongoDB Integration | Tracks daily download limits and user statistics |
| 🕵️ Headless Scraping | Powered by Selenium + Chrome for stable extraction |

---

## 🛠️ Requirements

- **Python** 3.10+
- **Google Chrome** (latest version)
- **MongoDB** (Atlas or local instance)
- **pip** packages (see [Installation](#%EF%B8%8F-installation))

---

## ⚙️ Configuration

Open your main script and replace the placeholders with your credentials:

```python
# --- CONFIGURATION ---
TOKEN            = "YOUR_TELEGRAM_BOT_TOKEN"       # Get from @BotFather on Telegram
MONGO_URI        = "YOUR_MONGODB_CONNECTION_URI"   # MongoDB Atlas connection string
VALID_LICENSE_KEY = "PREMIUM-2026-PRO"             # Your custom premium activation key
```

---

## 🖥️ Installation

**1. Clone the repository**

```bash
git clone https://github.com/yourusername/stock-downloader-bot.git
cd stock-downloader-bot
```

**2. Install dependencies**

```bash
pip install python-telegram-bot pymongo requests selenium webdriver-manager certifi
```

**3. Run the bot**

```bash
python main.py
```

---

## 🎮 Commands & Usage

| Command | Description |
|---|---|
| `/start` | Welcome message and main menu |
| `/activate <key>` | Activate premium membership with a license key |
| `📊 My Account` | View daily limits and total download statistics |

---

## ⚠️ Disclaimer

This project is intended for **educational purposes only**.  
Always respect the Terms of Service of content providers and ensure you have the appropriate rights before downloading any assets.

---

<div align="center">

Developed with ❤️ using **Python-Telegram-Bot** and **Selenium**

</div>
