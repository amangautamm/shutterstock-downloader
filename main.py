import time
import re
import requests
import io
import uuid
import asyncio
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from pymongo import MongoClient
import certifi

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
TOKEN = ''
MONGO_URI = ""

executor = ThreadPoolExecutor(max_workers=20)

# --- DATABASE ---
try:
    client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())
    db = client['StockDownloaderDB']
    users_col = db['users']
except Exception as e:
    print(f"❌ DB Error: {e}")

def get_user_data(user_id):
    today = str(datetime.now().date())
    user = users_col.find_one({"user_id": user_id})
    if not user:
        user = {"user_id": user_id, "is_paid": False, "total_downloads": 0, "last_download_date": today, "daily_count": 0}
        users_col.insert_one(user)
    if user.get('last_download_date') != today:
        users_col.update_one({"user_id": user_id}, {"$set": {"daily_count": 0, "last_download_date": today}})
        user['daily_count'] = 0
    return user

def generate_progress_bar(percentage, icon="🔹"):
    completed = int(percentage / 10)
    return icon * completed + "⬜" * (10 - completed)

# --- SCRAPER ---
def get_direct_link(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get("https://hdstockimages.com/")
        
        clean_url = url.split('?')[0]
        script = f"var callback = arguments[arguments.length - 1]; jQuery.ajax({{url: 'https://hdstockimages.com/wp-admin/admin-ajax.php', type: 'POST', data: {{ action: 'ajax_call_custom', loadSampleImage: 1, url: '{clean_url}' }}, success: function(res) {{ callback(res); }}, error: function() {{ callback('Error'); }} }});"
        
        res = driver.execute_async_script(script)
        urls = re.findall(r'(https?://[^\s<>"]+|www\.[^\s<>"]+)', str(res))
        driver.quit()
        if urls: return urls[0]
    except: pass
    return None

# --- HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🚀 <b>PREMIUM ASSET DOWNLOADER</b>\n\nSend Shutterstock link for Photos, Vectors, or PSDs.",
        parse_mode=ParseMode.HTML
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    try: await query.answer()
    except: pass

    # Filter for download button
    if query.data.startswith("dl_"):
        f_id = query.data.split("_")[1]
        media_url = context.bot_data.get(f_id)
        
        if not media_url:
            await query.message.reply_text("❌ <b>Session Expired!</b> Send link again.")
            return

        status_msg = await query.message.reply_text("⏳ <b>Starting Download...</b>", parse_mode=ParseMode.HTML)
        
        try:
            # Download Progress
            for p in [20, 50, 85]:
                await asyncio.sleep(0.4)
                bar = generate_progress_bar(p, "📥")
                await status_msg.edit_text(f"📡 <b>Downloading Asset</b>\n{bar} <b>{p}%</b>", parse_mode=ParseMode.HTML)

            r = requests.get(media_url, timeout=120)
            file_io = io.BytesIO(r.content)
            file_io.name = f"Asset_{f_id}.jpg"

            users_col.update_one({"user_id": user_id}, {"$inc": {"daily_count": 1, "total_downloads": 1}})
            await query.message.reply_document(document=file_io, caption="✅ <b>Success!</b>", parse_mode=ParseMode.HTML)
            await status_msg.delete()
        except:
            await status_msg.edit_text("❌ Download Failed.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text
    if "shutterstock.com" not in text: return

    # Limit Check
    user = get_user_data(user_id)
    if user['daily_count'] >= (20 if user['is_paid'] else 2):
        await update.message.reply_text("🔒 <b>Limit Reached!</b>")
        return

    # EXTRACTION PROGRESS
    status_msg = await update.message.reply_text("⚡ <b>Extracting... 0%</b>", parse_mode=ParseMode.HTML)
    
    # Background progress task
    async def extraction_timer():
        for p in [15, 35, 60, 85, 95]:
            await asyncio.sleep(1)
            try:
                bar = generate_progress_bar(p, "⚡")
                await status_msg.edit_text(f"🔍 <b>Fetching Premium Data</b>\n{bar} <b>{p}%</b>", parse_mode=ParseMode.HTML)
            except: break

    timer_task = asyncio.create_task(extraction_timer())
    loop = asyncio.get_event_loop()
    result_url = await loop.run_in_executor(executor, get_direct_link, text)
    timer_task.cancel() # Stop progress when done

    if result_url:
        # Fixed ID matching
        f_id = str(uuid.uuid4())[:6]
        context.bot_data[f_id] = result_url
        
        keyboard = [[InlineKeyboardButton("📥 Download File", callback_data=f"dl_{f_id}")],
                    [InlineKeyboardButton("🔗 Direct Link", url=result_url)]]
        
        await status_msg.edit_text(
            f"✅ <b>Extraction 100% Complete!</b>\n{generate_progress_bar(100, '✅')}", 
            parse_mode=ParseMode.HTML
        )
        await asyncio.sleep(0.5)
        await status_msg.delete()
        
        await update.message.reply_text(
            "<b>Select Download Option:</b>", 
            reply_markup=InlineKeyboardMarkup(keyboard), 
            parse_mode=ParseMode.HTML
        )
    else:
        await status_msg.edit_text("❌ Extraction Failed.")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 Bot is Online!")
    app.run_polling()

if __name__ == "__main__":
    main()
