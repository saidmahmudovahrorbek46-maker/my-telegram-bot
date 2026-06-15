
import telebot, random, os, json, datetime

bot = telebot.TeleBot("8992035812:AAE0rGeTagE0CaxnjkiSyV3ZdgAgH6vlsTw")
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
    {"kanji": "社", "reading": "야しろ", "meaning": "jamiyat", "image_path": "jamiyat.png"},
    {"kanji": "場", "reading": "ばしょ", "meaning": "joy", "image_path": "kanji_images/joy.png"},
    {"kanji": "自", "reading": "みずkara", "meaning": "o'zi", "image_path": "kanji_images/ozi.png"},
    {"kanji": "動", "reading": "うgoく", "meaning": "harakat", "image_path": "kanji_images/harakat.png"},
    {"kanji": "持", "reading": "もつ", "meaning": "ushlamoq", "image_path": "kanji_images/ushlamoq.png"},
    {"kanji": "新", "reading": "あたらしい", "meaning": "yangi", "image_path": "kanji_images/yangi.png"},
    {"kanji": "古", "reading": "ふるい", "meaning": "eski", "image_path": "kanji_images/eski.png"},
    {"kanji": "駅", "reading": "えき", "meaning": "vokzal", "image_path": "kanji_images/vokzal.png"},
    {"kanji": "力", "reading": "ちkara", "meaning": "kuch", "image_path": "kanji_images/kuch.png"}
]

words_list = [
    {"jp": "あさ", "uz": "ertalab", "level": "N5"}, {"jp": "いぬ", "uz": "it", "level": "N5"},
    {"jp": "みせ", "uz": "do'kon", "level": "N5"}, {"jp": "ともだち", "uz": "do'st", "level": "N5"},
    {"jp": "しけん", "uz": "imtihon", "level": "N4"}, {"jp": "あぶない", "uz": "xavfli", "level": "N5"},
    {"jp": "いしゃ", "uz": "shifokor", "level": "N5"}, {"jp": "おくる", "uz": "yubormoq", "level": "N5"},
    {"jp": "おmiやげ", "uz": "sovg'a", "level": "N5"}, {"jp": "かいもの", "uz": "xarid", "level": "N5"},
    {"jp": "かぜ", "uz": "shamollash", "level": "N5"}, {"jp": "あかるい", "uz": "yorug'", "level": "N5"},
    {"jp": "あね", "uz": "mening opam", "level": "N5"}, {"jp": "あに", "uz": "mening akam", "level": "N5"},
    {"jp": "いもうと", "uz": "mening singlim", "level": "N5"}, {"jp": "おとうと", "uz": "mening ukam", "level": "N5"},
    {"jp": "うみ", "uz": "dengiz", "level": "N5"}, {"jp": "えいが", "uz": "kino", "level": "N5"},
    {"jp": "えき", "uz": "vokzal", "level": "N5"}, {"jp": "かんじ", "uz": "ieroglif", "level": "N5"},
    {"jp": "きっぷ", "uz": "bilet", "level": "N5"}, {"jp": "くるま", "uz": "mashina", "level": "N5"},
    {"jp": "さいふ", "uz": "hamyon", "level": "N5"}, {"jp": "しんぶん", "uz": "gazeta", "level": "N5"},
    {"jp": "あんぜん", "uz": "xavfsiz", "level": "N4"}, {"jp": "いみ", "uz": "ma'no", "level": "N4"},
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
    {"jp": "さいきん", "uz": "shu kunlarda", "level": "N4"}, {"jp": "こんど", "uz": "keyingi safar", "level": "N4"},
    {"jp": "あいさつ", "uz": "salomlashish", "level": "N4"}, {"jp": "あじ", "uz": "ta'm / maza", "level": "N4"},
    {"jp": "あした", "uz": "ertaga", "level": "N5"}, {"jp": "あたま", "uz": "bosh", "level": "N5"},
    {"jp": "あついつい", "uz": "issiq", "level": "N5"}, {"jp": "あぶra", "uz": "yog'", "level": "N4"},
    {"jp": "あめ", "uz": "yomg'ir", "level": "N5"}, {"jp": "あんしん", "uz": "xotirjamlik", "level": "N4"},
    {"jp": "あんない", "uz": "boshlash", "level": "N4"}, {"jp": "いい", "uz": "yaxshi", "level": "N5"},
    {"jp": "いえ", "uz": "uy", "level": "N5"}, {"jp": "いけ", "uz": "hovuz", "level": "N5"},
    {"jp": "いけん", "uz": "fikr", "level": "N4"}, {"jp": "いそがしい", "uz": "band", "level": "N5"},
    {"jp": "いたい", "uz": "og'riqli", "level": "N5"}, {"jp": "いちば", "uz": "bozor", "level": "N4"}
]

def main_menu_keyboard():
    return telebot.types.ReplyKeyboardMarkup(resize_keyboard=True).add("📊 Kanji Test", "📝 So'z Test (N4/N5)").add("👥 Guruhda O'ynash ⚔️").add("🏆 Reyting (Top-10)", "👤 Shaxsiy Profil").add("❓ Adminga murojaat")
    @bot.message_handler(commands=['start'])
def start(m):
    user_data = update_user_stats(m.chat.id, m.from_user.first_name, check_streak=True)
    db = load_db()
    sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(m.chat.id)), 999)
    welcome_text = (
        f"🎌 <b>JLPT Variantli Test Bot v19.1</b>\n\n"
        f"🔥 Faollik zanjiri: <b>{user_data['streak']} kun</b>\n"
        f"🏆 Jami ballar: <b>{user_data['points']} ball</b>\n"
        f"🏛️ Saroydagi mavqe: <b>{get_rank_title(user_place)} ({user_place}-o'rin)</b>"
    )
    bot.send_message(m.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu_keyboard())

@bot.message_handler(commands=['test'])
def group_test_command(m):
    bot.send_message(
        m.chat.id, 
        "⚔️ <b>SHOHONA JANG BOSHLANDI!</b> ⚔️\n====================\n"
        "Saroyning eng sara botirlari hozir o'z bilimlarini sinashadi!\n"
        "Kanji rasmlari va so'z testlari yuborilmoqda...\n====================\n",
        parse_mode="HTML"
    )
    start_quiz_session_by_values(m.chat.id, random.choice(["kanji", "word"]), 5)

def ask_test_count(chat_id, mode):
    m = bot.send_message(chat_id, "📊 Nechta test yechasiz?", reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("5", "10", "15"))
    bot.register_next_step_handler(m, lambda msg: start_quiz_session(msg, mode))

def start_quiz_session(m, mode):
    try: total = int(m.text.strip())
    except: total = 5
    start_quiz_session_by_values(m.chat.id, mode, total)

def start_quiz_session_by_values(chat_id, mode, total):
    base = kanji_list if mode == "kanji" else words_list
    user_sessions[chat_id] = {"questions": random.sample(base, min(total, len(base))), "current_index": 0, "correct_count": 0, "total": min(total, len(base)), "type": mode}
    send_next_question(chat_id)

def send_next_question(chat_id):
    s = user_sessions.get(chat_id)
    if not s: return
    if s["current_index"] >= s["total"]:
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        
        output = "🎉 <b>SHOHONA JANG YAKUNLANDI!</b>\n====================\n"
        output += "🏆 <b>YAKUNIY REYTING (TOP-5):</b>\n\n"
        for idx, (uid, uinfo) in enumerate(sorted_users[:5]):
            output += f"{idx+1}. {get_rank_title(idx+1)} | <b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
        output += "====================\n🎯 Ballar profilingizga muvaffaqiyatli qo'shildi!"
        
        bot.send_message(chat_id, output, parse_mode="HTML", reply_markup=main_menu_keyboard())
        del user_sessions[chat_id]; return

    item = s["questions"][s["current_index"]]
    
    if s["type"] == "kanji":
        question_text = f"🎯 [Savol {s['current_index']+1}/{s['total']}] Ushbu Kanjining to'g'ri o'qilishi va o'zbekcha ma'nosini belgilang:"
        ok = f"{item['reading']} - {item['meaning']}"
        wr = [f"{k['reading']} - {k['meaning']}" for k in kanji_list if k["kanji"] != item["kanji"]]
    else:
        question_text = f"📝 [Savol {s['current_index']+1}/{s['total']}]\n\n🇯🇵 <b>「{item['jp']}」</b>\n\nUshbu yaponcha so'zning to'g'ri o'zbekcha tarjimasini belgilang:"
        ok = item['uz']
        wr = [w['uz'] for w in words_list if w['jp'] != item['jp']]

    opts = random.sample(wr, min(3, len(wr))) + [ok]
    random.shuffle(opts)
    correct_id = opts.index(ok)
    s["correct_string"] = ok

    if str(chat_id).startswith("-"):
        if s["type"] == "kanji" and os.path.exists(item["image_path"]):
            with open(item["image_path"], 'rb') as f:
                bot.send_photo(chat_id, f, caption="📋 Yuqoridagi rasmdagi Kanjiga diqqat qiling:")
        
        bot.send_poll(
            chat_id=chat_id,
            question=question_text,
            options=opts,
            type="quiz",
            correct_option_id=correct_id,
            open_period=60,
            is_anonymous=False
        )
        s["current_index"] += 1
        import threading
        threading.Timer(62, lambda: send_next_question(chat_id)).start()
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        for o in opts: markup.add(o)
        
        if s["type"] == "kanji" and os.path.exists(item["image_path"]):
            with open(item["image_path"], 'rb') as f:
                bot.send_photo(chat_id, f, caption=question_text, reply_markup=markup)
        else:
            bot.send_message(chat_id, question_text, parse_mode="HTML", reply_markup=markup)
@bot.poll_answer_handler()
def handle_poll_answer(pollAnswer):
    user_id = pollAnswer.user.id
    username = pollAnswer.user.first_name
    update_user_stats(user_id, username, points_to_add=15)

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
    
    # 📋 ASOSIY MENYU TUGMALARI TEKSHIRUVI
    if txt == "📊 Kanji Test": ask_test_count(cid, "kanji"); return
    if txt == "📝 So'z Test (N4/N5)": ask_test_count(cid, "word"); return
    if txt == "👥 Guruhda O'ynash ⚔️":
        bot.send_message(cid, "⚔️ <b>Guruhda O'yin Boshlash:</b>\n\nUshbu botni guruhga qo'shing va guruh ichida <code>/test</code> buyrug'ini yuboring. Bot rasmiy viktorina rejimini boshlaydi!", parse_mode="HTML")
        return
    
    if txt == "🏆 Reyting (Top-10)" or txt == "👤 Shaxsiy Profil":
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(cid)), 999)

        if txt == "🏆 Reyting (Top-10)":
            output = "🏆 <b>Shohona Jonli Reyting:</b>\n====================\n"
            for idx, (uid, uinfo) in enumerate(sorted_users[:10]):
                place = idx + 1
                output += f"{place:02d}. {get_rank_title(place)} | <b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
            output += "====================\n📈 Sizning o'rningiz: <b>{user_place}-o'rin</b>"
            bot.send_message(cid, output, parse_mode="HTML", reply_markup=main_menu_keyboard()); return
            
        if txt == "👤 Shaxsiy Profil":
            u = db.get(str(cid), {"name": m.from_user.first_name, "points": 0, "streak": 0})
            output = (
                f"👤 <b>SIZNING SHAXSIY PROFILINGIZ</b>\n====================\n"
                f"• Ismingiz: <b>{u['name']}</b>\n"
                f"• Jami ballar: <code>{u['points']} ball</code>\n"
                f"• Faollik zanjiri: <b>{u['streak']} kun</b>\n"
                f"• Joriy mavqeingiz: <b>{get_rank_title(user_place)} ({user_place}-o'rin)</b>\n===================="
            )
            bot.send_message(cid, output, parse_mode="HTML", reply_markup=main_menu_keyboard()); return

    # 🔥 JAVOBLAR JADVALINI TEKSHIRISH (Faqat joriy sessiya mavjud bo'lsa)
    if cid in user_sessions:
        s = user_sessions[cid]
        if txt == s["correct_string"]:
            s["correct_count"] += 1
            bot.send_message(cid, "✅ To‘g‘ri!")
        else:
            bot.send_message(cid, f"❌ Noto‘g‘ri!\nJavob: <b>{s['correct_string']}</b>", parse_mode="HTML")
        s["current_index"] += 1
        send_next_question(cid)
        return

    # 🔥 GURUH VA SHAXSIY KOTIB REJIMINI AJRATISH FIXED
    if not str(cid).startswith("-") and cid != ADMIN_ID:
        bot.forward_message(ADMIN_ID, cid, m.message_id)
        bot.send_message(ADMIN_ID, f"📩 <b>Xabar!</b>\nUser ID: {cid}\n\nJavob uchun <b>Reply</b> qiling.", parse_mode="HTML")
        bot.send_message(cid, "⏱ Xabaringiz adminga yetkazildi.")

bot.remove_webhook()
bot.infinity_polling()

