import os
from zoneinfo import ZoneInfo

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
DB_PATH = os.getenv("DB_PATH", "ustozbot.sqlite3")
TZ = ZoneInfo(os.getenv("TZ_NAME", "Asia/Tashkent"))

# Vergul bilan ajratilgan admin Telegram ID lari: to'lovni tasdiqlaydi.
ADMIN_IDS = {int(x) for x in os.getenv("ADMIN_IDS", "").split(",") if x.strip()}

# To'lov ma'lumoti (MVP: qo'lda o'tkazma, admin tasdiqlaydi).
PAYMENT_CARD = os.getenv("PAYMENT_CARD", "8600 **** **** ****")

# Eskiz.uz SMS. Bo'sh bo'lsa SMS faqat logga yoziladi.
ESKIZ_EMAIL = os.getenv("ESKIZ_EMAIL", "")
ESKIZ_PASSWORD = os.getenv("ESKIZ_PASSWORD", "")
ESKIZ_FROM = os.getenv("ESKIZ_FROM", "4546")

DIGEST_HOUR = 7  # kunlik/haftalik/oylik jadval soat 07:00 da
HOMEWORK_EVENING_HOUR = 18  # ertangi muddatli vazifalar haqida soat 18:00 da
