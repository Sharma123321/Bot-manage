import telebot
from telebot import types

# 🟢 CONFIGURATION SET (Direct file path setup)
API_TOKEN = '8764761380:AAHgpdixVRmVL8D71tqj3bHtgFRvJLXJqWg'
QR_IMAGE_PATH = 'upi_qr.jpg'  # Ab ye direct file dhoondhega, bina kisi folder ke!

bot = telebot.TeleBot(API_TOKEN)

# 📊 COMPLETE DATABASE
PLANS_DATA = {
    # --- NON ROOT PANEL ---
    "primehook": {"name": "PRIMEHOOK", "prices": {"1d": 100, "3d": 200, "7d": 400, "15d": 700, "30d": 1000}},
    "drip_client": {"name": "DRIP CLIENT", "prices": {"1d": 90, "3d": 180, "7d": 350, "15d": 600, "30d": 900}},
    "drip_proxy": {"name": "DRIP PROXY", "prices": {"1d": 90, "3d": 180, "7d": 350, "15d": 600, "30d": 900}},
    "silent_non_root": {"name": "SILENT NON ROOT", "prices": {"1d": 90, "3d": 180, "7d": 350, "15d": 600, "30d": 900}},
    "hg_client": {"name": "HG CLIENT", "prices": {"1d": 100, "3d": 200, "7d": 400, "15d": 700, "30d": 1000}},
    "br_mod": {"name": "BR MOD NON ROOT", "prices": {"1d": 90, "3d": 180, "7d": 350, "15d": 600, "30d": 900}},
    "pati_blue": {"name": "PATI BLUE", "prices": {"1d": 80, "3d": 160, "7d": 300, "15d": 500, "30d": 800}},
    "pato_orange": {"name": "PATO ORANGE", "prices": {"1d": 80, "3d": 160, "7d": 300, "15d": 500, "30d": 800}},
    
    # --- ROOT PANEL ---
    "root_prime": {"name": "ROOT PRIMEHOOK", "prices": {"1d": 120, "3d": 250, "7d": 500, "30d": 1200}},
    "root_drip": {"name": "ROOT DRIP CLIENT", "prices": {"1d": 110, "3d": 220, "7d": 450, "30d": 1100}},
    
    # --- BOOT IMAGE ---
    "boot_img": {"name": "CUSTOM BOOT IMAGE", "prices": {"1d": 50, "3d": 100, "7d": 200, "30d": 500}},
    
    # --- AVINCHARD ---
    "avinchard": {"name": "AVINCHARD PREMIUM", "prices": {"1d": 150, "3d": 300, "7d": 600, "30d": 1500}}
}

# 📋 KEYBOARD GENERATORS

def get_main_shop_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("📱 NON ROOT PANEL", callback_data="main_non_root"),
        types.InlineKeyboardButton("🛡️ ROOT PANEL", callback_data="main_root"),
        types.InlineKeyboardButton("💿 BOOT IMAGE", callback_data="main_boot"),
        types.InlineKeyboardButton("⚡ AVINCHARD", callback_data="main_avinchard")
    )
    return markup

def get_non_root_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        types.InlineKeyboardButton("🔑 PRIMEHOOK", callback_data="panel_primehook"),
        types.InlineKeyboardButton("🔹 DRIP CLIENT", callback_data="panel_drip_client"),
        types.InlineKeyboardButton("🔹 DRIP PROXY", callback_data="panel_drip_proxy"),
        types.InlineKeyboardButton("🔹 SILENT NON ROOT", callback_data="panel_silent_non_root"),
        types.InlineKeyboardButton("🔹 HG CLIENT", callback_data="panel_hg_client"),
        types.InlineKeyboardButton("🔹 BR MOD NON ROOT", callback_data="panel_br_mod"),
        types.InlineKeyboardButton("🔹 PATI BLUE", callback_data="panel_pati_blue"),
        types.InlineKeyboardButton("🔹 PATO ORANGE", callback_data="panel_pato_orange"),
        types.InlineKeyboardButton("🔙 Back to Main Shop", callback_data="main_shop")
    )
    return markup

# 🚀 STEP 1: INITIAL COMMAND ROUTE (START)
@bot.message_handler(commands=['start', 'shop'])
def send_welcome(message):
    bot.send_message(
        message.chat.id, 
        "▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n🛒 **WELCOME TO PREMIUM SHOP**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nChoose your panel category below 📥:", 
        reply_markup=get_main_shop_markup(),
        parse_mode="Markdown"
    )

# 🎛️ STEP 2: CALLBACK HANDLERS FOR NAVIGATION
@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    
    if call.data == "main_shop":
        bot.answer_callback_query(call.id)
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n🛒 **WELCOME TO PREMIUM SHOP**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nChoose your panel category below 📥:",
            reply_markup=get_main_shop_markup(),
            parse_mode="Markdown"
        )

    elif call.data == "main_non_root":
        bot.answer_callback_query(call.id)
        try:
            bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n👾 **NON ROOT PANEL**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nChoose a cheat/tool from the list below 📥",
                reply_markup=get_non_root_markup(),
                parse_mode="Markdown"
            )
        except Exception:
            bot.delete_message(call.message.chat.id, call.message.message_id)
            bot.send_message(
                call.message.chat.id,
                text="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n👾 **NON ROOT PANEL**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nChoose a cheat/tool from the list below 📥",
                reply_markup=get_non_root_markup(),
                parse_mode="Markdown"
            )

    elif call.data == "main_root":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("🛡️ ROOT PRIMEHOOK", callback_data="panel_root_prime"),
            types.InlineKeyboardButton("🛡️ ROOT DRIP CLIENT", callback_data="panel_root_drip"),
            types.InlineKeyboardButton("🔙 Back to Main Shop", callback_data="main_shop")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n🛡️ **ROOT PANEL**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nSelect Root Package:",
            reply_markup=markup, parse_mode="Markdown"
        )

    elif call.data == "main_boot":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("💿 GET CUSTOM BOOT IMAGE", callback_data="panel_boot_img"),
            types.InlineKeyboardButton("🔙 Back to Main Shop", callback_data="main_shop")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n💿 **BOOT IMAGE SUBMENU**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nSelect Package:",
            reply_markup=markup, parse_mode="Markdown"
        )

    elif call.data == "main_avinchard":
        bot.answer_callback_query(call.id)
        markup = types.InlineKeyboardMarkup(row_width=1)
        markup.add(
            types.InlineKeyboardButton("⚡ AVINCHARD PREMIUM BYPASS", callback_data="panel_avinchard"),
            types.InlineKeyboardButton("🔙 Back to Main Shop", callback_data="main_shop")
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id, message_id=call.message.message_id,
            text="▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n⚡ **AVINCHARD MENU**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nSelect Package:",
            reply_markup=markup, parse_mode="Markdown"
        )

    elif call.data.startswith("panel_"):
        bot.answer_callback_query(call.id)
        key_type = call.data.replace("panel_", "")
        
        if key_type in PLANS_DATA:
            item_info = PLANS_DATA[key_type]
            markup = types.InlineKeyboardMarkup(row_width=1)
            
            for duration, price in item_info["prices"].items():
                d_label = duration.replace("1d", "1 Day").replace("3d", "3 Days").replace("7d", "7 Days").replace("15d", "15 Days").replace("30d", "30 Days")
                markup.add(types.InlineKeyboardButton(f"⏱️ {d_label} — ₹{price}", callback_data=f"pay_{key_type}_{duration}"))
            
            back_target = "main_non_root" if "root_" not in key_type and key_type not in ["boot_img", "avinchard"] else "main_shop"
            markup.add(types.InlineKeyboardButton("🔙 Back to List", callback_data=back_target))

            try:
                bot.edit_message_text(
                    chat_id=call.message.chat.id, message_id=call.message.message_id,
                    text=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n👾 **{item_info['name']}**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nChoose a plan 📥",
                    reply_markup=markup, parse_mode="Markdown"
                )
            except Exception:
                bot.delete_message(call.message.chat.id, call.message.message_id)
                bot.send_message(
                    call.message.chat.id,
                    text=f"▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n👾 **{item_info['name']}**\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\nChoose a plan 📥",
                    reply_markup=markup, parse_mode="Markdown"
                )

    elif call.data.startswith("pay_"):
        bot.answer_callback_query(call.id)
        parts = call.data.split("_")
        duration = parts[-1] 
        key_type = "_".join(parts[1:-1]) 
        
        if key_type in PLANS_DATA and duration in PLANS_DATA[key_type]["prices"]:
            item_info = PLANS_DATA[key_type]
            amount = item_info["prices"][duration]
            
            display_duration = duration.upper().replace("D", " DAYS").replace("S DAYS", " DAY")
            if duration == "1d": display_duration = "1 DAY"

            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except Exception:
                pass
            
            markup = types.InlineKeyboardMarkup(row_width=1)
            done_btn = types.InlineKeyboardButton("✅ Payment Done", callback_data="payment_done")
            back_btn = types.InlineKeyboardButton("🔙 Back to Options", callback_data=f"panel_{key_type}")
            markup.add(done_btn, back_btn)

            payment_text = (
                f"💸 🖥️ **{item_info['name']}** 🖥️ 💸\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"✅ **SELECTED PLAN:** `{display_duration}`\n"
                f"💰 **TOTAL AMOUNT:** `₹{amount}`\n"
                f"⚡️ **DELIVERY STATUS:** `Instant Key`\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"📌 *Scan the QR code below to proceed with your ₹{amount} payment.*"
            )

            try:
                with open(QR_IMAGE_PATH, "rb") as qr_image:
                    bot.send_photo(
                        call.message.chat.id, photo=qr_image,
                        caption=payment_text, reply_markup=markup, parse_mode="Markdown"
                    )
            except FileNotFoundError:
                bot.send_message(call.message.chat.id, f"❌ Error: `{QR_IMAGE_PATH}` file aapki script ke sath nahi mili!")

    elif call.data == "payment_done":
        bot.answer_callback_query(call.id, "Verifying payment... Please wait!", show_alert=True)

# Run Bot
bot.infinity_polling()
                
