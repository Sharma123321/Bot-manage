import json
import os
import threading
import time

import telebot
from telebot import types

TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(TOKEN)

BASE_DIR = os.path.dirname(__file__)
QR_IMAGE_PATH = os.path.join(BASE_DIR, "upi_qr.jpg")
DEVICES_JSON_PATH = os.path.join(BASE_DIR, "devices.json")
MODELS_PER_PAGE = 8



def load_device_data():
    with open(DEVICES_JSON_PATH, "r") as file:
        return json.load(file)


def main_menu_markup():
    markup = types.InlineKeyboardMarkup(row_width=1)
    opt1 = types.InlineKeyboardButton("📲 Root App (₹50)", callback_data="main_root_app")
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
    "non_root_primehook": (
        "🔑 **PRIMEHOOK KEY**\n\n"
        "1 DAY  - ₹70\n"
        "3 DAY  - ₹160\n"
        "7 DAY  - ₹280\n"
        "15 DAY - ₹450\n"
        "30 DAY - ₹700"
    ),
    "non_root_drip_client": (
        "🔹 **DRIP CLIENT KEY**\n\n"
        "1 DAY  - ₹60\n"
        "3 DAY  - ₹140\n"
        "7 DAY  - ₹260\n"
        "15 DAY - ₹400\n"
        "30 DAY - ₹600"
    ),
    "non_root_drip_proxy": (
        "🔹 **DRIP PROXY KEY**\n\n"
        "1 DAY  - ₹60\n"
        "3 DAY  - ₹140\n"
        "7 DAY  - ₹260\n"
        "15 DAY - ₹400\n"
        "30 DAY - ₹600"
    ),
    "non_root_silent_non_root": (
        "🔹 **SILENT NON ROOT KEY**\n\n"
        "1 DAY  - ₹70\n"
        "3 DAY  - ₹150\n"
        "7 DAY  - ₹270\n"
        "15 DAY - ₹420\n"
        "30 DAY - ₹650"
    ),
    "non_root_hg_client": (
        "🔹 **HG CLIENT KEY**\n\n"
        "1 DAY  - ₹80\n"
        "3 DAY  - ₹180\n"
        "7 DAY  - ₹320\n"
        "15 DAY - ₹500\n"
        "30 DAY - ₹750"
    ),
    "non_root_br_mod": (
        "🔹 **BR MOD NON ROOT KEY**\n\n"
        "1 DAY  - ₹60\n"
        "3 DAY  - ₹140\n"
        "7 DAY  - ₹260\n"
        "15 DAY - ₹400\n"
        "30 DAY - ₹600"
    ),
    "non_root_pati_blue": (
        "🔹 **PATI BLUE KEY**\n\n"
        "1 DAY  - ₹60\n"
        "3 DAY  - ₹130\n"
        "7 DAY  - ₹240\n"
        "15 DAY - ₹380\n"
        "30 DAY - ₹550"
    ),
    "non_root_pato_orange": (
        "🔹 **PATO ORANGE KEY**\n\n"
        "1 DAY  - ₹60\n"
        "3 DAY  - ₹130\n"
        "7 DAY  - ₹240\n"
        "15 DAY - ₹380\n"
        "30 DAY - ₹550"
    ),
}


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



def get_drip_client_markup():
    m=types.InlineKeyboardMarkup(row_width=1)
    for d,a in [("1 DAY - ₹60",60),("3 DAY - ₹140",140),("7 DAY - ₹260",260),("15 DAY - ₹400",400),("30 DAY - ₹600",600)]:
        m.add(types.InlineKeyboardButton(d,callback_data=f"drip_client_plan_{a}"))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m




def get_primehook_markup():
    m=types.InlineKeyboardMarkup(row_width=1)
    for d,a in [("1 DAY - ₹70",70),("3 DAY - ₹160",160),("7 DAY - ₹280",280),("15 DAY - ₹450",450),("30 DAY - ₹700",700)]:
        m.add(types.InlineKeyboardButton(d,callback_data=f"primehook_plan_{a}"))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m

def get_silent_non_root_markup():
    m=types.InlineKeyboardMarkup(row_width=1)
    for d,c in [("1 DAY - ₹70","silent_plan_70"),("3 DAY - ₹150","silent_plan_150"),("7 DAY - ₹270","silent_plan_270"),("15 DAY - ₹420","silent_plan_420"),("30 DAY - ₹650","silent_plan_650")]:
        m.add(types.InlineKeyboardButton(d,callback_data=c))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m

def get_hg_client_markup():
    m=types.InlineKeyboardMarkup(row_width=1)
    
    for d,c in [("1 DAY - ₹80","hg_plan_80"),("3 DAY - ₹180","hg_plan_180"),("7 DAY - ₹320","hg_plan_320"),("15 DAY - ₹500","hg_plan_500"),("30 DAY - ₹750","hg_plan_750")]:
        m.add(types.InlineKeyboardButton(d,callback_data=c))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m

def get_br_mod_markup():
    m=types.InlineKeyboardMarkup(row_width=1)
    for d,c in [("1 DAY - ₹60","brmod_plan_60"),("3 DAY - ₹140","brmod_plan_140"),("7 DAY - ₹260","brmod_plan_260"),("15 DAY - ₹400","brmod_plan_400"),("30 DAY - ₹600","brmod_plan_600")]:
        m.add(types.InlineKeyboardButton(d,callback_data=c))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m


def get_pati_blue_markup():
    m=types.InlineKeyboardMarkup(row_width=1)
    for d,c in [("1 DAY - ₹60","pati_blue_plan_60"),("3 DAY - ₹130","pati_blue_plan_130"),("7 DAY - ₹240","pati_blue_plan_240"),("15 DAY - ₹380","pati_blue_plan_380"),("30 DAY - ₹550","pati_blue_plan_550")]:
        m.add(types.InlineKeyboardButton(d,callback_data=c))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m

def get_drip_proxy_markup():
    m=types.InlineKeyboardMarkup(row_width=1)
    for d,a in [("1 DAY - ₹60",60),("3 DAY - ₹140",140),("7 DAY - ₹260",260),("15 DAY - ₹400",400),("30 DAY - ₹600",600)]:
        m.add(types.InlineKeyboardButton(d,callback_data=f"drip_proxy_plan_{a}"))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m


def get_plan_markup(prefix,prices):
    m=types.InlineKeyboardMarkup(row_width=1)
    for d,a in prices:
        m.add(types.InlineKeyboardButton(d,callback_data=f"{prefix}_plan_{a}"))
    m.add(types.InlineKeyboardButton("↩️ Back",callback_data="main_non_root"))
    return m
PLAN_MAP={
"non_root_primehook":[("1 DAY - ₹70",70),("3 DAY - ₹160",160),("7 DAY - ₹280",280),("15 DAY - ₹450",450),("30 DAY - ₹700",700)],
"non_root_drip_proxy":[("1 DAY - ₹60",60),("3 DAY - ₹140",140),("7 DAY - ₹260",260),("15 DAY - ₹400",400),("30 DAY - ₹600",600)],
"non_root_silent_non_root":[("1 DAY - ₹70",70),("3 DAY - ₹150",150),("7 DAY - ₹270",270),("15 DAY - ₹420",420),("30 DAY - ₹650",650)],
"non_root_hg_client":[("1 DAY - ₹80",80),("3 DAY - ₹180",180),("7 DAY - ₹320",320),("15 DAY - ₹500",500),("30 DAY - ₹750",750)],
"non_root_br_mod":[("1 DAY - ₹60",60),("3 DAY - ₹140",140),("7 DAY - ₹260",260),("15 DAY - ₹400",400),("30 DAY - ₹600",600)],
"non_root_pati_blue":[("1 DAY - ₹60",60),("3 DAY - ₹130",130),("7 DAY - ₹240",240),("15 DAY - ₹380",380),("30 DAY - ₹550",550)],
"non_root_pato_orange":[("1 DAY - ₹60",60),("3 DAY - ₹130",130),("7 DAY - ₹240",240),("15 DAY - ₹380",380),("30 DAY - ₹550",550)],
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


# ----------------------------------------------------
# STEP 1: MAIN SHOP MENU
# ----------------------------------------------------
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


# ----------------------------------------------------
# STEP 2 & 3: CALLBACK HANDLER (CLICK LOGIC)
# ----------------------------------------------------
@bot.callback_query_handler(func=lambda call: True)
def handle_menu_clicks(call):

    # --- ROOT APP: SEEDHA QR AUR ₹100 PAYMENT DETAILS ---
    if call.data == "main_root_app":
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        send_payment_details(call.message.chat.id, "Root App", 100)

    # --- BOOT IMAGE PAR CLICK KARNE PAR BRANDS LIST ---
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

    # --- PAYMENT DONE (STYLISH LIVE TIMER) ---
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

    # --- AINCARD PAR CLICK KARNE PAR AINCARD MENU ---
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

    # --- AINCARD KEY ---
    elif call.data == "aincard_key":
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        send_payment_details(call.message.chat.id, "Aincard Key", 20)

    # --- AINCARD KEY APP ---
    elif call.data == "aincard_key_app":
        bot.answer_callback_query(call.id)
        try:
            bot.delete_message(call.message.chat.id, call.message.message_id)
        except Exception:
            pass
        send_payment_details(call.message.chat.id, "Aincard Key App", 100)

    # --- NON ROOT PANEL MENU ---
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

    elif call.data=="non_root_drip_client":
        try:
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔹 **DRIP CLIENT**\n\nSelect a plan:",reply_markup=get_drip_client_markup(),parse_mode="Markdown")
        except Exception:
            bot.send_message(call.message.chat.id,"🔹 **DRIP CLIENT**\n\nSelect a plan:",reply_markup=get_drip_client_markup(),parse_mode="Markdown")
    elif call.data.startswith("drip_client_plan_"):
        amount=int(call.data.split("_")[-1]);send_payment_details(call.message.chat.id,"DRIP CLIENT",amount)
    # --- NON ROOT PANEL ITEMS ---
    elif call.data=="non_root_silent_non_root":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔹 **SILENT NON ROOT**\n\nSelect a plan:",reply_markup=get_silent_non_root_markup(),parse_mode="Markdown")
    elif call.data.startswith("silent_plan_"):
        send_payment_details(call.message.chat.id,"SILENT NON ROOT",int(call.data.split("_")[-1]))
    elif call.data=="non_root_drip_proxy":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔹 **DRIP PROXY**\n\nSelect a plan:",reply_markup=get_drip_proxy_markup(),parse_mode="Markdown")
    elif call.data.startswith("drip_proxy_plan_"):
        amount=int(call.data.split("_")[-1]);send_payment_details(call.message.chat.id,"DRIP PROXY",amount)
    elif call.data=="non_root_hg_client":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔹 **HG CLIENT**\n\nSelect a plan:",reply_markup=get_hg_client_markup(),parse_mode="Markdown")
    elif call.data.startswith("hg_plan_"):
        send_payment_details(call.message.chat.id,"HG CLIENT",int(call.data.split("_")[-1]))
    elif call.data=="non_root_br_mod":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔹 **BR MOD NON ROOT**\n\nSelect a plan:",reply_markup=get_br_mod_markup(),parse_mode="Markdown")
    elif call.data.startswith("brmod_plan_"):
        send_payment_details(call.message.chat.id,"BR MOD NON ROOT",int(call.data.split("_")[-1]))
    elif call.data=="non_root_pati_blue":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔹 **PATI BLUE**\n\nSelect a plan:",reply_markup=get_pati_blue_markup(),parse_mode="Markdown")
    elif call.data.startswith("pati_blue_plan_"):
        send_payment_details(call.message.chat.id,"PATI BLUE",int(call.data.split("_")[-1]))
    elif call.data=="non_root_primehook":
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔑 **PRIMEHOOK**\n\nSelect a plan:",reply_markup=get_primehook_markup(),parse_mode="Markdown")
    elif call.data.startswith("primehook_plan_"):
        amount=int(call.data.split("_")[-1]);send_payment_details(call.message.chat.id,"PRIMEHOOK",amount)
    elif call.data.startswith("non_root_"):
        bot.answer_callback_query(call.id)
        plan_text=NON_ROOT_PLANS.get(call.data)
        if plan_text: bot.send_message(call.message.chat.id,plan_text,parse_mode="Markdown")


    elif call.data=="non_root_drip_client":
        try:
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="🔹 **DRIP CLIENT**\n\nSelect a plan:",reply_markup=get_drip_client_markup(),parse_mode="Markdown")
        except Exception:
            bot.send_message(call.message.chat.id,"🔹 **DRIP CLIENT**\n\nSelect a plan:",reply_markup=get_drip_client_markup(),parse_mode="Markdown")
    elif call.data.startswith("drip_client_plan_"):
        amount=int(call.data.split("_")[-1]);send_payment_details(call.message.chat.id,"DRIP CLIENT",amount)
    # --- NON ROOT PANEL ITEMS ---
    elif call.data.startswith("non_root_"):
        bot.answer_callback_query(call.id)
        plan_text=NON_ROOT_PLANS.get(call.data)
        if plan_text: bot.send_message(call.message.chat.id,plan_text,parse_mode="Markdown")


    
    elif call.data in PLAN_MAP:
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,text="Select a plan:",reply_markup=get_plan_markup(call.data,PLAN_MAP[call.data]),parse_mode="Markdown")
    elif "_plan_" in call.data and not call.data.startswith("drip_client"):
        parts=call.data.split("_plan_"); key=parts[0]; amt=int(parts[1]); send_payment_details(call.message.chat.id,key.replace("non_root_","").replace("_"," ").upper(),amt)
# --- BRAND SELECT HUA YA PAGE BADLA (Format: brand_<brandId>_<page>) ---
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
        row=[]
        for model_id, model_info in current_page_models:
            row.append(types.InlineKeyboardButton(model_info["name"], callback_data=f"model_{brand_id}_{model_id}"))
            if len(row)==2:
                markup.row(*row); row=[]
        if row: markup.row(*row)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id,
            text=f"Selected: **{brand_name}** (Page {page+1})\n\n👇 Apna model select karein:",
            reply_markup=markup,parse_mode="Markdown")

    elif call.data.startswith("model_"):
        device_data=load_device_data()
        _,brand_id,model_id=call.data.split("_",2)
        try:
            model_info=device_data[brand_id]["models"][model_id]
            qr_path = QR_IMAGE_PATH
            markup=types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("↩️ Back to Shop",callback_data="back_to_shop_clean"))
            with open(qr_path,"rb") as photo:
                bot.send_photo(call.message.chat.id,photo=photo,caption=model_info["text"],reply_markup=markup,parse_mode="Markdown")
        except Exception:
            bot.answer_callback_query(call.id,text="⚠️ QR Code file nahi mili!",show_alert=True)

    # --- WAPAS BRANDS LIST PAR JAANE KE LIYE ---
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

    # --- WAPAS MAIN MENU PAR JAANE KE LIYE ---
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
                
