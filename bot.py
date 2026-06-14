import telebot, random, os

bot = telebot.TeleBot("8992035812:AAHR6ixhqDqZ9nzW_kynOu_Jluy0cvpSdd8")
ADMIN_ID = 7523074495  
user_sessions = {}

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
    {"kanji": "持", "reading": "もつ", "meaning": "ushlamoq", "image_path": "kanji_images/ushlamoq.png"},
    {"kanji": "新", "reading": "あたらしい", "meaning": "yangi", "image_path": "kanji_images/yangi.png"},
    {"kanji": "古", "reading": "ふるい", "meaning": "eski", "image_path": "kanji_images/eski.png"},
    {"kanji": "駅", "reading": "えき", "meaning": "vokzal", "image_path": "kanji_images/vokzal.png"},
    {"kanji": "力", "reading": "ちkara", "meaning": "kuch", "image_path": "kanji_images/kuch.png"}
]

# 📝 ODDIY HIRAGANADA TUG'RI YOZILGAN SOHALAR RO'YXATI
words_list = [
    # --- ESKI VA DARAKTIv SO'ZLAR (55 TA) ---
    {"jp": "あさ", "uz": "ertalab", "level": "N5"},
    {"jp": "いぬ", "uz": "it", "level": "N5"},
    {"jp": "みせ", "uz": "do'kon", "level": "N5"},
    {"jp": "ともだち", "uz": "do'st", "level": "N5"},
    {"jp": "しけん", "uz": "imtihon", "level": "N4"},
    {"jp": "あぶない", "uz": "xavfli", "level": "N5"},
    {"jp": "いしゃ", "uz": "shifokor", "level": "N5"},
    {"jp": "おくる", "uz": "yubormoq", "level": "N5"},
    {"jp": "おみやげ", "uz": "sovg'a", "level": "N5"},
    {"jp": "かいもの", "uz": "xarid", "level": "N5"},
    {"jp": "かぜ", "uz": "shamollash", "level": "N5"},
    {"jp": "あかるい", "uz": "yorug'", "level": "N5"},
    {"jp": "あね", "uz": "mening opam", "level": "N5"},
    {"jp": "あに", "uz": "mening akam", "level": "N5"},
    {"jp": "いもうと", "uz": "mening singlim", "level": "N5"},
    {"jp": "おとうと", "uz": "mening ukam", "level": "N5"},
    {"jp": "うみ", "uz": "dengiz", "level": "N5"},
    {"jp": "えいが", "uz": "kino", "level": "N5"},
    {"jp": "えき", "uz": "vokzal", "level": "N5"},
    {"jp": "かんじ", "uz": "ieroglif", "level": "N5"},
    {"jp": "きっぷ", "uz": "bilet", "level": "N5"},
    {"jp": "くるま", "uz": "mashina", "level": "N5"},
    {"jp": "さいふ", "uz": "hamyon", "level": "N5"},
    {"jp": "しんぶん", "uz": "gazeta", "level": "N5"},
    {"jp": "あんぜん", "uz": "xavfsiz", "level": "N4"},
    {"jp": "いmi", "uz": "ma'no", "level": "N4"},
    {"jp": "うけつけ", "uz": "ro'yxatxona", "level": "N4"},
    {"jp": "うごく", "uz": "qimirlamoq", "level": "N4"},
    {"jp": "うそ", "uz": "yolg'on", "level": "N4"},
    {"jp": "おこる", "uz": "g'azablanmoq", "level": "N4"},
    {"jp": "おmoいだす", "uz": "eslamoq", "level": "N4"},
    {"jp": "おもちゃ", "uz": "o'yinchoq", "level": "N4"},
    {"jp": "かたづける", "uz": "yig'ishtirmoq", "level": "N4"},
    {"jp": "かんがえる", "uz": "o'ylamoq", "level": "N4"},
    {"jp": "がんばる", "uz": "harakat qilmoq", "level": "N4"},
    {"jp": "きびしい", "uz": "qattiqqo'l", "level": "N4"},
    {"jp": "くうこう", "uz": "aeroport", "level": "N4"},
    {"jp": "おくじょう", "uz": "tom", "level": "N4"},
    {"jp": "ちか", "uz": "yer osti", "level": "N4"},
    {"jp": "しゅっぱつ", "uz": "jo'nab ketish", "level": "N4"},
    {"jp": "とうちゃく", "uz": "yetib kelish", "level": "N4"},
    {"jp": "あつめる", "uz": "yig'moq", "level": "N4"},
    {"jp": "わかれる", "uz": "ajralishmoq", "level": "N4"},
    {"jp": "せまい", "uz": "tor", "level": "N4"},
    {"jp": "ひろい", "uz": "keng", "level": "N4"},
    {"jp": "くらい", "uz": "qorong'u", "level": "N4"},
    {"jp": "さいきん", "uz": "shu kunlarda", "level": "N4"},
    {"jp": "こんど", "uz": "keyingi safar", "level": "N4"},

    # --- YANA 100 TA ENg KO'P TUSHADIGAN OLTIN SO'ZLAR (YAdRO BAZA) ---
    {"jp": "あいさつ", "uz": "salomlashish", "level": "N4"},
    {"jp": "あじ", "uz": "ta'm / maza", "level": "N4"},
    {"jp": "あした", "uz": "ertaga", "level": "N5"},
    {"jp": "あたま", "uz": "bosh", "level": "N5"},
    {"jp": "あついつい", "uz": "issiq", "level": "N5"},
    {"jp": "あぶら", "uz": "yog'", "level": "N4"},
    {"jp": "あめ", "uz": "yomg'ir", "level": "N5"},
    {"jp": "あんしん", "uz": "xotirjamlik", "level": "N4"},
    {"jp": "あんない", "uz": "yo'riqnoma / boshlash", "level": "N4"},
    {"jp": "いい", "uz": "yaxshi", "level": "N5"},
    {"jp": "いえ", "uz": "uy", "level": "N5"},
    {"jp": "いけ", "uz": "hovuz", "level": "N5"},
    {"jp": "いけん", "uz": "fikr", "level": "N4"},
    {"jp": "いそがしい", "uz": "band", "level": "N5"},
    {"jp": "いたい", "uz": "og'riqli", "level": "N5"},
    {"jp": "いちば", "uz": "bozor", "level": "N4"},
    {"jp": "いつ", "uz": "qachon", "level": "N5"},
    {"jp": "いと", "uz": "ip", "level": "N4"},
    {"jp": "いなか", "uz": "qishloq", "level": "N4"},
    {"jp": "いのる", "uz": "duo qilmoq", "level": "N4"},
    {"jp": "いま", "uz": "hozir", "level": "N5"},
    {"jp": "うえる", "uz": "ekmoq", "level": "N4"},
    {"jp": "うた", "uz": "qo'shiq", "level": "N5"},
    {"jp": "うち", "uz": "uy / ichkarida", "level": "N5"},
    {"jp": "うつくしい", "uz": "go'zal", "level": "N4"},
    {"jp": "うつす", "uz": "ko'chirmoq", "level": "N4"},
    {"jp": "うまる", "uz": "tug'ilmoq", "level": "N4"},
    {"jp": "うりば", "uz": "sotuv bo'limi", "level": "N4"},
    {"jp": "うんてん", "uz": "haydash (mashina)", "level": "N4"},
    {"jp": "うんどう", "uz": "sport / mashq", "level": "N4"},
    {"jp": "えだ", "uz": "shox (daraxt)", "level": "N4"},
    {"jp": "えらぶ", "uz": "saylamoq / tanlamoq", "level": "N4"},
    {"jp": "お祝い", "uz": "tabrik", "level": "N4"},
    {"jp": "おかし", "uz": "shirinlik", "level": "N5"},
    {"jp": "おかね", "uz": "pul", "level": "N5"},
    {"jp": "おきる", "uz": "uyg'onmoq", "level": "N5"},
    {"jp": "おくさん", "uz": "turmush o'rtoq (birovning)", "level": "N4"},
    {"jp": "おくる", "uz": "kuzatib qo'ymoq", "level": "N4"},
    {"jp": "おこす", "uz": "uyg'otmoq", "level": "N4"},
    {"jp": "おしいれ", "uz": "javon (devoriy)", "level": "N4"},
    {"jp": "おじさん", "uz": "amaki / tog'a", "level": "N5"},
    {"jp": "おばさん", "uz": "xola / amma", "level": "N5"},
    {"jp": "おだやか", "uz": "tinch / xotirjam", "level": "N4"},
    {"jp": "おと", "uz": "tovush / ovoz", "level": "N5"},
    {"jp": "おととい", "uz": "o'tgan kuni", "level": "N5"},
    {"jp": "おととし", "uz": "o'tgan yili", "level": "N5"},
    {"jp": "おとな", "uz": "katta odam", "level": "N5"},
    {"jp": "おどろく", "uz": "hayron qolmoq", "level": "N4"},
    {"jp": "おふろ", "uz": "vanna", "level": "N5"},
    {"jp": "おぼえる", "uz": "eslab qolmoq", "level": "N5"},
    {"jp": "おもい", "uz": "og'ir", "level": "N5"},
    {"jp": "おもしろい", "uz": "qiziqarli", "level": "N5"},
    {"jp": "おわり", "uz": "tugashi / oxiri", "level": "N5"},
    {"jp": "かいがん", "uz": "dengiz qirg'og'i", "level": "N4"},
    {"jp": "かいぎ", "uz": "majlis", "level": "N4"},
    {"jp": "かいだん", "uz": "zina", "level": "N5"},
    {"jp": "かいさつ", "uz": "bilet tekshirish joyi", "level": "N4"},
    {"jp": "かえる", "uz": "o'zgartirmoq", "level": "N4"},
    {"jp": "かがく", "uz": "kimyo / fan", "level": "N4"},
    {"jp": "かがみ", "uz": "ko'zgu", "level": "N4"},
    {"jp": "かける", "uz": "ilmoq / qo'ng'iroq qilmoq", "level": "N5"},
    {"jp": "かざる", "uz": "bezatmoq", "level": "N4"},
    {"jp": "かじ", "uz": "yong'in", "level": "N4"},
    {"jp": "かしゅ", "uz": "xonanda", "level": "N4"},
    {"jp": "かた", "uz": "Yelka / usul", "level": "N4"},
    {"jp": "かたち", "uz": "shakl", "level": "N4"},
    {"jp": "かない", "uz": "mening ayolim", "level": "N4"},
    {"jp": "かなしい", "uz": "g'amgin", "level": "N4"},
    {"jp": "かね", "uz": "qo'ng'iroq", "level": "N4"},
    {"jp": "かみ", "uz": "soch / qog'oz", "level": "N5"},
    {"jp": "かようび", "uz": "seshanba", "level": "N5"},
    {"jp": "からだ", "uz": "tana / sog'liq", "level": "N5"},
    {"jp": "かりる", "uz": "qarzga olmoq", "level": "N5"},
    {"jp": "かわ", "uz": "daryo", "level": "N5"},
    {"jp": "かわく", "uz": "qurimoq", "level": "N4"},
    {"jp": "かわる", "uz": "o'zgariroq", "level": "N4"},
    {"jp": "かんたん", "uz": "oson", "level": "N5"},
    {"jp": "かんじ", "uz": "hissiyot", "level": "N4"},
    {"jp": "かんけい", "uz": "aloqa / munosabat", "level": "N4"},
    {"jp": "かんこう", "uz": "sayohat (turizm)", "level": "N4"},
    {"jp": "きあつ", "uz": "havo bosimi", "level": "N4"},
    {"jp": "きえる", "uz": "o'chmoq (chiroq)", "level": "N5"},
    {"jp": "きく", "uz": "eshitmoq / so'ramoq", "level": "N5"},
    {"jp": "きけん", "uz": "xavfli", "level": "N4"},
    {"jp": "きせつ", "uz": "fasl", "level": "N4"},
    {"jp": "きたない", "uz": "iflos", "level": "N5"},
    {"jp": "きっさてん", "uz": "qahvaxona", "level": "N5"},
    {"jp": "きまる", "uz": "hal bo'lmoq", "level": "N4"},
    {"jp": "きもち", "uz": "kayfiyat / tuyg'u", "level": "N5"},
    {"jp": "きもの", "uz": "milliy kiyim", "level": "N5"},
    {"jp": "きゅうこう", "uz": "tezurar poyezd", "level": "N4"},
    {"jp": "きょねん", "uz": "o'tgan yili", "level": "N5"},
    {"jp": "きらい", "uz": "yomon ko'rish", "level": "N5"},
    {"jp": "きれる", "uz": "kesilmoq", "level": "N4"},
    {"jp": "きんじょ", "uz": "mahalla / yaqin joy", "level": "N4"},
    {"jp": "くすり", "uz": "dori", "level": "N5"},
    {"jp": "くだもの", "uz": "meva", "level": "N5"},
    {"jp": "くち", "uz": "ogiz", "level": "N5"},
    {"jp": "くび", "uz": "bo'yin", "level": "N4"},
    {"jp": "くも", "uz": "bulut / o'rgimchak", "level": "N5"}
]


def main_menu_keyboard():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Kanji Test")
    markup.add("📝 So'z Test (N4/N5)")
    markup.add("📚 Ma'lumot", "❓ Adminga murojaat")
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "🎌 <b>JLPT N4/N5 Variantli Test Bot</b>\n\nTugmalarni tanlang:", parse_mode="HTML", reply_markup=main_menu_keyboard())

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
        bot.send_message(chat_id, f"🎉 <b>Yakunlandi!</b>\n✅ Natija: <b>{s['correct_count']}/{s['total']} ta</b>", parse_mode="HTML", reply_markup=main_menu_keyboard())
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
        markup.row(opts[0], opts[1])
        markup.row(opts[2], opts[3])
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
    if txt == "📚 Ma'lumot":
        bot.send_message(cid, f"📚 <b>Statistika:</b>\n• Kanjilar: {len(kanji_list)} ta\n• So'zlar: {len(words_list)} ta", parse_mode="HTML", reply_markup=main_menu_keyboard()); return
    if txt == "❓ Adminga murojaat":
        bot.send_message(cid, "✉️ Xabaringizni yozing:", reply_markup=main_menu_keyboard()); return

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

bot.infinity_polling()
