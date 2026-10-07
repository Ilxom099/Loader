"""UstozBot MVP — o'qituvchilar uchun dars jadvali, eslatma va uyga vazifa boti.

Ishga tushirish:  BOT_TOKEN=... ADMIN_IDS=123 python bot.py
"""
import asyncio
import html
import logging
from datetime import date, datetime, timedelta

from aiogram import Bot, Dispatcher, F, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import KeyboardButton, Message, ReplyKeyboardMarkup

import config
import schedule as sch
from db import DB, WEEKDAYS
from plans import PLANS, TRIAL_DAYS, TRIAL_PLAN, fmt_price, plans_text
from sms import send_sms

log = logging.getLogger("ustozbot")
db = DB(config.DB_PATH)
router = Router()

HELP = """<b>UstozBot buyruqlari</b>

<b>Sozlash</b>
/maktab 21-maktab — maktabni kiritish
/fan Matematika — fanni kiritish
/telefon +998901234567 — SMS uchun raqam

<b>Sinflar va o'quvchilar</b>
/sinf_qosh 7-A
/sinflar
/oquvchi_qosh 7-A | Aliyev Vali | +998901234567
/oquvchilar 7-A

<b>Dars jadvali</b>
/dars_qosh Dushanba 08:30 7-A Matematika 12-xona
/darslar — barcha darslar (ID bilan)
/dars_ochir 5
/bugun · /ertaga · /hafta · /oy

<b>Uyga vazifa</b>
/vazifa 7-A 15.10 | 25-mashq, 3-bet
  (muddat: 15.10, 2026-10-15, ertaga, +3)
/vazifalar · /bajarildi 4

<b>Obuna</b>
/tarif · /tolov pro · /holat"""

MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="/bugun"), KeyboardButton(text="/hafta"), KeyboardButton(text="/oy")],
        [KeyboardButton(text="/vazifalar"), KeyboardButton(text="/sinflar"), KeyboardButton(text="/holat")],
    ],
    resize_keyboard=True,
)


def clean(s: str) -> str:
    """Foydalanuvchi matni HTML xabarni buzmasin."""
    return html.escape(s.strip(), quote=False)


def now_local() -> datetime:
    return datetime.now(config.TZ)


def today() -> date:
    return now_local().date()


def is_active(teacher) -> bool:
    return date.fromisoformat(teacher["paid_until"]) >= today()


async def send_long(bot: Bot, chat_id: int, text: str):
    """Telegram 4096 belgidan uzun xabarni qatorlar bo'yicha bo'lib yuboradi."""
    chunk = ""
    for line in text.split("\n"):
        if len(chunk) + len(line) + 1 > 4000:
            await bot.send_message(chat_id, chunk)
            chunk = ""
        chunk += line + "\n"
    if chunk.strip():
        await bot.send_message(chat_id, chunk)


async def require_teacher(message: Message):
    teacher = db.get_teacher(message.from_user.id)
    if teacher is None:
        await message.answer("Avval /start bosing.")
        return None
    if not is_active(teacher):
        await message.answer("Obuna muddati tugagan. Davom ettirish uchun: /tarif")
        return None
    return teacher


# ---------------- ro'yxatdan o'tish va sozlamalar ----------------

@router.message(CommandStart())
async def cmd_start(message: Message):
    teacher = db.get_teacher(message.from_user.id)
    if teacher is None:
        until = today() + timedelta(days=TRIAL_DAYS - 1)
        db.create_teacher(message.from_user.id, clean(message.from_user.full_name), TRIAL_PLAN, until)
        await message.answer(
            f"Assalomu alaykum, {clean(message.from_user.full_name)}!\n\n"
            f"UstozBot dars jadvalingizni yuboradi, darsdan 60, 30 va 10 daqiqa oldin eslatadi "
            f"va uyga vazifalarni saqlaydi.\n\n"
            f"Sizga {TRIAL_DAYS} kun <b>{PLANS[TRIAL_PLAN]['title']}</b> bepul berildi "
            f"({until.strftime('%d.%m.%Y')} gacha).\n\n"
            f"Boshlash: /sinf_qosh 7-A, keyin /dars_qosh ...\nBarcha buyruqlar: /yordam",
            reply_markup=MENU,
        )
    else:
        await message.answer("Qaytganingizdan xursandmiz! /yordam", reply_markup=MENU)


@router.message(Command("yordam", "help"))
async def cmd_help(message: Message):
    await message.answer(HELP)


@router.message(Command("maktab"))
async def cmd_school(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    if not command.args:
        return await message.answer("Masalan: /maktab 21-maktab, Chilonzor")
    db.set_school(teacher["id"], clean(command.args))
    await message.answer("Maktab saqlandi.")


@router.message(Command("fan"))
async def cmd_subject(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    if not command.args:
        return await message.answer("Masalan: /fan Matematika")
    db.update_teacher(teacher["id"], subject=clean(command.args))
    await message.answer("Fan saqlandi.")


@router.message(Command("telefon"))
async def cmd_phone(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    phone = (command.args or "").replace(" ", "")
    if not (phone.startswith("+998") and len(phone) == 13 and phone[1:].isdigit()):
        return await message.answer("Raqamni +998901234567 ko'rinishida yozing.")
    db.update_teacher(teacher["id"], phone=phone)
    await message.answer("Telefon saqlandi. SMS eslatmalar Pro va Ultra tariflarida ishlaydi.")


# ---------------- sinflar va o'quvchilar ----------------

@router.message(Command("sinf_qosh"))
async def cmd_add_class(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    name = clean(command.args or "").upper()
    if not name:
        return await message.answer("Masalan: /sinf_qosh 7-A")
    limit = PLANS[teacher["plan"]]["max_classes"]
    existing = db.classes(teacher["id"])
    if limit is not None and len(existing) >= limit and name not in {c["name"] for c in existing}:
        return await message.answer(
            f"{PLANS[teacher['plan']]['title']} tarifida {limit} tagacha sinf. Ko'proq uchun: /tarif"
        )
    db.add_class(teacher["id"], name)
    await message.answer(f"{name} sinfi qo'shildi.")


@router.message(Command("sinflar"))
async def cmd_classes(message: Message):
    teacher = await require_teacher(message)
    if not teacher:
        return
    rows = db.classes(teacher["id"])
    if not rows:
        return await message.answer("Sinf yo'q. /sinf_qosh 7-A")
    await message.answer("<b>Sinflar</b>\n" + "\n".join(f"• {c['name']} — {c['n_students']} o'quvchi" for c in rows))


async def find_class(message: Message, teacher, name: str):
    name = clean(name).upper()
    cls = db.get_class(teacher["id"], name)
    if cls is None:
        await message.answer(f"{name} sinfi topilmadi. Avval: /sinf_qosh {name}")
    return cls


@router.message(Command("oquvchi_qosh"))
async def cmd_add_student(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    parts = [clean(p) for p in (command.args or "").split("|")]
    if len(parts) < 2 or not parts[1]:
        return await message.answer("Masalan: /oquvchi_qosh 7-A | Aliyev Vali | +998901234567")
    cls = await find_class(message, teacher, parts[0])
    if not cls:
        return
    phone = parts[2] if len(parts) > 2 and parts[2] else None
    db.add_student(cls["id"], parts[1], phone)
    await message.answer(f"{parts[1]} {cls['name']} sinfiga qo'shildi.")


@router.message(Command("oquvchilar"))
async def cmd_students(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    if not command.args:
        return await message.answer("Masalan: /oquvchilar 7-A")
    cls = await find_class(message, teacher, command.args)
    if not cls:
        return
    rows = db.students(cls["id"])
    if not rows:
        return await message.answer("Bu sinfda o'quvchi yo'q.")
    lines = [f"{i}. {s['full_name']}" + (f" — {s['parent_phone']}" if s["parent_phone"] else "") for i, s in enumerate(rows, 1)]
    await send_long(message.bot, message.chat.id, f"<b>{cls['name']} o'quvchilari</b>\n" + "\n".join(lines))


# ---------------- dars jadvali ----------------

@router.message(Command("dars_qosh"))
async def cmd_add_lesson(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    parts = clean(command.args or "").split()
    usage = "Masalan: /dars_qosh Dushanba 08:30 7-A Matematika 12-xona"
    if len(parts) < 3:
        return await message.answer(usage)
    weekday, start, class_name = sch.parse_weekday(parts[0]), sch.parse_time(parts[1]), parts[2]
    if weekday is None or start is None:
        return await message.answer("Kun yoki vaqt noto'g'ri.\n" + usage)
    cls = await find_class(message, teacher, class_name)
    if not cls:
        return
    subject = parts[3] if len(parts) > 3 else (teacher["subject"] or "Dars")
    room = " ".join(parts[4:]) or None
    lesson_id = db.add_lesson(teacher["id"], cls["id"], subject, weekday, start, room)
    await message.answer(f"Dars qo'shildi (ID {lesson_id}): {WEEKDAYS[weekday]} {start}, {cls['name']}, {subject}")


@router.message(Command("darslar"))
async def cmd_lessons(message: Message):
    teacher = await require_teacher(message)
    if not teacher:
        return
    rows = db.lessons(teacher["id"])
    if not rows:
        return await message.answer("Dars yo'q. /dars_qosh Dushanba 08:30 7-A Matematika")
    lines = [f"[{l['id']}] {WEEKDAYS[l['weekday']][:3]} {sch.lesson_line(l)}" for l in rows]
    await send_long(message.bot, message.chat.id, "<b>Barcha darslar</b>\n" + "\n".join(lines))


@router.message(Command("dars_ochir"))
async def cmd_delete_lesson(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    if not (command.args and command.args.strip().isdigit()):
        return await message.answer("Masalan: /dars_ochir 5 (ID /darslar da)")
    ok = db.delete_lesson(teacher["id"], int(command.args))
    await message.answer("Dars o'chirildi." if ok else "Bunday dars topilmadi.")


@router.message(Command("bugun", "ertaga"))
async def cmd_day(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    day = today() + timedelta(days=1 if command.command == "ertaga" else 0)
    await message.answer(sch.day_text(db.lessons(teacher["id"], day.weekday()), day))


@router.message(Command("hafta"))
async def cmd_week(message: Message):
    teacher = await require_teacher(message)
    if not teacher:
        return
    week_start = today() - timedelta(days=today().weekday())
    await send_long(message.bot, message.chat.id, sch.week_text(db.lessons(teacher["id"]), week_start))


@router.message(Command("oy"))
async def cmd_month(message: Message):
    teacher = await require_teacher(message)
    if not teacher:
        return
    if not PLANS[teacher["plan"]]["monthly_schedule"]:
        return await message.answer("Oylik jadval Pro va Ultra tariflarida. /tarif")
    t = today()
    await send_long(message.bot, message.chat.id, sch.month_text(db.lessons(teacher["id"]), t.year, t.month))


# ---------------- uyga vazifa ----------------

@router.message(Command("vazifa"))
async def cmd_homework(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    usage = "Masalan: /vazifa 7-A 15.10 | 25-mashq, 3-bet"
    head, _, text = (command.args or "").partition("|")
    head_parts = head.split()
    if len(head_parts) != 2 or not text.strip():
        return await message.answer(usage)
    cls = await find_class(message, teacher, head_parts[0])
    if not cls:
        return
    due = sch.parse_date(head_parts[1], today())
    if due is None or due < today():
        return await message.answer("Muddat noto'g'ri.\n" + usage)
    hw_id = db.add_homework(teacher["id"], cls["id"], clean(text), today(), due)
    await message.answer(
        f"Vazifa saqlandi (ID {hw_id}): {cls['name']}, muddat {due.strftime('%d.%m.%Y')}.\n"
        f"Muddatdan bir kun oldin soat {config.HOMEWORK_EVENING_HOUR}:00 da va muddat kuni ertalab eslataman."
    )


@router.message(Command("vazifalar"))
async def cmd_homeworks(message: Message):
    teacher = await require_teacher(message)
    if not teacher:
        return
    rows = db.homeworks(teacher["id"])
    if not rows:
        return await message.answer("Ochiq vazifa yo'q.")
    lines = [
        f"[{h['id']}] {h['class_name']} — {date.fromisoformat(h['due_on']).strftime('%d.%m')}: {h['text']}"
        for h in rows
    ]
    await send_long(message.bot, message.chat.id, "<b>Uyga vazifalar</b>\n" + "\n".join(lines) + "\n\nTekshirildi: /bajarildi ID")


@router.message(Command("bajarildi"))
async def cmd_done(message: Message, command: CommandObject):
    teacher = await require_teacher(message)
    if not teacher:
        return
    if not (command.args and command.args.strip().isdigit()):
        return await message.answer("Masalan: /bajarildi 4")
    ok = db.mark_homework_done(teacher["id"], int(command.args))
    await message.answer("Belgilandi ✅" if ok else "Bunday vazifa topilmadi.")


# ---------------- tarif va to'lov ----------------

@router.message(Command("tarif"))
async def cmd_plans(message: Message):
    await message.answer(plans_text())


@router.message(Command("holat"))
async def cmd_status(message: Message):
    teacher = db.get_teacher(message.from_user.id)
    if teacher is None:
        return await message.answer("Avval /start bosing.")
    plan = PLANS[teacher["plan"]]
    month = today().strftime("%Y-%m")
    state = "faol" if is_active(teacher) else "tugagan"
    await message.answer(
        f"Tarif: <b>{plan['title']}</b> ({state})\n"
        f"Muddat: {date.fromisoformat(teacher['paid_until']).strftime('%d.%m.%Y')} gacha\n"
        f"SMS: {db.sms_used(teacher['id'], month)} / {plan['sms_per_month']} (shu oy)\n"
        f"Telefon: {teacher['phone'] or 'kiritilmagan (/telefon)'}"
    )


@router.message(Command("tolov"))
async def cmd_pay(message: Message, command: CommandObject):
    teacher = db.get_teacher(message.from_user.id)
    if teacher is None:
        return await message.answer("Avval /start bosing.")
    args = (command.args or "").split()
    plan_key = args[0].lower() if args else ""
    if plan_key not in PLANS:
        return await message.answer("Masalan: /tolov pro  yoki  /tolov ultra 12  (12 oy — 2 oy bepul)")
    months = int(args[1]) if len(args) > 1 and args[1].isdigit() and 1 <= int(args[1]) <= 12 else 1
    # Yillik to'lov: 12 oy uchun 10 oy narxi.
    billable = 10 if months == 12 else months
    amount = PLANS[plan_key]["price"] * billable
    pay_id = db.create_payment(teacher["id"], plan_key, amount, months)
    await message.answer(
        f"To'lov #{pay_id}: {PLANS[plan_key]['title']}, {months} oy — <b>{fmt_price(amount)}</b>\n\n"
        f"Karta: <code>{config.PAYMENT_CARD}</code>\n"
        f"Izohga #{pay_id} yozing va chekni shu yerga yuboring. Admin tasdiqlagach obuna yoqiladi."
    )
    for admin in config.ADMIN_IDS:
        await message.bot.send_message(
            admin,
            f"Yangi to'lov #{pay_id}: {teacher['full_name']} (id {teacher['telegram_id']}), "
            f"{plan_key} × {months} oy = {fmt_price(amount)}\nTasdiqlash: /tasdiq {pay_id}",
        )


@router.message(F.photo | F.document)
async def forward_receipt(message: Message):
    """Chek rasmini adminlarga uzatadi."""
    for admin in config.ADMIN_IDS:
        await message.forward(admin)
    if config.ADMIN_IDS:
        await message.answer("Chek adminga yuborildi.")


@router.message(Command("tasdiq"))
async def cmd_confirm(message: Message, command: CommandObject):
    if message.from_user.id not in config.ADMIN_IDS:
        return
    if not (command.args and command.args.strip().isdigit()):
        return await message.answer("/tasdiq TOLOV_ID")
    pay = db.get_payment(int(command.args))
    if pay is None or pay["status"] == "paid":
        return await message.answer("To'lov topilmadi yoki allaqachon tasdiqlangan.")
    until = db.extend_subscription(pay["teacher_id"], pay["plan"], pay["months"], today())
    db.mark_payment_paid(pay["id"])
    teacher = db.teacher_by_id(pay["teacher_id"])
    await message.answer(f"Tasdiqlandi. {teacher['full_name']}: {pay['plan']} {until} gacha.")
    await message.bot.send_message(
        teacher["telegram_id"],
        f"✅ To'lov qabul qilindi. Tarif: <b>{PLANS[pay['plan']]['title']}</b>, "
        f"{until.strftime('%d.%m.%Y')} gacha. Rahmat!",
    )


@router.message(Command("statistika"))
async def cmd_stats(message: Message):
    if message.from_user.id not in config.ADMIN_IDS:
        return
    s = db.stats()
    await message.answer(
        f"O'qituvchilar: {s['teachers']}\nFaol obuna: {s['active']}\nJami tushum: {fmt_price(s['paid_sum'])}"
    )


# ---------------- fon jarayoni: eslatmalar va jadvallar ----------------

async def maybe_send_sms(teacher, lesson, offset: int, now: datetime):
    plan = PLANS[teacher["plan"]]
    if offset not in plan["sms_offsets"] or not teacher["phone"]:
        return
    month = now.strftime("%Y-%m")
    if db.sms_used(teacher["id"], month) >= plan["sms_per_month"]:
        return
    text = sch.sms_text(lesson, offset)
    if await asyncio.to_thread(send_sms, teacher["phone"], text):
        db.log_sms(teacher["id"], month, teacher["phone"], text)


async def send_digests(bot: Bot, teacher, now: datetime):
    t = now.date()
    plan = PLANS[teacher["plan"]]
    chat = teacher["telegram_id"]

    # Ertalabki jadvallar faqat 07:00–12:00 oralig'ida (bot kunduzi qayta ishga tushsa, kech "xayrli tong" ketmasin).
    if config.DIGEST_HOUR <= now.hour < 12:
        # Oylik — har oyning 1-kuni (Pro/Ultra), haftalik — dushanba, kunlik — har kuni.
        if t.day == 1 and plan["monthly_schedule"] and db.mark_digest(teacher["id"], "monthly", t.strftime("%Y-%m")):
            await send_long(bot, chat, sch.month_text(db.lessons(teacher["id"]), t.year, t.month))
        if t.weekday() == 0 and db.mark_digest(teacher["id"], "weekly", t.isoformat()):
            await send_long(bot, chat, sch.week_text(db.lessons(teacher["id"]), t))
        if db.mark_digest(teacher["id"], "daily", t.isoformat()):
            text = "☀️ Xayrli tong!\n\n" + sch.day_text(db.lessons(teacher["id"], t.weekday()), t)
            due = db.homeworks_due(teacher["id"], t)
            if due:
                text += "\n\n📚 <b>Bugun muddati tugaydigan vazifalar</b>\n" + "\n".join(
                    f"[{h['id']}] {h['class_name']}: {h['text']}" for h in due
                )
            await send_long(bot, chat, text)
            # Arxiv muddati o'tgan vazifalarni tozalash (kuniga bir marta).
            if plan["homework_archive_days"] is not None:
                db.purge_old_homeworks(teacher["id"], t - timedelta(days=plan["homework_archive_days"]))

    if now.hour >= config.HOMEWORK_EVENING_HOUR and db.mark_digest(teacher["id"], "hw_evening", t.isoformat()):
        due = db.homeworks_due(teacher["id"], t + timedelta(days=1))
        if due:
            await send_long(bot, chat, "📚 <b>Ertaga muddati tugaydigan vazifalar</b>\n" + "\n".join(
                f"[{h['id']}] {h['class_name']}: {h['text']}" for h in due
            ))


async def tick(bot: Bot):
    now = now_local().replace(tzinfo=None)
    for teacher in db.active_teachers(now.date()):
        try:
            for lesson, offset in sch.due_reminders(db.lessons(teacher["id"], now.weekday()), now):
                if db.mark_reminder(lesson["id"], now.date(), offset):
                    await bot.send_message(teacher["telegram_id"], sch.reminder_text(lesson, offset))
                    await maybe_send_sms(teacher, lesson, offset, now)
            await send_digests(bot, teacher, now)
        except Exception:
            # Bitta o'qituvchidagi xato (masalan botni bloklagan) boshqalarga ta'sir qilmasin.
            log.exception("tick xatosi, teacher_id=%s", teacher["id"])


async def scheduler_loop(bot: Bot):
    while True:
        await tick(bot)
        await asyncio.sleep(30)


async def main():
    logging.basicConfig(level=logging.INFO)
    if not config.BOT_TOKEN:
        raise SystemExit("BOT_TOKEN muhit o'zgaruvchisini kiriting.")
    bot = Bot(config.BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_router(router)
    asyncio.create_task(scheduler_loop(bot))
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
