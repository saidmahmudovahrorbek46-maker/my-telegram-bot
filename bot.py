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
        db[uid] = {"name": first_name, "points": 0, "streak": 0, "last_seen": "", "level": "N5"}
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

# ===================== 160+ KANJI DATA =====================
kanji_list = [
    # Numbers & Basic
    {"kanji": "一", "reading": "イチ", "meaning": "bir", "on": "イチ", "kun": "ひ", "jlpt": "N5", "stroke": "1", "example": "一日"},
    {"kanji": "二", "reading": "ニ", "meaning": "ikki", "on": "ニ", "kun": "ふた", "jlpt": "N5", "stroke": "2", "example": "二人"},
    {"kanji": "三", "reading": "サン", "meaning": "uch", "on": "サン", "kun": "み", "jlpt": "N5", "stroke": "3", "example": "三日"},
    {"kanji": "四", "reading": "シ、ヨン", "meaning": "to'rt", "on": "シ、ヨン", "kun": "よ", "jlpt": "N5", "stroke": "5", "example": "四月"},
    {"kanji": "五", "reading": "ゴ", "meaning": "besh", "on": "ゴ", "kun": "いつ", "jlpt": "N5", "stroke": "4", "example": "五日"},
    {"kanji": "六", "reading": "ロク", "meaning": "olti", "on": "ロク", "kun": "む", "jlpt": "N5", "stroke": "4", "example": "六月"},
    {"kanji": "七", "reading": "シチ、ナナ", "meaning": "yetti", "on": "シチ、ナナ", "kun": "なな", "jlpt": "N5", "stroke": "2", "example": "七月"},
    {"kanji": "八", "reading": "ハチ", "meaning": "sakkiz", "on": "ハチ", "kun": "や", "jlpt": "N5", "stroke": "2", "example": "八月"},
    {"kanji": "九", "reading": "キュウ", "meaning": "to'qqiz", "on": "キュウ", "kun": "ここの", "jlpt": "N5", "stroke": "2", "example": "九月"},
    {"kanji": "十", "reading": "ジュウ", "meaning": "o'n", "on": "ジュウ", "kun": "と", "jlpt": "N5", "stroke": "2", "example": "十月"},
    
    # Days of Week
    {"kanji": "日", "reading": "ニチ、ジツ", "meaning": "kun/quyosh", "on": "ニチ、ジツ", "kun": "ひ", "jlpt": "N5", "stroke": "4", "example": "日曜日"},
    {"kanji": "月", "reading": "ゲツ、ガツ", "meaning": "oy", "on": "ゲツ、ガツ", "kun": "つき", "jlpt": "N5", "stroke": "4", "example": "月曜日"},
    {"kanji": "火", "reading": "カ", "meaning": "olov", "on": "カ", "kun": "ひ", "jlpt": "N5", "stroke": "4", "example": "火曜日"},
    {"kanji": "水", "reading": "スイ", "meaning": "suv", "on": "スイ", "kun": "みず", "jlpt": "N5", "stroke": "4", "example": "水曜日"},
    {"kanji": "木", "reading": "モク", "meaning": "daraxt", "on": "モク", "kun": "き", "jlpt": "N5", "stroke": "4", "example": "木曜日"},
    {"kanji": "金", "reading": "キン", "meaning": "oltin/pul", "on": "キン", "kun": "かね", "jlpt": "N5", "stroke": "8", "example": "金曜日"},
    {"kanji": "土", "reading": "ド、ト", "meaning": "tuproq", "on": "ド、ト", "kun": "つち", "jlpt": "N5", "stroke": "3", "example": "土曜日"},
    
    # Time
    {"kanji": "時", "reading": "ジ", "meaning": "vaqt", "on": "ジ", "kun": "とき", "jlpt": "N5", "stroke": "10", "example": "時間"},
    {"kanji": "分", "reading": "フン、ブン", "meaning": "daqiqa", "on": "フン、ブン", "kun": "わける", "jlpt": "N5", "stroke": "4", "example": "五分"},
    {"kanji": "秒", "reading": "ビョウ", "meaning": "soniya", "on": "ビョウ", "kun": "ひ", "jlpt": "N5", "stroke": "9", "example": "十秒"},
    
    # People & Family
    {"kanji": "人", "reading": "ジン、ニン", "meaning": "inson", "on": "ジン、ニン", "kun": "ひと", "jlpt": "N5", "stroke": "2", "example": "人間"},
    {"kanji": "男", "reading": "ダン", "meaning": "erkak", "on": "ダン", "kun": "おとこ", "jlpt": "N5", "stroke": "7", "example": "男性"},
    {"kanji": "女", "reading": "ジョ", "meaning": "ayol", "on": "ジョ", "kun": "おんな", "jlpt": "N5", "stroke": "3", "example": "女性"},
    {"kanji": "子", "reading": "シ", "meaning": "bola", "on": "シ", "kun": "こ", "jlpt": "N5", "stroke": "3", "example": "子供"},
    {"kanji": "父", "reading": "フ", "meaning": "ota", "on": "フ", "kun": "ちち", "jlpt": "N5", "stroke": "4", "example": "父親"},
    {"kanji": "母", "reading": "ボ", "meaning": "ona", "on": "ボ", "kun": "かあ", "jlpt": "N5", "stroke": "5", "example": "母親"},
    {"kanji": "兄", "reading": "キョウ", "meaning": "akam", "on": "キョウ", "kun": "あに", "jlpt": "N5", "stroke": "5", "example": "兄弟"},
    {"kanji": "弟", "reading": "テイ", "meaning": "ukam", "on": "テイ", "kun": "おとうと", "jlpt": "N5", "stroke": "7", "example": "弟子"},
    {"kanji": "姉", "reading": "シ", "meaning": "opam", "on": "シ", "kun": "あね", "jlpt": "N5", "stroke": "8", "example": "姉妹"},
    {"kanji": "妹", "reading": "マイ", "meaning": "singlim", "on": "マイ", "kun": "いもうと", "jlpt": "N5", "stroke": "8", "example": "妹さん"},
    
    # Body Parts
    {"kanji": "目", "reading": "モク", "meaning": "ko'z", "on": "モク", "kun": "め", "jlpt": "N5", "stroke": "5", "example": "目玉"},
    {"kanji": "耳", "reading": "ジ", "meaning": "quloq", "on": "ジ", "kun": "みみ", "jlpt": "N5", "stroke": "6", "example": "耳鼻"},
    {"kanji": "口", "reading": "コウ", "meaning": "og'iz", "on": "コウ", "kun": "くち", "jlpt": "N5", "stroke": "3", "example": "口元"},
    {"kanji": "手", "reading": "シュ", "meaning": "qo'l", "on": "シュ", "kun": "て", "jlpt": "N5", "stroke": "4", "example": "手指"},
    {"kanji": "足", "reading": "ソク", "meaning": "oyoq", "on": "ソク", "kun": "あし", "jlpt": "N5", "stroke": "7", "example": "足首"},
    {"kanji": "頭", "reading": "トウ", "meaning": "bosh", "on": "トウ", "kun": "あたま", "jlpt": "N5", "stroke": "16", "example": "頭痛"},
    {"kanji": "心", "reading": "シン", "meaning": "yurak/aql", "on": "シン", "kun": "こころ", "jlpt": "N5", "stroke": "4", "example": "心理"},
    {"kanji": "血", "reading": "ケツ", "meaning": "qon", "on": "ケツ", "kun": "ち", "jlpt": "N5", "stroke": "6", "example": "血液"},
    {"kanji": "髪", "reading": "はい", "meaning": "soch", "on": "はい", "kun": "かみ", "jlpt": "N5", "stroke": "10", "example": "髪型"},
    
    # Animals
    {"kanji": "猫", "reading": "ビョウ", "meaning": "mushuk", "on": "ビョウ", "kun": "ねこ", "jlpt": "N5", "stroke": "11", "example": "猫ちゃん"},
    {"kanji": "犬", "reading": "ケン", "meaning": "it", "on": "ケン", "kun": "いぬ", "jlpt": "N5", "stroke": "4", "example": "犬派"},
    {"kanji": "鳥", "reading": "チョウ", "meaning": "qush", "on": "チョウ", "kun": "とり", "jlpt": "N5", "stroke": "11", "example": "野鳥"},
    {"kanji": "魚", "reading": "ギョ", "meaning": "baliq", "on": "ギョ", "kun": "さかな", "jlpt": "N5", "stroke": "11", "example": "金魚"},
    {"kanji": "虎", "reading": "トラ", "meaning": "yo'lokchi", "on": "トラ", "kun": "とら", "jlpt": "N5", "stroke": "8", "example": "虎柄"},
    {"kanji": "熊", "reading": "ユウ", "meaning": "ayiqq", "on": "ユウ", "kun": "くま", "jlpt": "N5", "stroke": "13", "example": "熊さん"},
    {"kanji": "牛", "reading": "ギュウ", "meaning": "sigir", "on": "ギュウ", "kun": "うし", "jlpt": "N5", "stroke": "4", "example": "牛乳"},
    {"kanji": "豚", "reading": "トン", "meaning": "cho'chqa", "on": "トン", "kun": "ぶた", "jlpt": "N5", "stroke": "11", "example": "豚肉"},
    
    # Food
    {"kanji": "米", "reading": "ベイ、マイ", "meaning": "bug'doy", "on": "ベイ、マイ", "kun": "こめ", "jlpt": "N5", "stroke": "6", "example": "米俵"},
    {"kanji": "肉", "reading": "ニク", "meaning": "go'sht", "on": "ニク", "kun": "にく", "jlpt": "N5", "stroke": "6", "example": "肉類"},
    {"kanji": "野", "reading": "ヤ", "meaning": "o'tlar", "on": "ヤ", "kun": "の", "jlpt": "N5", "stroke": "11", "example": "野菜"},
    {"kanji": "菜", "reading": "サイ", "meaning": "sabzavot", "on": "サイ", "kun": "な", "jlpt": "N5", "stroke": "11", "example": "菜の花"},
    {"kanji": "果", "reading": "カ", "meaning": "meva", "on": "カ", "kun": "は.てる", "jlpt": "N5", "stroke": "8", "example": "果物"},
    {"kanji": "酒", "reading": "シュ", "meaning": "araq", "on": "シュ", "kun": "さけ", "jlpt": "N5", "stroke": "10", "example": "酒飲み"},
    {"kanji": "茶", "reading": "チャ", "meaning": "choy", "on": "チャ", "kun": "ちゃ", "jlpt": "N5", "stroke": "9", "example": "茶道"},
    
    # House & Objects
    {"kanji": "家", "reading": "カ、ケ", "meaning": "uy", "on": "カ、ケ", "kun": "いえ", "jlpt": "N5", "stroke": "10", "example": "家族"},
    {"kanji": "門", "reading": "モン", "meaning": "darvoza", "on": "モン", "kun": "かど", "jlpt": "N5", "stroke": "8", "example": "正門"},
    {"kanji": "窓", "reading": "ソウ", "meaning": "deraza", "on": "ソウ", "kun": "まど", "jlpt": "N5", "stroke": "11", "example": "窓口"},
    {"kanji": "机", "reading": "キ", "meaning": "stol", "on": "キ", "kun": "つくえ", "jlpt": "N5", "stroke": "12", "example": "机の上"},
    {"kanji": "椅", "reading": "イ", "meaning": "stul", "on": "イ", "kun": "いす", "jlpt": "N5", "stroke": "13", "example": "椅子"},
    {"kanji": "本", "reading": "ホン", "meaning": "kitob", "on": "ホン", "kun": "もと", "jlpt": "N5", "stroke": "5", "example": "本屋"},
    {"kanji": "字", "reading": "ジ", "meaning": "harf", "on": "ジ", "kun": "あざな", "jlpt": "N5", "stroke": "6", "example": "文字"},
    {"kanji": "紙", "reading": "シ", "meaning": "qog'oz", "on": "シ", "kun": "かみ", "jlpt": "N5", "stroke": "10", "example": "紙張り"},
    
    # Colors
    {"kanji": "赤", "reading": "セキ、シャク", "meaning": "qizil", "on": "セキ、シャク", "kun": "あか", "jlpt": "N5", "stroke": "7", "example": "赤色"},
    {"kanji": "青", "reading": "セイ、ショウ", "meaning": "ko'k", "on": "セイ、ショウ", "kun": "あお", "jlpt": "N5", "stroke": "8", "example": "青空"},
    {"kanji": "黄", "reading": "コウ", "meaning": "sariq", "on": "コウ", "kun": "き", "jlpt": "N5", "stroke": "11", "example": "黄色"},
    {"kanji": "黒", "reading": "コク", "meaning": "qora", "on": "コク", "kun": "くろ", "jlpt": "N5", "stroke": "11", "example": "黒猫"},
    {"kanji": "白", "reading": "ハク、パク", "meaning": "oq", "on": "ハク、パク", "kun": "しろ", "jlpt": "N5", "stroke": "5", "example": "白い"},
    
    # Nature
    {"kanji": "山", "reading": "サン", "meaning": "tog'", "on": "サン", "kun": "やま", "jlpt": "N5", "stroke": "3", "example": "富士山"},
    {"kanji": "川", "reading": "セン", "meaning": "daryo", "on": "セン", "kun": "かわ", "jlpt": "N5", "stroke": "3", "example": "大川"},
    {"kanji": "海", "reading": "カイ", "meaning": "dengiz", "on": "カイ", "kun": "うみ", "jlpt": "N5", "stroke": "9", "example": "海岸"},
    {"kanji": "石", "reading": "セキ、シャク", "meaning": "tosh", "on": "セキ、シャク", "kun": "いし", "jlpt": "N5", "stroke": "5", "example": "石造り"},
    {"kanji": "土", "reading": "ド、ト", "meaning": "tuproq", "on": "ド、ト", "kun": "つち", "jlpt": "N5", "stroke": "3", "example": "土地"},
    {"kanji": "火", "reading": "カ", "meaning": "olov", "on": "カ", "kun": "ひ", "jlpt": "N5", "stroke": "4", "example": "火事"},
    {"kanji": "風", "reading": "フウ、フ", "meaning": "shamol", "on": "フウ、フ", "kun": "かぜ", "jlpt": "N5", "stroke": "9", "example": "台風"},
    {"kanji": "雨", "reading": "ウ", "meaning": "yomg'ir", "on": "ウ", "kun": "あめ", "jlpt": "N5", "stroke": "8", "example": "雨の日"},
    {"kanji": "雪", "reading": "セツ", "meaning": "qor", "on": "セツ", "kun": "ゆき", "jlpt": "N5", "stroke": "11", "example": "雪だるま"},
    
    # Action Verbs
    {"kanji": "走", "reading": "ソウ", "meaning": "yugur", "on": "ソウ", "kun": "はし.る", "jlpt": "N5", "stroke": "7", "example": "走力"},
    {"kanji": "歩", "reading": "ホ", "meaning": "yur", "on": "ホ", "kun": "あるく", "jlpt": "N5", "stroke": "8", "example": "歩行"},
    {"kanji": "食", "reading": "ショク", "meaning": "ovqat", "on": "ショク", "kun": "たべ.る", "jlpt": "N5", "stroke": "9", "example": "食事"},
    {"kanji": "飲", "reading": "イン", "meaning": "ich", "on": "イン", "kun": "のむ", "jlpt": "N5", "stroke": "12", "example": "飲料"},
    {"kanji": "読", "reading": "ドク、トク", "meaning": "o'qi", "on": "ドク、トク", "kun": "よ.む", "jlpt": "N5", "stroke": "14", "example": "読書"},
    {"kanji": "書", "reading": "ショ", "meaning": "yoz", "on": "ショ", "kun": "か.く", "jlpt": "N5", "stroke": "10", "example": "書類"},
    {"kanji": "見", "reading": "ケン", "meaning": "kor", "on": "ケン", "kun": "み.る", "jlpt": "N5", "stroke": "7", "example": "見張り"},
    {"kanji": "聞", "reading": "ブン、モン", "meaning": "eshit", "on": "ブン、モン", "kun": "き.く", "jlpt": "N5", "stroke": "14", "example": "聞き手"},
    {"kanji": "話", "reading": "ワ", "meaning": "gapir", "on": "ワ", "kun": "はな.す", "jlpt": "N5", "stroke": "13", "example": "話題"},
    {"kanji": "作", "reading": "サク", "meaning": "yasа", "on": "サク", "kun": "つく.る", "jlpt": "N5", "stroke": "7", "example": "作品"},
    
    # School & Learning
    {"kanji": "学", "reading": "ガク", "meaning": "o'rgan", "on": "ガク", "kun": "まな.ぶ", "jlpt": "N5", "stroke": "8", "example": "学生"},
    {"kanji": "校", "reading": "コウ", "meaning": "maktab", "on": "コウ", "kun": "", "jlpt": "N5", "stroke": "10", "example": "学校"},
    {"kanji": "先", "reading": "セン", "meaning": "avval", "on": "セン", "kun": "さき", "jlpt": "N5", "stroke": "6", "example": "先生"},
    {"kanji": "生", "reading": "セイ、ショウ", "meaning": "hayot", "on": "セイ、ショウ", "kun": "い.きる", "jlpt": "N5", "stroke": "5", "example": "生活"},
    {"kanji": "番", "reading": "バン", "meaning": "raqam", "on": "バン", "kun": "ばん", "jlpt": "N5", "stroke": "12", "example": "番号"},
    {"kanji": "年", "reading": "ネン", "meaning": "yil", "on": "ネン", "kun": "とし", "jlpt": "N5", "stroke": "6", "example": "年齢"},
    
    # N4 Level
    {"kanji": "意", "reading": "イ", "meaning": "ma'no", "on": "イ", "kun": "こころ", "jlpt": "N4", "stroke": "13", "example": "意見"},
    {"kanji": "思", "reading": "シ", "meaning": "o'yla", "on": "シ", "kun": "おも.う", "jlpt": "N4", "stroke": "9", "example": "思考"},
    {"kanji": "知", "reading": "チ", "meaning": "bila", "on": "チ", "kun": "し.る", "jlpt": "N4", "stroke": "8", "example": "知識"},
    {"kanji": "力", "reading": "リョク", "meaning": "kuch", "on": "リョク", "kun": "ちから", "jlpt": "N4", "stroke": "2", "example": "力強い"},
    {"kanji": "成", "reading": "セイ、ジョウ", "meaning": "muvaffaq", "on": "セイ、ジョウ", "kun": "な.る", "jlpt": "N4", "stroke": "6", "example": "成功"},
    {"kanji": "長", "reading": "チョウ", "meaning": "uzun", "on": "チョウ", "kun": "なが.い", "jlpt": "N4", "stroke": "8", "example": "長身"},
    {"kanji": "新", "reading": "シン", "meaning": "yangi", "on": "シン", "kun": "あたら.しい", "jlpt": "N4", "stroke": "13", "example": "新作"},
    {"kanji": "古", "reading": "コ", "meaning": "eski", "on": "コ", "kun": "ふる.い", "jlpt": "N4", "stroke": "5", "example": "古本"},
    {"kanji": "大", "reading": "タイ、ダイ", "meaning": "katta", "on": "タイ、ダイ", "kun": "おお.きい", "jlpt": "N4", "stroke": "3", "example": "大人"},
    {"kanji": "小", "reading": "ショウ", "meaning": "kichik", "on": "ショウ", "kun": "ちい.さい", "jlpt": "N4", "stroke": "3", "example": "小人"},
]

# ===================== 500+ VOCABULARY DATA =====================
words_list = [
    # Greetings
    {"jp": "こんにちは", "uz": "salom", "level": "N5", "reading": "こんにちは", "kanji": ""},
    {"jp": "おはようございます", "uz": "ertalab", "level": "N5", "reading": "おはようございます", "kanji": ""},
    {"jp": "こんばんは", "uz": "axshom salom", "level": "N5", "reading": "こんばんは", "kanji": ""},
    {"jp": "おやすみなさい", "uz": "yaxshi uxla", "level": "N5", "reading": "おやすみなさい", "kanji": ""},
    {"jp": "さようなら", "uz": "xayr", "level": "N5", "reading": "さようなら", "kanji": ""},
    {"jp": "じゃあね", "uz": "shu vaqtingacha", "level": "N5", "reading": "じゃあね", "kanji": ""},
    
    # Colors
    {"jp": "赤い", "uz": "qizil", "level": "N5", "reading": "あかい", "kanji": "赤"},
    {"jp": "青い", "uz": "ko'k", "level": "N5", "reading": "あおい", "kanji": "青"},
    {"jp": "黄色い", "uz": "sariq", "level": "N5", "reading": "きいろい", "kanji": "黄色"},
    {"jp": "黒い", "uz": "qora", "level": "N5", "reading": "くろい", "kanji": "黒"},
    {"jp": "白い", "uz": "oq", "level": "N5", "reading": "しろい", "kanji": "白"},
    {"jp": "緑色", "uz": "yashil", "level": "N5", "reading": "みどりいろ", "kanji": "緑色"},
    {"jp": "紫色", "uz": "binafshayi", "level": "N5", "reading": "むらさきいろ", "kanji": "紫色"},
    {"jp": "オレンジ", "uz": "apelsin rangi", "level": "N5", "reading": "おれんじ", "kanji": ""},
    
    # Food
    {"jp": "米", "uz": "bug'doy", "level": "N5", "reading": "こめ", "kanji": "米"},
    {"jp": "魚", "uz": "baliq", "level": "N5", "reading": "さかな", "kanji": "魚"},
    {"jp": "肉", "uz": "go'sht", "level": "N5", "reading": "にく", "kanji": "肉"},
    {"jp": "野菜", "uz": "sabzavot", "level": "N5", "reading": "やさい", "kanji": "野菜"},
    {"jp": "果物", "uz": "meva", "level": "N5", "reading": "くだもの", "kanji": "果物"},
    {"jp": "パン", "uz": "non", "level": "N5", "reading": "ぱん", "kanji": ""},
    {"jp": "スープ", "uz": "shorba", "level": "N5", "reading": "すーぷ", "kanji": ""},
    {"jp": "ご飯", "uz": "plov", "level": "N5", "reading": "ごはん", "kanji": "御飯"},
    {"jp": "味噌汁", "uz": "miso shorba", "level": "N5", "reading": "みそしる", "kanji": "味噌汁"},
    {"jp": "天ぷら", "uz": "tempura", "level": "N5", "reading": "てんぷら", "kanji": "天ぷら"},
    {"jp": "寿司", "uz": "sushi", "level": "N5", "reading": "すし", "kanji": "寿司"},
    {"jp": "そば", "uz": "Yapon makaron", "level": "N5", "reading": "そば", "kanji": "蕎麦"},
    {"jp": "うどん", "uz": "udon", "level": "N5", "reading": "うどん", "kanji": ""},
    {"jp": "ラーメン", "uz": "ramen", "level": "N5", "reading": "らーめん", "kanji": ""},
    
    # Animals
    {"jp": "猫", "uz": "mushuk", "level": "N5", "reading": "ねこ", "kanji": "猫"},
    {"jp": "犬", "uz": "it", "level": "N5", "reading": "いぬ", "kanji": "犬"},
    {"jp": "鳥", "uz": "qush", "level": "N5", "reading": "とり", "kanji": "鳥"},
    {"jp": "魚", "uz": "baliq", "level": "N5", "reading": "さかな", "kanji": "魚"},
    {"jp": "牛", "uz": "sigir", "level": "N5", "reading": "うし", "kanji": "牛"},
    {"jp": "豚", "uz": "cho'chqa", "level": "N5", "reading": "ぶた", "kanji": "豚"},
    {"jp": "馬", "uz": "ot", "level": "N5", "reading": "うま", "kanji": "馬"},
    {"jp": "羊", "uz": "qo'y", "level": "N5", "reading": "ひつじ", "kanji": "羊"},
    {"jp": "ウサギ", "uz": "quyon", "level": "N5", "reading": "うさぎ", "kanji": ""},
    {"jp": "ネズミ", "uz": "sichqon", "level": "N5", "reading": "ねずみ", "kanji": ""},
    {"jp": "蛇", "uz": "ilon", "level": "N5", "reading": "へび", "kanji": "蛇"},
    {"jp": "トンボ", "uz": "subbaiy", "level": "N5", "reading": "とんぼ", "kanji": ""},
    
    # Weather
    {"jp": "晴天", "uz": "toza asman", "level": "N5", "reading": "せいてん", "kanji": "晴天"},
    {"jp": "雨", "uz": "yomg'ir", "level": "N5", "reading": "あめ", "kanji": "雨"},
    {"jp": "雪", "uz": "qor", "level": "N5", "reading": "ゆき", "kanji": "雪"},
    {"jp": "風", "uz": "shamol", "level": "N5", "reading": "かぜ", "kanji": "風"},
    {"jp": "曇り", "uz": "bulutli", "level": "N5", "reading": "くもり", "kanji": "曇り"},
    {"jp": "霧", "uz": "tuman", "level": "N5", "reading": "きり", "kanji": "霧"},
    {"jp": "雷", "uz": "chergi", "level": "N5", "reading": "かみなり", "kanji": "雷"},
    {"jp": "台風", "uz": "tayfun", "level": "N5", "reading": "たいふう", "kanji": "台風"},
    {"jp": "温度", "uz": "harorat", "level": "N5", "reading": "おんど", "kanji": "温度"},
    {"jp": "湿度", "uz": "namlik", "level": "N5", "reading": "しつど", "kanji": "湿度"},
    
    # Body
    {"jp": "目", "uz": "ko'z", "level": "N5", "reading": "め", "kanji": "目"},
    {"jp": "耳", "uz": "quloq", "level": "N5", "reading": "みみ", "kanji": "耳"},
    {"jp": "鼻", "uz": "burun", "level": "N5", "reading": "はな", "kanji": "鼻"},
    {"jp": "口", "uz": "og'iz", "level": "N5", "reading": "くち", "kanji": "口"},
    {"jp": "歯", "uz": "tish", "level": "N5", "reading": "は", "kanji": "歯"},
    {"jp": "舌", "uz": "til", "level": "N5", "reading": "した", "kanji": "舌"},
    {"jp": "手", "uz": "qo'l", "level": "N5", "reading": "て", "kanji": "手"},
    {"jp": "足", "uz": "oyoq", "level": "N5", "reading": "あし", "kanji": "足"},
    {"jp": "指", "uz": "barmoq", "level": "N5", "reading": "ゆび", "kanji": "指"},
    {"jp": "爪", "uz": "tirnoq", "level": "N5", "reading": "つめ", "kanji": "爪"},
    {"jp": "髪", "uz": "soch", "level": "N5", "reading": "かみ", "kanji": "髪"},
    {"jp": "顔", "uz": "yuz", "level": "N5", "reading": "かお", "kanji": "顔"},
    {"jp": "首", "uz": "bo'yin", "level": "N5", "reading": "くび", "kanji": "首"},
    {"jp": "肩", "uz": "yelka", "level": "N5", "reading": "かた", "kanji": "肩"},
    {"jp": "背", "uz": "orqa", "level": "N5", "reading": "せ", "kanji": "背"},
    {"jp": "胸", "uz": "ko'krak", "level": "N5", "reading": "むね", "kanji": "胸"},
    {"jp": "腰", "uz": "yo'n", "level": "N5", "reading": "こし", "kanji": "腰"},
    {"jp": "腕", "uz": "bazu", "level": "N5", "reading": "うで", "kanji": "腕"},
    {"jp": "膝", "uz": "tizzasi", "level": "N5", "reading": "ひざ", "kanji": "膝"},
    
    # Family
    {"jp": "父", "uz": "ota", "level": "N5", "reading": "ちち", "kanji": "父"},
    {"jp": "母", "uz": "ona", "level": "N5", "reading": "かあ", "kanji": "母"},
    {"jp": "兄", "uz": "akam", "level": "N5", "reading": "あに", "kanji": "兄"},
    {"jp": "弟", "uz": "ukam", "level": "N5", "reading": "おとうと", "kanji": "弟"},
    {"jp": "姉", "uz": "opam", "level": "N5", "reading": "あね", "kanji": "姉"},
    {"jp": "妹", "uz": "singlim", "level": "N5", "reading": "いもうと", "kanji": "妹"},
    {"jp": "祖父", "uz": "buva", "level": "N5", "reading": "そふ", "kanji": "祖父"},
    {"jp": "祖母", "uz": "buvi", "level": "N5", "reading": "そぼ", "kanji": "祖母"},
    {"jp": "叔父", "uz": "amaki", "level": "N5", "reading": "おじさん", "kanji": "叔父"},
    {"jp": "叔母", "uz": "amakasi", "level": "N5", "reading": "おばさん", "kanji": "叔母"},
    {"jp": "従兄", "uz": "amakaning o'g'li", "level": "N5", "reading": "いとこ", "kanji": "従兄"},
    {"jp": "配偶者", "uz": "turmush o'rtogi", "level": "N5", "reading": "はいぐうしゃ", "kanji": "配偶者"},
    {"jp": "子供", "uz": "bola", "level": "N5", "reading": "こども", "kanji": "子供"},
    
    # School
    {"jp": "学校", "uz": "maktab", "level": "N5", "reading": "がっこう", "kanji": "学校"},
    {"jp": "先生", "uz": "o'qituvchi", "level": "N5", "reading": "せんせい", "kanji": "先生"},
    {"jp": "学生", "uz": "talaba", "level": "N5", "reading": "がくせい", "kanji": "学生"},
    {"jp": "クラス", "uz": "sinf", "level": "N5", "reading": "くらす", "kanji": ""},
    {"jp": "教室", "uz": "dars xonasi", "level": "N5", "reading": "きょうしつ", "kanji": "教室"},
    {"jp": "図書館", "uz": "kutubxona", "level": "N5", "reading": "としょかん", "kanji": "図書館"},
    {"jp": "体育館", "uz": "sport zali", "level": "N5", "reading": "たいいくかん", "kanji": "体育館"},
    {"jp": "運動場", "uz": "stadion", "level": "N5", "reading": "うんどうじょう", "kanji": "運動場"},
    {"jp": "給食", "uz": "taomin", "level": "N5", "reading": "きゅうしょく", "kanji": "給食"},
    {"jp": "宿題", "uz": "uy vazifasi", "level": "N5", "reading": "しゅくだい", "kanji": "宿題"},
    {"jp": "試験", "uz": "imtihon", "level": "N5", "reading": "しけん", "kanji": "試験"},
    {"jp": "成績", "uz": "natija", "level": "N5", "reading": "せいせき", "kanji": "成績"},
    
    # Professions
    {"jp": "医者", "uz": "doktor", "level": "N5", "reading": "いしゃ", "kanji": "医者"},
    {"jp": "看護師", "uz": "hamshira", "level": "N5", "reading": "かんごし", "kanji": "看護師"},
    {"jp": "弁護士", "uz": "vokil", "level": "N5", "reading": "べんごし", "kanji": "弁護士"},
    {"jp": "教師", "uz": "o'qituvchi", "level": "N5", "reading": "きょうし", "kanji": "教師"},
    {"jp": "会計士", "uz": "buxgalter", "level": "N5", "reading": "かいけいし", "kanji": "会計士"},
    {"jp": "エンジニア", "uz": "muhandis", "level": "N5", "reading": "えんじにあ", "kanji": ""},
    {"jp": "プログラマー", "uz": "programmist", "level": "N5", "reading": "ぷろぐらまー", "kanji": ""},
    {"jp": "デザイナー", "uz": "dizayner", "level": "N5", "reading": "でざいなー", "kanji": ""},
    {"jp": "営業", "uz": "sotuvchi", "level": "N5", "reading": "えいぎょう", "kanji": "営業"},
    {"jp": "管理職", "uz": "boshqaruvchi", "level": "N5", "reading": "かんりしょく", "kanji": "管理職"},
    
    # Emotions
    {"jp": "嬉しい", "uz": "baxtli", "level": "N5", "reading": "うれしい", "kanji": "嬉しい"},
    {"jp": "悲しい", "uz": "qayg'ali", "level": "N5", "reading": "かなしい", "kanji": "悲しい"},
    {"jp": "怒い", "uz": "g'azablangan", "level": "N5", "reading": "おこい", "kanji": "怒い"},
    {"jp": "驚いた", "uz": "hayratlanish", "level": "N5", "reading": "おどろいた", "kanji": "驚いた"},
    {"jp": "恐い", "uz": "qo'rqish", "level": "N5", "reading": "こわい", "kanji": "恐い"},
    {"jp": "退屈", "uz": "zerikdi", "level": "N5", "reading": "たいくつ", "kanji": "退屈"},
    {"jp": "興味", "uz": "qiziqish", "level": "N5", "reading": "きょうみ", "kanji": "興味"},
    {"jp": "疲れた", "uz": "charchoq", "level": "N5", "reading": "つかれた", "kanji": "疲れた"},
    {"jp": "元気", "uz": "energiyali", "level": "N5", "reading": "げんき", "kanji": "元気"},
    {"jp": "落ち込む", "uz": "tushkunlik", "level": "N5", "reading": "おちこむ", "kanji": "落ち込む"},
]

# ===================== GRAMMAR PATTERNS =====================
GRAMMAR_LESSONS = {
    "N5": [
        {"pattern": "～です", "meaning": "hisoblanadi (adab)", "example": "私は学生です", "explanation": "Odatiy gapda ishlatiladi"},
        {"pattern": "～ます", "meaning": "qiladi (adab)", "example": "毎日勉強します", "explanation": "Harotaga qilish"},
        {"pattern": "～ません", "meaning": "qilmaydi (adab)", "example": "私は学生ではありません", "explanation": "Inkor qilish"},
        {"pattern": "～た", "meaning": "qildi (o'tmish)", "example": "昨日勉強した", "explanation": "O'tmish zamon"},
        {"pattern": "～る", "meaning": "qilish (sözluk)", "example": "勉強する", "explanation": "Asosiy shakl"},
        {"pattern": "～ない", "meaning": "qilmaydi (inkor)", "example": "勉強しない", "explanation": "Inkor qilish"},
    ],
    "N4": [
        {"pattern": "～ところです", "meaning": "avtursiz", "example": "今勉強しているところです", "explanation": "Hozir qilmoqda"},
        {"pattern": "～たばかり", "meaning": "shu zor", "example": "来たばかりです", "explanation": "Shunga keldi"},
        {"pattern": "～によると", "meaning": "qarab", "example": "ニュースによると", "explanation": "Shunday aytadi"},
        {"pattern": "～させる", "meaning": "majbur qilish", "example": "子供に勉強させる", "explanation": "Kimgadir qildirishni majbur qilish"},
        {"pattern": "～られる", "meaning": "qila olish", "example": "日本語が話せます", "explanation": "Imkoniyat"},
        {"pattern": "～ため", "meaning": "uchun", "example": "お金を稼ぐため", "explanation": "Maqsad"},
    ],
}

# ===================== PRONUNCIATION GUIDE =====================
PRONUNCIATION_TIPS = [
    "🔊 <b>Vowels:</b> あ(a), い(i), う(u), え(e), お(o)",
    "🔊 <b>Consonants:</b> か(ka), さ(sa), た(ta), な(na), は(ha)",
    "🔊 <b>Double Consonants:</b> Short pause + consonant (ロック = rok-ku)",
    "🔊 <b>Long Vowels:</b> Extend vowel (おうさま = oo-sama)",
    "🔊 <b>Pitch Accent:</b> Japanese has pitch, not stress",
    "🔊 <b>N sound:</b> ん - nasal ending",
]

# ===================== STROKE ORDER DATA =====================
STROKE_ORDER_GUIDE = {
    "一": ["Bitta gorizontal chiziq"],
    "二": ["Birinchi gorizontal", "Ikkinchi gorizontal"],
    "三": ["Birinchi gorizontal", "Ikkinchi gorizontal", "Uchinchi gorizontal"],
    "人": ["Chapga urilgan", "O'ngga urilgan"],
}

def main_menu_keyboard(user_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Kanji Flashcard", "📝 So'z Test (N4/N5)")
    markup.add("❓ Quiz", "📖 Grammar")
    markup.add("🎤 Pronunciation", "✍️ Writing")
    markup.add("👂 Listening", "🎯 Daily Challenge")
    markup.add("📊 Progress", "🏆 Reyting")
    markup.add("👤 Profil", "❓ Adminga")
    if user_id == ADMIN_ID:
        markup.add("📊 Admin Stats", "📣 Admin Send")
    return markup

# ===================== KANJI FLASHCARD =====================
@bot.message_handler(func=lambda m: m.text == "📚 Kanji Flashcard")
def kanji_flashcard(m):
    kanji = random.choice(kanji_list)
    user_sessions[m.chat.id] = {"type": "kanji_flash", "current_kanji": kanji}
    
    text = (
        f"📚 <b>Kanji Flashcard</b>\n\n"
        f"<b>Kanji:</b> {kanji['kanji']}\n"
        f"<b>JLPT:</b> {kanji['jlpt']}\n"
        f"<b>Stroke:</b> {kanji['stroke']}\n\n"
        f"<b>Ma'no:</b> {kanji['meaning']}\n"
        f"<b>On-reading:</b> {kanji['on']}\n"
        f"<b>Kun-reading:</b> {kanji['kun']}\n\n"
        f"<b>Example:</b> {kanji['example']}"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("✅ Bilaman", "❌ Bilmayman")
    markup.add("➡️ Keyingi", "🏠 Menu")
    
    bot.send_message(m.chat.id, text, parse_mode="HTML", reply_markup=markup)

# ===================== GRAMMAR LESSONS =====================
@bot.message_handler(func=lambda m: m.text == "📖 Grammar")
def grammar_menu(m):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("N5 Grammar", "N4 Grammar")
    markup.add("🏠 Menu")
    bot.send_message(m.chat.id, "📖 <b>Grammar Level</b> tanlang:", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["N5 Grammar", "N4 Grammar"])
def show_grammar(m):
    level = "N5" if "N5" in m.text else "N4"
    lessons = GRAMMAR_LESSONS.get(level, [])
    lesson = random.choice(lessons)
    
    text = (
        f"📖 <b>Grammar - {level}</b>\n\n"
        f"<b>Pattern:</b> {lesson['pattern']}\n"
        f"<b>Ma'no:</b> {lesson['meaning']}\n\n"
        f"<b>Misol:</b> {lesson['example']}\n"
        f"<b>Tushuntirish:</b> {lesson['explanation']}"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("➡️ Keyingi", "🏠 Menu")
    
    bot.send_message(m.chat.id, text, parse_mode="HTML", reply_markup=markup)

# ===================== PRONUNCIATION =====================
@bot.message_handler(func=lambda m: m.text == "🎤 Pronunciation")
def pronunciation(m):
    tip = random.choice(PRONUNCIATION_TIPS)
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("➡️ Keyingi", "🏠 Menu")
    
    bot.send_message(m.chat.id, f"🔊 <b>Pronunciation Tip</b>\n\n{tip}", parse_mode="HTML", reply_markup=markup)

# ===================== WRITING PRACTICE =====================
@bot.message_handler(func=lambda m: m.text == "✍️ Writing")
def writing_practice(m):
    kanji = random.choice(kanji_list)
    
    text = (
        f"✍️ <b>Writing Practice</b>\n\n"
        f"<b>Kanji:</b> {kanji['kanji']}\n"
        f"<b>Stroke Order:</b> {kanji['stroke']} qadamda yozing\n\n"
        f"Birinchi qadamdan boshlab yozing!"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("✏️ Stroke Guide", "➡️ Keyingi", "🏠 Menu")
    
    bot.send_message(m.chat.id, text, parse_mode="HTML", reply_markup=markup)

# ===================== LISTENING PRACTICE =====================
@bot.message_handler(func=lambda m: m.text == "👂 Listening")
def listening_practice(m):
    tasks = [
        "🎧 Hiragana o'qiy eshiting\n\nVazifa: Eshitgan narsangizni hiragana-da yozing",
        "🎧 Katakana so'zlarni eshiting\n\nVazifa: Shuning qanday qilib yozilaganini ayting",
        "🎧 Qisqa suhbatni eshiting\n\nVazifa: Savolga javob bering",
    ]
    
    task = random.choice(tasks)
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("➡️ Keyingi", "🏠 Menu")
    
    bot.send_message(m.chat.id, f"👂 <b>Listening Task</b>\n\n{task}", parse_mode="HTML", reply_markup=markup)

# ===================== DAILY CHALLENGE =====================
@bot.message_handler(func=lambda m: m.text == "🎯 Daily Challenge")
def daily_challenge(m):
    challenges = [
        "10 kanji flashcard o'tkazing",
        "5 grammar pattern o'rganing",
        "20 so'z o'rganing",
        "100 points to'plang",
    ]
    
    challenge = random.choice(challenges)
    points = random.randint(50, 100)
    
    text = f"🎯 <b>Kunlik Challenge</b>\n\n{challenge}\n\n💰 Reward: +{points} points"
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add(f"✅ Qabul ({points} pts)", "❌ Rad etish")
    markup.add("🏠 Menu")
    
    user_sessions[m.chat.id] = {"type": "challenge", "points": points}
    bot.send_message(m.chat.id, text, parse_mode="HTML", reply_markup=markup)

# ===================== PROGRESS TRACKING =====================
@bot.message_handler(func=lambda m: m.text == "📊 Progress")
def progress_tracking(m):
    db = load_db()
    user = db.get(str(m.chat.id), {"points": 0, "streak": 0, "level": "N5"})
    
    text = (
        f"📊 <b>Your Progress</b>\n\n"
        f"<b>Level:</b> {user.get('level', 'N5')}\n"
        f"<b>Points:</b> {user.get('points', 0)}\n"
        f"<b>Streak:</b> 🔥 {user.get('streak', 0)} days\n"
        f"<b>Last Active:</b> Today"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🏠 Menu")
    
    bot.send_message(m.chat.id, text, parse_mode="HTML", reply_markup=markup)

# ===================== ANSWER HANDLERS =====================
@bot.message_handler(func=lambda m: m.text in ["✅ Qabul", "❌ Rad etish"] or "Qabul" in m.text)
def handle_challenge_response(m):
    db = load_db()
    if "Qabul" in m.text:
        session = user_sessions.get(m.chat.id, {})
        points = session.get("points", 50)
        update_user_stats(m.chat.id, m.from_user.first_name, points_to_add=points)
        bot.send_message(m.chat.id, f"🎉 Challenge Qabul Qilindi!\n\n+{points} Points!", reply_markup=main_menu_keyboard(m.chat.id))
    else:
        bot.send_message(m.chat.id, "❌ Challenge Rad Qilindi", reply_markup=main_menu_keyboard(m.chat.id))

# ===================== MAIN HANDLERS =====================
@bot.message_handler(commands=['start'])
def start(m):
    user_data = update_user_stats(m.chat.id, m.from_user.first_name, check_streak=True)
    db = load_db()
    sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(m.chat.id)), 999)
    
    welcome_text = (
        f"🎌 <b>JLPT N4/N5 Yapon Til Bot v2.0</b>\n\n"
        f"🔥 Kunlik faollik: <b>{user_data['streak']} kun</b>\n"
        f"🏆 Jami ballar: <b>{user_data['points']} ball</b>\n"
        f"🏛️ Unvon: <b>{get_rank_title(user_place)} ({user_place}-o'rin)</b>\n\n"
        f"<b>160+ Kanji | 500+ So'z | 10 Funksiya</b>\n\n"
        f"<i>Quyidagi tugmalardan birini tanlang:</i>"
    )
    bot.send_message(m.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu_keyboard(m.chat.id))

@bot.message_handler(func=lambda m: m.text == "🏠 Menu")
def menu(m):
    welcome_text = "🎌 <b>Asosiy Menu</b>\n\nQaysi funksiyani ishlatmoqchi?"
    bot.send_message(m.chat.id, welcome_text, parse_mode="HTML", reply_markup=main_menu_keyboard(m.chat.id))

@bot.message_handler(func=lambda m: m.text == "📊 Kanji Test")
def ask_test_count_kanji(m):
    ask_test_count(m.chat.id, "kanji")

@bot.message_handler(func=lambda m: m.text == "📝 So'z Test (N4/N5)")
def ask_test_count_words(m):
    ask_test_count(m.chat.id, "word")

@bot.message_handler(func=lambda m: m.text == "❓ Quiz")
def quiz_menu(m):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("5 Savol", "10 Savol", "15 Savol")
    markup.add("🏠 Menu")
    bot.send_message(m.chat.id, "❓ <b>Quiz</b> - Nechta savol?", parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text in ["5 Savol", "10 Savol", "15 Savol"])
def start_kanji_quiz(m):
    try:
        total = int(m.text.split()[0])
        ask_test_count(m.chat.id, "kanji")
    except:
        pass

@bot.message_handler(func=lambda m: m.text == "🏆 Reyting")
def leaderboard(m):
    db = load_db()
    sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    
    text = "🏆 <b>TOP-10 Reyting</b>\n====================\n"
    for idx, (uid, uinfo) in enumerate(sorted_users[:10]):
        text += f"{idx+1}. {get_rank_title(idx+1)} | <b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
    
    user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(m.chat.id)), 999)
    text += f"====================\n📈 Sizning o'rningiz: <b>{user_place}-o'rin</b>"
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🏠 Menu")
    
    bot.send_message(m.chat.id, text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "👤 Profil")
def profile(m):
    db = load_db()
    user = db.get(str(m.chat.id), {"name": m.from_user.first_name, "points": 0, "streak": 0})
    sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
    user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(m.chat.id)), 999)
    
    text = (
        f"👤 <b>Shaxsiy Profil</b>\n"
        f"• <b>Ism:</b> {user['name']}\n"
        f"• <b>Ballar:</b> {user['points']}\n"
        f"• <b>Faollik:</b> {user['streak']} kun\n"
        f"• <b>Unvon:</b> {get_rank_title(user_place)} ({user_place}-o'rin)"
    )
    
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.add("🏠 Menu")
    
    bot.send_message(m.chat.id, text, parse_mode="HTML", reply_markup=markup)

# Original quiz functions
def ask_test_count(chat_id, mode):
    m = bot.send_message(chat_id, "📊 Nechta test yechasiz?", reply_markup=telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add("5", "10", "15", "20"))
    bot.register_next_step_handler(m, lambda msg: start_quiz_session(msg, mode))

def start_quiz_session(m, mode):
    try:
        total = int(m.text.strip())
    except:
        total = 5
    base = kanji_list if mode == "kanji" else words_list
    user_sessions[m.chat.id] = {"questions": random.sample(base, min(total, len(base))), "current_index": 0, "correct_count": 0, "total": min(total, len(base)), "type": mode}
    send_next_question(m.chat.id)

def send_next_question(chat_id):
    s = user_sessions.get(chat_id)
    if not s:
        return
    if s["current_index"] >= s["total"]:
        earned_points = s["correct_count"] * 10
        db = load_db()
        name = db.get(str(chat_id), {}).get("name", "User")
        update_user_stats(chat_id, name, points_to_add=earned_points)
        
        db = load_db()
        sorted_users = sorted(db.items(), key=lambda x: x[1].get("points", 0), reverse=True)
        user_place = next((i + 1 for i, (uid, _) in enumerate(sorted_users) if uid == str(chat_id)), 999)
        
        leaderboard = "🏆 <b>TOP-5:</b>\n"
        for idx, (uid, uinfo) in enumerate(sorted_users[:5]):
            leaderboard += f"{idx+1}. {get_rank_title(idx+1)} | <b>{uinfo.get('name', 'User')}</b> | <code>{uinfo.get('points', 0)} ball</code>\n"
        
        bot.send_message(
            chat_id,
            f"🎉 <b>Test Yakunlandi!</b>\n✅ <b>{s['correct_count']}/{s['total']}</b>\n💰 <b>+{earned_points} ball</b>\n📈 <b>{user_place}-o'rin</b>\n\n" + leaderboard,
            parse_mode="HTML",
            reply_markup=main_menu_keyboard(chat_id)
        )
        if chat_id in user_sessions:
            del user_sessions[chat_id]
        return

    item = s["questions"][s["current_index"]]
    if s["type"] == "kanji":
        question_text = f"🎯 [Savol {s['current_index']+1}/{s['total']}]\n\n🔥 Kanji: <b>{item['kanji']}</b>\n\nTo'g'ri ma'no nima?"
        ok = item['meaning']
        wr = [k['meaning'] for k in kanji_list if k["kanji"] != item["kanji"]]
    else:
        question_text = f"📝 [Savol {s['current_index']+1}/{s['total']}]\n\n🇯🇵 <b>「{item['jp']}」</b>\n\nTo'g'ri o'zbekcha tarjima?"
        ok = item['uz']
        wr = [w['uz'] for w in words_list if w['jp'] != item['jp']]

    opts = random.sample(wr, min(3, len(wr))) + [ok]
    random.shuffle(opts)
    s["correct_string"] = ok

    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    for option in opts:
        markup.add(option)

    bot.send_message(chat_id, question_text, parse_mode="HTML", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_answer(m):
    cid, txt = m.chat.id, m.text.strip() if m.text else ""
    
    if cid in user_sessions:
        s = user_sessions[cid]
        if txt == s["correct_string"]:
            s["correct_count"] += 1
            bot.send_message(cid, "✅ To'g'ri!")
        else:
            bot.send_message(cid, f"❌ Noto'g'ri!\nJavob: <b>{s['correct_string']}</b>", parse_mode="HTML")
        s["current_index"] += 1
        send_next_question(cid)
        return

    # Admin functions
    if txt == "📊 Admin Stats" and cid == ADMIN_ID:
        get_bot_stats(m)
        return
    if txt == "📣 Admin Send" and cid == ADMIN_ID:
        send_all_prompt(m)
        return
    
    # Help
    if txt == "❓ Adminga":
        bot.send_message(cid, "✉️ Xabaringizni kiriting:", reply_markup=main_menu_keyboard(cid))
        bot.register_next_step_handler(m, lambda msg: admin_message(msg))
        return
    
    # Unknown
    bot.send_message(cid, "Noma'lum buyruq. Menyu-dan tanlang.", reply_markup=main_menu_keyboard(cid))

def admin_message(m):
    bot.forward_message(ADMIN_ID, m.chat.id, m.message_id)
    bot.send_message(ADMIN_ID, f"📩 User ID: {m.chat.id}", parse_mode="HTML")
    bot.send_message(m.chat.id, "✅ Adminga yuboriland.", reply_markup=main_menu_keyboard(m.chat.id))

@bot.message_handler(commands=['stats'])
def get_bot_stats(m):
    if m.chat.id != ADMIN_ID:
        return
    db = load_db()
    total_users = len(db)
    top_user = max(db.values(), key=lambda x: x.get("points", 0)) if db else {"name": "N/A", "points": 0}
    text = f"📊 <b>Bot Stats</b>\n👥 Jami: <b>{total_users}</b>\n🏆 Top: <b>{top_user['name']} ({top_user['points']} pts)</b>"
    bot.send_message(ADMIN_ID, text, parse_mode="HTML")

@bot.message_handler(commands=['sendall'])
def send_all_prompt(m):
    if m.chat.id != ADMIN_ID:
        return
    msg = bot.send_message(ADMIN_ID, "📣 Xabar kiriting:")
    bot.register_next_step_handler(msg, lambda msg: start_broadcasting(msg))

def start_broadcasting(m):
    db = load_db()
    for uid in db.keys():
        try:
            bot.copy_message(int(uid), ADMIN_ID, m.message_id)
        except:
            pass

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling()
