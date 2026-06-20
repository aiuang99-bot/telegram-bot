import os
import logging
import random
import datetime
from datetime import datetime, timedelta
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# Load environment variables
load_dotenv()

# Get token from environment variable
TOKEN = os.getenv("BOT_TOKEN")

# Jika tidak ditemukan, coba cara lain (untuk Railway)
if not TOKEN:
    print("🔍 Mencoba membaca token dari environment...")
    TOKEN = os.environ.get("BOT_TOKEN")
    
if not TOKEN:
    print("❌ ERROR: BOT_TOKEN tidak ditemukan!")
    print("📝 Pastikan BOT_TOKEN sudah ditambahkan di Environment Variables Railway")
    print("📝 Atau buat file .env dengan BOT_TOKEN=token_anda")
    exit(1)

print(f"✅ Token ditemukan! Panjang token: {len(TOKEN)} karakter")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Data storage
user_data_store = {}
game_data = {}

# ============ HELPER FUNCTIONS ============

def get_current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

# ============ COMMAND HANDLERS ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /start"""
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

*Gunakan /help untuk melihat semua perintah*
    """
    
    keyboard = [
        [InlineKeyboardButton("📰 Berita", callback_data="news"),
         InlineKeyboardButton("🌤️ Cuaca", callback_data="weather")],
        [InlineKeyboardButton("🎮 Game", callback_data="games"),
         InlineKeyboardButton("📊 Polling", callback_data="poll")],
        [InlineKeyboardButton("❓ Bantuan", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /help"""
    help_text = """
📚 *DAFTAR PERINTAH BOT*

*Perintah Dasar:*
/start - Mulai bot
/help - Tampilkan bantuan
/about - Tentang bot

*Fitur:*
/news - Berita terbaru
/weather [kota] - Info cuaca
/qr [teks] - Buat QR Code
/ai [pesan] - Chat dengan AI
/games - Daftar game
/poll - Buat polling
/stats - Statistik pengguna
/feedback [pesan] - Kirim feedback

*Contoh Penggunaan:*
/weather Jakarta
/qr https://example.com
/ai Apa itu Python?
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /about"""
    about_text = """
🤖 *Tentang Bot Ini*

Bot Telegram dengan berbagai fitur lengkap.

*Teknologi:*
• Python 3.9+
• python-telegram-bot v20.7
• API Telegram

*Fitur:*
✅ Berita
✅ Cuaca
✅ Game
✅ QR Code
✅ AI Chat
✅ Polling
✅ Dan lainnya!

*Versi:* 2.0.0
    """
    await update.message.reply_text(about_text, parse_mode="Markdown")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /news"""
    await update.message.reply_text("📰 *Mengambil berita terbaru...*", parse_mode="Markdown")
    
    # Mock data berita (gunakan API nyata untuk production)
    mock_news = [
        {
            "title": "Teknologi AI Semakin Canggih",
            "description": "Perkembangan AI di tahun 2026 semakin pesat...",
            "url": "https://example.com/news1"
        },
        {
            "title": "Update Kebijakan Digital",
            "description": "Pemerintah merilis kebijakan baru tentang ekonomi digital...",
            "url": "https://example.com/news2"
        },
        {
            "title": "Inovasi Startup Indonesia",
            "description": "Startup lokal berhasil menciptakan inovasi terbaru...",
            "url": "https://example.com/news3"
        }
    ]
    
    news_text = "📰 *Berita Terkini*\n\n"
    for i, item in enumerate(mock_news, 1):
        news_text += f"{i}. *{item['title']}*\n"
        news_text += f"   {item['description']}\n"
        news_text += f"   [Baca Selengkapnya]({item['url']})\n\n"
    
    keyboard = [[InlineKeyboardButton("🔄 Refresh", callback_data="refresh_news")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        news_text,
        reply_markup=reply_markup,
        parse_mode="Markdown",
        disable_web_page_preview=True
    )

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /weather"""
    city = " ".join(context.args) if context.args else "Jakarta"
    
    # Simulasi data cuaca (gunakan API nyata untuk production)
    weather_data = {
        "city": city,
        "temperature": random.randint(25, 35),
        "condition": random.choice(["Cerah ☀️", "Berawan ☁️", "Hujan Ringan 🌦️", "Hujan Lebat 🌧️"]),
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
    
    keyboard = [
        [InlineKeyboardButton("🔄 Refresh", callback_data=f"refresh_weather_{city}")],
        [InlineKeyboardButton("📍 Kota Lain", callback_data="weather_other")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(weather_text, reply_markup=reply_markup, parse_mode="Markdown")

async def qr_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /qr"""
    if not context.args:
        await update.message.reply_text(
            "📱 *Cara Buat QR Code*\n\n"
            "/qr [teks atau URL]\n\n"
            "Contoh:\n"
            "/qr https://example.com\n"
            "/qr Halo dunia!",
            parse_mode="Markdown"
        )
        return
    
    text = " ".join(context.args)
    await update.message.reply_text(f"⏳ Membuat QR Code untuk: `{text}`", parse_mode="Markdown")
    
    # Gunakan API gratis untuk generate QR Code
    qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data={text}"
    
    keyboard = [[InlineKeyboardButton("🔄 Buat Lagi", callback_data="qr_new")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_photo(
        qr_url,
        caption=f"✅ *QR Code berhasil dibuat!*\n\n📝 Teks: {text}",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def ai_chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /ai"""
    if not context.args:
        await update.message.reply_text(
            "💬 *Chat dengan AI*\n\n"
            "/ai [pesan]\n\n"
            "Contoh:\n"
            "/ai Apa itu kecerdasan buatan?",
            parse_mode="Markdown"
        )
        return
    
    question = " ".join(context.args)
    await update.message.reply_text("💭 *AI sedang berpikir...*", parse_mode="Markdown")
    
    # Simulasi response AI (gunakan API OpenAI untuk production)
    responses = [
        f"Menarik! Tentang '{question}', menurut saya...",
        f"Terima kasih atas pertanyaannya. '{question}' adalah topik yang bagus.",
        f"Dari sudut pandang saya, '{question}' ...",
        f"Saya akan coba menjawab tentang '{question}'."
    ]
    
    ai_response = random.choice(responses)
    await update.message.reply_text(
        f"🤖 *AI Response*\n\n{ai_response}\n\n"
        f"❓ Pertanyaan: {question}",
        parse_mode="Markdown"
    )

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /games"""
    games_text = """
🎮 *DAFTAR GAME*

Pilih game yang ingin dimainkan:

1. 🎲 *Tebak Angka* - Tebak angka 1-100
2. 🪨📄✂️ *Batu-Gunting-Kertas*

*Cara Main:*
Gunakan tombol di bawah atau ketik:
/game [nomor]

Contoh: /game 1
    """
    
    keyboard = [
        [InlineKeyboardButton("🎲 Tebak Angka", callback_data="game_guess"),
         InlineKeyboardButton("🪨 Batu-Gunting-Kertas", callback_data="game_rps")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(games_text, reply_markup=reply_markup, parse_mode="Markdown")

async def game_guess_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai game tebak angka"""
    chat_id = update.effective_chat.id
    game_data[chat_id] = {
        'number': random.randint(1, 100),
        'attempts': 0,
        'game': 'guess'
    }
    
    await update.message.reply_text(
        "🎲 *Game Tebak Angka*\n\n"
        "Saya telah memilih angka antara 1-100.\n"
        "Kirimkan angka tebakan Anda!\n\n"
        "Contoh: 50",
        parse_mode="Markdown"
    )

async def game_rps_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mulai game batu-gunting-kertas"""
    keyboard = [
        [InlineKeyboardButton("🪨 Batu", callback_data="rps_batu"),
         InlineKeyboardButton("📄 Kertas", callback_data="rps_kertas"),
         InlineKeyboardButton("✂️ Gunting", callback_data="rps_gunting")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🪨📄✂️ *Batu-Gunting-Kertas*\n\n"
        "Pilih salah satu:",
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )

async def poll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /poll"""
    poll_text = """
📊 *Buat Polling*

Kirimkan polling dengan format:
/poll "Pertanyaan" "Pilihan1" "Pilihan2" "Pilihan3"

Contoh:
/poll "Hari favorit Anda?" "Senin" "Selasa" "Rabu"

Atau gunakan tombol di bawah:
    """
    
    keyboard = [[InlineKeyboardButton("✅ Buat Polling Sederhana", callback_data="poll_simple")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(poll_text, reply_markup=reply_markup, parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /stats"""
    stats_text = f"""
📊 *Statistik Pengguna*

👤 *Nama:* {update.effective_user.first_name}
🆔 *ID:* {update.effective_user.id}
📝 *Username:* @{update.effective_user.username or 'Tidak ada'}

📅 *Total Pengguna Terdaftar:* {len(user_data_store)}
🕐 *Waktu:* {get_current_time()}

*Fitur yang Tersedia:* 10+
    """
    await update.message.reply_text(stats_text, parse_mode="Markdown")

async def feedback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk perintah /feedback"""
    if not context.args:
        await update.message.reply_text(
            "📝 *Kirim Feedback*\n\n"
            "/feedback [pesan]\n\n"
            "Contoh:\n"
            "/feedback Botnya keren!",
            parse_mode="Markdown"
        )
        return
    
    feedback_text = " ".join(context.args)
    user = update.effective_user
    
    await update.message.reply_text(
        f"✅ *Terima kasih atas feedbacknya!*\n\n"
        f"📝 Pesan: {feedback_text}\n\n"
        "Masukan Anda sangat berarti untuk pengembangan bot ini.",
        parse_mode="Markdown"
    )

# ============ CALLBACK QUERY HANDLER ============

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk tombol inline"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "help":
        await help_command(query, context)
    
    elif data == "news" or data == "refresh_news":
        await news(query, context)
    
    elif data == "weather":
        await weather(query, context)
    
    elif data.startswith("refresh_weather_"):
        city = data.split("_")[2]
        context.args = [city]
        await weather(query, context)
    
    elif data == "games":
        await games(query, context)
    
    elif data == "game_guess":
        await game_guess_start(query, context)
    
    elif data == "game_rps":
        await game_rps_start(query, context)
    
    elif data == "poll" or data == "poll_simple":
        await poll(query, context)
    
    elif data == "qr_new":
        await qr_code(query, context)
    
    elif data == "weather_other":
        await query.edit_message_text(
            "🌤️ *Cek Cuaca Kota Lain*\n\n"
            "Gunakan perintah:\n"
            "/weather [nama_kota]\n\n"
            "Contoh:\n"
            "/weather Bandung\n"
            "/weather Surabaya",
            parse_mode="Markdown"
        )
    
    elif data.startswith("rps_"):
        user_choice = data.split("_")[1]
        choices = {"batu": "🪨", "kertas": "📄", "gunting": "✂️"}
        bot_choice = random.choice(list(choices.keys()))
        
        # Tentukan pemenang
        if user_choice == bot_choice:
            result = "🤝 Seri!"
        elif (user_choice == "batu" and bot_choice == "gunting") or \
             (user_choice == "gunting" and bot_choice == "kertas") or \
             (user_choice == "kertas" and bot_choice == "batu"):
            result = "🎉 Anda Menang!"
        else:
            result = "😅 Bot Menang!"
        
        await query.edit_message_text(
            f"🪨📄✂️ *Hasil Permainan*\n\n"
            f"👤 Anda: {choices[user_choice]}\n"
            f"🤖 Bot: {choices[bot_choice]}\n\n"
            f"🏆 {result}\n\n"
            f"Main lagi dengan /games",
            parse_mode="Markdown"
        )
    
    else:
        await query.edit_message_text(
            "❓ *Fungsi dalam pengembangan*\n\n"
            "Fitur ini sedang dikembangkan.",
            parse_mode="Markdown"
        )

# ============ MESSAGE HANDLER ============

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler untuk pesan biasa"""
    chat_id = update.effective_chat.id
    message_text = update.message.text
    
    # Cek apakah sedang dalam game tebak angka
    if chat_id in game_data and game_data[chat_id].get('game') == 'guess':
        try:
            guess = int(message_text)
            target = game_data[chat_id]['number']
            game_data[chat_id]['attempts'] += 1
            
            if guess < target:
                await update.message.reply_text(
                    f"📈 *Terlalu kecil!* Coba lagi. (Percobaan ke-{game_data[chat_id]['attempts']})",
                    parse_mode="Markdown"
                )
            elif guess > target:
                await update.message.reply_text(
                    f"📉 *Terlalu besar!* Coba lagi. (Percobaan ke-{game_data[chat_id]['attempts']})",
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    f"🎉 *Selamat!* Anda benar!\n"
                    f"Angka: {target}\n"
                    f"Jumlah percobaan: {game_data[chat_id]['attempts']}\n\n"
                    f"Main lagi dengan /games",
                    parse_mode="Markdown"
                )
                del game_data[chat_id]
        except ValueError:
            await update.message.reply_text("❌ Mohon kirimkan angka yang valid!")
    
    else:
        # Simpan user data
        user = update.effective_user
        if user.id not in user_data_store:
            user_data_store[user.id] = {
                'username': user.username,
                'first_name': user.first_name,
                'join_date': get_current_time()
            }
        
        await update.message.reply_text(
            f"👋 Halo {user.first_name}!\n\n"
            f"Saya menerima pesan Anda.\n"
            f"Gunakan /help untuk melihat perintah yang tersedia.",
            parse_mode="Markdown"
        )

# ============ MAIN FUNCTION ============

def main():
    """Menjalankan bot"""
    print("🚀 Starting bot...")
    print(f"Bot token: {TOKEN[:10]}...")
    
    # Buat application
    application = Application.builder().token(TOKEN).build()
    
    # Tambahkan command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("about", about))
    application.add_handler(CommandHandler("news", news))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("qr", qr_code))
    application.add_handler(CommandHandler("ai", ai_chat))
    application.add_handler(CommandHandler("games", games))
    application.add_handler(CommandHandler("game", games))
    application.add_handler(CommandHandler("poll", poll))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("feedback", feedback))
    
    # Tambahkan callback query handler
    application.add_handler(CallbackQueryHandler(button_handler))
    
    # Tambahkan message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Jalankan bot
    print("✅ Bot is running! Press Ctrl+C to stop.")
    print("📱 Buka Telegram dan cari bot Anda")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()