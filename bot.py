import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ============ AMBIL TOKEN ============
TOKEN = os.environ.get("BOT_TOKEN")

if not TOKEN:
    print("❌ ERROR: BOT_TOKEN tidak ditemukan!")
    print("📝 Tambahkan BOT_TOKEN di Environment Variables Railway")
    exit(1)

print(f"✅ Token berhasil dibaca!")

# Enable logging
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

# Data storage
user_data = {}
game_data = {}

# ============ COMMANDS ============

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    welcome = f"🎉 Halo {user.first_name}! Saya Bot Super Lengkap!\n\nGunakan /help untuk melihat perintah."
    keyboard = [[InlineKeyboardButton("📰 Berita", callback_data="news"), InlineKeyboardButton("🌤️ Cuaca", callback_data="weather")]]
    await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
📚 *PERINTAH BOT*
/start - Mulai
/help - Bantuan
/about - Tentang bot
/news - Berita
/weather - Cuaca
/games - Game
/stats - Statistik
    """
    await update.message.reply_text(help_text, parse_mode="Markdown")

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Bot Telegram v2.0\nDibuat dengan Python", parse_mode="Markdown")

async def news(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📰 Berita: Bot berhasil berjalan!", parse_mode="Markdown")

async def weather(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = " ".join(context.args) if context.args else "Jakarta"
    await update.message.reply_text(f"🌤️ Cuaca di {city}: {random.randint(25,35)}°C", parse_mode="Markdown")

async def games(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎲 Tebak Angka", callback_data="game_guess")],
        [InlineKeyboardButton("🪨 Batu-Gunting-Kertas", callback_data="game_rps")]
    ]
    await update.message.reply_text("🎮 Pilih game:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"📊 Total pengguna: {len(user_data)}", parse_mode="Markdown")

# ============ CALLBACKS ============

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "news":
        await news(query, context)
    elif query.data == "weather":
        await weather(query, context)
    elif query.data == "game_guess":
        chat_id = query.message.chat_id
        game_data[chat_id] = {'number': random.randint(1, 100), 'attempts': 0}
        await query.edit_message_text("🎲 Tebak angka 1-100! Kirim angka tebakanmu.")
    elif query.data == "game_rps":
        keyboard = [
            [InlineKeyboardButton("🪨 Batu", callback_data="rps_batu"),
             InlineKeyboardButton("📄 Kertas", callback_data="rps_kertas"),
             InlineKeyboardButton("✂️ Gunting", callback_data="rps_gunting")]
        ]
        await query.edit_message_text("Pilih:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data.startswith("rps_"):
        user = query.data.split("_")[1]
        bot = random.choice(["batu", "kertas", "gunting"])
        emoji = {"batu": "🪨", "kertas": "📄", "gunting": "✂️"}
        
        if user == bot:
            result = "🤝 Seri!"
        elif (user == "batu" and bot == "gunting") or (user == "gunting" and bot == "kertas") or (user == "kertas" and bot == "batu"):
            result = "🎉 Kamu Menang!"
        else:
            result = "😅 Bot Menang!"
        
        await query.edit_message_text(f"Kamu: {emoji[user]}\nBot: {emoji[bot]}\n\n{result}")

# ============ MESSAGE HANDLER ============

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    text = update.message.text
    
    if chat_id in game_data:
        try:
            guess = int(text)
            target = game_data[chat_id]['number']
            game_data[chat_id]['attempts'] += 1
            
            if guess < target:
                await update.message.reply_text(f"📈 Terlalu kecil! (Percobaan ke-{game_data[chat_id]['attempts']})")
            elif guess > target:
                await update.message.reply_text(f"📉 Terlalu besar! (Percobaan ke-{game_data[chat_id]['attempts']})")
            else:
                await update.message.reply_text(f"🎉 Benar! Angkanya {target}! ({game_data[chat_id]['attempts']} percobaan)")
                del game_data[chat_id]
        except ValueError:
            await update.message.reply_text("❌ Kirim angka yang valid!")
    else:
        user = update.effective_user
        if user.id not in user_data:
            user_data[user.id] = user.first_name
        await update.message.reply_text(f"👋 Pesan diterima! Gunakan /help")

# ============ MAIN ============

def main():
    print("🚀 Starting bot...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("about", about))
    app.add_handler(CommandHandler("news", news))
    app.add_handler(CommandHandler("weather", weather))
    app.add_handler(CommandHandler("games", games))
    app.add_handler(CommandHandler("stats", stats))
    
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Bot is running!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
