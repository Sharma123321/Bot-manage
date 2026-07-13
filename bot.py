import json
import os
import threading
import time
import telebot
from telebot import types

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(__file__)
QR_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "upi_qr.jpg")
DEVICES_JSON_PATH = os.path.join(BASE_DIR, "devices.json")
MODELS_PER_PAGE = 8

def load_device_data():
    with open(DEVICES_JSON_PATH, "r") as file:
        return json.load(file)

def main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Price Updated
    opt1 = types.InlineKeyboardButton("📲 Root App (₹50)", callback_data="main_root_app")
    opt2 = types.InlineKeyboardButton("🖼️ Boot Image (All Brands)", callback_data="main_boot_image")
    opt3 = types.InlineKeyboardButton("💳 Aincard", callback_data="main_aincard")
    opt4 = types.InlineKeyboardButton("📱 NON ROOT PANEL", callback_data="main_non_root")
    markup.add(opt1, opt2, opt3, opt4)
    return markup

def get_aincard_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    # Price Updated
    markup.add(types.InlineKeyboardButton("🔑 Aincard Key (₹20)", callback_data="aincard_key"))
    markup.add(types.InlineKeyboardButton("📲 Aincard Key App (₹100)", callback_data="aincard_key_app"))
    markup.add(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    return markup

NON_ROOT_ITEMS = [
    ("🔑 PRIMEHOOK", "non_root_primehook"),
    ("🔹 DRIP CLIENT", "non_root_drip_client"),
    ("🔹 DRIP PROXY", "non_root_drip_proxy"),
    ("🔹 SILENT NON ROOT", "non_root_silent_non_root"),
    ("🔹 HG CLIENT", "non_root_hg_client"),
    ("🔹 BR MOD NON ROOT", "non_root_br_mod"),
    ("🔹 PATI BLUE", "non_root_pati_blue"),
    ("🔹 PATO ORANGE", "non_root_pato_orange"),
]

NON_ROOT_PLANS = {
    "non_root_primehook": "🔑 **PRIMEHOOK KEY**\n\n1 DAY  - ₹70\n3 DAY  - ₹160\n7 DAY  - ₹280\n15 DAY - ₹450\n30 DAY - ₹700",
    "non_root_drip_client": "🔹 **DRIP CLIENT KEY**\n\n1 DAY  - ₹60\n3 DAY  - ₹140\n7 DAY  - ₹260\n15 DAY - ₹400\n30 DAY - ₹600",
    "non_root_drip_proxy": "🔹 **DRIP PROXY KEY**\n\n1 DAY  - ₹60\n3 DAY  - ₹140\n7 DAY  - ₹260\n15 DAY - ₹400\n30 DAY - ₹600",
    "non_root_silent_non_root": "🔹 **SILENT NON ROOT KEY**\n\n1 DAY  - ₹70\n3 DAY  - ₹150\n7 DAY  - ₹270\n15 DAY - ₹420\n30 DAY - ₹650",
    "non_root_hg_client": "🔹 **HG CLIENT KEY**\n\n1 DAY  - ₹80\n3 DAY  - ₹180\n7 DAY  - ₹320\n15 DAY - ₹500\n30 DAY - ₹750",
    "non_root_br_mod": "🔹 **BR MOD NON ROOT KEY**\n\n1 DAY  - ₹60\n3 DAY  - ₹140\n7 DAY  - ₹260\n15 DAY - ₹400\n30 DAY - ₹600",
    "non_root_pati_blue": "🔹 **PATI BLUE KEY**\n\n1 DAY  - ₹60\n3 DAY  - ₹130\n7 DAY  - ₹240\n15 DAY - ₹380\n30 DAY - ₹550",
    "non_root_pato_orange": "🔹 **PATO ORANGE KEY**\n\n1 DAY  - ₹60\n3 DAY  - ₹130\n7 DAY  - ₹240\n15 DAY - ₹380\n30 DAY - ₹550",
}

def get_non_root_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton("🔑 PRIMEHOOK", callback_data="non_root_primehook"))
    markup.row(types.InlineKeyboardButton("🔹 DRIP CLIENT", callback_data="non_root_drip_client"), types.InlineKeyboardButton("🔹 DRIP PROXY", callback_data="non_root_drip_proxy"))
    markup.row(types.InlineKeyboardButton("🔹 SILENT NON ROOT", callback_data="non_root_silent_non_root"))
    markup.row(types.InlineKeyboardButton("🔹 HG CLIENT", callback_data="non_root_hg_client"))
    markup.row(types.InlineKeyboardButton("🔹 BR MOD NON ROOT", callback_data="non_root_br_mod"))
    markup.row(types.InlineKeyboardButton("🔹 PATI BLUE", callback_data="non_root_pati_blue"), types.InlineKeyboardButton("🔹 PATO ORANGE", callback_data="non_root_pato_orange"))
    markup.row(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    return markup

def get_brands_markup():
    device_data = load_device_data()
    markup = types.InlineKeyboardMarkup(row_width=2)
    row = []
    for brand_id, brand_info in device_data.items():
        row.append(types.InlineKeyboardButton(brand_info["devices.json"], callback_data=f"brand_{brand_id}_0"))
        if len(row) == 2: markup.row(*row); row = []
    if row: markup.row(*row)
    markup.add(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    return markup

def build_timer_text(remaining):
    total = 120
    minutes, seconds = divmod(remaining, 60)
    filled_slots = round(((total - remaining) / total) * 10)
    bar = "▓" * filled_slots + "░" * (10 - filled_slots)
    return f"✅ *Payment Done!*\n━━━━━━━━━━━━━━\n🔍 Verifying payment...\n\n`[{bar}]`\n🕐 *{minutes:02}:{seconds:02}* remaining\n━━━━━━━━━━━━━━"

def run_payment_timer(chat_id, message_id):
    for remaining in range(120, -1, -2):
        try: bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=build_timer_text(remaining), parse_mode="Markdown")
        except: pass
        time.sleep(2)
    try: bot.edit_message_text(chat_id=chat_id, message_id=message_id, text="⚠️ *Payment Not Received*", parse_mode="Markdown")
    except: pass

def send_payment_details(chat_id, item_name, amount):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("✅ Payment Done", callback_data="payment_done"))
    markup.add(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    with open(QR_IMAGE_PATH, "rb") as qr_image:
        bot.send_photo(chat_id, photo=qr_image, caption=f"💸 **PAYMENT DETAILS**\n\n🔹 **Item:** {item_name}\n🔹 **Amount:** ₹{amount}\n\n📌 *Scan QR to pay ₹{amount}.*", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=["shop", "start"])
def send_shop_menu(message):
    bot.send_message(message.chat.id, "🛒 **SHOP MENU**", reply_markup=main_menu_markup(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_menu_clicks(call):
    if call.data == "main_root_app": send_payment_details(call.message.chat.id, "Root App", 50)
    elif call.data == "main_boot_image": bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📱 **SELECT BRAND**", reply_markup=get_brands_markup(), parse_mode="Markdown")
    elif call.data == "main_aincard": bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💳 **AINCARD MENU**", reply_markup=get_aincard_markup(), parse_mode="Markdown")
    elif call.data == "aincard_key": send_payment_details(call.message.chat.id, "Aincard Key", 20)
    elif call.data == "aincard_key_app": send_payment_details(call.message.chat.id, "Aincard Key App", 100)
    elif call.data == "main_non_root": bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📱 **NON ROOT PANEL**", reply_markup=get_non_root_markup(), parse_mode="Markdown")
    elif call.data.startswith("non_root_"): bot.send_message(call.message.chat.id, NON_ROOT_PLANS.get(call.data, "Plan not found"), parse_mode="Markdown")
    elif call.data == "payment_done":
        sent = bot.send_message(call.message.chat.id, build_timer_text(120), parse_mode="Markdown")
        threading.Thread(target=run_payment_timer, args=(sent.chat.id, sent.message_id), daemon=True).start()
    elif call.data.startswith("brand_"):
        parts = call.data.split("_")
        brand_id, page = parts[1], int(parts[2])
        data = load_device_data()
        models = list(data[brand_id]["models"].items())
        markup = types.InlineKeyboardMarkup()
        for m_id, m_info in models[page*MODELS_PER_PAGE:(page+1)*MODELS_PER_PAGE]: markup.add(types.InlineKeyboardButton(m_info["name"], callback_data=f"model_{brand_id}_{m_id}"))
        if (page+1)*MODELS_PER_PAGE < len(models): markup.add(types.InlineKeyboardButton("Next ➡️", callback_data=f"brand_{brand_id}_{page+1}"))
        markup.add(types.InlineKeyboardButton("↩️ Back", callback_data="main_boot_image"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="👇 Select Model (₹200)", reply_markup=markup, parse_mode="Markdown")
    elif call.data.startswith("model_"): send_payment_details(call.message.chat.id, "Boot Image", 200)
    elif call.data == "back_to_shop_clean": bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="🛒 **SHOP MENU**", reply_markup=main_menu_markup(), parse_mode="Markdown")

bot.infinity_polling()
    
