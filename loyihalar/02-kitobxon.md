# 02. Kitobxon kundaligi

**Daraja:** Boshlang'ich · **Muddat:** 2 hafta · **Jamoa:** 1–2 o'quvchi

## Muammo
Kitob o'qish odatini kuzatish va o'zini rag'batlantirish qiyin.

**Foydalanuvchilar:** Barcha sinf o'quvchilari, kutubxonachi

## Asosiy funksiyalar (MVP)
- /kitob — o'qilayotgan kitob nomi va jami sahifa soni
- /oqidim 25 — bugun o'qilgan sahifalar; progress foizda ko'rsatiladi
- Kechqurun 20:00 da "Bugun o'qidingmi?" eslatmasi
- Kitob tugaganda 1–5 baho va bir gapli fikr qoldirish

## Buyruqlar
`/start` `/kitob` `/oqidim` `/statistika` `/tavsiya`

## Ma'lumotlar bazasi
- `users`: telegram_id, ism, sinf
- `books`: user_id, nomi, muallif, jami_sahifa, tugadi
- `reading_log`: book_id, sana, sahifalar
- `reviews`: book_id, baho, fikr

## Bosqichlar
- 1-hafta: kitob qo'shish, sahifa yozish, progress foizi
- 2-hafta: kechki eslatma, oylik statistika, boshqalar baho bergan kitoblar ro'yxati (/tavsiya)

## Bonus vazifalar
- Oyning eng ko'p o'qigan o'quvchisi
- Kitob yakunlanganda sertifikat rasmi (Pillow)

## Nimani o'rganasiz
- FSM (bosqichma-bosqich so'rash)
- rejalashtirilgan xabarlar
- SQL GROUP BY

## Daromad g'oyasi
Maktab kutubxonasi uchun yillik obuna: sinflar reytingi va hisobotlar.

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
