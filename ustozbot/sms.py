"""Eskiz.uz orqali SMS yuborish. Login ma'lumoti berilmagan bo'lsa SMS faqat logga yoziladi."""
import json
import logging
import urllib.request

import config

log = logging.getLogger(__name__)
_token: str | None = None


def _post(url: str, data: dict, token: str | None = None) -> dict:
    req = urllib.request.Request(url, data=json.dumps(data).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.loads(resp.read())


def send_sms(phone: str, text: str) -> bool:
    """Sinxron chaqiruv; botdan asyncio.to_thread orqali chaqiriladi."""
    global _token
    if not (config.ESKIZ_EMAIL and config.ESKIZ_PASSWORD):
        log.info("SMS (sinov rejimi) %s: %s", phone, text)
        return True
    try:
        if _token is None:
            auth = _post(
                "https://notify.eskiz.uz/api/auth/login",
                {"email": config.ESKIZ_EMAIL, "password": config.ESKIZ_PASSWORD},
            )
            _token = auth["data"]["token"]
        _post(
            "https://notify.eskiz.uz/api/message/sms/send",
            {"mobile_phone": phone.lstrip("+"), "message": text, "from": config.ESKIZ_FROM},
            _token,
        )
        return True
    except Exception:
        log.exception("SMS yuborilmadi: %s", phone)
        _token = None  # keyingi safar qayta login
        return False
