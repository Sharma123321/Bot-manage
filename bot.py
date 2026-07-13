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


def get_non_root_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.row(types.InlineKeyboardButton("🔑 PRIMEHOOK", callback_data="non_root_primehook"))
    markup.row(
        types.InlineKeyboardButton("🔹 DRIP CLIENT", callback_data="non_root_drip_client"),
        types.InlineKeyboardButton("🔹 DRIP PROXY", callback_data="non_root_drip_proxy"),
    )
    markup.row(types.InlineKeyboardButton("🔹 SILENT NON ROOT", callback_data="non_root_silent_non_root"))
    markup.row(types.InlineKeyboardButton("🔹 HG CLIENT", callback_data="non_root_hg_client"))
    markup.row(types.InlineKeyboardButton("🔹 BR MOD NON ROOT", callback_data="non_root_br_mod"))
    markup.row(
        types.InlineKeyboardButton("🔹 PATI BLUE", callback_data="non_root_pati_blue"),
        types.InlineKeyboardButton("🔹 PATO ORANGE", callback_data="non_root_pato_orange"),
    )
    markup.row(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    return markup


# Sabhi Non Root items ki pricing aur details
PLANS_DATA = {
    "primehook": {"name": "PRIMEHOOK", "prices": {"1d": 70, "3d": 160, "7d": 280, "15d": 450, "30d": 700}},
    "drip_client": {"name": "DRIP CLIENT", "prices": {"1d": 60, "3d": 140, "7d": 260, "15d": 400, "30d": 600}},
    "drip_proxy": {"name": "DRIP PROXY", "prices": {"1d": 60, "3d": 140, "7d": 260, "15d": 400, "30d": 600}},
    "silent_non_root": {"name": "SILENT NON ROOT", "prices": {"1d": 70, "3d": 150, "7d": 270, "15d": 420, "30d": 650}},
    "hg_client": {"name": "HG CLIENT", "prices": {"1d": 80, "3d": 180, "7d": 320, "15d": 500, "30d": 750}},
    "br_mod": {"name": "BR MOD NON ROOT", "prices": {"1d": 60, "3d": 140, "7d": 260, "15d": 400, "30d": 600}},
    "pati_blue": {"name": "PATI BLUE", "prices": {"1d": 60, "3d": 130, "7d": 240, "15d": 380, "30d": 550}},
    "pato_orange": {"name": "PATO ORANGE", "prices": {"1d": 60, "3d": 130, "7d": 240, "15d": 380, "30d": 550}},
}


def get_brands_markup():
    device_data = load_device_data()
    markup = types.InlineKeyboardMarkup(row_width=2)
    row = []
    for brand_id, brand_info in device_data.items():
        row.append(types.InlineKeyboardButton(brand_info["name"], callback_data=f"brand_{brand_id}_0"))
        if len(row) == 2:
            markup.row(*row)
            row = []
    if row:
        markup.row(*row)
    markup.add(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))
    return markup


def build_timer_text(remaining):
    total = 120
    minutes = remaining // 60
    seconds = remaining % 60
    filled_slots = round(((total - remaining) / total) * 10)
    bar = "▓" * filled_slots + "░" * (10 - filled_slots)
    return (
        "✅ *Payment Done!*\n"
        "━━━━━━━━━━━━━━\n"
        "🔍 Verifying your payment...\n\n"
        f"`[{bar}]`\n"
        f"🕐 *{minutes:02}:{seconds:02}* remaining\n"
        "━━━━━━━━━━━━━━"
    )


def run_payment_timer(chat_id, message_id):
    for remaining in range(120, -1, -2):
        try:
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text=build_timer_text(remaining),
                parse_mode="Markdown",
            )
        except Exception:
            pass
        time.sleep(2)
    try:
        bot.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=(
                "⚠️ *Payment Not Received*\n\n"
                "If you have already paid, click ✅ Payment Done again.\n"
                "Otherwise, please complete the payment first."
            ),
            parse_mode="Markdown",
        )
    except Exception:
        pass


def send_payment_details(chat_id, item_name, amount):
    markup = types.InlineKeyboardMarkup()
    done_btn = types.InlineKeyboardButton("✅ Payment Done", callback_data="payment_done")
    back_btn = types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean")
    markup.add(done_btn)
    markup.add(back_btn)

    payment_text = (
        "💸 **PAYMENT DETAILS**\n\n"
        f"🔹 **Item:** {item_name}\n"
        f"🔹 **Amount:** ₹{amount}\n"
        "🔹 **Time:** Instant Delivery\n\n"
        f"📌 *Scan the QR code to pay ₹{amount}.*"
    )

    with open(QR_IMAGE_PATH, "rb") as qr_image:
        bot.send_photo(
            chat_id,
            photo=qr_image,
            caption=payment_text,
            reply_markup=markup,
            parse_mode="Markdown",
        )


@bot.message_handler(commands=["shop", "start"])
def send_shop_menu(message):
    bot.send_message(
        message.chat.id,
        "🛒 **SHOP MENU**\n\nChoose an option below to proceed:",
        reply_markup=main_menu_markup(),
        parse_mode="Markdown",
    )


@bot.message_handler(commands=["id"])
def send_id(message):
    bot.send_message(message.chat.id, f"🆔 Your Telegram ID: {message.from_user.id}")


@bot.callback_query_handler(func=lambda call: True)
def handle_menu_clicks(call):

    if call.data == "main_root_app":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        send_payment_details(call.message.chat.id, "Root App", 100)

    elif call.data == "main_boot_image":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📱 **SELECT BRAND**\n\nChoose your device brand from the list below:",
                reply_markup=get_brands_markup(),
                parse_mode="Markdown",
            )
        except Exception:
            bot.send_message(
                call.message.chat.id,
                "📱 **SELECT BRAND**\n\nChoose your device brand from the list below:",
                reply_markup=get_brands_markup(),
                parse_mode="Markdown",
            )

    elif call.data == "payment_done":
        bot.answer_callback_query(call.id)
        sent = bot.send_message(
            call.message.chat.id,
            build_timer_text(120),
            parse_mode="Markdown",
        )
        threading.Thread(
            target=run_payment_timer,
            args=(sent.chat.id, sent.message_id),
            daemon=True,
        ).start()

    elif call.data == "main_aincard":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="💳 **AINCARD MENU**\n\nChoose an option below:",
                reply_markup=get_aincard_markup(),
                parse_mode="Markdown",
            )
        except Exception:
            bot.send_message(
                call.message.chat.id,
                "💳 **AINCARD MENU**\n\nChoose an option below:",
                reply_markup=get_aincard_markup(),
                parse_mode="Markdown",
            )

    elif call.data == "aincard_key":
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        send_payment_details(call.message.chat.id, "Aincard Key", 20)

    elif call.data == "aincard_key_app":
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        send_payment_details(call.message.chat.id, "Aincard Key App", 100)

    # --- NON ROOT PANEL MAIN MENU ---
    elif call.data == "main_non_root":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📱 **NON ROOT PANEL**\n\nChoose an option below:",
                reply_markup=get_non_root_markup(),
                parse_mode="Markdown",
            )
        except Exception:
            bot.send_message(
                call.message.chat.id,
                "📱 **NON ROOT PANEL**\n\nChoose an option below:",
                reply_markup=get_non_root_markup(),
                parse_mode="Markdown",
            )

    # --- NON ROOT PANELS PAR CLICK ---
    elif call.data.startswith("non_root_"):
        bot.answer_callback_query(call.id)
        key_type = call.data.replace("non_root_", "")
        
        if key_type in PLANS_DATA:
            item_info = PLANS_DATA[key_type]
            markup = types.InlineKeyboardMarkup(row_width=2)
            
            btn_1d = types.InlineKeyboardButton(f"1 DAY - ₹{item_info['prices']['1d']}", callback_data=f"pay_{key_type}_1d")
            btn_3d = types.InlineKeyboardButton(f"3 DAY - ₹{item_info['prices']['3d']}", callback_data=f"pay_{key_type}_3d")
            btn_7d = types.InlineKeyboardButton(f"7 DAY - ₹{item_info['prices']['7d']}", callback_data=f"pay_{key_type}_7d")
            btn_15d = types.InlineKeyboardButton(f"15 DAY - ₹{item_info['prices']['15d']}", callback_data=f"pay_{key_type}_15d")
            btn_30d = types.InlineKeyboardButton(f"30 DAY - ₹{item_info['prices']['30d']}", callback_data=f"pay_{key_type}_30d")
            back_btn = types.InlineKeyboardButton("🔙 Back to List", callback_data="main_non_root")
            
            markup.add(btn_1d, btn_3d)
            markup.add(btn_7d, btn_15d)
            markup.add(btn_30d)
            markup.add(back_btn)

            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"🔹 **{item_info['name']} MENU**\n\nChoose your validity plan below:",
                reply_markup=markup,
                parse_mode="Markdown",
            )

    # --- VALIDITY PLANS PAR CLICK KARNE PAR PAY DETAILS ---
    elif call.data.startswith("pay_"):
        bot.answer_callback_query(call.id)
        parts = call.data.split("_")
        duration = parts[-1] 
        key_type = "_".join(parts[1:-1])
        
        if key_type in PLANS_DATA and duration in PLANS_DATA[key_type]["prices"]:
            item_info = PLANS_DATA[key_type]
            amount = item_info["prices"][duration]
            display_duration = duration.upper().replace("D", " DAY")
            
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
                
            send_payment_details(call.message.chat.id, f"{item_info['name']} ({display_duration})", amount)

    # --- BRAND PAGE SELECTION LOGIC ---
    elif call.data.startswith("brand_"):
        device_data = load_device_data()
        parts = call.data.split("_")
        brand_id = parts[1]
        page = int(parts[2])

        if brand_id not in device_data:
            bot.answer_callback_query(call.id, text="⚠️ Brand not found!", show_alert=True)
            return

        brand_name = device_data[brand_id]["name"]
        models_list = list(device_data[brand_id]["models"].items())

        start_idx = page * MODELS_PER_PAGE
        end_idx = start_idx + MODELS_PER_PAGE
        current_page_models = models_list[start_idx:end_idx]

        markup = types.InlineKeyboardMarkup()
        row = []
        for model_id, model_info in current_page_models:
            row.append(types.InlineKeyboardButton(model_info["name"], callback_data=f"model_{brand_id}_{model_id}"))
            if len(row) == 2:
                markup.row(*row)
                row = []
        if row:
            markup.row(*row)

        nav_buttons = []
        if page > 0:
            nav_buttons.append(types.InlineKeyboardButton("⬅️ Back", callback_data=f"brand_{brand_id}_{page - 1}"))
        if end_idx < len(models_list):
            nav_buttons.append(types.InlineKeyboardButton("Next ➡️", callback_data=f"brand_{brand_id}_{page + 1}"))
        if nav_buttons:
            markup.row(*nav_buttons)

        markup.add(types.InlineKeyboardButton("📱 Main Menu (Brands)", callback_data="back_to_brands"))

        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=f"Selected: **{brand_name}** (Page {page + 1})\n\n👇 Apna model select karein:",
                reply_markup=markup,
                parse_mode="Markdown",
            )
        except Exception:
            bot.send_message(
                call.message.chat.id,
                f"Selected: **{brand_name}** (Page {page + 1})\n\n👇 Apna model select karein:",
                reply_markup=markup,
                parse_mode="Markdown",
            )

    # --- MODEL SELECT KARNE PAR QR LOGIC (FIXED INNER PATHS) ---
    elif call.data.startswith("model_"):
        device_data = load_device_data()
        parts = call.data.split("_", 2)
        brand_id = parts[1]
        model_id = parts[2]

        try:
            model_info = device_data[brand_id]["models"][model_id]
            
            # Absolute path matching update for system compatibility
            qr_relative_path = model_info["qr"]
            if qr_relative_path.startswith("assets/"):
                qr_relative_path = qr_relative_path.replace("assets/", "", 1)
                
            qr_path = os.path.join(BASE_DIR, "assets", qr_relative_path)

            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass

            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("↩️ Back to Shop", callback_data="back_to_shop_clean"))

            with open(qr_path, "rb") as photo:
                bot.send_photo(
                    call.message.chat.id,
                    photo=photo,
                    caption=model_info["text"],
                    reply_markup=markup,
                    parse_mode="Markdown",
                )
        except Exception:
            bot.answer_callback_query(call.id, text="⚠️ QR Code file load nahi ho saki!", show_alert=True)

    elif call.data == "back_to_brands":
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="📱 **SELECT BRAND**\n\nChoose your device brand from the list below:",
                reply_markup=get_brands_markup(),
                parse_mode="Markdown",
            )
        except Exception:
            bot.send_message(
                call.message.chat.id,
                "📱 **SELECT BRAND**\n\nChoose your device brand from the list below:",
                reply_markup=get_brands_markup(),
                parse_mode="Markdown",
            )

    elif call.data == "back_to_shop_clean":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        bot.send_message(
            call.message.chat.id,
            "🛒 **SHOP MENU**\n\nChoose an option below to proceed:",
            reply_markup=main_menu_markup(),
            parse_mode="Markdown",
        )


print("Bot started...")
bot.infinity_polling()
    
