"""data.py dan Markdown rejalar va bitta HTML sahifa yasaydi.

    python build.py            # Markdown fayllarni yangilaydi
    python build.py page.html  # qo'shimcha ravishda HTML sahifa
"""
import html
import sys
from pathlib import Path

from data import GENERAL, LEVELS, PROJECTS

HERE = Path(__file__).parent


def md_list(items):
    return "\n".join(f"- {i}" for i in items)


def project_md(n, p):
    return f"""# {n:02d}. {p['title']}

**Daraja:** {LEVELS[p['level']]} · **Muddat:** {p['weeks']} hafta · **Jamoa:** {p['team']}

## Muammo
{p['problem']}

**Foydalanuvchilar:** {p['users']}

## Asosiy funksiyalar (MVP)
{md_list(p['features'])}

## Buyruqlar
{' '.join(f'`{c}`' for c in p['commands'])}

## Ma'lumotlar bazasi
{md_list(f'`{t.split(":")[0]}`:{t.split(":", 1)[1]}' for t in p['tables'])}

## Bosqichlar
{md_list(p['steps'])}

## Bonus vazifalar
{md_list(p['bonus'])}

## Nimani o'rganasiz
{md_list(p['skills'])}

## Daromad g'oyasi
{p['money']}

---
Baholash mezonlari va boshlash yo'riqnomasi: [README.md](README.md)
"""


def index_md():
    rows = "\n".join(
        f"| {n:02d} | [{p['title']}]({n:02d}-{p['slug']}.md) | {LEVELS[p['level']]} | {p['weeks']} hafta |"
        for n, p in enumerate(PROJECTS, 1)
    )
    rubric = "\n".join(f"| {name} | {pts} | {desc} |" for name, pts, desc in GENERAL["rubric"])
    return f"""# O'quvchilar uchun 15 ta loyiha rejasi

UstozBot kabi maktab hayotidagi real muammoni hal qiladigan Telegram botlar.
Har bir reja: muammo, funksiyalar, buyruqlar, ma'lumotlar bazasi, haftalik bosqichlar,
bonus vazifalar, o'rganiladigan ko'nikmalar va daromad g'oyasi.

| № | Loyiha | Daraja | Muddat |
|---|---|---|---|
{rows}

## Texnologiyalar
{md_list(GENERAL['stack'])}

## Qanday boshlash kerak
{md_list(GENERAL['start'])}

## Baholash (100 ball)
| Mezon | Ball | Nima tekshiriladi |
|---|---|---|
{rubric}

Fayllar `build.py` orqali `data.py` dan yasaladi — rejani o'zgartirish uchun `data.py` ni tahrirlang.
"""


def e(s):
    return html.escape(s, quote=True)


def li(items):
    return "".join(f"<li>{e(i)}</li>" for i in items)


def project_html(n, p):
    tables = "".join(
        f"<li><code>{e(t.split(':')[0])}</code><span>{e(t.split(':', 1)[1])}</span></li>" for t in p["tables"]
    )
    steps = "".join(
        f"<li><b>{e(s.split(':')[0])}</b>{e(s.split(':', 1)[1])}</li>" for s in p["steps"]
    )
    cmds = "".join(f"<code>{e(c)}</code>" for c in p["commands"])
    dots = "".join('<i class="on"></i>' if i < p["level"] else "<i></i>" for i in range(3))
    return f"""
<article class="proj" id="p{n:02d}" data-level="{p['level']}">
  <header class="proj-head">
    <span class="num">{n:02d}</span>
    <div class="ttl">
      <h2>{e(p['title'])}</h2>
      <p class="meta"><span class="lvl" aria-label="Daraja {p['level']} / 3">{dots}{LEVELS[p['level']]}</span><span>{p['weeks']} hafta</span><span>{e(p['team'])}</span></p>
    </div>
  </header>
  <p class="problem"><span class="lbl">Muammo</span>{e(p['problem'])}</p>
  <p class="users"><span class="lbl">Kimlar uchun</span>{e(p['users'])}</p>
  <div class="cols">
    <section><h3>MVP funksiyalari</h3><ul class="feat">{li(p['features'])}</ul></section>
    <section>
      <h3>Buyruqlar</h3><div class="cmds">{cmds}</div>
      <h3>Ma'lumotlar bazasi</h3><ul class="tables">{tables}</ul>
    </section>
  </div>
  <h3>Bosqichlar</h3>
  <ol class="steps">{steps}</ol>
  <div class="cols three">
    <section><h3>Bonus</h3><ul>{li(p['bonus'])}</ul></section>
    <section><h3>O'rganasiz</h3><ul>{li(p['skills'])}</ul></section>
    <section class="money"><h3>Daromad g'oyasi</h3><p>{e(p['money'])}</p></section>
  </div>
</article>"""


def page_html():
    toc = "".join(
        f'<a class="toc-item" href="#p{n:02d}" data-level="{p["level"]}"><span class="num">{n:02d}</span>'
        f'<span class="t">{e(p["title"])}</span><span class="s">{LEVELS[p["level"]]} · {p["weeks"]} hafta</span></a>'
        for n, p in enumerate(PROJECTS, 1)
    )
    projects = "".join(project_html(n, p) for n, p in enumerate(PROJECTS, 1))
    rubric = "".join(
        f"<tr><td>{e(name)}</td><td class='pts'>{pts}</td><td>{e(desc)}</td></tr>" for name, pts, desc in GENERAL["rubric"]
    )
    counts = {lv: sum(p["level"] == lv for p in PROJECTS) for lv in LEVELS}
    filters = "".join(
        f'<button type="button" id="f{lv}" data-f="{lv}">{name} <span>{counts[lv]}</span></button>'
        for lv, name in LEVELS.items()
    )
    return TEMPLATE.replace("{{TOC}}", toc).replace("{{PROJECTS}}", projects).replace(
        "{{RUBRIC}}", rubric).replace("{{FILTERS}}", filters).replace(
        "{{STACK}}", li(GENERAL["stack"])).replace("{{START}}", li(GENERAL["start"]))


TEMPLATE = """<title>Loyihalar daftari</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500..800&family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=JetBrains+Mono:wght@400;600&display=swap">
<style>
/* Layout: daftar varag'i — katakli fon, chap tomonda loyiha raqami, kontent bir ustunda 1100px gacha */
:root {
  --bg: #EEF1F6; --paper: #FFFFFF; --grid: #DCE3EE; --ink: #16203A; --muted: #56617A;
  --line: #D5DCE8; --accent: #2440C2; --accent-soft: #E3E8FB; --mark: #FFE173; --mark-ink: #3A2E00;
  --display: "Bricolage Grotesque", "Trebuchet MS", sans-serif;
  --body: "Atkinson Hyperlegible", Verdana, sans-serif;
  --mono: "JetBrains Mono", "Courier New", monospace;
}
@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {
  --bg: #0F1424; --paper: #171E33; --grid: #1C2440; --ink: #E7ECF7; --muted: #A2ACC4;
  --line: #2C3654; --accent: #8EA2FF; --accent-soft: #232D52; --mark: #E8C64A; --mark-ink: #2A2100; color-scheme: dark } }
:root[data-theme="dark"] {
  --bg: #0F1424; --paper: #171E33; --grid: #1C2440; --ink: #E7ECF7; --muted: #A2ACC4;
  --line: #2C3654; --accent: #8EA2FF; --accent-soft: #232D52; --mark: #E8C64A; --mark-ink: #2A2100; color-scheme: dark }
* { box-sizing: border-box }
body { background: var(--bg); color: var(--ink); font: 17px/1.6 var(--body);
  background-image: linear-gradient(var(--grid) 1px, transparent 1px), linear-gradient(90deg, var(--grid) 1px, transparent 1px);
  background-size: 28px 28px; }
.wrap { max-width: 1100px; margin: 0 auto; padding: 48px 20px 80px; display: flex; flex-direction: column; gap: 40px }
h1, h2, h3 { font-family: var(--display); text-wrap: balance; margin: 0 }
h1 { font-size: clamp(36px, 6vw, 64px); line-height: 1.02; font-weight: 800; letter-spacing: -0.02em }
h1 mark { background: linear-gradient(transparent 55%, var(--mark) 55%); color: inherit; padding: 0 4px }
.intro { display: flex; flex-direction: column; gap: 16px; max-width: 760px }
.intro p { margin: 0; color: var(--muted); font-size: 19px }
.eyebrow { font: 600 13px var(--mono); letter-spacing: 0.12em; text-transform: uppercase; color: var(--accent) }
.filters { display: flex; flex-wrap: wrap; gap: 8px }
.filters button { font: 700 15px var(--body); padding: 8px 14px; border-radius: 999px; border: 1.5px solid var(--line);
  background: var(--paper); color: var(--ink); cursor: pointer }
.filters button span { color: var(--muted); font-weight: 400; margin-left: 4px }
.filters button[aria-pressed="true"] { background: var(--ink); color: var(--paper); border-color: var(--ink) }
.filters button[aria-pressed="true"] span { color: inherit; opacity: .7 }
button:focus-visible, a:focus-visible { outline: 3px solid var(--accent); outline-offset: 2px }
.toc { display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 0; background: var(--paper);
  border: 1.5px solid var(--line); border-radius: 14px; overflow: hidden }
.toc-item { display: grid; grid-template-columns: 44px 1fr; column-gap: 12px; padding: 14px 18px; text-decoration: none; color: inherit;
  border-bottom: 1px solid var(--line); border-right: 1px solid var(--line) }
.toc-item:hover { background: var(--accent-soft) }
.toc-item .num { grid-row: span 2; font: 800 24px var(--display); color: var(--accent) }
.toc-item .t { font-weight: 700; line-height: 1.3 }
.toc-item .s { font-size: 14px; color: var(--muted) }
.proj { background: var(--paper); border: 1.5px solid var(--line); border-radius: 18px; padding: clamp(20px, 4vw, 40px);
  display: flex; flex-direction: column; gap: 18px; scroll-margin-top: 16px }
.proj-head { display: flex; gap: 18px; align-items: flex-start }
.proj-head .num { font: 800 clamp(44px, 7vw, 72px)/0.9 var(--display); color: var(--accent); letter-spacing: -0.04em }
.ttl { display: flex; flex-direction: column; gap: 8px; min-width: 0 }
.ttl h2 { font-size: clamp(24px, 3.4vw, 34px); line-height: 1.12 }
.meta { display: flex; flex-wrap: wrap; gap: 6px 16px; margin: 0; font-size: 15px; color: var(--muted) }
.lvl { display: inline-flex; align-items: center; gap: 4px; font-weight: 700; color: var(--ink) }
.lvl i { width: 10px; height: 10px; border-radius: 50%; border: 1.5px solid var(--accent) }
.lvl i.on { background: var(--accent) }
.lvl i:last-of-type { margin-right: 4px }
.lbl { display: block; font: 600 12px var(--mono); letter-spacing: 0.1em; text-transform: uppercase; color: var(--muted); margin-bottom: 2px }
.problem { margin: 0; font-size: 20px; max-width: 70ch; padding: 12px 16px; background: var(--accent-soft); border-radius: 10px }
.users { margin: 0 }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 28px }
.cols.three { grid-template-columns: repeat(3, 1fr); gap: 24px; padding-top: 18px; border-top: 1.5px dashed var(--line) }
.cols > section { min-width: 0; display: flex; flex-direction: column; gap: 8px }
h3 { font-size: 18px; font-weight: 700 }
.cols > section h3 + * { margin-bottom: 10px }
ul, ol { margin: 0; padding-left: 20px; display: flex; flex-direction: column; gap: 6px }
.feat li::marker { color: var(--accent) }
.cmds { display: flex; flex-wrap: wrap; gap: 6px }
code { font: 500 14px var(--mono); background: var(--accent-soft); color: var(--ink); padding: 2px 7px; border-radius: 6px; overflow-wrap: anywhere }
.tables { list-style: none; padding: 0 }
.tables li { display: flex; flex-direction: column; gap: 2px; font-size: 15px; color: var(--muted) }
.tables li code { align-self: flex-start; font-weight: 600 }
.steps { list-style: none; padding: 0; display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px }
.steps li { border: 1.5px solid var(--line); border-radius: 10px; padding: 12px 14px; display: flex; flex-direction: column; gap: 4px; font-size: 15px }
.steps b { font-family: var(--mono); font-size: 13px; color: var(--accent); text-transform: uppercase; letter-spacing: .06em }
.money p { margin: 0; background: var(--mark); color: var(--mark-ink); padding: 10px 12px; border-radius: 8px; font-size: 15px }
.general { display: grid; grid-template-columns: 1fr 1fr; gap: 28px; background: var(--paper); border: 1.5px solid var(--line);
  border-radius: 18px; padding: clamp(20px, 4vw, 40px) }
.general > section { min-width: 0; display: flex; flex-direction: column; gap: 10px }
.general .wide { grid-column: 1 / -1 }
.tbl { overflow-x: auto }
table { border-collapse: collapse; width: 100%; font-size: 15px }
th, td { text-align: left; padding: 10px 12px; border-bottom: 1px solid var(--line); vertical-align: top }
th { font: 600 12px var(--mono); letter-spacing: .1em; text-transform: uppercase; color: var(--muted) }
td.pts { font: 700 18px var(--display); color: var(--accent); font-variant-numeric: tabular-nums }
.empty { color: var(--muted) }
@media (max-width: 760px) {
  .cols, .cols.three, .general { grid-template-columns: 1fr }
  .proj-head { flex-direction: column; gap: 6px }
  .toc { grid-template-columns: 1fr }
}
@media (prefers-reduced-motion: no-preference) { html { scroll-behavior: smooth } }
</style>
<div class="wrap">
  <header class="intro">
    <span class="eyebrow">Maktab · Telegram botlar · 15 reja</span>
    <h1>O'quvchilar uchun <mark>loyihalar daftari</mark></h1>
    <p>UstozBot kabi maktabdagi haqiqiy muammoni hal qiladigan 15 ta loyiha. Har bir rejada funksiyalar, buyruqlar, ma'lumotlar bazasi, haftalik bosqichlar va daromad g'oyasi bor. Rejani tanlang, jamoa tuzing va haftama-hafta quring.</p>
  </header>
  <nav class="filters" aria-label="Daraja bo'yicha saralash">
    <button type="button" id="f0" data-f="0" aria-pressed="true">Hammasi <span>15</span></button>{{FILTERS}}
  </nav>
  <nav class="toc" aria-label="Loyihalar ro'yxati">{{TOC}}</nav>
  {{PROJECTS}}
  <section class="general" id="qoidalar">
    <section><h2>Texnologiyalar</h2><ul>{{STACK}}</ul></section>
    <section><h2>Qanday boshlash kerak</h2><ol>{{START}}</ol></section>
    <section class="wide"><h2>Baholash — 100 ball</h2>
      <div class="tbl"><table><thead><tr><th>Mezon</th><th>Ball</th><th>Nima tekshiriladi</th></tr></thead><tbody>{{RUBRIC}}</tbody></table></div>
    </section>
  </section>
</div>
<script>
(function () {
  var buttons = document.querySelectorAll('.filters button');
  function apply(f) {
    buttons.forEach(function (b) { b.setAttribute('aria-pressed', String(b.dataset.f === f)); });
    document.querySelectorAll('[data-level]').forEach(function (el) {
      if (el.matches('button')) return;
      el.hidden = f !== '0' && el.dataset.level !== f;
    });
    try { localStorage.setItem('loyiha-filter', f); } catch (e) {}
  }
  buttons.forEach(function (b) { b.addEventListener('click', function () { apply(b.dataset.f); }); });
  var saved = '0';
  try { saved = localStorage.getItem('loyiha-filter') || '0'; } catch (e) {}
  apply(saved);
})();
</script>
"""


def main():
    for old in HERE.glob("[0-9][0-9]-*.md"):
        old.unlink()
    for n, p in enumerate(PROJECTS, 1):
        (HERE / f"{n:02d}-{p['slug']}.md").write_text(project_md(n, p), encoding="utf-8")
    (HERE / "README.md").write_text(index_md(), encoding="utf-8")
    if len(sys.argv) > 1:
        Path(sys.argv[1]).write_text(page_html(), encoding="utf-8")


if __name__ == "__main__":
    main()
