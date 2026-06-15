import telebot, random, os, json, datetime

bot = telebot.TeleBot("8992035812:AAG1av18rlMX4SAmqv0HZO56hdeYmF8bQAM")
ADMIN_ID = 7523074495  
user_sessions = {}
DB_FILE = "bot_users.json"

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
    {"kanji": "先", "reading": "さki", "meaning": "avval", "image_path": "kanji_images/avval.png"},
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
    {"kanji": "自", "reading": "みずから", "meaning": "o'zi", "image_path": "kanji_images/ozi.png"},
    {"kanji": "動", "reading": "うごく", "meaning": "harakat", "image_path": "kanji_images/harakat.png"},
    {"kanji": "持", "reading": "もつ", "meaning": "ushlamoq", "image_path": "kanji_images/ushlamoq.png"},
    {"kanji": "新", "reading": "あたらしい", "meaning": "yangi", "image_path": "kanji_images/yangi.png"},
    {"kanji": "古", "reading": "ふるい", "meaning": "eski", "image_path": "kanji_images/eski.png"},
    {"kanji": "駅", "reading": "えき", "meaning": "vokzal", "image_path": "kanji_images/vokzal.png"},
    {"kanji": "力", "reading": "ちから", "meaning": "kuch", "image_path": "kanji_images/kuch.png"}
]

words_list = [
    {"jp": "あさ", "uz": "ertalab", "level": "N5"}, {"jp": "いぬ", "uz": "it", "level": "N5"},
    {"jp": "みせ", "uz": "do'kon", "level": "N5"}, {"jp": "ともだち", "uz": "do'st", "level": "N5"},
    {"jp": "しけん", "uz": "imtihon", "level": "N4"}, {"jp": "あぶない", "uz": "xavfli", "level": "N5"},
    {"jp": "いしゃ", "uz": "shifokor", "level": "N5"}, {"jp": "おくる", "uz": "yubormoq", "level": "N5"},
    {"jp": "おみяげ", "uz": "sovg'a", "level": "N5"}, {"jp": "かいもの", "uz": "xarid", "level": "N5"},
    {"jp": "かぜ", "uz": "shamollash", "level": "N5"}, {"jp": "あかるい", "uz": "yorug'", "level": "N5"},
    {"jp": "あね", "uz": "mening opam", "level": "N5"}, {"jp": "あに", "uz": "mening akam", "level": "N5"},
    {"jp": "いもうと", "uz": "mening singlim", "level": "N5"}, {"jp": "おとうと", "uz": "mening ukam", "level": "N5"},
    {"jp": "うみ", "uz": "dengiz", "level": "N5"}, {"jp": "えいが", "uz": "kino", "level": "N5"},
    {"jp": "えき", "uz": "vokzal", "level": "N5"}, {"jp": "かんじ", "uz": "ieroglif", "level": "N5"},
    {"jp": "きっぷ", "uz": "bilet", "level": "N5"}, {"jp": "くるま", "uz": "mashina", "level": "N5"},
    {"jp": "さいふ", "uz": "hamyon", "level": "N5"}, {"jp": "しんぶん", "uz": "gazeta", "level": "N5"},
    {"jp": "あんぜん", "uz": "xavfsiz", "level": "N4"}, {"jp": "いmi", "uz": "ma'no", "level": "N4"},
    {"jp": "うけつけ", "uz": "ro'yxatxona", "level": "N4"}, {"jp": "うごく", "uz": "qimirlamoq", "level": "N4"},
    {"jp": "うそ", "uz": "yolg'on", "level": "N4"}, {"jp": "おこる", "uz": "g'azablanmoq", "level": "N4"},
    {"jp": "おもいだす", "uz": "eslamoq", "level": "N4"}, {"jp": "おもちゃ", "uz": "o'yinchoq", "level": "N4"},
    {"jp": "かたづける", "uz": "yig'ishtirmoq", "level": "N4"}, {"jp": "かんがえる", "uz": "o'ylamoq", "level": "N4"},
    {"jp": "がんばる", "uz": "harakat qilmoq", "level": "N4"}, {"jp": "きびしい", "uz": "qattiqqo'l", "level": "N4"},
    {"jp": "くうこう", "uz": "aeroport", "level": "N4"}, {"jp": "おくじょう", "uz": "tom", "level": "N4"},
    {"jp": "ちか", "uz": "yer osti", "level": "N4"}, {"jp": "しゅっぱつ", "uz": "jo'nab ketish", "level": "N4"},
    {"jp": "とうちゃく", "uz": "yetib kelish", "level": "N4"}, {"jp": "あtsuめる", "uz": "yig'moq", "level": "N4"},
    {"jp": "わかれる", "uz": "ajralishmoq", "level": "N4"}, {"jp": "せmai", "uz": "tor", "level": "N4"},
    {"jp": "ひろい", "uz": "keng", "level": "N4"}, {"jp": "くらい", "uz": "qorong'u", "level": "N4"},
    {"jp": "さいきん", "uz": "shu kunlarda", "level": "N4"}, {"jp": "こんど", "uz": "keyingi safar", "level": "N4"}
]

def main_menu_keyboard():
    return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add("📊 Kanji Test", "📝 So'z Test (N4/N5)").add("🏆 Reyting (Top-10)", "👤 Shaxsiy Profil").add("❓ Adminga murojaat")
@bot.message_handler(commands=['start'])
def start(m):
    user_data = update_user_stats(m.chat.id, m.from_user.first_name, check_streak=True)
    welcome_text = (
        f"🎌 <b>JLPT N4/N5 Variantli Test Bot v16.1</b>\n\n"
        f"🔥 Kunlik faollik zanjiri: <b>{user_data['streak']} kun</b>\n"
        f"🏆 Jami ballaringiz: <b>{user_data['points']} ball</b>\n\n"
        f"Pastdagi tugmalardan foydalanib testni boshlang:"
    )
    bot.send_message(m.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu_keyboard())

def ask_test_count(chat_id, mode):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("5", "10", "15", "20")
    m = bot.send_message(chat_id, "📊 Nechta test yechasiz?", reply_markup=markup)
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
        bot.send_message(chat_id, f"🎉 <b>Test yakunlandi!</b>\n✅ To'g'ri javoblar: <b>{s['correct_count']}/{s['total']} ta</b>\n💰 Bonus: <b>+{earned_points} ball</b>", parse_mode="HTML", reply_markup=main_menu_keyboard())
        del user_sessions[chat_id]; return

    item = s["questions"][s["current_index"]]
    if s["type"] == "kanji":
        ok = f"{item['reading']} - {item['meaning']}"
        wr = [f"{k['reading']} - {k['meaning']}" for k in kanji_list if k["kanji"] != item["kanji"]]
    else:
        ok = item['uz']
        wr = [w['uz'] for w in words_list if w['jp'] != item['jp']]

    opts = random.sample(wr, min(3, len(wr))) + [ok]
    random.shuffle(opts)
    s["correct_string"] = ok
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    if len(opts) >= 4:
        markup.row(opts[:2], opts[2:])
    else:
        for o in opts: markup.add(o)

    if s["type"] == "kanji":
        if os.path.exists(item["image_path"]):
            with open(item["image_path"], 'rb') as f:
                bot.send_photo(chat_id, f, caption=f"📝 <b>Kanji {s['current_index']+1}/{s['total']}:</b>\nTo'g'ri javobni tanlang:", parse_mode="HTML", reply_markup=markup)
        else:
            bot.send_message(chat_id, f"📝 <b>Kanji {s['current_index']+1}/{s['total']}:</b>\n🎯 Kanji: <b>{item['kanji']}</b>\n\nTo'g'ri javobni tanlang:", parse_mode="HTML", reply_markup=markup)
    else:
        bot.send_message(chat_id, f"📝 <b>So'z {s['current_index']+1}/{s['total']} ({item['level']}):</b>\n\n🇯🇵 Yaponcha: <b>{item['jp']}</b>\n\nTarjimasini tanlang:", parse_mode="HTML", reply_markup=markup)

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
    
    if txt == "🏆 Reyting (Top-10)" or txt == "👤 Shaxsiy Profil":
        db = load_db()
        # Foydalanuvchilarni ballari bo'yicha yuqoridan pastga tartiblash
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        
        # Foydalanuvchining jonli o'rnini aniqlash
        user_place = 999
        for index, (uid, uinfo) in enumerate(sorted_users):
            if uid == str(cid):
                user_place = index + 1
                break

        if txt == "🏆 Reyting (Top-10)":
            output = "🏆 <b>Shohona Jonli Reyting:</b>\n\n"
            for idx, (uid, uinfo) in enumerate(sorted_users[:10]):
                place = idx + 1
                # O'rniga qarab shohona unvonlar
                if place == 1: lvl = "👑 Qirol"
                elif place == 2: lvl = "📜 Vazir"
                elif place <= 4: lvl = "⚔️ Amir"
                elif place <= 6: lvl = "🛡️ Sohibqiron"
                else: lvl = "👨‍🌾 Fuqaro"
                
                output += f"{place}. <b>{uinfo.get('name', 'User')}</b> — <code>{uinfo.get('points', 0)} ball</code> ({lvl})\n"
            bot.send_message(cid, output, parse_mode="HTML", reply_markup=main_menu_keyboard()); return
            
        if txt == "👤 Shaxsiy Profil":
            u = db.get(str(cid), {"name": m.from_user.first_name, "points": 0, "streak": 0})
            
            # Shaxsiy kabinetda unvon matnlari
            if user_place == 1:
                rank_title = "👑 <b>Qirol — Siz mutloq shohsiz!</b>"
                next_rank = "🎯 Taxtni hech kimga bermang!"
            elif user_place == 2:
                rank_title = "📜 <b>Vazir — Qirolning o'ng qo'lisiz!</b>"
                next_rank = "🚀 Birgina test bilan Qirolni taxtdan ag'darishingiz mumkin!"
            elif user_place <= 4:
                rank_title = "⚔️ <b>Amir — Davlat sarkardasisiz!</b>"
                next_rank = "📈 Vazir darajasiga ko'tarilishga oz qoldi!"
            elif user_place <= 6:
                rank_title = "🛡️ <b>Sohibqiron — Qahramonsiz!</b>"
                next_rank = "⚔️ Kuchli sarkardalar safiga kirishga harakat qiling!"
            else:
                rank_title = "👨‍🌾 <b>Fuqaro — Oddiy o'rganuvchisiz</b>"
                next_rank = f"Hozir reytingda <b>{user_place}-o'rindasiz</b>. Test yechib tezroq saroyga yo'l oling!"

            output = (
                f"👤 <b>Sizning shaxsiy profilingiz:</b>\n\n"
                f"• Ismingiz: <b>{u['name']}</b>\n"
                f"• To'plangan ballar: <b>{u['points']} ball</b>\n"
                f"• Faollik zanjiri: <b>{u['streak']} kun</b>\n\n"
                f"🏛️ Saroydagi mavqeingiz:\n{rank_title}\n\n"
                f"📈 {next_rank}"
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
