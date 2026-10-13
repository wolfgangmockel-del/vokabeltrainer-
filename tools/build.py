"""Builds the three vocab trainers from src/ and the CSV lists.

Run from the repository root:  python3 tools/build.py
Outputs: ./ (Englisch), ./kroatisch/, ./spanisch/
"""
import csv
import json
import os

from PIL import Image, ImageDraw, ImageFont

APPS = [
    dict(code="en", out=".", csv="vokabeln.csv", name="Englisch", tts="en-GB",
         title="Grundwortschatz 2000", short="Englisch", key="gws2000.v1", cache="gws2000",
         label="EN·DE", light="#1f4fb5", dark="#7aa2ff", dark_ink="#0b1430"),
    dict(code="hr", out="kroatisch", csv="vokabeln-hr.csv", name="Kroatisch", tts="hr-HR",
         title="Kroatisch A2", short="Kroatisch", key="vokabeln.hr.v1", cache="kroatisch",
         label="HR·DE", light="#b3262e", dark="#ff8f8f", dark_ink="#2b0b0d"),
    dict(code="es", out="spanisch", csv="vokabeln-es.csv", name="Spanisch", tts="es-ES",
         title="Spanisch A2", short="Spanisch", key="vokabeln.es.v1", cache="spanisch",
         label="ES·DE", light="#a34a06", dark="#f6ad55", dark_ink="#2b1600"),
]
VERSION = "3"


def load_words(path):
    rows = list(csv.reader(open(path, encoding="utf-8"), delimiter=";"))[1:]
    groups, words = [], []
    for r in rows:
        if len(r) >= 5:  # Kroatisch/Spanisch: Wort;Deutsch;Teil;Nr;Kapitel
            g = r[4]
            if g not in groups:
                groups.append(g)
            words.append([r[0], r[1], groups.index(g)])
        else:  # Englisch: Englisch;Deutsch;Seite
            words.append([r[0], r[1]])
    return words, groups


def icon(path, n, label, color):
    im = Image.new("RGB", (n, n), color)
    d = ImageDraw.Draw(im)
    m = n * 0.2
    d.rounded_rectangle([m, m * 1.15, n - m, n - m * 1.15], radius=n * 0.04, fill="#ffffff")
    d.line([m, n * 0.42, n - m, n * 0.42], fill="#e8a3a3", width=max(2, n // 60))
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf", int(n * 0.2))
    except OSError:
        f = ImageFont.load_default()
    d.text((n / 2, n * 0.6), label, fill="#1b2433", font=f, anchor="mm")
    im.save(path)


def main():
    app = open("src/app.html", encoding="utf-8").read()
    sw = open("src/sw.js", encoding="utf-8").read()
    for a in APPS:
        os.makedirs(a["out"], exist_ok=True)
        words, groups = load_words(a["csv"])
        data = {a["code"]: dict(name=a["name"], title=a["title"], tts=a["tts"], rec=a["tts"],
                                words=words, groups=groups)}
        with open(os.path.join(a["out"], "vocab.js"), "w", encoding="utf-8") as f:
            f.write("window.VOCAB=" + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n")
        accent = ("" if a["code"] == "en" else
                  f':root{{--accent:{a["light"]}}}'
                  f'@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--accent:{a["dark"]};--accent-ink:{a["dark_ink"]}}}}}'
                  f':root[data-theme="dark"]{{--accent:{a["dark"]};--accent-ink:{a["dark_ink"]}}}\n')
        html = (app.replace("{{TITLE}}", a["title"]).replace("{{THEME}}", a["light"])
                .replace("{{STORAGE_KEY}}", a["key"]).replace("{{ACCENT_CSS}}", accent))
        open(os.path.join(a["out"], "index.html"), "w", encoding="utf-8").write(html)
        open(os.path.join(a["out"], "sw.js"), "w", encoding="utf-8").write(
            sw.replace("{{CACHE}}", f'{a["cache"]}-v{VERSION}'))
        manifest = dict(name=a["title"], short_name=a["short"], start_url="./", scope="./",
                        display="standalone", background_color="#eef0f3", theme_color=a["light"], lang="de",
                        icons=[dict(src=f"icon-{n}.png", sizes=f"{n}x{n}", type="image/png", purpose="any maskable")
                               for n in (192, 512)])
        with open(os.path.join(a["out"], "manifest.webmanifest"), "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        for n in (192, 512):
            icon(os.path.join(a["out"], f"icon-{n}.png"), n, a["label"], a["light"])
        print(a["out"], len(words), "Einträge")


if __name__ == "__main__":
    main()
