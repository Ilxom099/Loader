# 14. Ota-ona — o'qituvchi uchrashuv navbati

**Daraja:** Murakkab · **Muddat:** 4 hafta · **Jamoa:** 2–3 o'quvchi

## Muammo
Ota-onalar majlisida hammasi bir vaqtda keladi, o'qituvchi bilan alohida gaplashish uchun uzoq navbat.

**Foydalanuvchilar:** O'qituvchilar (vaqt ochadi), ota-onalar (band qiladi)

## Asosiy funksiyalar (MVP)
- O'qituvchi bo'sh vaqt oraliqlarini ochadi (masalan, 15 daqiqalik slotlar)
- Ota-ona o'qituvchi va bo'sh slotni tanlaydi
- Bir slotni ikki kishi band qila olmaydi; bekor qilish mumkin
- Uchrashuvdan 1 kun va 1 soat oldin eslatma

## Buyruqlar
`/start` `/oqituvchilar` `/band_qilish` `/uchrashuvlarim` `/slot_och` `/bekor`

## Ma'lumotlar bazasi
- `teachers`: telegram_id, ism, fan
- `slots`: teacher_id, boshlanish, tugash, holat
- `bookings`: slot_id, parent_id, farzand_ismi, izoh

## Bosqichlar
- 1-hafta: o'qituvchi slot ochadi
- 2-hafta: ota-ona band qiladi, ikki marta band qilishni oldini olish
- 3-hafta: eslatmalar, bekor qilish
- 4-hafta: kunlik jadval o'qituvchiga, statistika

## Bonus vazifalar
- Onlayn uchrashuv havolasi (Google Meet) qo'shish
- Uchrashuvdan keyin qisqa so'rovnoma

## Nimani o'rganasiz
- vaqt oraliqlari bilan ishlash
- poyga holati (race condition)
- eslatmalar

## Daromad g'oyasi
Xususiy maktablar va o'quv markazlari uchun oylik obuna.

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
