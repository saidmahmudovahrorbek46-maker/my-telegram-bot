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
    # Greetings
    {"jp": "こんにちは", "uz": "salom", "level": "N5"}, {"jp": "おはようございます", "uz": "ertalab", "level": "N5"},
    {"jp": "こんばんは", "uz": "axshom salom", "level": "N5"}, {"jp": "おやすみなさい", "uz": "yaxshi uxla", "level": "N5"},
    {"jp": "さようなら", "uz": "xayr", "level": "N5"}, {"jp": "じゃあね", "uz": "shu vaqtingacha", "level": "N5"},
    {"jp": "ありがとう", "uz": "rahmat", "level": "N5"}, {"jp": "どうぞ", "uz": "iltimos", "level": "N5"},
    {"jp": "すみません", "uz": "kechirasiz", "level": "N5"}, {"jp": "おつかれさまです", "uz": "hastalik uchun rahmat", "level": "N5"},
    
    # Colors
    {"jp": "あかい", "uz": "qizil", "level": "N5"}, {"jp": "あおい", "uz": "ko'k", "level": "N5"},
    {"jp": "きいろい", "uz": "sariq", "level": "N5"}, {"jp": "くろい", "uz": "qora", "level": "N5"},
    {"jp": "しろい", "uz": "oq", "level": "N5"}, {"jp": "みどりいろ", "uz": "yashil", "level": "N5"},
    {"jp": "むらさきいろ", "uz": "binafshayi", "level": "N5"}, {"jp": "オレンジ", "uz": "apelsin rangi", "level": "N5"},
    {"jp": "ピンク", "uz": "pushti", "level": "N5"}, {"jp": "グレー", "uz": "kulrang", "level": "N5"},
    {"jp": "ちゃいろ", "uz": "jigarrang", "level": "N5"}, {"jp": "こい", "uz": "quyuq", "level": "N5"},
    {"jp": "あわい", "uz": "engil", "level": "N5"}, {"jp": "あかるい", "uz": "yorug'", "level": "N5"},
    {"jp": "くらい", "uz": "qorong'u", "level": "N5"}, {"jp": "あざやか", "uz": "yorqin", "level": "N4"},
    {"jp": "こうたく", "uz": "yaltiroq", "level": "N4"}, {"jp": "つや", "uz": "lalmi", "level": "N4"},
    {"jp": "くすんだ", "uz": "xira", "level": "N4"}, {"jp": "まっしろ", "uz": "sof oq", "level": "N4"},
    {"jp": "ふかい", "uz": "chuqur", "level": "N4"}, {"jp": "あさい", "uz": "soyaroq", "level": "N4"},
    {"jp": "のうし", "uz": "quyuq binafshayi", "level": "N4"}, {"jp": "うすむらさき", "uz": "engil binafshayi", "level": "N4"},
    {"jp": "からしいろ", "uz": "sargarbarg", "level": "N4"}, {"jp": "てつこん", "uz": "qo'ra ko'k", "level": "N4"},
    {"jp": "きんいろ", "uz": "oltin rangi", "level": "N4"}, {"jp": "ぎんいろ", "uz": "kumush rangi", "level": "N4"},
    
    # Food
    {"jp": "こめ", "uz": "bug'doy", "level": "N5"}, {"jp": "さかな", "uz": "baliq", "level": "N5"},
    {"jp": "にく", "uz": "go'sht", "level": "N5"}, {"jp": "やさい", "uz": "sabzavot", "level": "N5"},
    {"jp": "くだもの", "uz": "meva", "level": "N5"}, {"jp": "パン", "uz": "non", "level": "N5"},
    {"jp": "スープ", "uz": "shorba", "level": "N5"}, {"jp": "ごはん", "uz": "plov", "level": "N5"},
    {"jp": "みそしる", "uz": "miso shorba", "level": "N5"}, {"jp": "てんぷら", "uz": "tempura", "level": "N5"},
    {"jp": "すし", "uz": "sushi", "level": "N5"}, {"jp": "そば", "uz": "Yapon makaron", "level": "N5"},
    {"jp": "うどん", "uz": "udon", "level": "N5"}, {"jp": "ラーメン", "uz": "ramen", "level": "N5"},
    {"jp": "たまご", "uz": "tuxum", "level": "N5"}, {"jp": "ぎゅうにゅう", "uz": "sut", "level": "N5"},
    {"jp": "チーズ", "uz": "pishloq", "level": "N5"}, {"jp": "バター", "uz": "moy", "level": "N5"},
    {"jp": "しお", "uz": "tuz", "level": "N5"}, {"jp": "さとう", "uz": "qand", "level": "N5"},
    {"jp": "しょうゆ", "uz": "soy susi", "level": "N5"}, {"jp": "あぶら", "uz": "yog'", "level": "N5"},
    {"jp": "す", "uz": "sirka", "level": "N5"}, {"jp": "こしょう", "uz": "qora ziravo'y", "level": "N5"},
    {"jp": "とうがらし", "uz": "qizil qalampir", "level": "N5"}, {"jp": "はちみつ", "uz": "asal", "level": "N5"},
    {"jp": "ジャム", "uz": "murabbо", "level": "N5"}, {"jp": "ピーナッツ", "uz": "arахис", "level": "N5"},
    {"jp": "アーモンド", "uz": "badom", "level": "N5"}, {"jp": "クッキー", "uz": "печенье", "level": "N5"},
    {"jp": "ケーキ", "uz": "keks", "level": "N5"}, {"jp": "アイスクリーム", "uz": "muzqaymoq", "level": "N5"},
    {"jp": "チョコレート", "uz": "shokolad", "level": "N5"}, {"jp": "キャンディ", "uz": "salyut", "level": "N5"},
    {"jp": "りんご", "uz": "olma", "level": "N5"}, {"jp": "バナナ", "uz": "banan", "level": "N5"},
    {"jp": "オレンジ", "uz": "apelsin", "level": "N5"}, {"jp": "いちご", "uz": "qulupnay", "level": "N5"},
    {"jp": "ぶどう", "uz": "uzum", "level": "N5"}, {"jp": "すいか", "uz": "qovun", "level": "N5"},
    {"jp": "メロン", "uz": "qovun", "level": "N5"}, {"jp": "れもん", "uz": "limon", "level": "N5"},
    {"jp": "ライム", "uz": "laym", "level": "N5"}, {"jp": "もも", "uz": "shaftoli", "level": "N5"},
    {"jp": "アボカド", "uz": "avokado", "level": "N5"}, {"jp": "とまと", "uz": "pomidor", "level": "N5"},
    {"jp": "にんじん", "uz": "sabzi", "level": "N5"}, {"jp": "じゃがいも", "uz": "kartoshka", "level": "N5"},
    {"jp": "たまねぎ", "uz": "piyoz", "level": "N5"}, {"jp": "にんにく", "uz": "sarmsaq", "level": "N5"},
    {"jp": "キャベツ", "uz": "karam", "level": "N5"}, {"jp": "ブロッコリー", "uz": "koloflor", "level": "N5"},
    {"jp": "キュウリ", "uz": "bodring", "level": "N5"}, {"jp": "ピーマン", "uz": "bolgar kalampir", "level": "N5"},
    {"jp": "レタス", "uz": "tuz piyozi", "level": "N5"}, {"jp": "ほうれんそう", "uz": "paluq", "level": "N5"},
    {"jp": "とうもろこし", "uz": "misai", "level": "N5"}, {"jp": "まめ", "uz": "loviya", "level": "N5"},
    {"jp": "かき", "uz": "ustirka", "level": "N5"}, {"jp": "エビ", "uz": "kreveti", "level": "N5"},
    {"jp": "カニ", "uz": "krab", "level": "N5"}, {"jp": "タコ", "uz": "osminog", "level": "N5"},
    {"jp": "イカ", "uz": "smutskalmar", "level": "N5"}, {"jp": "かい", "uz": "qo'ng'ir", "level": "N5"},
    
    # Animals
    {"jp": "ねこ", "uz": "mushuk", "level": "N5"}, {"jp": "いぬ", "uz": "it", "level": "N5"},
    {"jp": "とり", "uz": "qush", "level": "N5"}, {"jp": "さかな", "uz": "baliq", "level": "N5"},
    {"jp": "うし", "uz": "sigir", "level": "N5"}, {"jp": "ぶた", "uz": "cho'chqa", "level": "N5"},
    {"jp": "うま", "uz": "ot", "level": "N5"}, {"jp": "ひつじ", "uz": "qo'y", "level": "N5"},
    {"jp": "ウサギ", "uz": "quyon", "level": "N5"}, {"jp": "ねずみ", "uz": "sichqon", "level": "N5"},
    {"jp": "へび", "uz": "ilon", "level": "N5"}, {"jp": "とんぼ", "uz": "subbaiy", "level": "N5"},
    {"jp": "くも", "uz": "o'rgimchak", "level": "N5"}, {"jp": "ちょう", "uz": "kapalak", "level": "N5"},
    {"jp": "はち", "uz": "ari", "level": "N5"}, {"jp": "みつばち", "uz": "ari", "level": "N5"},
    {"jp": "かえる", "uz": "qo'ng'iz", "level": "N5"}, {"jp": "かめ", "uz": "toshbaqa", "level": "N5"},
    {"jp": "ワニ", "uz": "timsoh", "level": "N5"}, {"jp": "ペンギン", "uz": "pingvin", "level": "N5"},
    {"jp": "ふくろう", "uz": "boʻrino", "level": "N5"}, {"jp": "わし", "uz": "burgut", "level": "N5"},
    {"jp": "だちょう", "uz": "ot quvi", "level": "N5"}, {"jp": "パンダ", "uz": "panda", "level": "N5"},
    {"jp": "ライオン", "uz": "arslon", "level": "N5"}, {"jp": "とら", "uz": "yo'lokchi", "level": "N5"},
    {"jp": "ひょう", "uz": "leopard", "level": "N5"}, {"jp": "ぞう", "uz": "fil", "level": "N5"},
    {"jp": "キリン", "uz": "ziraffe", "level": "N5"}, {"jp": "しまうま", "uz": "zebra", "level": "N5"},
    {"jp": "くま", "uz": "ayiqq", "level": "N5"}, {"jp": "アルパカ", "uz": "alpaka", "level": "N5"},
    {"jp": "ラッパ", "uz": "latun", "level": "N5"}, {"jp": "かも", "uz": "o't o'rigi", "level": "N5"},
    {"jp": "はくちょう", "uz": "qug'u", "level": "N5"}, {"jp": "くじら", "uz": "kit", "level": "N5"},
    {"jp": "あざらし", "uz": "mo'rin it", "level": "N5"}, {"jp": "ゴリラ", "uz": "gorilla", "level": "N5"},
    {"jp": "さる", "uz": "maymun", "level": "N5"}, {"jp": "スカンク", "uz": "scunk", "level": "N5"},
    {"jp": "やまあらし", "uz": "tikanbilgan", "level": "N5"}, {"jp": "はりねずみ", "uz": "sanchqi", "level": "N5"},
    
    # Weather
    {"jp": "せいてん", "uz": "toza asman", "level": "N5"}, {"jp": "あめ", "uz": "yomg'ir", "level": "N5"},
    {"jp": "ゆき", "uz": "qor", "level": "N5"}, {"jp": "かぜ", "uz": "shamol", "level": "N5"},
    {"jp": "くもり", "uz": "bulutli", "level": "N5"}, {"jp": "きり", "uz": "tuman", "level": "N5"},
    {"jp": "かみなり", "uz": "chergi", "level": "N5"}, {"jp": "たいふう", "uz": "tayfun", "level": "N5"},
    {"jp": "おんど", "uz": "harorat", "level": "N5"}, {"jp": "しつど", "uz": "namlik", "level": "N5"},
    {"jp": "ぼうう", "uz": "shiddatli yomg'ir", "level": "N4"}, {"jp": "ふぶき", "uz": "qor bo'ronasi", "level": "N4"},
    {"jp": "はれ", "uz": "toza", "level": "N5"}, {"jp": "くもりぞら", "uz": "bulutli asman", "level": "N5"},
    {"jp": "にじ", "uz": "kamonli", "level": "N5"}, {"jp": "ひょう", "uz": "shusha qor", "level": "N4"},
    {"jp": "つゆ", "uz": "shab", "level": "N4"}, {"jp": "しも", "uz": "qirg'oq", "level": "N4"},
    {"jp": "そよかぜ", "uz": "engil shamol", "level": "N4"}, {"jp": "むかいかぜ", "uz": "boshga shamol", "level": "N4"},
    {"jp": "えんてんか", "uz": "qaynoq quyosh ostida", "level": "N4"}, {"jp": "とうけつ", "uz": "muzlab ketish", "level": "N4"},
    {"jp": "とける", "uz": "erib ketish", "level": "N4"}, {"jp": "かんそう", "uz": "quruq", "level": "N4"},
    {"jp": "むしあつい", "uz": "nam va issiq", "level": "N4"}, {"jp": "うきとい", "uz": "yomg'ir faslı", "level": "N4"},
    {"jp": "かんき", "uz": "quruq faslı", "level": "N4"}, {"jp": "しきい", "uz": "to'rt fasl", "level": "N4"},
    
    # Body Parts
    {"jp": "め", "uz": "ko'z", "level": "N5"}, {"jp": "みみ", "uz": "quloq", "level": "N5"},
    {"jp": "はな", "uz": "burun", "level": "N5"}, {"jp": "くち", "uz": "og'iz", "level": "N5"},
    {"jp": "は", "uz": "tish", "level": "N5"}, {"jp": "した", "uz": "til", "level": "N5"},
    {"jp": "て", "uz": "qo'l", "level": "N5"}, {"jp": "あし", "uz": "oyoq", "level": "N5"},
    {"jp": "ゆび", "uz": "barmoq", "level": "N5"}, {"jp": "つめ", "uz": "tirnoq", "level": "N5"},
    {"jp": "かみ", "uz": "soch", "level": "N5"}, {"jp": "かお", "uz": "yuz", "level": "N5"},
    {"jp": "くび", "uz": "bo'yin", "level": "N5"}, {"jp": "かた", "uz": "yelka", "level": "N5"},
    {"jp": "せ", "uz": "orqa", "level": "N5"}, {"jp": "むね", "uz": "ko'krak", "level": "N5"},
    {"jp": "こし", "uz": "yo'n", "level": "N5"}, {"jp": "うで", "uz": "bazu", "level": "N5"},
    {"jp": "ひざ", "uz": "tizzasi", "level": "N5"}, {"jp": "ひじ", "uz": "tirsak", "level": "N5"},
    {"jp": "てくび", "uz": "qo'l bilayi", "level": "N5"}, {"jp": "あしくび", "uz": "oyoq bilayi", "level": "N5"},
    {"jp": "まゆげ", "uz": "qoshlar", "level": "N5"}, {"jp": "しょうげ", "uz": "kirpiklar", "level": "N5"},
    {"jp": "ほお", "uz": "yanaklar", "level": "N5"}, {"jp": "くちびる", "uz": "lablar", "level": "N5"},
    {"jp": "あご", "uz": "jag'i", "level": "N5"}, {"jp": "のど", "uz": "har", "level": "N5"},
    {"jp": "はい", "uz": "o'pka", "level": "N5"}, {"jp": "しんぞう", "uz": "yurak", "level": "N5"},
    {"jp": "かんぞう", "uz": "jigar", "level": "N5"}, {"jp": "い", "uz": "oshqozon", "level": "N5"},
    {"jp": "ちょう", "uz": "ichak", "level": "N5"}, {"jp": "じんぞう", "uz": "buyrak", "level": "N5"},
    {"jp": "ぼうこう", "uz": "shushsha pufak", "level": "N5"}, {"jp": "けっかん", "uz": "qon tomir", "level": "N5"},
    {"jp": "ほね", "uz": "suyak", "level": "N5"}, {"jp": "かんせつ", "uz": "bo'g'in", "level": "N5"},
    {"jp": "きんにく", "uz": "mushak", "level": "N5"}, {"jp": "しぼう", "uz": "yog'", "level": "N5"},
    {"jp": "ひふ", "uz": "teri", "level": "N5"}, {"jp": "けつ", "uz": "qon", "level": "N5"},
    
    # Family
    {"jp": "ちち", "uz": "ota", "level": "N5"}, {"jp": "かあ", "uz": "ona", "level": "N5"},
    {"jp": "あに", "uz": "akam", "level": "N5"}, {"jp": "おとうと", "uz": "ukam", "level": "N5"},
    {"jp": "あね", "uz": "opam", "level": "N5"}, {"jp": "いもうと", "uz": "singlim", "level": "N5"},
    {"jp": "そふ", "uz": "buva", "level": "N5"}, {"jp": "そぼ", "uz": "buvi", "level": "N5"},
    {"jp": "おじさん", "uz": "amaki", "level": "N5"}, {"jp": "おばさん", "uz": "amakasi", "level": "N5"},
    {"jp": "いとこ", "uz": "amakaning o'g'li", "level": "N5"}, {"jp": "はいぐうしゃ", "uz": "turmush o'rtogi", "level": "N5"},
    {"jp": "こども", "uz": "bola", "level": "N5"}, {"jp": "むすこ", "uz": "o'g'li", "level": "N5"},
    {"jp": "むすめ", "uz": "qizi", "level": "N5"}, {"jp": "まご", "uz": "nemasi", "level": "N5"},
    {"jp": "ぎふ", "uz": "k'oyingiz ota", "level": "N5"}, {"jp": "ぎぼ", "uz": "k'oyingiz ona", "level": "N5"},
    {"jp": "けいふ", "uz": "o'rinbosamiz", "level": "N5"}, {"jp": "けいぼ", "uz": "o'rinbosamiz", "level": "N5"},
    {"jp": "きょうだい", "uz": "aka-uka", "level": "N5"}, {"jp": "しまい", "uz": "opa-singal", "level": "N5"},
    {"jp": "ふうふ", "uz": "odam-ayol", "level": "N5"}, {"jp": "つま", "uz": "hotina", "level": "N5"},
    {"jp": "おっと", "uz": "eri", "level": "N5"}, {"jp": "りょうしん", "uz": "ota-ona", "level": "N5"},
    {"jp": "しんゆう", "uz": "yaqin do'st", "level": "N4"}, {"jp": "どうりょう", "uz": "hamkasb", "level": "N4"},
    {"jp": "どうきゅうせい", "uz": "bir sinfdagi", "level": "N4"}, {"jp": "せんぱい", "uz": "katta", "level": "N4"},
    {"jp": "こうはい", "uz": "kichik", "level": "N4"}, {"jp": "ししょう", "uz": "o'qituvchi", "level": "N4"},
    
    # Original words (fixed - hiragana/katakana)
    {"jp": "あさ", "uz": "ertalab", "level": "N5"}, {"jp": "いぬ", "uz": "it", "level": "N5"},
    {"jp": "みせ", "uz": "do'kon", "level": "N5"}, {"jp": "ともだち", "uz": "do'st", "level": "N5"},
    {"jp": "しけん", "uz": "imtihon", "level": "N4"}, {"jp": "あぶない", "uz": "xavfli", "level": "N5"},
    {"jp": "いしゃ", "uz": "shifokor", "level": "N5"}, {"jp": "おくる", "uz": "yubormoq", "level": "N5"},
    {"jp": "おみやげ", "uz": "sovg'a", "level": "N5"}, {"jp": "かいもの", "uz": "xarid", "level": "N5"},
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
    {"jp": "とうちゃく", "uz": "yetib kelish", "level": "N4"}, {"jp": "あつめる", "uz": "yig'moq", "level": "N4"},
    {"jp": "わかれる", "uz": "ajralishmoq", "level": "N4"}, {"jp": "せまい", "uz": "tor", "level": "N4"},
    {"jp": "ひろい", "uz": "keng", "level": "N4"}, {"jp": "くらい", "uz": "qorong'u", "level": "N4"},
    {"jp": "さいきん", "uz": "shu kunlarda", "level": "N4"}, {"jp": "こんど", "uz": "keyingi safar", "level": "N4"},
    {"jp": "あいさつ", "uz": "salomlashish", "level": "N4"}, {"jp": "あじ", "uz": "ta'm / maza", "level": "N4"},
    {"jp": "あした", "uz": "ertaga", "level": "N5"}, {"jp": "あたま", "uz": "bosh", "level": "N5"},
    {"jp": "あつい", "uz": "issiq", "level": "N5"}, {"jp": "あぶら", "uz": "yog'", "level": "N4"},
    {"jp": "あめ", "uz": "yomg'ir", "level": "N5"}, {"jp": "あんしん", "uz": "xotirjamlik", "level": "N4"},
    {"jp": "あんない", "uz": "boshlash", "level": "N4"}, {"jp": "いい", "uz": "yaxshi", "level": "N5"},
    {"jp": "いえ", "uz": "uy", "level": "N5"}, {"jp": "いけ", "uz": "hovuz", "level": "N5"},
    {"jp": "いけん", "uz": "fikr", "level": "N4"}, {"jp": "いそがしい", "uz": "band", "level": "N5"},
    {"jp": "いたい", "uz": "og'riqli", "level": "N5"}, {"jp": "いちば", "uz": "bozor", "level": "N4"}
]

def main_menu_keyboard(user_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📊 Kanji Test", "📝 So'z Test (N4/N5)")
    markup.add("🏆 Reyting (Top-10)", "👤 Shaxsiy Profil")
    markup.add("❓ Adminga murojaat")
    # Faqat admin kirganda menyuning eng tagiga maxsus tugmalar qo'shiladi
    if user_id == ADMIN_ID:
        markup.add("📊 Admin: Statistika", "📣 Admin: Xabar Yuborish")
    return markup

@bot.message_handler(commands=['stats'], func=lambda m: m.chat.id == ADMIN_ID)
def get_bot_stats(m):
    db = load_db()
    total_users = len(db)
    if total_users > 0:
        top_user = max(db.values(), key=lambda x: x.get("points", 0))
        top_name = top_user.get("name", "Noma'lum")
        top_points = top_user.get("points", 0)
        bonus_text = f"🏆 Eng ko'p ball to'plagan: <b>{top_name}</b> ({top_points} ball)"
    else:
        bonus_text = "🚫 Hozircha foydalanuvchilar yo'q."

    text = f"📊 <b>Bot Statistikasi:</b>\n\n👥 Jami foydalanuvchilar: <b>{total_users} ta odam</b>\n{bonus_text}"
    bot.send_message(ADMIN_ID, text, parse_mode="HTML")

@bot.message_handler(commands=['sendall'], func=lambda m: m.chat.id == ADMIN_ID)
def send_all_prompt(m):
    msg = bot.send_message(ADMIN_ID, "📣 Hammaga yuboriladigan xabar matnini (yoki rasm/video) kiriting:")
    bot.register_next_step_handler(msg, start_broadcasting)

def start_broadcasting(m):
    db = load_db()
    uids = list(db.keys())
    total_users = len(uids)
    if total_users == 0:
        bot.send_message(ADMIN_ID, "❌ Bazada birorta ham foydalanuvchi yo'q.")
        return
    bot.send_message(ADMIN_ID, f"🚀 {total_users} ta foydalanuvchiga xabar yuborish boshlandi...")
    success, failed = 0, 0
    for uid in uids:
        try:
            bot.copy_message(chat_id=int(uid), from_chat_id=ADMIN_ID, message_id=m.message_id)
            success += 1
        except Exception:
            failed += 1
    bot.send_message(ADMIN_ID, f"📊 **Rassilka yakunlandi!**\n\n✅ Muvaffaqiyatli: {success} ta\n❌ Bloklaganlar: {failed} ta", parse_mode="Markdown")

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
        update_user_stats(chat_id, name, points_to_add=earned_points)
        
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(chat_id)), 999)
        
        leaderboard = "🏆 <b>SHOHONA REYTING JADVALI (TOP-5):</b>\n====================\n"
        for idx, (uid, uinfo) in enumerate(sorted_users[:5]):
            leaderboard += f"{idx+1}. {get_rank_title(idx+1)} | <b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
        leaderboard += "====================\n"
        
        bot.send_message(
            chat_id, 
            f"🎉 <b>Test yakunlandi!</b>\n✅ Natijangiz: <b>{s['correct_count']}/{s['total']} ta</b>\n💰 Bonus: <b>+{earned_points} ball</b>\n"
            f"📈 Joriy o'rningiz: <b>{user_place}-o'rin</b>\n\n" + leaderboard, 
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

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message)
def admin_reply(m):
    try:
        if m.reply_to_message.forward_from:
            uid = m.reply_to_message.forward_from.id
        else:
            lines = m.reply_to_message.text.split("\n")
            id_line = [l for l in lines if "User ID:" in l][0]
            uid = int(id_line.split("User ID:")[1].strip())
            
        bot.copy_message(uid, ADMIN_ID, m.message_id)
        bot.send_message(ADMIN_ID, "✅ Yuborildi.")
    except Exception as e: 
        bot.send_message(ADMIN_ID, f"❌ Xato: {e}")

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
                output += f"{place:02d}. {get_rank_title(place)} | <b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
            output += "====================\n"
            output += f"📈 Sizning o'rningiz: <b>{user_place}-o'rin</b>"
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

        if txt == "📊 Admin: Statistika" and cid == ADMIN_ID:
            get_bot_stats(m); return

        if txt == "📣 Admin: Xabar Yuborish" and cid == ADMIN_ID:
            send_all_prompt(m); return

    if txt == "❓ Adminga murojaat":
        bot.send_message(cid, "✉️ Xabaringizni kiriting. Admin tez orada javob beradi:", reply_markup=main_menu_keyboard(cid))
        return

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

    if not str(cid).startswith("-") and cid != ADMIN_ID:
        bot.forward_message(ADMIN_ID, cid, m.message_id)
        bot.send_message(ADMIN_ID, f"📩 <b>Yangi xabar!</b>\nUser ID: {cid}\n\nJavob berish uchun <b>Reply</b> qiling.", parse_mode="HTML")
        bot.send_message(cid, "⏱ Xabaringiz adminga yetkazildi.")

if __name__ == "__main__":
    bot.remove_webhook()
    print("Bot muvaffaqiyatli ishga tushdi...")
    bot.infinity_polling()
