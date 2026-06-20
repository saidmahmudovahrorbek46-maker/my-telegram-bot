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
    {"jp": "すみません", "uz": "kechirasiz", "level": "N5"}, {"jp": "お疲れ様です", "uz": "hastalik uchun rahmat", "level": "N5"},
    
    # Colors
    {"jp": "赤い", "uz": "qizil", "level": "N5"}, {"jp": "青い", "uz": "ko'k", "level": "N5"},
    {"jp": "黄色い", "uz": "sariq", "level": "N5"}, {"jp": "黒い", "uz": "qora", "level": "N5"},
    {"jp": "白い", "uz": "oq", "level": "N5"}, {"jp": "緑色", "uz": "yashil", "level": "N5"},
    {"jp": "紫色", "uz": "binafshayi", "level": "N5"}, {"jp": "オレンジ", "uz": "apelsin rangi", "level": "N5"},
    {"jp": "ピンク", "uz": "pushti", "level": "N5"}, {"jp": "gray", "uz": "kulrang", "level": "N5"},
    {"jp": "茶色", "uz": "jigarrang", "level": "N5"}, {"jp": "濃い", "uz": "quyuq", "level": "N5"},
    {"jp": "淡い", "uz": "engil", "level": "N5"}, {"jp": "明るい", "uz": "yorug'", "level": "N5"},
    {"jp": "暗い", "uz": "qorong'u", "level": "N5"}, {"jp": "鮮やか", "uz": "yorqin", "level": "N4"},
    {"jp": "光沢", "uz": "yaltiroq", "level": "N4"}, {"jp": "艶", "uz": "lalmi", "level": "N4"},
    {"jp": "くすんだ", "uz": "xira", "level": "N4"}, {"jp": "真っ白", "uz": "sof oq", "level": "N4"},
    {"jp": "深い", "uz": "chuqur", "level": "N4"}, {"jp": "浅い", "uz": "soyaroq", "level": "N4"},
    {"jp": "濃紫", "uz": "quyuq binafshayi", "level": "N4"}, {"jp": "薄紫", "uz": "engil binafshayi", "level": "N4"},
    {"jp": "辛子色", "uz": "sargarbarg", "level": "N4"}, {"jp": "鉄紺", "uz": "qo'ra ko'k", "level": "N4"},
    {"jp": "金色", "uz": "oltin rangi", "level": "N4"}, {"jp": "銀色", "uz": "kumush rangi", "level": "N4"},
    
    # Food
    {"jp": "米", "uz": "bug'doy", "level": "N5"}, {"jp": "魚", "uz": "baliq", "level": "N5"},
    {"jp": "肉", "uz": "go'sht", "level": "N5"}, {"jp": "野菜", "uz": "sabzavot", "level": "N5"},
    {"jp": "果物", "uz": "meva", "level": "N5"}, {"jp": "パン", "uz": "non", "level": "N5"},
    {"jp": "スープ", "uz": "shorba", "level": "N5"}, {"jp": "ご飯", "uz": "plov", "level": "N5"},
    {"jp": "味噌汁", "uz": "miso shorba", "level": "N5"}, {"jp": "天ぷら", "uz": "tempura", "level": "N5"},
    {"jp": "寿司", "uz": "sushi", "level": "N5"}, {"jp": "そば", "uz": "Yapon makaron", "level": "N5"},
    {"jp": "うどん", "uz": "udon", "level": "N5"}, {"jp": "ラーメン", "uz": "ramen", "level": "N5"},
    {"jp": "卵", "uz": "tuxum", "level": "N5"}, {"jp": "牛乳", "uz": "sut", "level": "N5"},
    {"jp": "チーズ", "uz": "pishloq", "level": "N5"}, {"jp": "バター", "uz": "moy", "level": "N5"},
    {"jp": "塩", "uz": "tuz", "level": "N5"}, {"jp": "砂糖", "uz": "qand", "level": "N5"},
    {"jp": "醤油", "uz": "soy susi", "level": "N5"}, {"jp": "油", "uz": "yog'", "level": "N5"},
    {"jp": "酢", "uz": "sirka", "level": "N5"}, {"jp": "胡椒", "uz": "qora ziravo'y", "level": "N5"},
    {"jp": "唐辛子", "uz": "qizil qalampir", "level": "N5"}, {"jp": "はちみつ", "uz": "asal", "level": "N5"},
    {"jp": "ジャム", "uz": "murabbо", "level": "N5"}, {"jp": "ピーナッツ", "uz": "arахис", "level": "N5"},
    {"jp": "アーモンド", "uz": "badom", "level": "N5"}, {"jp": "クッキー", "uz": "печенье", "level": "N5"},
    {"jp": "ケーキ", "uz": "keks", "level": "N5"}, {"jp": "アイスクリーム", "uz": "muzqaymoq", "level": "N5"},
    {"jp": "チョコレート", "uz": "shokolad", "level": "N5"}, {"jp": "キャンディ", "uz": "salyut", "level": "N5"},
    {"jp": "リンゴ", "uz": "olma", "level": "N5"}, {"jp": "バナナ", "uz": "banan", "level": "N5"},
    {"jp": "オレンジ", "uz": "apelsin", "level": "N5"}, {"jp": "イチゴ", "uz": "qulupnay", "level": "N5"},
    {"jp": "ぶどう", "uz": "uzum", "level": "N5"}, {"jp": "スイカ", "uz": "qovun", "level": "N5"},
    {"jp": "メロン", "uz": "qovun", "level": "N5"}, {"jp": "レモン", "uz": "limon", "level": "N5"},
    {"jp": "ライム", "uz": "laym", "level": "N5"}, {"jp": "モモ", "uz": "shaftoli", "level": "N5"},
    {"jp": "アボカド", "uz": "avokado", "level": "N5"}, {"jp": "トマト", "uz": "pomidor", "level": "N5"},
    {"jp": "ニンジン", "uz": "sabzi", "level": "N5"}, {"jp": "じゃがいも", "uz": "kartoshka", "level": "N5"},
    {"jp": "玉ねぎ", "uz": "piyoz", "level": "N5"}, {"jp": "ニンニク", "uz": "sarmsaq", "level": "N5"},
    {"jp": "キャベツ", "uz": "karam", "level": "N5"}, {"jp": "ブロッコリー", "uz": "koloflor", "level": "N5"},
    {"jp": "キュウリ", "uz": "bodring", "level": "N5"}, {"jp": "ピーマン", "uz": "bolgar kalampir", "level": "N5"},
    {"jp": "レタス", "uz": "tuz piyozi", "level": "N5"}, {"jp": "スピナッチ", "uz": "paluq", "level": "N5"},
    {"jp": "トウモロコシ", "uz": "misai", "level": "N5"}, {"jp": "豆", "uz": "loviya", "level": "N5"},
    {"jp": "牡蠣", "uz": "ustirka", "level": "N5"}, {"jp": "エビ", "uz": "kreveti", "level": "N5"},
    {"jp": "カニ", "uz": "krab", "level": "N5"}, {"jp": "タコ", "uz": "osminog", "level": "N5"},
    {"jp": "イカ", "uz": "smutskalmar", "level": "N5"}, {"jp": "貝", "uz": "qo'ng'ir", "level": "N5"},
    
    # Animals
    {"jp": "猫", "uz": "mushuk", "level": "N5"}, {"jp": "犬", "uz": "it", "level": "N5"},
    {"jp": "鳥", "uz": "qush", "level": "N5"}, {"jp": "魚", "uz": "baliq", "level": "N5"},
    {"jp": "牛", "uz": "sigir", "level": "N5"}, {"jp": "豚", "uz": "cho'chqa", "level": "N5"},
    {"jp": "馬", "uz": "ot", "level": "N5"}, {"jp": "羊", "uz": "qo'y", "level": "N5"},
    {"jp": "ウサギ", "uz": "quyon", "level": "N5"}, {"jp": "ネズミ", "uz": "sichqon", "level": "N5"},
    {"jp": "蛇", "uz": "ilon", "level": "N5"}, {"jp": "トンボ", "uz": "subbaiy", "level": "N5"},
    {"jp": "蜘蛛", "uz": "o'rgimchak", "level": "N5"}, {"jp": "蝶", "uz": "kapalak", "level": "N5"},
    {"jp": "ハチ", "uz": "ari", "level": "N5"}, {"jp": "ミツバチ", "uz": "ari", "level": "N5"},
    {"jp": "蛙", "uz": "qo'ng'iz", "level": "N5"}, {"jp": "カメ", "uz": "toshbaqa", "level": "N5"},
    {"jp": "ワニ", "uz": "timsoh", "level": "N5"}, {"jp": "ペンギン", "uz": "pingvin", "level": "N5"},
    {"jp": "フクロウ", "uz": "boʻrino", "level": "N5"}, {"jp": "ワシ", "uz": "burgut", "level": "N5"},
    {"jp": "ダチョウ", "uz": "ot quvi", "level": "N5"}, {"jp": "ペンダ", "uz": "panda", "level": "N5"},
    {"jp": "ライオン", "uz": "arslon", "level": "N5"}, {"jp": "トラ", "uz": "yo'lokchi", "level": "N5"},
    {"jp": "豹", "uz": "leopard", "level": "N5"}, {"jp": "象", "uz": "fil", "level": "N5"},
    {"jp": "キリン", "uz": "ziraffe", "level": "N5"}, {"jp": "シマウマ", "uz": "zebra", "level": "N5"},
    {"jp": "熊", "uz": "ayiqq", "level": "N5"}, {"jp": "アルパカ", "uz": "alpaka", "level": "N5"},
    {"jp": "ラッパ", "uz": "latun", "level": "N5"}, {"jp": "カモ", "uz": "o't o'rigi", "level": "N5"},
    {"jp": "白鳥", "uz": "qug'u", "level": "N5"}, {"jp": "クジラ", "uz": "kit", "level": "N5"},
    {"jp": "アザラシ", "uz": "mo'rin it", "level": "N5"}, {"jp": "ゴリラ", "uz": "gorilla", "level": "N5"},
    {"jp": "サル", "uz": "maymun", "level": "N5"}, {"jp": "スカンク", "uz": "scunk", "level": "N5"},
    {"jp": "ヤマアラシ", "uz": "tikanbilgan", "level": "N5"}, {"jp": "ハリネズミ", "uz": "sanchqi", "level": "N5"},
    
    # Weather
    {"jp": "晴天", "uz": "toza asman", "level": "N5"}, {"jp": "雨", "uz": "yomg'ir", "level": "N5"},
    {"jp": "雪", "uz": "qor", "level": "N5"}, {"jp": "風", "uz": "shamol", "level": "N5"},
    {"jp": "曇り", "uz": "bulutli", "level": "N5"}, {"jp": "霧", "uz": "tuman", "level": "N5"},
    {"jp": "雷", "uz": "chergi", "level": "N5"}, {"jp": "台風", "uz": "tayfun", "level": "N5"},
    {"jp": "温度", "uz": "harorat", "level": "N5"}, {"jp": "湿度", "uz": "namlik", "level": "N5"},
    {"jp": "暴雨", "uz": "shiddatli yomg'ir", "level": "N4"}, {"jp": "吹雪", "uz": "qor bo'ronasi", "level": "N4"},
    {"jp": "晴れ", "uz": "toza", "level": "N5"}, {"jp": "曇り空", "uz": "bulutli asman", "level": "N5"},
    {"jp": "虹", "uz": "kamonli", "level": "N5"}, {"jp": "雹", "uz": "shusha qor", "level": "N4"},
    {"jp": "露", "uz": "shab", "level": "N4"}, {"jp": "霜", "uz": "qirg'oq", "level": "N4"},
    {"jp": "そよ風", "uz": "engil shamol", "level": "N4"}, {"jp": "向風", "uz": "boshga shamol", "level": "N4"},
    {"jp": "炎天下", "uz": "qaynoq quyosh ostida", "level": "N4"}, {"jp": "凍結", "uz": "muzlab ketish", "level": "N4"},
    {"jp": "融ける", "uz": "erib ketish", "level": "N4"}, {"jp": "乾燥", "uz": "quruq", "level": "N4"},
    {"jp": "蒸し暑い", "uz": "nam va issiq", "level": "N4"}, {"jp": "雨季", "uz": "yomg'ir faslı", "level": "N4"},
    {"jp": "乾季", "uz": "quruq faslı", "level": "N4"}, {"jp": "四季", "uz": "to'rt fasl", "level": "N4"},
    
    # Body Parts
    {"jp": "目", "uz": "ko'z", "level": "N5"}, {"jp": "耳", "uz": "quloq", "level": "N5"},
    {"jp": "鼻", "uz": "burun", "level": "N5"}, {"jp": "口", "uz": "og'iz", "level": "N5"},
    {"jp": "歯", "uz": "tish", "level": "N5"}, {"jp": "舌", "uz": "til", "level": "N5"},
    {"jp": "手", "uz": "qo'l", "level": "N5"}, {"jp": "足", "uz": "oyoq", "level": "N5"},
    {"jp": "指", "uz": "barmoq", "level": "N5"}, {"jp": "爪", "uz": "tirnoq", "level": "N5"},
    {"jp": "髪", "uz": "soch", "level": "N5"}, {"jp": "顔", "uz": "yuz", "level": "N5"},
    {"jp": "首", "uz": "bo'yin", "level": "N5"}, {"jp": "肩", "uz": "yelka", "level": "N5"},
    {"jp": "背", "uz": "orqa", "level": "N5"}, {"jp": "胸", "uz": "ko'krak", "level": "N5"},
    {"jp": "腰", "uz": "yo'n", "level": "N5"}, {"jp": "腕", "uz": "bazu", "level": "N5"},
    {"jp": "膝", "uz": "tizzasi", "level": "N5"}, {"jp": "肘", "uz": "tirsak", "level": "N5"},
    {"jp": "手首", "uz": "qo'l bilayi", "level": "N5"}, {"jp": "足首", "uz": "oyoq bilayi", "level": "N5"},
    {"jp": "眉毛", "uz": "qoshlar", "level": "N5"}, {"jp": "睫毛", "uz": "kirpiklar", "level": "N5"},
    {"jp": "頬", "uz": "yanaklar", "level": "N5"}, {"jp": "唇", "uz": "lablar", "level": "N5"},
    {"jp": "顎", "uz": "jag'i", "level": "N5"}, {"jp": "喉", "uz": "har", "level": "N5"},
    {"jp": "肺", "uz": "o'pka", "level": "N5"}, {"jp": "心臓", "uz": "yurak", "level": "N5"},
    {"jp": "肝臓", "uz": "jigar", "level": "N5"}, {"jp": "胃", "uz": "oshqozon", "level": "N5"},
    {"jp": "腸", "uz": "ichak", "level": "N5"}, {"jp": "腎臓", "uz": "buyrak", "level": "N5"},
    {"jp": "膀胱", "uz": "shushsha pufak", "level": "N5"}, {"jp": "血管", "uz": "qon tomir", "level": "N5"},
    {"jp": "骨", "uz": "suyak", "level": "N5"}, {"jp": "関節", "uz": "bo'g'in", "level": "N5"},
    {"jp": "筋肉", "uz": "mushak", "level": "N5"}, {"jp": "脂肪", "uz": "yog'", "level": "N5"},
    {"jp": "皮膚", "uz": "teri", "level": "N5"}, {"jp": "血", "uz": "qon", "level": "N5"},
    
    # Family
    {"jp": "父", "uz": "ota", "level": "N5"}, {"jp": "母", "uz": "ona", "level": "N5"},
    {"jp": "兄", "uz": "akam", "level": "N5"}, {"jp": "弟", "uz": "ukam", "level": "N5"},
    {"jp": "姉", "uz": "opam", "level": "N5"}, {"jp": "妹", "uz": "singlim", "level": "N5"},
    {"jp": "祖父", "uz": "buva", "level": "N5"}, {"jp": "祖母", "uz": "buvi", "level": "N5"},
    {"jp": "叔父", "uz": "amaki", "level": "N5"}, {"jp": "叔母", "uz": "amakasi", "level": "N5"},
    {"jp": "従兄", "uz": "amakaning o'g'li", "level": "N5"}, {"jp": "配偶者", "uz": "turmush o'rtogi", "level": "N5"},
    {"jp": "子供", "uz": "bola", "level": "N5"}, {"jp": "息子", "uz": "o'g'li", "level": "N5"},
    {"jp": "娘", "uz": "qizi", "level": "N5"}, {"jp": "孫", "uz": "nemasi", "level": "N5"},
    {"jp": "義父", "uz": "k'oyingiz ota", "level": "N5"}, {"jp": "義母", "uz": "k'oyingiz ona", "level": "N5"},
    {"jp": "継父", "uz": "o'rinbosamiz", "level": "N5"}, {"jp": "継母", "uz": "o'rinbosamiz", "level": "N5"},
    {"jp": "兄弟", "uz": "aka-uka", "level": "N5"}, {"jp": "姉妹", "uz": "opa-singal", "level": "N5"},
    {"jp": "夫婦", "uz": "odam-ayol", "level": "N5"}, {"jp": "妻", "uz": "hotina", "level": "N5"},
    {"jp": "夫", "uz": "eri", "level": "N5"}, {"jp": "両親", "uz": "ota-ona", "level": "N5"},
    {"jp": "親友", "uz": "yaqin do'st", "level": "N4"}, {"jp": "同僚", "uz": "hamkasb", "level": "N4"},
    {"jp": "同級生", "uz": "bir sinfdagi", "level": "N4"}, {"jp": "先輩", "uz": "katta", "level": "N4"},
    {"jp": "後輩", "uz": "kichik", "level": "N4"}, {"jp": "師匠", "uz": "o'qituvchi", "level": "N4"},
    
    # Original words (fixed)
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
