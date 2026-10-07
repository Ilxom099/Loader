"""Tariflar va ularning limitlari. Taqdimotdagi solishtirma jadval bilan bir xil."""

PLANS = {
    "start": {
        "title": "Start",
        "price": 5_000,
        "max_classes": 3,
        "monthly_schedule": False,
        "sms_per_month": 0,
        "sms_offsets": [],  # Telegram eslatma bor, SMS yo'q
        "homework_archive_days": 30,
        "share_homework": False,
        "ai_requests": 0,
    },
    "pro": {
        "title": "Pro",
        "price": 30_000,
        "max_classes": None,  # cheksiz
        "monthly_schedule": True,
        "sms_per_month": 100,
        "sms_offsets": [10],  # SMS faqat "10 daqiqa qoldi" uchun
        "homework_archive_days": 365,
        "share_homework": True,
        "ai_requests": 0,
    },
    "ultra": {
        "title": "Ultra",
        "price": 100_000,
        "max_classes": None,
        "monthly_schedule": True,
        "sms_per_month": 500,
        "sms_offsets": [60, 30, 10],
        "homework_archive_days": None,  # cheksiz
        "share_homework": True,
        "ai_requests": 50,
    },
}

TRIAL_PLAN = "pro"
TRIAL_DAYS = 14

# Darsdan necha daqiqa oldin Telegram eslatma yuboriladi (barcha tariflar).
REMINDER_OFFSETS = [60, 30, 10]


def fmt_price(amount: int) -> str:
    return f"{amount:,}".replace(",", " ") + " so'm"


def plans_text() -> str:
    lines = ["<b>Tariflar (oyiga, 1 o'qituvchi)</b>\n"]
    for key, p in PLANS.items():
        classes = "cheksiz" if p["max_classes"] is None else f"{p['max_classes']} ta"
        archive = "cheksiz" if p["homework_archive_days"] is None else f"{p['homework_archive_days']} kun"
        monthly = "bor" if p["monthly_schedule"] else "yo'q"
        lines.append(
            f"<b>{p['title']}</b> — {fmt_price(p['price'])}\n"
            f"  • sinflar: {classes}\n"
            f"  • oylik jadval: {monthly}\n"
            f"  • SMS: {p['sms_per_month']} / oy\n"
            f"  • vazifa arxivi: {archive}\n"
            f"  • AI so'rovlar: {p['ai_requests']} / oy\n"
        )
    lines.append(f"Yangi foydalanuvchiga {TRIAL_DAYS} kun Pro bepul.\nTo'lov: /tolov start | pro | ultra")
    return "\n".join(lines)
