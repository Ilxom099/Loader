# 15. Eko-musobaqa: makulatura va plastik yig'ish

**Daraja:** Murakkab · **Muddat:** 4 hafta · **Jamoa:** 3 o'quvchi

## Muammo
Makulatura yig'ish aksiyalarida qaysi sinf qancha topshirgani qog'ozda yuritiladi va qiziqish tez so'nadi.

**Foydalanuvchilar:** Sinflar, eko-klub, maktab ma'muriyati

## Asosiy funksiyalar (MVP)
- Mas'ul topshirilgan hajmni kiritadi: sinf, tur (qog'oz, plastik, batareya), kg
- Sinflar reytingi, haftalik va umumiy
- Saqlangan daraxtlar va CO₂ taxminiy hisobi (formula kodda ko'rsatiladi)
- Har dushanba e'lon: o'tgan hafta g'olibi

## Buyruqlar
`/start` `/topshirish` `/reyting` `/mening_sinfim` `/natija` `/admin`

## Ma'lumotlar bazasi
- `classes`: nomi, sinf_rahbari
- `deposits`: class_id, tur, kg, sana, kiritgan_id
- `factors`: tur, daraxt_koeff, co2_koeff

## Bosqichlar
- 1-hafta: sinflar va topshirishni kiritish
- 2-hafta: reyting va haftalik e'lon
- 3-hafta: ekologik ta'sir hisobi, grafik rasm (matplotlib)
- 4-hafta: maktablararo musobaqa rejimi

## Bonus vazifalar
- Telegram Mini App'da jonli reyting
- Topshirish joylari xaritasi

## Nimani o'rganasiz
- agregatsiya va reytinglar
- matplotlib grafiklari
- manbali koeffitsientlar bilan ishlash

## Daromad g'oyasi
Qayta ishlash kompaniyalari homiyligi; tuman bo'yicha musobaqa tashkil qilish.

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
