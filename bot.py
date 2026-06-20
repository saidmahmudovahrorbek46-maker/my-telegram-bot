import telebot
import random
import os
import json
import datetime

# Bot sozlamalari
bot = telebot.TeleBot("8992035812:AAEkWKoCH1hviSDEnLdEMOoaT6D60L0MVts")
ADMIN_ID = 7523074495  
user_sessions = {}
DB_FILE = "bot_users.json"

# Sohta odamlar ro'yxati va ismlari
FAKE_USERS_DATA = [
    {"id": "fake_1", "name": "Akira_Kun", "points": 120, "streak": 5, "last_seen": "", "is_fake": True},
    {"id": "fake_2", "name": "Madina_N5", "points": 90, "streak": 3, "last_seen": "", "is_fake": True},
    {"id": "fake_3", "name": "Bekzod_Sensei", "points": 150, "streak": 7, "last_seen": "", "is_fake": True},
    {"id": "fake_4", "name": "Sakura_chan", "points": 60, "streak": 2, "last_seen": "", "is_fake": True},
    {"id": "fake_5", "name": "Hiroshi", "points": 210, "streak": 12, "last_seen": "", "is_fake": True},
    {"id": "fake_6", "name": "Asliddin_JLPT", "points": 180, "streak": 8, "last_seen": "", "is_fake": True},
    {"id": "fake_7", "name": "Yuki_99", "points": 40, "streak": 1, "last_seen": "", "is_fake": True},
    {"id": "fake_8", "name": "Jasur_Tokyo", "points": 130, "streak": 4, "last_seen": "", "is_fake": True},
    {"id": "fake_9", "name": "Kenji_San", "points": 170, "streak": 6, "last_seen": "", "is_fake": True},
    {"id": "fake_10", "name": "Dilnoza_Kanjis", "points": 110, "streak": 3, "last_seen": "", "is_fake": True}
]

def load_db():
    db = {}
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            try: 
                db = json.load(f)
            except: 
                db = {}
    
    # Agar bazada sohta odamlar bo'lmasa, ularni qo'shish
    updated = False
    for fake in FAKE_USERS_DATA:
        if fake["id"] not in db:
            db[fake["id"]] = {
                "name": fake["name"],
                "points": fake["points"],
                "streak": fake["streak"],
                "last_seen": fake["last_seen"],
                "is_fake": True
            }
            updated = True
    if updated:
        save_db(db)
    return db

def save_db(db):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db, f, ensure_ascii=False, indent=4)

def update_user_stats(user_id, first_name, points_to_add=0, check_streak=False):
    db = load_db()
    uid = str(user_id)
    today = str(datetime.date.today())
    if uid not in db:
        db[uid] = {"name": first_name, "points": 0, "streak": 0, "last_seen": "", "is_fake": False}
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

def update_fake_users_progress(user_id):
    """Foydalanuvchi test yechganda sohta odamlarning ballarini ham biroz oshirish"""
    db = load_db()
    user_points = db.get(str(user_id), {}).get("points", 0)
    
    for uid, uinfo in db.items():
        if uinfo.get("is_fake", False):
            # Sohta foydalanuvchilar faolligini oshirish (+10 dan +50 ballgacha tasodifiy)
            uinfo["points"] += random.choice([10, 20, 30, 40, 50])
            
            # Agar eng kuchli sohta foydalanuvchi odamdan ortda bo'lsa, uni sun'iy ravishda foydalanuvchidan biroz oldinga o'tkazish
            if uinfo["points"] < user_points and random.random() < 0.3:
                uinfo["points"] = user_points + random.randint(10, 40)
    save_db(db)

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
    {"kanji": "校", "reading": "こう", "meaning": "maktab", "image_path": "kanji_images/maktab.png"},
    {"kanji": "先", "reading": "さき", "meaning": "avval", "image_path": "kanji_images/avval.png"},
    {"kanji": "生", "reading": "きる", "meaning": "hayot", "image_path": "kanji_images/hayot.png"},
    {"kanji": "高", "reading": "たかい", "meaning": "baland", "image_path": "kanji_images/baland.png"},
    {"kanji": "車", "reading": "くるま", "meaning": "mashina", "image_path": "kanji_images/mashina.png"},
    {"kanji": "国", "reading": "くに", "meaning": "davlat", "image_path": "kanji_images/davlat.png"},
    {"kanji": "語", "reading": "ご", "meaning": "til", "image_path": "kanji_images/til.png"},
    {"kanji": "何", "reading": "なに", "meaning": "nima", "image_path": "kanji_images/nima.png"},
    {"kanji": "時", "reading": "とき", "meaning": "vaqt", "image_path": "kanji_images/vaqt.png"},
    {"kanji": "分", "reading": "わける", "meaning": "daqiqa", "image_path": "kanji_images/daqiqa.png"},
    {"kanji": "間", "reading": "あいだ", "meaning": "oraliq", "image_path": "kanji_images/oraliq.png"},
    {"kanji": "会", "reading": "あう", "meaning": "uchrashuv", "image_path": "kanji_images/uchrashuv.png"},
    {"kanji": "社", "reading": "やしろ", "meaning": "jamiyat", "image_path": "kanji_images/jamiyat.png"},
    {"kanji": "場", "reading": "ばしょ", "meaning": "joy", "image_path": "kanji_images/joy.png"},
    {"kanji": "自", "reading": "みずkara", "meaning": "o'zi", "image_path": "kanji_images/ozi.png"},
    {"kanji": "動", "reading": "うgoく", "meaning": "harakat", "image_path": "kanji_images/harakat.png"},
    {"kanji": "持", "reading": "moつ", "meaning": "ushlamoq", "image_path": "kanji_images/ushlamoq.png"},
    {"kanji": "新", "reading": "あたらしい", "meaning": "yangi", "image_path": "kanji_images/yangi.png"},
    {"kanji": "古", "reading": "ふるい", "meaning": "eski", "image_path": "kanji_images/eski.png"},
    {"kanji": "駅", "reading": "えき", "meaning": "vokzal", "image_path": "kanji_images/vokzal.png"},
    {"kanji": "力", "reading": "ちkara", "meaning": "kuch", "image_path": "kanji_images/kuch.png"}
]

words_list = [
    {"jp": "こんにちは", "uz": "salom", "level": "N5"}, {"jp": "おはようございます", "uz": "ertalab", "level": "N5"},
    {"jp": "こんばんは", "uz": "axshom salom", "level": "N5"}, {"jp": "おやすみなさい", "uz": "yaxshi uxla", "level": "N5"},
    {"jp": "さようなら", "uz": "xayr", "level": "N5"}, {"jp": "じゃあね", "uz": "shu vaqtingacha", "level": "N5"},
    {"jp": "ありがとう", "uz": "rahmat", "level": "N5"}, {"jp": "どうぞ", "uz": "iltimos", "level": "N5"},
    {"jp": "すみません", "uz": "kechirasiz", "level": "N5"}, {"jp": "おつかれさまです", "uz": "hastalik uchun rahmat", "level": "N5"},
    {"jp": "あかい", "uz": "qizil", "level": "N5"}, {"jp": "あおい", "uz": "ko'k", "level": "N5"},
    {"jp": "きいろい", "uz": "sariq", "level": "N5"}, {"jp": "くろい", "uz": "qora", "level": "N5"},
    {"jp": "しろい", "uz": "oq", "level": "N5"}, {"jp": "みどりいろ", "uz": "yashil", "level": "N5"},
    {"jp": "あさ", "uz": "ertalab", "level": "N5"}, {"jp": "いぬ", "uz": "it", "level": "N5"},
    {"jp": "みせ", "uz": "do'kon", "level": "N5"}, {"jp": "ともだち", "uz": "do'st", "level": "N5"}
]

def main_menu_keyboard(user_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Kanji Test", "📝 So'z Test (N4/N5)")
    markup.add("🏆 Reyting (Top-10)", "👤 Shaxsiy Profil")
    markup.add("❓ Adminga murojaat")
    if user_id == ADMIN_ID:
        markup.add("📊 Admin: Statistika", "📣 Admin: Xabar Yuborish")
    return markup

@bot.message_handler(commands=['stats'], func=lambda m: m.chat.id == ADMIN_ID)
def get_bot_stats(m):
    db = load_db()
    total_users = len([x for x in db.values() if not x.get("is_fake", False)])
    total_fakes = len([x for x in db.values() if x.get("is_fake", False)])
    
    if len(db) > 0:
        top_user = max(db.values(), key=lambda x: x.get("points", 0))
        top_name = top_user.get("name", "Noma'lum")
        top_points = top_user.get("points", 0)
        bonus_text = f"🏆 Eng ko'p ball to'plagan: <b>{top_name}</b> ({top_points} ball)"
    else:
        bonus_text = "🚫 Hozircha foydalanuvchilar yo'q."

    text = f"📊 <b>Bot Statistikasi:</b>\n\n👥 Haqiqiy foydalanuvchilar: <b>{total_users} ta</b>\n🤖 Tizimdagi botlar: <b>{total_fakes} ta</b>\n{bonus_text}"
    bot.send_message(ADMIN_ID, text, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(m):
    user_data = update_user_stats(m.chat.id, m.from_user.first_name, check_streak=True)
    db = load_db()
    sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(m.chat.id)), 999)
    
    welcome_text = (
        f"🎌 <b>JLPT N4/N5 Barqaror Test Bot v21.5</b>\n\n"
        f"🔥 Kunlik faollik: <b>{user_data['streak']} kun</b>\n"
        f"🏆 Jami ballar: <b>{user_data['points']} ball</b>\n"
        f"🏛️ Mavqeingiz: <b>{get_rank_title(user_place)} ({user_place}-o'rin)</b>\n\n"
        f"<i>Quyidagi tugmalardan birini tanlang va testni boshlang:</i>"
    )
    bot.send_message(m.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu_keyboard(m.chat.id))

def ask_test_count(chat_id, mode):
    m = bot.send_message(chat_id, "📊 Nechta test yechasiz?", reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("5", "10", "15", "20"))
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
        
        # Test tugagach foydalanuvchiga ball berish va sohta foydalanuvchilarni ham o'stirish
        update_user_stats(chat_id, name, points_to_add=earned_points)
        update_fake_users_progress(chat_id)
        
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(chat_id)), 999)
        
        leaderboard = "🏆 <b>SHOHONA REYTING JADVALI (TOP-5):</b>\n====================\n"
        for idx, (uid, uinfo) in enumerate(sorted_users[:5]):
            leaderboard += f"{idx+1}. {get_rank_title(idx+1)} | <b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
        leaderboard += "====================\n"
        
        # Agar foydalanuvchi 1-o'rinda bo'lmasa, motivatsiya beruvchi xabarni qo'shish
        alert_text = ""
        if user_place > 1:
            leader_name = sorted_users[0][1].get("name")
            alert_text = f"\n⚠️ <b>Ogohlantirish:</b> Sizni reytingda quvib o'tishdi! Hozirda 1-o'rinni <b>{leader_name}</b> egallab turibdi. Tezroq test yechib o'zib keting! 🔥\n"

        bot.send_message(
            chat_id, 
            f"🎉 <b>Test yakunlandi!</b>\n✅ Natijangiz: <b>{s['correct_count']}/{s['total']} ta</b>\n💰 Bonus: <b>+{earned_points} ball</b>\n"
            f"📈 Joriy o'rningiz: <b>{user_place}-o'rin</b>\n" + alert_text + "\n" + leaderboard, 
            parse_mode="HTML", 
            reply_markup=main_menu_keyboard(chat_id)
        )
        if chat_id in user_sessions: del user_sessions[chat_id]
        return

    item = s["questions"][s["current_index"]]
    if s["type"] == "kanji":
        question_text = f"🎯 [Savol {s['current_index']+1}/{s['total']}] Ushbu Kanjining to'g'ri o'qilishi va ma'nosini belgilang:\n\n🔥 Kanji: <b>{item['kanji']}</b>"
        ok = f"{item['reading']} - {item['meaning']}"
        wr = [f"{k['reading']} - {k['meaning']}" for k in kanji_list if k["kanji"] != item["kanji"]]
    else:
        question_text = f"📝 [Savol {s['current_index']+1}/{s['total']}]\n\n🇯🇵 Yaponcha: <b>「{item['jp']}」</b>\n\nTo'g'ri o'zbekcha tarjimani belgilang:"
        ok = item['uz']
        wr = [w['uz'] for w in words_list if w['jp'] != item['jp']]

    opts = random.sample(wr, min(3, len(wr))) + [ok]
    random.shuffle(opts)
    s["correct_string"] = ok
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in opts: markup.add(option)

    if s["type"] == "kanji" and os.path.exists(item["image_path"]):
        with open(item["image_path"], 'rb') as f:
            bot.send_photo(chat_id, f, caption=question_text, parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(chat_id, question_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_messages(m):
    cid, txt = m.chat.id, m.text.strip() if m.text else ""
    
    if txt == "📊 Kanji Test": ask_test_count(cid, "kanji"); return
    if txt == "📝 So'z Test (N4/N5)": ask_test_count(cid, "word"); return
    
    if txt in ["🏆 Reyting (Top-10)", "👤 Shaxsiy Profil", "📊 Admin: Statistika", "📣 Admin: Xabar Yuborish"]:
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(cid)), 999)

        if txt == "🏆 Reyting (Top-10)":
            output = "🏆 <b>SHOHONA REYTING JADVALI (TOP-10)</b>\n====================\n"
            for idx, (uid, uinfo) in enumerate(sorted_users[:10]):
                place = idx + 1
                is_bot = "🤖 " if uinfo.get("is_fake", False) else "👤 "
                output += f"{place:02d}. {get_rank_title(place)} | {is_bot}<b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
            output += "====================\n"
            output += f"📈 Sizning o'rningiz: <b>{user_place}-o'rin</b>"
            
            if user_place > 1:
                output += f"\n\n🚨 <i>Sizdan o'zib ketishdi! Reytingda peshqadam bo'lish uchun ko'proq test yeching!</i>"
                
            bot.send_message(cid, output, parse_mode="HTML", reply_markup=main_menu_keyboard(cid)); return
            
        if txt == "👤 Shaxsiy Profil":
            u = db.get(str(cid), {"name": m.from_user.first_name, "points": 0, "streak": 0})
            output = (
                f"👤 <b>SIZNING SHAXSIY PROFILINGIZ</b>\n====================\n"
                f"• Ismingiz: <b>{u['name']}</b>\n"
                f"• Jami ballar: <code>{u['points']} ball</code>\n"
                f"• Faollik zanjiri: <b>{u['streak']} kun</b>\n"
                f"• Joriy unvon: <b>{get_rank_title(user_place)} ({user_place}-o'rin)</b>\n===================="
            )
            bot.send_message(cid, output, parse_mode="HTML", reply_markup=main_menu_keyboard(cid)); return

    if cid in user_sessions:
        s = user_sessions[cid]
        if txt in ["📊 Kanji Test", "📝 So'z Test (N4/N5)", "🏆 Reyting (Top-10)", "👤 Shaxsiy Profil", "❓ Adminga murojaat"]:
            bot.send_message(cid, "⚠️ Iltimos, avval joriy testni yakunlang!")
            send_next_question(cid)
            return
            
        if txt == s["correct_string"]:
            s["correct_count"] += 1
            bot.send_message(cid, "✅ To‘g‘ri!")
        else:
            bot.send_message(cid, f"❌ Noto‘g‘ri!\nJavob: <b>{s['correct_string']}</b>", parse_mode="HTML")
        s["current_index"] += 1
        send_next_question(cid)
        return

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
