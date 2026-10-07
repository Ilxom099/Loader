# UstozBot — biznes-reja (qisqa)

## 1. Muammo
O'qituvchi kuniga bir necha dars o'tadi, jadval tez-tez o'zgaradi (almashtirish, ko'chirilgan dars),
uyga vazifalar va ularning muddati daftarda yoki xotirada qoladi, sinflar va o'quvchilar ro'yxati tarqoq.

## 2. Yechim
Telegram bot — o'qituvchilar allaqachon har kuni foydalanadigan ilova ichida:
kunlik / haftalik / oylik jadval, darsdan 60/30/10 daqiqa oldin eslatma (Telegram + SMS),
uyga vazifalar arxivi va muddat eslatmalari, sinf va o'quvchilar ro'yxati.

## 3. Tariflar va ularni nima oqlaydi

| Tarif | Narx | Kimga | Asosiy qiymat |
|---|---|---|---|
| **Start** | 5 000 so'm / oy | Har qanday o'qituvchi, kirish eshigi | Jadval + Telegram eslatma, 3 sinf |
| **Pro** | 30 000 so'm / oy | Ko'p sinfli, faol o'qituvchi | Cheksiz sinf, oylik jadval + eksport, 100 SMS, vazifani sinf guruhiga yuborish, davomat, almashtirish xabari |
| **Ultra** | 100 000 so'm / oy | Sinf rahbari, repetitor, metodist | 500 SMS, AI (dars rejasi, test, vazifa g'oyalari), baholar jurnali, ota-onaga haftalik hisobot, shaxsiy yordam |

**Muhim:** Telegram xabari bepul, SMS esa pullik. Bir o'qituvchiga barcha eslatmalar SMS bilan
oyiga ~330 SMS (5 dars × 3 eslatma × 22 kun) kerak bo'ladi — 5 000 so'm buni qoplamaydi.
Shuning uchun Start'da SMS yo'q, Pro'da faqat "10 daqiqa qoldi" SMS (≈110/oy → 100 limit),
Ultra'da 500. Qoida: SMS xarajati tarif narxining 30% idan oshmasin. Bir SMS narxi: **[__ so'm]**
— provayder (Eskiz, Playmobile) bilan shartnoma bo'yicha aniqlanadi va limitlar qayta hisoblanadi.

## 4. Qo'shimcha daromad manbalari
1. **Maktab litsenziyasi (B2B)** — butun maktab uchun yillik paket: admin panel, jadvalni direktor/o'quv
   bo'limi yuklaydi, barcha o'qituvchilar Pro. Narx: **[__ so'm / yil]**.
2. **SMS paketlari** — limitdan keyin 100 / 300 / 1000 talik paketlar ustama bilan.
3. **Ota-ona obunasi** — farzandning vazifa, davomat, baholari haqida haftalik xabar.
4. **Yillik to'lov** — 12 oy uchun 10 oy narxi (botda `/tolov pro 12`).

## 5. Daromad modeli (taxmin, bozor ma'lumoti emas)
Taxmin: pullik foydalanuvchilarning 60% Start, 30% Pro, 10% Ultra.
O'rtacha daromad: 0,6×5 000 + 0,3×30 000 + 0,1×100 000 = **22 000 so'm / oy**.

| Ssenariy | Pullik o'qituvchi | Oylik | Yillik |
|---|---|---|---|
| Pilot | 500 | 11 mln so'm | 132 mln so'm |
| O'sish | 2 000 | 44 mln so'm | 528 mln so'm |
| Masshtab | 10 000 | 220 mln so'm | 2,64 mlrd so'm |

Maktab litsenziyasi va SMS paketlari bu hisobga kirmagan.

## 6. Xarajatlar (to'ldirish kerak)
| Modda | Oyiga |
|---|---|
| VPS server | [__ so'm] |
| SMS (Pro/Ultra limitlari bo'yicha) | [__ so'm] |
| To'lov tizimi komissiyasi (Payme/Click) | [__ %] |
| AI API (Ultra) | [__ so'm] |
| Marketing | [__ so'm] |

## 7. Qo'shish kerak bo'lgan xizmatlar (bosqichma-bosqich)
- **3–4 oy:** Payme / Click avtomatik to'lov, Eskiz SMS shlyuz, Excel import, almashtirish xabarlari,
  referral (`/start ref_KOD`).
- **5–8 oy:** AI yordamchi, baholar jurnali, davomat, ota-ona hisobotlari, PDF/Excel eksport.
- **9–12 oy:** Maktab admin paneli (Telegram Mini App), maktab litsenziyasi, PostgreSQL, zaxira nusxa,
  bayram va ta'til kunlari kalendari.

## 8. Sotuv va marketing
14 kun bepul Pro · "3 hamkasbni taklif qil — 1 oy Pro bepul" · o'qituvchilar Telegram guruhlari va
metodik kanallar · maktab direktorlariga bepul demo.

## 9. Xavflar
| Xavf | Javob |
|---|---|
| O'qituvchi to'lashni istamaydi | Start 5 000 so'm, 14 kun sinov |
| Jadvalni kiritish qiyin | Excel import, maktab admini bir marta yuklaydi |
| SMS xarajati | Tarif limitlari, qo'shimcha paketlar |
| Shaxsiy ma'lumotlar | O'zbekiston qonunchiligiga mos mahalliy saqlash (yurist bilan tekshirish), minimal maydonlar |
| Elektron jurnallar raqobati | Shaxsiy yordamchi sifatida pozitsiya, integratsiya |

## 10. Keyingi qadamlar
1. Botni serverga joylash, 3 maktabda 30 o'qituvchi bilan bepul pilot.
2. SMS provayder va Payme / Click bilan shartnoma.
3. 2 oydan keyin Start va Pro tariflarini yoqish.
