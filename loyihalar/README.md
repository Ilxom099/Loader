# O'quvchilar uchun 15 ta loyiha rejasi

UstozBot kabi maktab hayotidagi real muammoni hal qiladigan Telegram botlar.
Har bir reja: muammo, funksiyalar, buyruqlar, ma'lumotlar bazasi, haftalik bosqichlar,
bonus vazifalar, o'rganiladigan ko'nikmalar va daromad g'oyasi.

| № | Loyiha | Daraja | Muddat |
|---|---|---|---|
| 01 | [So'zBot — inglizcha so'z yodlash](01-lugat-bot.md) | Boshlang'ich | 2 hafta |
| 02 | [Kitobxon kundaligi](02-kitobxon.md) | Boshlang'ich | 2 hafta |
| 03 | [Misol trenajyori](03-misol-trenajyor.md) | Boshlang'ich | 2 hafta |
| 04 | [Maktab oshxonasi menyusi](04-oshxona-menyu.md) | Boshlang'ich | 2 hafta |
| 05 | [Imtihon sanog'i va reja](05-imtihon-sanoq.md) | Boshlang'ich | 2 hafta |
| 06 | [Sinf viktorinasi (Quiz) boti](06-quiz-bot.md) | O'rta | 3 hafta |
| 07 | [Davomat boti](07-davomat.md) | O'rta | 3 hafta |
| 08 | [O'quvchining vazifa daftari](08-vazifa-daftari.md) | O'rta | 3 hafta |
| 09 | [Maktab e'lonlari va to'garaklar](09-elonlar.md) | O'rta | 3 hafta |
| 10 | [Yo'qolgan buyumlar boti](10-topilmalar.md) | O'rta | 3 hafta |
| 11 | [Maktab kutubxonasi boti](11-kutubxona.md) | Murakkab | 4 hafta |
| 12 | [Ustoz–shogird (o'zaro yordam) boti](12-ustoz-shogird.md) | Murakkab | 4 hafta |
| 13 | [Olimpiadaga tayyorgarlik trekeri](13-olimpiada.md) | Murakkab | 4 hafta |
| 14 | [Ota-ona — o'qituvchi uchrashuv navbati](14-uchrashuv-navbati.md) | Murakkab | 4 hafta |
| 15 | [Eko-musobaqa: makulatura va plastik yig'ish](15-eko-musobaqa.md) | Murakkab | 4 hafta |

## Texnologiyalar
- Python 3.11+ va aiogram 3 — Telegram bot uchun
- SQLite — ma'lumotlar bazasi (o'rnatish shart emas)
- Git va GitHub — kodni saqlash va jamoada ishlash
- Namuna kod: ustozbot/ papkasi — buyruqlar, eslatmalar, tariflar qanday yozilganini ko'ring

## Qanday boshlash kerak
- BotFather'da yangi bot yarating va tokenni oling (tokenni hech kimga bermang, GitHub'ga yuklamang)
- pip install aiogram; tokenni BOT_TOKEN muhit o'zgaruvchisiga yozing
- Avval /start ga javob beradigan eng oddiy botni ishga tushiring
- Har haftaning oxirida ishlaydigan versiyani o'qituvchiga ko'rsating

## Baholash (100 ball)
| Mezon | Ball | Nima tekshiriladi |
|---|---|---|
| Ishlaydi | 30 | Rejadagi asosiy funksiyalar xatosiz ishlaydi |
| Kod sifati | 20 | Fayllarga bo'lingan, tushunarli nomlar, izohlar |
| Ma'lumotlar bazasi | 15 | Jadvallar rejaga mos, ma'lumot qayta ishga tushirilganda saqlanadi |
| Foydalanuvchi tajribasi | 15 | Tushunarli xabarlar, tugmalar, xatoda yordam matni |
| Taqdimot | 10 | Muammo, yechim, jonli namoyish 5 daqiqada |
| Bonus | 10 | Kamida bitta bonus vazifa bajarilgan |

Fayllar `build.py` orqali `data.py` dan yasaladi — rejani o'zgartirish uchun `data.py` ni tahrirlang.
