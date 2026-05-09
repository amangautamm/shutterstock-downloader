# 🚀 Premium Stock Asset Downloader Bot

A professional Telegram bot built with **Python** to extract and download premium stock assets including **Photos, Vectors, PSDs, and 3D Models**. This bot is optimized for speed and features a real-time progress tracking UI.

---

## ✨ Key Features

- 🖼️ **Multi-Asset Support:** Download high-resolution Photos, PSDs, Vectors, and 3D Models.
- ⚡ **Live Progress UI:** 
  - **Extraction:** Real-time percentage bar during the bypass/scraping phase.
  - **Download:** Visual progress bar while fetching the file to Telegram.
- 🛡️ **Smart Filtering:** Automatically blocks Video and Audio links to optimize API/Scraper usage.
- 💎 **Premium System:** Built-in license key activation system (`/activate`) to manage user tiers.
- 📊 **Database Integration:** Uses **MongoDB** to track daily download limits and user statistics.
- 🕵️ **Headless Scraping:** Powered by Selenium and Chrome for stable extraction.

---

## 🛠️ Requirements

- **Python:** 3.10 or higher
- **Browser:** Google Chrome (Latest version)
- **Database:** MongoDB (Atlas or local instance)
- **Libraries:** See `requirements.txt`

---

## 🚀 Installation & Setup

1. **Clone the Repo:**
   ```bash
   git clone [https://github.com/yourusername/stock-downloader-bot.git](https://github.com/yourusername/stock-downloader-bot.git)
   cd stock-downloader-bot
   python main.py

   # --- CONFIGURATION ---
TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'          # Get from @BotFather
MONGO_URI = "YOUR_MONGODB_CONNECTION_URI"  # Your MongoDB Atlas String
VALID_LICENSE_KEY = "PREMIUM-2026-PRO"     # Your custom activation key
