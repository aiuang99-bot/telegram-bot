import os
import logging
import random
import datetime
from datetime import datetime, timedelta
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# ============ AMBIL TOKEN ============
# Coba baca dari berbagai sumber
TOKEN = os.getenv("BOT_TOKEN") or os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN tidak ditemukan!")
    print("📝 Silakan tambahkan BOT_TOKEN di Environment Variables Railway")
    exit(1)

print(f"✅ Token berhasil dibaca! Panjang token: {len(TOKEN)} karakter")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Data storage
user_data_store = {}
game_data = {}

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============ COMMAND HANDLERS ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome_text = f"""
🎉 *Selamat Datang di Bot Super Lengkap!* 🎉

Halo *{user.first_name}*! 👋

Saya adalah bot dengan berbagai fitur menarik:

📰 *Berita* - Dapatkan berita terbaru
🌤️ *Cuaca* - Cek informasi cuaca
🎮 *Game* - Mainkan game seru
📊 *Polling* - Buat voting
📱 *QR Code* - Generate QR Code
💬 *AI Chat* - Chat dengan AI

Gunakan /help untuk melihat semua perintah
    """
    
    keyboard = [
        [InlineKeyboardButton("📰 Berita", callback_data="news"),
         InlineKeyboardButton("🌤️ Cuaca", callback_data="weather")],
        [InlineKeyboardButton("🎮 Game", callback_data="games"),
         InlineKeyboardButton("📊 Polling", callback_data="poll")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 *DAFTAR PERINTAH BOT*

/start - Mulai bot
/help - Tampilkan bantuan
/about - Tentang bot
/news - Berita terbaru
/weather [kota] - Info cuaca
/qr [teks] - Buat QR Code
/ai [pesan] - Chat dengan AI
/games - Daftar game
/poll - Buat polling
/stats - Statistik pengguna
/feedback [pesan] - Kirim feedback
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Tentang Bot Ini*\n\nBot Telegram dengan berbagai fitur lengkap.\n\nVersi: 2.0.0",
        parse_mode="Markdown"
    )

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📰 *Mengambil berita terbaru...*", parse_mode="Markdown")
    
    mock_news = [
        {"title": "Teknologi AI Semakin Canggih", "description": "Perkembangan AI di tahun 2026...", "url": "https://example.com/1"},
        {"title": "Update Kebijakan Digital", "description": "Pemerintah merilis kebijakan baru...", "url": "https://example.com/2"},
        {"title": "Inovasi Startup Indonesia", "description": "Startup lokal berhasil menciptakan inovasi...", "url": "https://example.com/3"}
    ]
    
    news_text = "📰 *Berita Terkini*\n\n"
    for i, item in enumerate(mock_news, 1):
        news_text += f"{i}. *{item['title']}*\n   {item['description']}\n   [Baca]({item['url']})\n\n"
    
    keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh_news")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(news_text, reply_markup=reply_markup, parse_mode="Markdown", disable_web_page_preview=True)

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args) if context.args else "Jakarta"
    
    weather_data = {
        "city": city,
        "temperature": random.randint(25, 35),
        "condition": random.choice(["Cerah ☀️", "Berawan ☁️", "Hujan Ringan 🌦️"]),
        "humidity": random.randint(60, 90),
        "wind": random.randint(5, 25)
    }
    
    weather_text = f"""
🌤️ *Informasi Cuaca*

📍 *Lokasi:* {weather_data['city']}
🌡️ *Suhu:* {weather_data['temperature']}°C
☁️ *Kondisi:* {weather_data['condition']}
💧 *Kelembaban:* {weather_data['humidity']}%
💨 *Angin:* {weather_data['wind']} km/jam

🕐 Update: {get_current_time()}
    """
    
    await update.message.reply_text(weather_text, parse_mode="Markdown")

async def qr_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("📱 /qr [teks atau URL]\nContoh: /qr https://example.com", parse_mode="Markdown")
        return
    
    text = " ".join(context.args)
    await update.message.reply_text(f"⏳ Membuat QR Code untuk: `{text}`", parse_mode="Markdown")
    
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"
    await update.message.reply_photo(qr_url, caption=f"✅ *QR Code berhasil dibuat!*\n\n📝 Teks: {text}", parse_mode="Markdown")

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("💬 /ai [pesan]\nContoh: /ai Apa itu Python?", parse_mode="Markdown")
        return
    
    question = " ".join(context.args)
    await update.message.reply_text("💭 *AI sedang berpikir...*", parse_mode="Markdown")
    
    responses = [
        f"Menarik! Tentang '{question}', menurut saya...",
        f"Terima kasih atas pertanyaannya. '{question}' adalah topik yang bagus."
    ]
    
    await update.message.reply_text(f"🤖 *AI Response*\n\n{random.choice(responses)}", parse_mode="Markdown")

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    games_text = """
🎮 *DAFTAR GAME*

1. 🎲 *Tebak Angka* - Tebak angka 1-100
2. 🪨📄✂️ *Batu-Gunting-Kertas*

Gunakan /game [nomor]
Contoh: /game 1
    """
    
    keyboard = [
        [InlineKeyboardButton("🎲 Tebak Angka", callback_data="game_guess"),
         InlineKeyboardButton("🪨 Batu-Gunting-Kertas", callback_data="game_rps")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(games_text, reply_markup=reply_markup, parse_mode="Markdown")

async def game_guess_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    game_data[chat_id] = {'number': random.randint(1, 100), 'attempts': 0, 'game': 'guess'}
    
    await update.message.reply_text(
        "🎲 *Game Tebak Angka*\n\nSaya telah memilih angka antara 1-100.\nKirimkan angka tebakan Anda!",
        parse_mode="Markdown"
    )

async def game_rps_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🪨 Batu", callback_data="rps_batu"),
         InlineKeyboardButton("📄 Kertas", callback_data="rps_kertas"),
         InlineKeyboardButton("✂️ Gunting", callback_data="rps_gunting")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text("🪨📄✂️ *Batu-Gunting-Kertas*\n\nPilih salah satu:", reply_markup=reply_markup, parse_mode="Markdown")

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📊 *Buat Polling*\n\n/poll 'Pertanyaan' 'Pilihan1' 'Pilihan2'", parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 *Statistik*\n\nTotal Pengguna: {len(user_data_store)}", parse_mode="Markdown")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("📝 /feedback [pesan]", parse_mode="Markdown")
        return
    
    feedback_text = " ".join(context.args)
    await update.message.reply_text(f"✅ *Terima kasih atas feedbacknya!*\n\n📝 Pesan: {feedback_text}", parse_mode="Markdown")

# ============ CALLBACK HANDLER ============

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "help":
        await help_command(query, context)
    elif data == "news" or data == "refresh_news":
        await news(query, context)
    elif data == "weather":
        await weather(query, context)
    elif data == "games":
        await games(query, context)
    elif data == "game_guess":
        await game_guess_start(query, context)
    elif data == "game_rps":
        await game_rps_start(query, context)
    elif data == "poll":
        await poll(query, context)
    elif data == "qr_new":
        await qr_code(query, context)
    elif data.startswith("rps_"):
        user_choice = data.split("_")[1]
        choices = {"batu": "🪨", "kertas": "📄", "gunting": "✂️"}
        bot_choice = random.choice(list(choices.keys()))
        
        if user_choice == bot_choice:
            result = "🤝 Seri!"
        elif (user_choice == "batu" and bot_choice == "gunting") or \
             (user_choice == "gunting" and bot_choice == "kertas") or \
             (user_choice == "kertas" and bot_choice == "batu"):
            result = "🎉 Anda Menang!"
        else:
            result = "😅 Bot Menang!"
        
        await query.edit_message_text(
            f"🪨📄✂️ *Hasil Permainan*\n\n👤 Anda: {choices[user_choice]}\n🤖 Bot: {choices[bot_choice]}\n\n🏆 {result}",
            parse_mode="Markdown"
        )

# ============ MESSAGE HANDLER ============

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message_text = update.message.text
    
    if chat_id in game_data and game_data[chat_id].get('game') == 'guess':
        try:
            guess = int(message_text)
            target = game_data[chat_id]['number']
            game_data[chat_id]['attempts'] += 1
            
            if guess < target:
                await update.message.reply_text(f"📈 *Terlalu kecil!* (Percobaan ke-{game_data[chat_id]['attempts']})", parse_mode="Markdown")
            elif guess > target:
                await update.message.reply_text(f"📉 *Terlalu besar!* (Percobaan ke-{game_data[chat_id]['attempts']})", parse_mode="Markdown")
            else:
                await update.message.reply_text(f"🎉 *Selamat!* Angka: {target}\nJumlah percobaan: {game_data[chat_id]['attempts']}", parse_mode="Markdown")
                del game_data[chat_id]
        except ValueError:
            await update.message.reply_text("❌ Mohon kirimkan angka yang valid!")
    else:
        user = update.effective_user
        if user.id not in user_data_store:
            user_data_store[user.id] = {'username': user.username, 'first_name': user.first_name, 'join_date': get_current_time()}
        
        await update.message.reply_text(f"👋 Halo {user.first_name}!\nGunakan /help untuk melihat perintah.", parse_mode="Markdown")

# ============ MAIN ============

def main():
    print("🚀 Starting bot...")
    print(f"📱 Bot token: {TOKEN[:10]}...")

    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("qr", qr_code))
    application.add_handler(CommandHandler("ai", ai_chat))
    application.add_handler(CommandHandler("games", games))
    application.add_handler(CommandHandler("poll", poll))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("feedback", feedback))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running! Press Ctrl+C to stop.")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
