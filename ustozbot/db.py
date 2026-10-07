"""SQLite ombori. MVP uchun sinxron sqlite3 yetarli; keyin PostgreSQL'ga ko'chiriladi."""
import sqlite3
from datetime import date, datetime, timedelta

SCHEMA = """
CREATE TABLE IF NOT EXISTS schools (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE,
    district TEXT,
    license TEXT
);
CREATE TABLE IF NOT EXISTS teachers (
    id INTEGER PRIMARY KEY,
    telegram_id INTEGER NOT NULL UNIQUE,
    full_name TEXT NOT NULL,
    phone TEXT,
    subject TEXT,
    school_id INTEGER REFERENCES schools(id),
    plan TEXT NOT NULL,
    paid_until TEXT NOT NULL,           -- YYYY-MM-DD, shu kun ham kiradi
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS classes (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    UNIQUE (teacher_id, name)
);
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    class_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    full_name TEXT NOT NULL,
    parent_phone TEXT
);
CREATE TABLE IF NOT EXISTS lessons (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    class_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    subject TEXT NOT NULL,
    weekday INTEGER NOT NULL,           -- 0 = Dushanba ... 6 = Yakshanba
    start_time TEXT NOT NULL,           -- HH:MM
    room TEXT
);
CREATE TABLE IF NOT EXISTS homeworks (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id) ON DELETE CASCADE,
    class_id INTEGER NOT NULL REFERENCES classes(id) ON DELETE CASCADE,
    text TEXT NOT NULL,
    given_on TEXT NOT NULL,
    due_on TEXT NOT NULL,
    done INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS reminders_sent (
    lesson_id INTEGER NOT NULL,
    day TEXT NOT NULL,
    offset_min INTEGER NOT NULL,
    PRIMARY KEY (lesson_id, day, offset_min)
);
CREATE TABLE IF NOT EXISTS digests_sent (
    teacher_id INTEGER NOT NULL,
    kind TEXT NOT NULL,                 -- daily | weekly | monthly | hw_evening
    period_key TEXT NOT NULL,
    PRIMARY KEY (teacher_id, kind, period_key)
);
CREATE TABLE IF NOT EXISTS sms_log (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL,
    month TEXT NOT NULL,                -- YYYY-MM
    phone TEXT NOT NULL,
    text TEXT NOT NULL,
    sent_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY,
    teacher_id INTEGER NOT NULL REFERENCES teachers(id),
    plan TEXT NOT NULL,
    amount INTEGER NOT NULL,
    months INTEGER NOT NULL,
    status TEXT NOT NULL,               -- pending | paid
    created_at TEXT NOT NULL
);
"""

WEEKDAYS = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]


class DB:
    def __init__(self, path: str):
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row
        self.conn.execute("PRAGMA foreign_keys = ON")
        self.conn.executescript(SCHEMA)

    def _one(self, sql, args=()):
        return self.conn.execute(sql, args).fetchone()

    def _all(self, sql, args=()):
        return self.conn.execute(sql, args).fetchall()

    def _exec(self, sql, args=()):
        cur = self.conn.execute(sql, args)
        self.conn.commit()
        return cur

    # --- o'qituvchilar ---
    def get_teacher(self, telegram_id: int):
        return self._one("SELECT * FROM teachers WHERE telegram_id = ?", (telegram_id,))

    def create_teacher(self, telegram_id: int, full_name: str, plan: str, paid_until: date):
        self._exec(
            "INSERT INTO teachers (telegram_id, full_name, plan, paid_until, created_at) VALUES (?, ?, ?, ?, ?)",
            (telegram_id, full_name, plan, paid_until.isoformat(), datetime.now().isoformat(timespec="seconds")),
        )
        return self.get_teacher(telegram_id)

    def update_teacher(self, teacher_id: int, **fields):
        cols = ", ".join(f"{k} = ?" for k in fields)
        self._exec(f"UPDATE teachers SET {cols} WHERE id = ?", (*fields.values(), teacher_id))

    def set_school(self, teacher_id: int, school_name: str):
        self._exec("INSERT OR IGNORE INTO schools (name) VALUES (?)", (school_name,))
        school = self._one("SELECT id FROM schools WHERE name = ?", (school_name,))
        self.update_teacher(teacher_id, school_id=school["id"])

    def active_teachers(self, today: date):
        return self._all("SELECT * FROM teachers WHERE paid_until >= ?", (today.isoformat(),))

    def extend_subscription(self, teacher_id: int, plan: str, months: int, today: date) -> date:
        t = self._one("SELECT paid_until FROM teachers WHERE id = ?", (teacher_id,))
        start = max(today, date.fromisoformat(t["paid_until"]) + timedelta(days=1))
        until = start + timedelta(days=30 * months - 1)
        self.update_teacher(teacher_id, plan=plan, paid_until=until.isoformat())
        return until

    # --- sinflar va o'quvchilar ---
    def add_class(self, teacher_id: int, name: str):
        self._exec("INSERT OR IGNORE INTO classes (teacher_id, name) VALUES (?, ?)", (teacher_id, name))
        return self.get_class(teacher_id, name)

    def get_class(self, teacher_id: int, name: str):
        return self._one("SELECT * FROM classes WHERE teacher_id = ? AND name = ?", (teacher_id, name))

    def classes(self, teacher_id: int):
        return self._all(
            "SELECT c.*, (SELECT COUNT(*) FROM students s WHERE s.class_id = c.id) AS n_students "
            "FROM classes c WHERE teacher_id = ? ORDER BY name",
            (teacher_id,),
        )

    def add_student(self, class_id: int, full_name: str, parent_phone: str | None):
        self._exec(
            "INSERT INTO students (class_id, full_name, parent_phone) VALUES (?, ?, ?)",
            (class_id, full_name, parent_phone),
        )

    def students(self, class_id: int):
        return self._all("SELECT * FROM students WHERE class_id = ? ORDER BY full_name", (class_id,))

    # --- darslar ---
    def add_lesson(self, teacher_id, class_id, subject, weekday, start_time, room):
        cur = self._exec(
            "INSERT INTO lessons (teacher_id, class_id, subject, weekday, start_time, room) VALUES (?, ?, ?, ?, ?, ?)",
            (teacher_id, class_id, subject, weekday, start_time, room),
        )
        return cur.lastrowid

    def delete_lesson(self, teacher_id: int, lesson_id: int) -> bool:
        cur = self._exec("DELETE FROM lessons WHERE id = ? AND teacher_id = ?", (lesson_id, teacher_id))
        return cur.rowcount > 0

    def lessons(self, teacher_id: int, weekday: int | None = None):
        sql = (
            "SELECT l.*, c.name AS class_name FROM lessons l JOIN classes c ON c.id = l.class_id "
            "WHERE l.teacher_id = ?"
        )
        args = [teacher_id]
        if weekday is not None:
            sql += " AND l.weekday = ?"
            args.append(weekday)
        return self._all(sql + " ORDER BY l.weekday, l.start_time", args)

    # --- uyga vazifalar ---
    def add_homework(self, teacher_id, class_id, text, given_on: date, due_on: date):
        cur = self._exec(
            "INSERT INTO homeworks (teacher_id, class_id, text, given_on, due_on) VALUES (?, ?, ?, ?, ?)",
            (teacher_id, class_id, text, given_on.isoformat(), due_on.isoformat()),
        )
        return cur.lastrowid

    def homeworks(self, teacher_id: int, only_open=True):
        sql = (
            "SELECT h.*, c.name AS class_name FROM homeworks h JOIN classes c ON c.id = h.class_id "
            "WHERE h.teacher_id = ?"
        )
        if only_open:
            sql += " AND h.done = 0"
        return self._all(sql + " ORDER BY h.due_on", (teacher_id,))

    def homeworks_due(self, teacher_id: int, due_on: date):
        return self._all(
            "SELECT h.*, c.name AS class_name FROM homeworks h JOIN classes c ON c.id = h.class_id "
            "WHERE h.teacher_id = ? AND h.due_on = ? AND h.done = 0",
            (teacher_id, due_on.isoformat()),
        )

    def mark_homework_done(self, teacher_id: int, hw_id: int) -> bool:
        cur = self._exec("UPDATE homeworks SET done = 1 WHERE id = ? AND teacher_id = ?", (hw_id, teacher_id))
        return cur.rowcount > 0

    def purge_old_homeworks(self, teacher_id: int, older_than: date):
        self._exec("DELETE FROM homeworks WHERE teacher_id = ? AND due_on < ?", (teacher_id, older_than.isoformat()))

    # --- yuborilganlar jurnali (takror yubormaslik uchun) ---
    def mark_reminder(self, lesson_id: int, day: date, offset: int) -> bool:
        cur = self._exec(
            "INSERT OR IGNORE INTO reminders_sent (lesson_id, day, offset_min) VALUES (?, ?, ?)",
            (lesson_id, day.isoformat(), offset),
        )
        return cur.rowcount > 0

    def mark_digest(self, teacher_id: int, kind: str, period_key: str) -> bool:
        cur = self._exec(
            "INSERT OR IGNORE INTO digests_sent (teacher_id, kind, period_key) VALUES (?, ?, ?)",
            (teacher_id, kind, period_key),
        )
        return cur.rowcount > 0

    # --- SMS ---
    def sms_used(self, teacher_id: int, month: str) -> int:
        return self._one(
            "SELECT COUNT(*) AS n FROM sms_log WHERE teacher_id = ? AND month = ?", (teacher_id, month)
        )["n"]

    def log_sms(self, teacher_id: int, month: str, phone: str, text: str):
        self._exec(
            "INSERT INTO sms_log (teacher_id, month, phone, text, sent_at) VALUES (?, ?, ?, ?, ?)",
            (teacher_id, month, phone, text, datetime.now().isoformat(timespec="seconds")),
        )

    # --- to'lovlar ---
    def create_payment(self, teacher_id: int, plan: str, amount: int, months: int):
        cur = self._exec(
            "INSERT INTO payments (teacher_id, plan, amount, months, status, created_at) VALUES (?, ?, ?, ?, 'pending', ?)",
            (teacher_id, plan, amount, months, datetime.now().isoformat(timespec="seconds")),
        )
        return cur.lastrowid

    def get_payment(self, payment_id: int):
        return self._one("SELECT * FROM payments WHERE id = ?", (payment_id,))

    def mark_payment_paid(self, payment_id: int):
        self._exec("UPDATE payments SET status = 'paid' WHERE id = ?", (payment_id,))

    def teacher_by_id(self, teacher_id: int):
        return self._one("SELECT * FROM teachers WHERE id = ?", (teacher_id,))

    def stats(self):
        return {
            "teachers": self._one("SELECT COUNT(*) AS n FROM teachers")["n"],
            "active": self._one("SELECT COUNT(*) AS n FROM teachers WHERE paid_until >= date('now')")["n"],
            "paid_sum": self._one("SELECT COALESCE(SUM(amount), 0) AS s FROM payments WHERE status = 'paid'")["s"],
        }
