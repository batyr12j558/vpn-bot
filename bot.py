import telebot
import os

# 🔐 TOKEN-i şu ýere goý (täze, BotFather-dan alnan)
BOT_TOKEN = "TOKENI_BU_YERE_GOY"

# 👑 Admin ID (öz Telegram ID-ň)
ADMIN_ID = 123456789

bot = telebot.TeleBot(BOT_TOKEN)

waiting_users = {}

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "Töleg edip skrenshot iberiň 📸\n"
        "Admin tassyklandan soň giriş maglumatlary berler."
    )

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    waiting_users[user_id] = message.chat.id

    caption = (
        f"🧾 Täze töleg skrenshoty\n"
        f"👤 User ID: {user_id}\n\n"
        f"/ok {user_id} — tassykla\n"
        f"/not {user_id} — inkär et"
    )

    bot.send_photo(
        ADMIN_ID,
        message.photo[-1].file_id,
        caption=caption
    )

@bot.message_handler(commands=['ok'])
def approve(message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()
    if len(parts) != 2:
        bot.send_message(ADMIN_ID, "Ulanyş: /ok USER_ID")
        return

    user_id = int(parts[1])

    if user_id in waiting_users:
        chat_id = waiting_users[user_id]

        bot.send_message(
            chat_id,
            "✅ Töleg tassyklandy!\n\n"
            "🔐 VPN Panel:\n"
            "https://toppvpn.svxpodpiska.online/dashboard/#/login\n"
            "👤 Login: Diller\n"
            "🔑 Password: 1"
        )

        del waiting_users[user_id]
        bot.send_message(ADMIN_ID, "Berildi ✅")

@bot.message_handler(commands=['not'])
def reject(message):
    if message.from_user.id != ADMIN_ID:
        return

    parts = message.text.split()
    if len(parts) != 2:
        return

    user_id = int(parts[1])
    waiting_users.pop(user_id, None)
    bot.send_message(ADMIN_ID, f"❌ User {user_id} inkär edildi")

# ▶️ Diňe ŞU polling bolmaly (biri ýeterlik)
bot.polling(none_stop=True)