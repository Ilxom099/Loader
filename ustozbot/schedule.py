"""Jadval matnlari va eslatma vaqtini hisoblash. Telegramga bog'liq emas — testlash oson."""
import calendar
from datetime import date, datetime, timedelta

from db import WEEKDAYS
from plans import REMINDER_OFFSETS

# Server bir necha daqiqa to'xtab qolsa ham eslatma yo'qolmasin, lekin eskirgani ham ketmasin.
REMINDER_WINDOW_MIN = 5

MONTHS = ["Yanvar", "Fevral", "Mart", "Aprel", "May", "Iyun",
          "Iyul", "Avgust", "Sentabr", "Oktabr", "Noyabr", "Dekabr"]


def lesson_line(lesson) -> str:
    room = f", {lesson['room']}" if lesson["room"] else ""
    return f"{lesson['start_time']} — {lesson['class_name']}, {lesson['subject']}{room}"


def day_text(lessons, day: date) -> str:
    head = f"<b>{WEEKDAYS[day.weekday()]}, {day.strftime('%d.%m.%Y')}</b>"
    if not lessons:
        return head + "\nDars yo'q."
    return head + "\n" + "\n".join(f"{i}. {lesson_line(l)}" for i, l in enumerate(lessons, 1))


def week_text(all_lessons, week_start: date) -> str:
    parts = [f"<b>Haftalik jadval ({week_start.strftime('%d.%m')} — {(week_start + timedelta(days=6)).strftime('%d.%m')})</b>"]
    for i in range(7):
        day = week_start + timedelta(days=i)
        todays = [l for l in all_lessons if l["weekday"] == i]
        if todays or i < 6:
            parts.append(day_text(todays, day))
    return "\n\n".join(parts)


def month_text(all_lessons, year: int, month: int) -> str:
    days_in_month = calendar.monthrange(year, month)[1]
    total = 0
    parts = [f"<b>Oylik jadval — {MONTHS[month - 1]} {year}</b>"]
    for d in range(1, days_in_month + 1):
        day = date(year, month, d)
        todays = [l for l in all_lessons if l["weekday"] == day.weekday()]
        if not todays:
            continue
        total += len(todays)
        short = "; ".join(f"{l['start_time']} {l['class_name']}" for l in todays)
        parts.append(f"{day.strftime('%d.%m')} {WEEKDAYS[day.weekday()][:3]}: {short}")
    parts.append(f"\nJami: {total} ta dars")
    return "\n".join(parts)


def due_reminders(lessons, now: datetime):
    """(dars, offset) juftlari: hozir yuborilishi kerak bo'lgan eslatmalar.

    `now` — mahalliy vaqt (naive yoki aware, faqat sana/soat ishlatiladi).
    """
    result = []
    for lesson in lessons:
        if lesson["weekday"] != now.weekday():
            continue
        h, m = map(int, lesson["start_time"].split(":"))
        start = now.replace(hour=h, minute=m, second=0, microsecond=0)
        for offset in REMINDER_OFFSETS:
            fire_at = start - timedelta(minutes=offset)
            if fire_at <= now < fire_at + timedelta(minutes=REMINDER_WINDOW_MIN):
                result.append((lesson, offset))
    return result


def reminder_text(lesson, offset: int) -> str:
    room = f"\nXona: {lesson['room']}" if lesson["room"] else ""
    return (
        f"⏰ <b>{offset} daqiqadan keyin dars</b>\n"
        f"{lesson['start_time']} — {lesson['class_name']}, {lesson['subject']}{room}"
    )


def sms_text(lesson, offset: int) -> str:
    room = f", {lesson['room']}" if lesson["room"] else ""
    return f"UstozBot: {offset} daqiqadan keyin dars {lesson['start_time']} {lesson['class_name']} {lesson['subject']}{room}"


def parse_time(s: str) -> str | None:
    try:
        return datetime.strptime(s, "%H:%M").strftime("%H:%M")
    except ValueError:
        return None


def parse_weekday(s: str) -> int | None:
    s = s.lower().replace("‘", "'").replace("’", "'")
    for i, name in enumerate(WEEKDAYS):
        if name.lower().startswith(s[:3]) and len(s) >= 2:
            return i
    if s.isdigit() and 1 <= int(s) <= 7:
        return int(s) - 1
    return None


def parse_date(s: str, today: date) -> date | None:
    """'2026-10-15', '15.10', '15.10.2026', 'ertaga', '+3' formatlari."""
    s = s.strip().lower()
    if s == "ertaga":
        return today + timedelta(days=1)
    if s.startswith("+") and s[1:].isdigit():
        return today + timedelta(days=int(s[1:]))
    for fmt in ("%Y-%m-%d", "%d.%m.%Y"):
        try:
            return datetime.strptime(s, fmt).date()
        except ValueError:
            pass
    # Yilsiz sana (15.10): shu yil, o'tib ketgan bo'lsa keyingi yil.
    for year in (today.year, today.year + 1):
        try:
            d = datetime.strptime(f"{s}.{year}", "%d.%m.%Y").date()
        except ValueError:
            continue
        if d >= today:
            return d
    return None
