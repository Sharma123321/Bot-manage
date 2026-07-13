import json
import os
import threading
import time

import telebot
from telebot import types

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(__file__)
# QR PATH YAHAN UPDATE KAR DIYA HAI
QR_IMAGE_PATH = os.path.join(BASE_DIR, "assets", "upi_qr.jpg") 
DEVICES_JSON_PATH = os.path.join(BASE_DIR, "devices.json")
MODELS_PER_PAGE = 8

def load_device_data():
    with open(DEVICES_JSON_PATH, "r") as file:
        return json.load(file)

def main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    opt1 = types.InlineKeyboardButton("📲 Root App (₹100)", callback_data="main_root_app")
    opt2 = types.InlineKeyboardButton("🖼️ Boot Image (All Brands)", callback_data="main_boot_image")
    opt3 = types.InlineKeyboardButton("💳 Aincard", callback_data="main_aincard")
    opt4 = types.InlineKeyboardButton("📱 NON ROOT PANEL", callback_data="main_non_root")
    markup.add(opt1, opt2, opt3, opt4)
    return markup

def get_aincard_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(types.InlineKeyboardButton("🔑 Aincard Key", callback_data="aincard_key"))
    markup.add(types.InlineKeyboardButton("📲 Aincard Key App", callback_data="aincard_key_app"))
    markup.add(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    return markup

NON_ROOT_PLANS = {
    "non_root_primehook": ("🔑 **PRIMEHOOK KEY**\n\n1 DAY - ₹70\n3 DAY - ₹160\n7 DAY - ₹280\n15 DAY - ₹450\n30 DAY - ₹700"),
    "non_root_drip_client": ("🔹 **DRIP CLIENT KEY**\n\n1 DAY - ₹60\n3 DAY - ₹140\n7 DAY - ₹260\n15 DAY - ₹400\n30 DAY - ₹600"),
    "non_root_drip_proxy": ("🔹 **DRIP PROXY KEY**\n\n1 DAY - ₹60\n3 DAY - ₹140\n7 DAY - ₹260\n15 DAY - ₹400\n30 DAY - ₹600"),
    "non_root_silent_non_root": ("🔹 **SILENT NON ROOT KEY**\n\n1 DAY - ₹70\n3 DAY - ₹150\n7 DAY - ₹270\n15 DAY - ₹420\n30 DAY - ₹650"),
    "non_root_hg_client": ("🔹 **HG CLIENT KEY**\n\n1 DAY - ₹80\n3 DAY - ₹180\n7 DAY - ₹320\n15 DAY - ₹500\n30 DAY - ₹750"),
    "non_root_br_mod": ("🔹 **BR MOD NON ROOT KEY**\n\n1 DAY - ₹60\n3 DAY - ₹140\n7 DAY - ₹260\n15 DAY - ₹400\n30 DAY - ₹600"),
    "non_root_pati_blue": ("🔹 **PATI BLUE KEY**\n\n1 DAY - ₹60\n3 DAY - ₹130\n7 DAY - ₹240\n15 DAY - ₹380\n30 DAY - ₹550"),
    "non_root_pato_orange": ("🔹 **PATO ORANGE KEY**\n\n1 DAY - ₹60\n3 DAY - ₹130\n7 DAY - ₹240\n15 DAY - ₹380\n30 DAY - ₹550"),
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
        row.append(types.InlineKeyboardButton(brand_info["name"], callback_data=f"brand_{brand_id}_0"))
        if len(row) == 2:
            markup.row(*row); row = []
    if row: markup.row(*row)
    markup.add(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    return markup

def build_timer_text(remaining):
    total = 120
    minutes, seconds = divmod(remaining, 60)
    filled_slots = round(((total - remaining) / total) * 10)
    bar = "▓" * filled_slots + "░" * (10 - filled_slots)
    return f"✅ *Payment Done!*\n━━━━━━━━━━━━━━\n🔍 Verifying your payment...\n\n`[{bar}]`\n🕐 *{minutes:02}:{seconds:02}* remaining\n━━━━━━━━━━━━━━"

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
    
    payment_text = f"💸 **PAYMENT DETAILS**\n\n🔹 **Item:** {item_name}\n🔹 **Amount:** ₹{amount}\n🔹 **Time:** Instant Delivery\n\n📌 *Scan the QR code to pay ₹{amount}.*"
    
    with open(QR_IMAGE_PATH, "rb") as qr_image:
        bot.send_photo(chat_id, photo=qr_image, caption=payment_text, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=["shop", "start"])
def send_shop_menu(message):
    bot.send_message(message.chat.id, "🛒 **SHOP MENU**\n\nChoose an option below to proceed:", reply_markup=main_menu_markup(), parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_menu_clicks(call):
    if call.data == "main_root_app":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        send_payment_details(call.message.chat.id, "Root App", 100)
    
    elif call.data == "main_boot_image":
        try: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📱 **SELECT BRAND**", reply_markup=get_brands_markup(), parse_mode="Markdown")
        except: bot.send_message(call.message.chat.id, "📱 **SELECT BRAND**", reply_markup=get_brands_markup(), parse_mode="Markdown")
    
    elif call.data == "payment_done":
        bot.answer_callback_query(call.id)
        sent = bot.send_message(call.message.chat.id, build_timer_text(120), parse_mode="Markdown")
        threading.Thread(target=run_payment_timer, args=(sent.chat.id, sent.message_id), daemon=True).start()

    elif call.data == "main_aincard":
        try: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="💳 **AINCARD MENU**", reply_markup=get_aincard_markup(), parse_mode="Markdown")
        except: bot.send_message(call.message.chat.id, "💳 **AINCARD MENU**", reply_markup=get_aincard_markup(), parse_mode="Markdown")

    elif call.data in ["aincard_key", "aincard_key_app"]:
        bot.answer_callback_query(call.id)
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        amount = 20 if call.data == "aincard_key" else 100
        send_payment_details(call.message.chat.id, "Aincard Key" if amount == 20 else "Aincard Key App", amount)

    elif call.data == "main_non_root":
        try: bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📱 **NON ROOT PANEL**", reply_markup=get_non_root_markup(), parse_mode="Markdown")
        except: bot.send_message(call.message.chat.id, "📱 **NON ROOT PANEL**", reply_markup=get_non_root_markup(), parse_mode="Markdown")

    elif call.data.startswith("non_root_"):
        bot.answer_callback_query(call.id)
        if call.data in NON_ROOT_PLANS:
            bot.send_message(call.message.chat.id, NON_ROOT_PLANS[call.data], parse_mode="Markdown")

    elif call.data == "back_to_shop_clean":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        bot.send_message(call.message.chat.id, "🛒 **SHOP MENU**\n\nChoose an option below to proceed:", reply_markup=main_menu_markup(), parse_mode="Markdown")

bot.infinity_polling()
                                   
