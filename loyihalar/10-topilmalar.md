# 10. Yo'qolgan buyumlar boti

**Daraja:** O'rta · **Muddat:** 3 hafta · **Jamoa:** 2 o'quvchi

## Muammo
Maktabda yo'qolgan buyum egasini topish uchun hamma joyni so'rab chiqish kerak.

**Foydalanuvchilar:** O'quvchilar, navbatchi o'qituvchi

## Asosiy funksiyalar (MVP)
- "Yo'qotdim" va "Topdim" e'lonlari: rasm, toifa, joy, sana
- Toifa va kalit so'z bo'yicha qidiruv
- Yangi "topildi" e'loni mos "yo'qotdim" egasiga avtomatik xabar beradi
- Moderator e'lonni tasdiqlaydi; egasiga qaytgach yopiladi

## Buyruqlar
`/start` `/yoqotdim` `/topdim` `/qidir` `/menikilar`

## Ma'lumotlar bazasi
- `items`: turi (lost/found), toifa, tavsif, rasm, joy, sana, holat, egasi_id
- `matches`: lost_id, found_id, xabar_yuborildi

## Bosqichlar
- 1-hafta: e'lon qo'shish FSM orqali, rasm
- 2-hafta: qidiruv, moderatsiya
- 3-hafta: avtomatik moslashtirish (toifa + kalit so'zlar)

## Bonus vazifalar
- 30 kundan eski e'lonlarni arxivlash
- Topgan o'quvchiga "rahmat" ballari

## Nimani o'rganasiz
- matn bo'yicha qidiruv (LIKE)
- moderatsiya oqimi
- oddiy moslashtirish algoritmi

## Daromad g'oyasi
Ijtimoiy loyiha: daromad emas, maktab tanlovlari va grantlar uchun portfolio.

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
