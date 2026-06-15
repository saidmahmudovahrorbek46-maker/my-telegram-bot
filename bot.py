import telebot, random, os, json, datetime

# ⚠️ Telegram Bot Token
bot = telebot.TeleBot("8992035812:AAE0rGeTagE0CaxnjkiSyV3ZdgAgH6vlsTw")
ADMIN_ID = 7523074495  
user_sessions = {}
DB_FILE = "bot_users.json"

# LUG'ATLAR VA MA'LUMOTLAR BAZASI
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
    if uid not in db:
        db[uid] = {"name": first_name, "points": 0, "streak": 0, "last_seen": ""}
    db[uid]["name"] = first_name
    if points_to_add > 0:
        db[uid]["points"] += points_to_add
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
    {"kanji": "木", "reading": "き", "meaning": "daraxt", "image_path": "kanji_images/daraxt.png"}
]

words_list = [
    {"jp": "あさ", "uz": "ertalab", "level": "N5"},
    {"jp": "いぬ", "uz": "it", "level": "N5"},
    {"jp": "みせ", "uz": "do'kon", "level": "N5"},
    {"jp": "ともだち", "uz": "do'st", "level": "N5"},
    {"jp": "しけん", "uz": "imtihon", "level": "N4"}
]

# 🔊 CHOUKAI (TINGLASH) TESTLARI UCHUN AUDIOLAR RO'YXATI
# Ovozli fayllarni kompyuterda choukai_audios/ papkasiga joylashingiz kerak
choukai_list = [
    {"audio_path": "choukai_audios/audio1.mp3", "uz": "Kino ko'rish", "level": "N4"},
    {"audio_path": "choukai_audios/audio2.mp3", "uz": "Vokzalga borish", "level": "N4"},
    {"audio_path": "choukai_audios/audio3.mp3", "uz": "Do'stini kutish", "level": "N4"},
    {"audio_path": "choukai_audios/audio4.mp3", "uz": "Dars tayyorlash", "level": "N5"},
    {"audio_path": "choukai_audios/audio5.mp3", "uz": "Kitob sotib olish", "level": "N5"}
]

def main_menu_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("📊 Kanji Test", "📝 So'z Test (N4/N5)")
    markup.row("🔊 Choukai (Audioli) Test")
    markup.row("🏆 Reyting (Top-10)", "👤 Shaxsiy Profil")
    markup.row("❓ Adminga murojaat")
    return markup
@bot.message_handler(commands=['start'])
def start(m):
    user_data = update_user_stats(m.chat.id, m.from_user.first_name, check_streak=True)
    db = load_db()
    sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(m.chat.id)), 999)
    title = get_rank_title(user_place)
    
    welcome_text = (
        f"🎌 <b>JLPT N4/N5 Professional Test Bot v17.0</b>\n\n"
        f"👤 Foydalanuvchi: <b>{m.from_user.first_name}</b>\n"
        f"🔥 Faollik zanjiri: <b>{user_data['streak']} kun</b>\n"
        f"🏆 Jami ballar: <b>{user_data['points']} ball</b>\n"
        f"🏛️ Shohona mavqe: <b>{title} (Mavqeda {user_place}-o'rin)</b>\n\n"
        f"<i>Tayyor bo'lsangiz, quyidagi tugmalardan birini tanlang va testni boshlang:</i>"
    )
    bot.send_message(m.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu_keyboard())

def ask_test_count(chat_id, mode):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("5", "10", "15", "20")
    m = bot.send_message(chat_id, "📊 Nechta test yechmoqchisiz?", reply_markup=markup)
    bot.register_next_step_handler(m, lambda msg: start_quiz_session(msg, mode))

def start_quiz_session(m, mode):
    try: total = int(m.text.strip())
    except: total = 5
    if mode == "kanji": base = kanji_list
    elif mode == "word": base = words_list
    else: base = choukai_list
    
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
        
        # 📊 AVTOMATIK REYTING VA TARTIBLI DIZAYN
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(chat_id)), 999)
        
        leaderboard = "🏆 <b>YAKUNIY JONLI REYTING (TOP-10)</b>\n"
        leaderboard += "—" * 20 + "\n"
        for idx, (uid, uinfo) in enumerate(sorted_users[:10]):
            place = idx + 1
            lvl = get_rank_title(place)
            leaderboard += f"{place:02d}. {lvl:<12} | <b>{uinfo.get('name', 'User'):<12}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
        leaderboard += "—" * 20 + "\n"
        
        bot.send_message(
            chat_id, 
            f"🎉 <b>Test yakunlandi!</b>\n✅ To'g'ri javoblar: <b>{s['correct_count']}/{s['total']} ta</b>\n💰 Bonus: <b>+{earned_points} ball</b>\n"
            f"📈 Sizning joriy o'rningiz: <b>{user_place}-o'rin</b>\n\n" + leaderboard, 
            parse_mode="HTML", 
            reply_markup=main_menu_keyboard()
        )
        del user_sessions[chat_id]; return

    item = s["questions"][s["current_index"]]
    if s["type"] == "kanji":
        ok = f"{item['reading']} - {item['meaning']}"
        wr = [f"{k['reading']} - {k['meaning']}" for k in kanji_list if k["kanji"] != item["kanji"]]
    elif s["type"] == "word":
        ok = item['uz']
        wr = [w['uz'] for w in words_list if w['jp'] != item['jp']]
    else:
        ok = item['uz']
        wr = [c['uz'] for c in choukai_list if c['audio_path'] != item['audio_path']]

    opts = random.sample(wr, min(3, len(wr))) + [ok]
    random.shuffle(opts)
    s["correct_string"] = ok
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in opts: markup.add(option)

    if s["type"] == "kanji":
        if os.path.exists(item["image_path"]):
            with open(item["image_path"], 'rb') as f:
                bot.send_photo(chat_id, f, caption=f"📝 <b>Kanji {s['current_index']+1}/{s['total']}:</b>\nTo'g'ri javobni tanlang:", parse_mode="HTML", reply_markup=markup)
        else:
            bot.send_message(chat_id, f"📝 <b>Kanji {s['current_index']+1}/{s['total']}:</b>\n🎯 Kanji: <b>{item['kanji']}</b>\n\nTo'g'ri javobni tanlang:", parse_mode="HTML", reply_markup=markup)
    elif s["type"] == "word":
        bot.send_message(chat_id, f"📝 <b>So'z {s['current_index']+1}/{s['total']} ({item['level']}):</b>\n\n🇯🇵 Yaponcha: <b>{item['jp']}</b>\n\nTarjimasini tanlang:", parse_mode="HTML", reply_markup=markup)
    else:
        # 🔊 AUDIO YUBORISH QISMI
        if os.path.exists(item["audio_path"]):
            with open(item["audio_path"], 'rb') as audio:
                bot.send_audio(chat_id, audio, caption=f"🔊 <b>Choukai {s['current_index']+1}/{s['total']} ({item['level']}):</b>\nAudioni eshiting va to'g'ri javobni tanlang:", parse_mode="HTML", reply_markup=markup)
        else:
            bot.send_message(chat_id, f"🔊 <b>Choukai {s['current_index']+1}/{s['total']}:</b>\n⚠️ Audio topilmadi (Fayl qo'yilmagan).\nTo'g'ri javob: {ok}", reply_markup=markup)

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message)
def admin_reply(m):
    try:
        uid = m.reply_to_message.forward_from.id if m.reply_to_message.forward_from else int(m.reply_to_message.text.split("ID: ").split("\n").strip())
        bot.copy_message(uid, ADMIN_ID, m.message_id)
        bot.send_message(ADMIN_ID, "✅ Yuborildi.")
    except Exception as e: bot.send_message(ADMIN_ID, f"❌ Xato: {e}")

@bot.message_handler(func=lambda m: True)
def handle_messages(m):
    cid, txt = m.chat.id, m.text.strip()
    if txt == "📊 Kanji Test": ask_test_count(cid, "kanji"); return
    if txt == "📝 So'z Test (N4/N5)": ask_test_count(cid, "word"); return
    if txt == "🔊 Choukai (Audioli) Test": ask_test_count(cid, "choukai"); return
    
    if txt == "🏆 Reyting (Top-10)" or txt == "👤 Shaxsiy Profil":
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(cid)), 999)

        if txt == "🏆 Reyting (Top-10)":
            output = "🏆 <b>JONLI REYTING JADVALI (SAROY)</b>\n"
            output += "—" * 20 + "\n"
            for idx, (uid, uinfo) in enumerate(sorted_users[:10]):
                place = idx + 1
                lvl = get_rank_title(place)
                output += f"{place:02d}. {lvl:<12} | <b>{uinfo.get('name', 'User'):<12}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
            output += "—" * 20 + "\n"
            output += f"📈 Sizning o'rningiz: <b>{user_place}-o'rin</b>"
            bot.send_message(cid, output, parse_mode="HTML", reply_markup=main_menu_keyboard()); return
            
        if txt == "👤 Shaxsiy Profil":
            u = db.get(str(cid), {"name": m.from_user.first_name, "points": 0, "streak": 0})
            rank_title = get_rank_title(user_place)
            
            output = (
                f"👤 <b>SIZNING SHAXSIY PROFILINGIZ:</b>\n"
                f"—" * 20 + "\n"
                f"• Ismingiz: <b>{u['name']}</b>\n"
                f"• Jami ballar: <code>{u['points']} ball</code>\n"
                f"• Faollik zanjiri: <b>{u['streak']} kun</b>\n"
                f"• Joriy mavqeingiz: <b>{rank_title} ({user_place}-o'rin)</b>\n"
                f"—" * 20 + "\n"
            )
            bot.send_message(cid, output, parse_mode="HTML", reply_markup=main_menu_keyboard()); return
        
    if txt == "❓ Adminga murojaat":
        bot.send_message(cid, "✉️ Xabaringizni kiriting:", reply_markup=main_menu_keyboard()); return

    if cid in user_sessions:
        s = user_sessions[cid]
        if txt == s["correct_string"]:
            s["correct_count"] += 1; bot.send_message(cid, "✅ To‘g‘ri!")
        else: bot.send_message(cid, f"❌ Noto‘g‘ri!\nJavob: <b>{s['correct_string']}</b>", parse_mode="HTML")
        s["current_index"] += 1; send_next_question(cid); return

    if cid != ADMIN_ID:
        bot.forward_message(ADMIN_ID, cid, m.message_id)
        bot.send_message(ADMIN_ID, f"📩 <b>Xabar!</b>\nUser ID: {cid}\n\nJavob uchun <b>Reply</b> qiling.", parse_mode="HTML")
        bot.send_message(cid, "⏱ Xabaringiz adminga yetkazildi.")

bot.remove_webhook()
bot.infinity_polling()
