# 11. Maktab kutubxonasi boti

**Daraja:** Murakkab · **Muddat:** 4 hafta · **Jamoa:** 2–3 o'quvchi

## Muammo
Kitob bor-yo'qligini bilish uchun kutubxonaga borish kerak, qaytarish muddati unutiladi.

**Foydalanuvchilar:** O'quvchilar, kutubxonachi

## Asosiy funksiyalar (MVP)
- Katalog: nomi, muallif, nusxalar soni bo'yicha qidiruv
- Kitobni band qilish; kutubxonachi berilganini tasdiqlaydi
- Qaytarish muddatidan 2 kun oldin va kechikkanda eslatma
- Band qilingan kitob qaytsa navbatdagi o'quvchiga xabar

## Buyruqlar
`/start` `/qidir` `/band` `/kitoblarim` `/admin_ber` `/admin_qaytdi`

## Ma'lumotlar bazasi
- `books`: nomi, muallif, isbn, nusxalar, mavjud
- `loans`: book_id, user_id, berildi, muddat, qaytdi
- `reservations`: book_id, user_id, sana, navbat

## Bosqichlar
- 1-hafta: katalog import (Excel), qidiruv
- 2-hafta: band qilish va berish/qaytarish
- 3-hafta: muddat eslatmalari, navbat
- 4-hafta: statistika: eng ko'p o'qilgan kitoblar, qarzdorlar

## Bonus vazifalar
- Telegram Mini App ko'rinishidagi katalog
- ISBN orqali kitob muqovasini olish

## Nimani o'rganasiz
- tranzaksiyalar (nusxalar soni)
- navbat mantiqi
- Excel import

## Daromad g'oyasi
Maktab va xususiy kutubxonalar uchun yillik obuna.

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
