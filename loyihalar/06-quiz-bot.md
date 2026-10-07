# 06. Sinf viktorinasi (Quiz) boti

**Daraja:** O'rta · **Muddat:** 3 hafta · **Jamoa:** 2 o'quvchi

## Muammo
O'qituvchi tez test o'tkazib, natijani darhol ko'rishni xohlaydi.

**Foydalanuvchilar:** O'qituvchi (test tuzadi), o'quvchilar (yechadi)

## Asosiy funksiyalar (MVP)
- O'qituvchi savollarni matn yoki Excel fayl orqali yuklaydi
- Test kodi beriladi; o'quvchi /test KOD bilan kiradi
- Har savolga vaqt chegarasi, javoblar aralashtiriladi
- O'qituvchiga natijalar jadvali va Excel fayl

## Buyruqlar
`/start` `/yangi_test` `/savol_qosh` `/test` `/natijalar`

## Ma'lumotlar bazasi
- `quizzes`: teacher_id, nomi, kod, savol_vaqti, faol
- `questions`: quiz_id, matn, variantlar, togri_index
- `attempts`: quiz_id, student_id, ball, boshlandi, tugadi
- `answers`: attempt_id, question_id, tanlov, togri

## Bosqichlar
- 1-hafta: test va savol yaratish, test kodi
- 2-hafta: o'quvchi testni yechadi, vaqt chegarasi, ball
- 3-hafta: Excel import/eksport (openpyxl), natijalar jadvali

## Bonus vazifalar
- Telegram guruhida jonli viktorina (Kahoot uslubida)
- Savol rasmlari

## Nimani o'rganasiz
- rollar (o'qituvchi/o'quvchi)
- openpyxl
- FSM
- taymerlar

## Daromad g'oyasi
Start: oyiga 5 ta test bepul; Pro o'qituvchi: cheksiz test va Excel hisobot.

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
