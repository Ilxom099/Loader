# 01. So'zBot — inglizcha so'z yodlash

**Daraja:** Boshlang'ich · **Muddat:** 2 hafta · **Jamoa:** 1–2 o'quvchi

## Muammo
O'quvchilar yangi so'zlarni yodlaydi, lekin takrorlamagani uchun tez unutadi.

**Foydalanuvchilar:** Ingliz tilini o'rganayotgan o'quvchilar

## Asosiy funksiyalar (MVP)
- Har kuni soat 08:00 da 5 ta yangi so'z (so'z, tarjima, misol gap)
- /test — 5 ta savol, 4 ta variantli tugmalar bilan
- Xato javob berilgan so'zlar 1, 3 va 7 kundan keyin qayta so'raladi
- /natija — to'g'ri javoblar foizi va ketma-ket kunlar (streak)

## Buyruqlar
`/start` `/bugun` `/test` `/natija` `/daraja A1|A2|B1`

## Ma'lumotlar bazasi
- `users`: telegram_id, ism, daraja, streak, oxirgi_kun
- `words`: so'z, tarjima, misol, daraja
- `answers`: user_id, word_id, to'g'ri (0/1), sana, keyingi_takror

## Bosqichlar
- 1-hafta: 200 ta so'zni CSV faylga yig'ish, /start va /bugun, inline tugmali test
- 2-hafta: takrorlash jadvali (1-3-7 kun), har kungi xabar, /natija

## Bonus vazifalar
- So'zning talaffuzi (ovozli xabar)
- Sinf bo'yicha haftalik reyting

## Nimani o'rganasiz
- aiogram: buyruqlar va inline tugmalar
- CSV o'qish
- SQLite
- sana bilan ishlash

## Daromad g'oyasi
Bepul: kuniga 5 so'z. Premium (5 000 so'm/oy): IELTS so'z to'plamlari va cheksiz test.

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
