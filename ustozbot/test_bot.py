"""Telegramsiz testlar: python -m unittest test_bot.py"""
import asyncio
import os
import tempfile
import unittest
from datetime import date, datetime

os.environ.setdefault("DB_PATH", os.path.join(tempfile.mkdtemp(), "test.sqlite3"))

import bot  # noqa: E402
import schedule as sch  # noqa: E402
from db import DB  # noqa: E402


class FakeBot:
    def __init__(self):
        self.sent = []

    async def send_message(self, chat_id, text, **kw):
        self.sent.append((chat_id, text))


class ScheduleTests(unittest.TestCase):
    lesson = {"id": 1, "weekday": 0, "start_time": "08:30", "class_name": "7-A", "subject": "Matematika", "room": "12"}

    def test_reminders_60_30_10(self):
        monday = datetime(2026, 10, 5)  # dushanba
        self.assertEqual([o for _, o in sch.due_reminders([self.lesson], monday.replace(hour=7, minute=30))], [60])
        self.assertEqual([o for _, o in sch.due_reminders([self.lesson], monday.replace(hour=8, minute=2))], [30])
        self.assertEqual([o for _, o in sch.due_reminders([self.lesson], monday.replace(hour=8, minute=24))], [10])
        self.assertEqual(sch.due_reminders([self.lesson], monday.replace(hour=8, minute=26)), [])
        self.assertEqual(sch.due_reminders([self.lesson], datetime(2026, 10, 6, 8, 20)), [])  # seshanba

    def test_parsers(self):
        today = date(2026, 10, 7)
        self.assertEqual(sch.parse_weekday("Dushanba"), 0)
        self.assertEqual(sch.parse_weekday("payshanba"), 3)
        self.assertEqual(sch.parse_weekday("6"), 5)
        self.assertIsNone(sch.parse_weekday("xyz"))
        self.assertEqual(sch.parse_time("8:05"), "08:05")
        self.assertIsNone(sch.parse_time("25:00"))
        self.assertEqual(sch.parse_date("15.10", today), date(2026, 10, 15))
        self.assertEqual(sch.parse_date("01.09", today), date(2027, 9, 1))
        self.assertEqual(sch.parse_date("ertaga", today), date(2026, 10, 8))
        self.assertEqual(sch.parse_date("+3", today), date(2026, 10, 10))

    def test_month_text(self):
        text = sch.month_text([self.lesson], 2026, 10)
        self.assertIn("Jami: 4 ta dars", text)  # oktabr 2026: 4 ta dushanba


class TickTests(unittest.TestCase):
    def setUp(self):
        bot.db = DB(":memory:")
        self.t = bot.db.create_teacher(111, "Ustoz", "ultra", date(2030, 1, 1))
        cls = bot.db.add_class(self.t["id"], "7-A")
        bot.db.add_lesson(self.t["id"], cls["id"], "Fizika", 0, "09:00", None)
        bot.db.add_homework(self.t["id"], cls["id"], "5-mashq", date(2026, 10, 1), date(2026, 10, 6))
        bot.db.update_teacher(self.t["id"], phone="+998901234567")

    def run_tick(self, when: datetime, fake: FakeBot):
        bot.now_local = lambda: when
        asyncio.run(bot.tick(fake))

    def test_reminder_sent_once_and_sms_counted(self):
        fake = FakeBot()
        self.run_tick(datetime(2026, 10, 5, 8, 50), fake)
        self.run_tick(datetime(2026, 10, 5, 8, 51), fake)
        reminders = [t for _, t in fake.sent if "daqiqadan keyin dars" in t]
        self.assertEqual(len(reminders), 1)
        self.assertEqual(bot.db.sms_used(self.t["id"], "2026-10"), 1)

    def test_digests(self):
        fake = FakeBot()
        self.run_tick(datetime(2026, 10, 5, 7, 0), fake)  # dushanba: haftalik + kunlik
        texts = [t for _, t in fake.sent]
        self.assertTrue(any("Haftalik jadval" in t for t in texts))
        self.assertTrue(any("Xayrli tong" in t for t in texts))
        fake.sent.clear()
        self.run_tick(datetime(2026, 10, 5, 18, 0), fake)  # ertaga muddati — 5-mashq
        self.assertTrue(any("5-mashq" in t for _, t in fake.sent))

    def test_expired_teacher_gets_nothing(self):
        bot.db.update_teacher(self.t["id"], paid_until="2026-10-01")
        fake = FakeBot()
        self.run_tick(datetime(2026, 10, 5, 8, 50), fake)
        self.assertEqual(fake.sent, [])


if __name__ == "__main__":
    unittest.main()
