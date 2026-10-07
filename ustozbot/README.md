# UstozBot — o'qituvchilar uchun Telegram yordamchi (MVP)

Maktab o'qituvchisiga dars jadvalini yuboradigan, darsdan **60, 30 va 10 daqiqa oldin** eslatadigan,
uyga vazifalarni saqlab muddati haqida xabar beradigan Telegram bot. Sinflar, o'quvchilar va
o'qituvchilar ro'yxati bitta joyda saqlanadi.

## Imkoniyatlar (MVP)

| Funksiya | Qanday ishlaydi |
|---|---|
| Kunlik jadval | Har kuni 07:00 da bugungi darslar + bugun muddati tugaydigan vazifalar |
| Haftalik jadval | Har dushanba 07:00 da |
| Oylik jadval | Har oyning 1-kuni 07:00 da (Pro, Ultra) |
| Dars eslatmasi | Darsdan 60 / 30 / 10 daqiqa oldin Telegram xabar; Pro'da 10 daqiqalik SMS, Ultra'da uchalasi SMS |
| Uyga vazifa | `/vazifa` bilan saqlanadi; muddatdan bir kun oldin 18:00 da va muddat kuni ertalab eslatma |
| Sinflar, o'quvchilar | Sinf, o'quvchi F.I.Sh va ota-ona telefoni |
| Tariflar | Start / Pro / Ultra limitlari (`plans.py`), 14 kun bepul Pro, obuna muddati tugasa eslatmalar to'xtaydi |
| To'lov | MVP: karta orqali o'tkazma, admin `/tasdiq` bilan yoqadi; 12 oy uchun 10 oy narxi |

## Tariflar

| | Start | Pro | Ultra |
|---|---|---|---|
| Narx / oy | 5 000 so'm | 30 000 so'm | 100 000 so'm |
| Sinflar | 3 ta | cheksiz | cheksiz |
| Kunlik / haftalik jadval | ✅ | ✅ | ✅ |
| Oylik jadval | — | ✅ | ✅ |
| Telegram eslatma 60/30/10 | ✅ | ✅ | ✅ |
| SMS eslatma | — | 100 / oy (10 daqiqa oldin) | 500 / oy (60/30/10) |
| Vazifa arxivi | 30 kun | 1 yil | cheksiz |
| AI yordamchi (keyingi bosqich) | — | — | 50 so'rov / oy |

Batafsil biznes-model: [BIZNES_REJA.md](BIZNES_REJA.md).

## Ishga tushirish

```bash
cd ustozbot
pip install -r requirements.txt
export BOT_TOKEN="BotFather bergan token"
export ADMIN_IDS="sizning_telegram_id"
export PAYMENT_CARD="8600 1234 5678 9012"
# ixtiyoriy, SMS uchun (bo'sh bo'lsa SMS faqat logga yoziladi):
export ESKIZ_EMAIL="..." ESKIZ_PASSWORD="..."
python bot.py
```

Testlar: `python -m unittest test_bot.py`

## Buyruqlar

| Buyruq | Misol |
|---|---|
| `/start`, `/yordam` | |
| `/maktab`, `/fan`, `/telefon` | `/telefon +998901234567` |
| `/sinf_qosh`, `/sinflar` | `/sinf_qosh 7-A` |
| `/oquvchi_qosh`, `/oquvchilar` | `/oquvchi_qosh 7-A \| Aliyev Vali \| +998901234567` |
| `/dars_qosh` | `/dars_qosh Dushanba 08:30 7-A Matematika 12-xona` |
| `/darslar`, `/dars_ochir` | `/dars_ochir 5` |
| `/bugun`, `/ertaga`, `/hafta`, `/oy` | |
| `/vazifa` | `/vazifa 7-A 15.10 \| 25-mashq, 3-bet` (muddat: `15.10`, `2026-10-15`, `ertaga`, `+3`) |
| `/vazifalar`, `/bajarildi` | `/bajarildi 4` |
| `/tarif`, `/tolov`, `/holat` | `/tolov pro`, `/tolov ultra 12` |
| Admin: `/tasdiq`, `/statistika` | `/tasdiq 7` |

## Tuzilishi

```
bot.py        — buyruqlar va har 30 soniyadagi fon jarayoni (eslatmalar, jadvallar)
schedule.py   — jadval matnlari, eslatma vaqtini hisoblash, sana/vaqt parserlari
db.py         — SQLite sxemasi: schools, teachers, classes, students, lessons,
                homeworks, reminders_sent, digests_sent, sms_log, payments
plans.py      — tariflar va limitlar
sms.py        — Eskiz.uz SMS
config.py     — muhit o'zgaruvchilari
```

## Keyingi bosqich

Payme / Click avtomatik to'lov, Excel'dan jadval importi, davomat va baholar jurnali,
vazifani sinf guruhiga va ota-onalarga yuborish, almashtirish (zamena) xabarlari,
AI yordamchi (dars rejasi, test), maktab admin paneli (Telegram Mini App), PostgreSQL.
