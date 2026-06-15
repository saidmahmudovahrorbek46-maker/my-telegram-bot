import telebot, random, os, json, datetime

bot = telebot.TeleBot("8992035812:AAEkWKoCH1hviSDEnLdEMOoaT6D60L0MVts")
ADMIN_ID = 7523074495  
user_sessions, DB_FILE = {}, "bot_users.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_db(db):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def update_user_stats(user_id, first_name, points_to_add=0, check_streak=False):
    db = load_db()
    uid = str(user_id)
    today = str(datetime.date.today())
    if uid not in db: db[uid] = {"name": first_name, "points": 0, "streak": 0, "last_seen": ""}
    db[uid]["name"] = first_name
    if points_to_add > 0: db[uid]["points"] += points_to_add
    if check_streak:
        last_seen = db[uid]["last_seen"]
        if last_seen != today:
            yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
            db[uid]["streak"] = db[uid]["streak"] + 1 if last_seen == yesterday else 1
            db[uid]["last_seen"] = today
    save_db(db)
    return db[uid]

def get_rank_title(place):
    if place == 1: return "👑 Qirol"
    elif place == 2: return "📜 Vazir"
    elif place <= 4: return "⚔️ Amir"
    elif place <= 6: return "🛡️ Sohibqiron"
    return "👨‍🌾 Fuqaro"

kanji_list = [
    {"kanji": "日", "reading": "ひ", "meaning": "kun", "image_path": "kanji_images/kun.png"},
    {"kanji": "月", "reading": "つき", "meaning": "oy", "image_path": "kanji_images/oy.png"},
    {"kanji": "火", "reading": "ひ", "meaning": "olov", "image_path": "kanji_images/olov.png"},
    {"kanji": "水", "reading": "みず", "meaning": "suv", "image_path": "kanji_images/suv.png"},
    {"kanji": "木", "reading": "き", "meaning": "daraxt", "image_path": "kanji_images/daraxt.png"},
    {"kanji": "金", "reading": "かね", "meaning": "oltin", "image_path": "kanji_images/oltin.png"},
    {"kanji": "土", "reading": "つち", "meaning": "yer", "image_path": "kanji_images/yer.png"},
    {"kanji": "人", "reading": "ひと", "meaning": "inson", "image_path": "kanji_images/inson.png"},
    {"kanji": "学", "reading": "まなぶ", "meaning": "ilm", "image_path": "kanji_images/ilm.png"},
    {"kanji": "校", "reading": "こう", "meaning": "maktab", "image_path": "kanji_images/maktab.png"}
]

words_list = [
    {"jp": "あさ", "uz": "ertalab"}, {"jp": "いぬ", "uz": "it"},
    {"jp": "みせ", "uz": "do'kon"}, {"jp": "ともだち", "uz": "do'st"},
    {"jp": "しけん", "uz": "imtihon"}, {"jp": "あんぜん", "uz": "xavfsiz"}
]

def main_menu_keyboard():
    return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add("📊 Kanji Test", "📝 So'z Test (N4/N5)").add("🏆 Reyting (Top-10)", "👤 Shaxsiy Profil").add("❓ Adminga murojaat")

@bot.message_handler(commands=['stats'], func=lambda m: m.chat.id == ADMIN_ID)
def get_bot_stats(m):
    db = load_db()
    total_users = len(db)
    bonus = f"🏆 Top xodim: {max(db.values(), key=lambda x: x.get('points', 0))['name']}" if total_users > 0 else ""
    bot.send_message(ADMIN_ID, f"📊 Jami foydalanuvchilar: <b>{total_users} ta odam</b>\n{bonus}", parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(m):
    user_data = update_user_stats(m.chat.id, m.from_user.first_name, check_streak=True)
    db = load_db()
    sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(m.chat.id)), 999)
    welcome_text = f"🎌 <b>JLPT Bot v21.5</b>\n\n🔥 Faollik: <b>{user_data['streak']} kun</b>\n🏆 Ballar: <b>{user_data['points']} ball</b>\n🏛️ O'rin: <b>{user_place}-o'rin</b>"
    bot.send_message(m.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu_keyboard())

def ask_test_count(chat_id, mode):
    m = bot.send_message(chat_id, "📊 Nechta test yechasiz?", reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("5", "10", "15"))
    bot.register_next_step_handler(m, lambda msg: start_quiz_session(msg, mode))

def start_quiz_session(m, mode):
    try: total = int(m.text.strip())
    except: total = 5
    base = kanji_list if mode == "kanji" else words_list
    user_sessions[m.chat.id] = {"questions": random.sample(base, min(total, len(base))), "current_index": 0, "correct_count": 0, "total": min(total, len(base)), "type": mode}
    send_next_question(m.chat.id)

def send_next_question(chat_id):
    s = user_sessions.get(chat_id)
    if not s: return
    if s["current_index"] >= s["total"]:
        earned_points = s["correct_count"] * 10
        db = load_db()
        name = db.get(str(chat_id), {}).get("name", "Foydalanuvchi")
        update_user_stats(chat_id, name, points_to_add=earned_points)
        bot.send_message(chat_id, f"🎉 Test yakunlandi! Natijangiz: {s['correct_count']}/{s['total']}\n💰 Bonus: +{earned_points} ball", reply_markup=main_menu_keyboard())
        if chat_id in user_sessions: del user_sessions[chat_id]
        return

    item = s["questions"][s["current_index"]]
    if s["type"] == "kanji":
        question_text = f"🎯 Kanjining o'qilishi va ma'nosini belgilang:\n🔥 Kanji: <b>{item['kanji']}</b>"
        ok = f"{item['reading']} - {item['meaning']}"
        wr = [f"{k['reading']} - {k['meaning']}" for k in kanji_list if k["kanji"] != item["kanji"]]
    else:
        question_text = f"📝 To'g'ri o'zbekcha tarjimani belgilang:\n🇯🇵 Yaponcha: <b>「{item['jp']}」</b>"
        ok = item['uz']
        wr = [w['uz'] for w in words_list if w['jp'] != item['jp']]

    opts = random.sample(wr, min(3, len(wr))) + [ok]
    random.shuffle(opts)
    s["correct_string"] = ok
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in opts: markup.add(option)

    if s["type"] == "kanji" and os.path.exists(item["image_path"]):
        with open(item["image_path"], 'rb') as f: bot.send_photo(chat_id, f, caption=question_text, parse_mode="HTML", reply_markup=markup)
    else: bot.send_message(chat_id, question_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message)
def admin_reply(m):
    try:
        if m.reply_to_message.forward_from: uid = m.reply_to_message.forward_from.id
        else:
            lines = m.reply_to_message.text.split("\n")
            id_line = [l for l in lines if "User ID:" in l][0]
            uid = int(id_line.split("User ID:")[1].strip())
        bot.copy_message(uid, ADMIN_ID, m.message_id)
        bot.send_message(ADMIN_ID, "✅ Yuborildi.")
    except Exception as e: bot.send_message(ADMIN_ID, f"❌ Xato: {e}")

@bot.message_handler(func=lambda m: True)
def handle_messages(m):
    cid, txt = m.chat.id, m.text.strip() if m.text else ""
    if txt == "📊 Kanji Test": ask_test_count(cid, "kanji"); return
    if txt == "📝 So'z Test (N4/N5)": ask_test_count(cid, "word"); return
    if txt in ["🏆 Reyting (Top-10)", "👤 Shaxsiy Profil"]:
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(cid)), 999)
        if txt == "🏆 Reyting (Top-10)":
            output = "🏆 TOP-10 REYTING\n" + "\n".join([f"{i+1}. {u[1].get('name')} | {u[1].get('points')} ball" for i, u in enumerate(sorted_users[:10])])
            bot.send_message(cid, output, reply_markup=main_menu_keyboard()); return
        if txt == "👤 Shaxsiy Profil":
            u = db.get(str(cid), {"name": m.from_user.first_name, "points": 0, "streak": 0})
            bot.send_message(cid, f"👤 Profil:\n• Ism: {u['name']}\n• Ball: {u['points']}\n• O'rin: {user_place}", reply_markup=main_menu_keyboard()); return
    if txt == "❓ Adminga murojaat":
        bot.send_message(cid, "✉️ Xabaringizni kiriting:", reply_markup=main_menu_keyboard()); return

    if cid in user_sessions:
        s = user_sessions[cid]
        if txt in ["📊 Kanji Test", "📝 So'z Test (N4/N5)", "🏆 Reyting (Top-10)", "👤 Shaxsiy Profil", "❓ Adminga murojaat"]:
            bot.send_message(cid, "⚠️ Iltimos, avval testni yakunlang!")
            send_next_question(cid); return
        if txt == s["correct_string"]:  bot.send_message(cid, "✅ To‘g‘ri!")
        else: bot.send_message(cid, f"❌ Noto‘g‘ri! Javob: {s['correct_string']}")
        s["current_index"] += 1
        send_next_question(cid); return

    if cid != ADMIN_ID:
        bot.forward_message(ADMIN_ID, cid, m.message_id)
        bot.send_message(ADMIN_ID, f"📩 Yangi xabar!\nUser ID: {cid}\nJavob berish uchun Reply qiling.")
        bot.send_message(cid, "⏱ Xabaringiz adminga yetkazildi.")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
