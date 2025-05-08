import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = "7802477774:AAGcoUP8-QZ6kdbK_OO_Vy-diPxqyiRSdbk"
PASSWORD = "69"

# To store verified users
allowed_users = set()

def convert_timestamp(timestamp):
    from datetime import datetime
    try:
        return datetime.fromtimestamp(int(timestamp)).strftime('%d/%m/%Y (%I:%M:%S %p)')
    except:
        return "Unknown"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in allowed_users:
        await update.message.reply_text("Welcome back! Send /get {uid} to get player info.")
    else:
        await update.message.reply_text("Please enter the password to continue:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in allowed_users:
        if text == PASSWORD:
            allowed_users.add(user_id)
            await update.message.reply_text("Access granted! Send /get {uid} to get player info.")
        else:
            await update.message.reply_text("Wrong password! Try again.")
        return

    # If message is "/get {uid}"
    if text.startswith("/get") and len(text.split()) == 2:
        uid = text.split()[1]
        if not uid.isdigit():
            await update.message.reply_text("Please provide a valid Free Fire UID (numbers only).")
            return

        api_url = f"https://freefireinfo-tanhung.onrender.com/info?&uid={uid}&region=sg"

        try:
            response = requests.get(api_url)
            data = response.json()

            basic = data.get("basicInfo", {})
            pet = data.get("petInfo", {})
            clan = data.get("clanBasicInfo", {})
            captain = data.get("captainBasicInfo", {})

            msg = (
                f"╒═══ 𝗣𝗟𝗔𝗬𝗘𝗥 𝗔𝗖𝗧𝗜𝗩𝗜𝗧𝗬 ════════════\n"
                f"🔹 **Last Login:** {convert_timestamp(basic.get('lastLoginAt', '0'))}\n"
                f"🔹 **Created At:** {convert_timestamp(basic.get('createAt', '0'))}\n\n"
                
                f"╒═══ 𝗔𝗖𝗖𝗢𝗨𝗡𝗧 𝗗𝗘𝗧𝗔𝗜𝗟𝗦 ════════════\n"
                f"🔹 **Name:** {basic.get('nickname', 'N/A')}\n"
                f"🔹 **UID:** {basic.get('accountId', 'N/A')}\n"
                f"🔹 **Level:** {basic.get('level', 'N/A')}\n"
                f"🔹 **Likes:** {basic.get('liked', '0')}\n"
                f"🔹 **Badges:** {basic.get('badgeCnt', '0')}\n"
                f"🔹 **Experience:** {basic.get('exp', '0')}\n"
                f"🔹 **Honor Score:** {basic.get('honorScore', '0')}\n"
                f"🔹 **Preferred Mode:** {basic.get('preferMode', 'N/A')}\n"
                f"🔹 **Language:** {basic.get('language', 'N/A')}\n"
                f"🔹 **Bio:** {basic.get('signature', 'No Signature')}\n\n"
                
                f"╒═══ 𝗣𝗟𝗔𝗬𝗘𝗥 𝗢𝗩𝗘𝗥𝗩𝗜𝗘𝗪 ════════════\n"
                f"🔹 **Equipped Skills:** {', '.join(basic.get('equippedSkills', []))}\n"
                f"🔹 **BR Rank Points:** {basic.get('brRankPoints', '0')}\n"
                f"🔹 **Current BR Rank:** {basic.get('rank', 'N/A')}\n"
                f"🔹 **CS Rank Points:** {basic.get('csRankPoints', '0')}\n"
                f"🔹 **Current CS Rank:** {basic.get('csRank', 'N/A')}\n"
                f"🔹 **Title:** {basic.get('title', 'N/A')}\n"
                f"🔹 **Game Version:** {basic.get('gameVersion', 'N/A')}\n\n"
                
                f"╒═══ 𝐏𝐄𝐓 𝐈𝐍𝐅𝐎 ════════════\n"
                f"🔹 **Pet Name:** {pet.get('name', 'N/A')}\n"
                f"🔹 **Level:** {pet.get('level', 'N/A')}\n"
                f"🔹 **Exp:** {pet.get('exp', '0')}\n"
                f"🔹 **Star Marked:** {'Yes' if pet.get('starMarked', False) else 'No'}\n"
                f"🔹 **Selected:** {'Yes' if pet.get('selected', False) else 'No'}\n\n"
                
                f"╒═══ 𝐆𝐔𝐈𝐋𝐃 𝐈𝐍𝐅𝐎 ════════════\n"
                f"🔹 **Name:** {clan.get('name', 'N/A')}\n"
                f"🔹 **ID:** {clan.get('id', 'N/A')}\n"
                f"🔹 **Level:** {clan.get('level', 'N/A')}\n"
                f"🔹 **Members:** {clan.get('memberNum', '0')}\n"
                f"🔹 **Capacity:** {clan.get('capacity', '0')}\n\n"
                
                f"╒═══ 𝐋𝐄𝐀𝐃𝐄𝐑 𝐈𝐍𝐅𝐎 ════════════\n"
                f"🔹 **Name:** {captain.get('nickname', 'N/A')}\n"
                f"🔹 **UID:** {captain.get('uid', 'N/A')}\n"
                f"🔹 **Level:** {captain.get('level', 'N/A')}\n"
                f"🔹 **Likes:** {captain.get('liked', '0')}\n"
                f"🔹 **Badges:** {captain.get('badgeCnt', '0')}\n"
                f"🔹 **Title:** {captain.get('title', 'N/A')}\n"
                f"🔹 **BR Rank Points:** {captain.get('brRankPoints', '0')}\n"
                f"🔹 **Current BR Rank:** {captain.get('rank', 'N/A')}\n"
                f"🔹 **CS Rank Points:** {captain.get('csRankPoints', '0')}\n"
                f"🔹 **Current CS Rank:** {captain.get('csRank', 'N/A')}\n"
                f"🔹 **Last Login:** {convert_timestamp(captain.get('lastLoginAt', '0'))}\n"
                f"🔹 **Account Created At:** {convert_timestamp(captain.get('createAt', '0'))}\n"
            )

            await update.message.reply_text(msg, parse_mode="Markdown")

        except Exception as e:
            await update.message.reply_text("Something went wrong while fetching data. Please check the UID.")
    else:
        await update.message.reply_text("Invalid command. Use /get {uid} to fetch player info.")

async def handle_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if user_id not in allowed_users:
        if text == PASSWORD:
            allowed_users.add(user_id)
            await update.message.reply_text("Access granted! Send /get {uid} to get player info.")
        else:
            await update.message.reply_text("Wrong password! Try again.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("get", handle_message))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_password))

    print("Bot is running...")
    app.run_polling()
