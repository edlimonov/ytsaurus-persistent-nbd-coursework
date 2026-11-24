#!/usr/bin/env python3
"""Render the coursework architecture diagrams as dependency-free SVG files."""

from html import escape
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FONT = "Arial, DejaVu Sans, sans-serif"


def text(x, y, value, size=15, color="#e8eef8", anchor="middle", weight="normal"):
    return (
        f'<text x="{x}" y="{y}" fill="{color}" font-family="{FONT}" '
        f'font-size="{size}" text-anchor="{anchor}" font-weight="{weight}">'
        f"{escape(value)}</text>"
    )


def svg_open(width, height, title):
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
        f'viewBox="0 0 {width} {height}" role="img" aria-label="{escape(title)}">',
        '<defs><marker id="arrow" markerWidth="9" markerHeight="8" refX="8" refY="4" '
        'orient="auto"><path d="M 0 0 L 9 4 L 0 8 z" fill="#71c4d8"/></marker></defs>',
        f'<rect width="{width}" height="{height}" fill="#111c2c"/>',
        text(32, 39, title, 23, "#ffffff", "start", "bold"),
        text(width - 28, 38, "24.11.2026 · NFR-001/002/003/004/007/008", 12, "#a9bdd1", "end"),
    ]


def box(x, y, w, h, lines, tone="blue"):
    fill = {"blue": "#203d5b", "teal": "#164d56", "gold": "#5c4927"}[tone]
    out = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" '
        f'fill="{fill}" stroke="#7ea8c1" stroke-width="1.4"/>'
    ]
    total = len(lines)
    for i, line in enumerate(lines):
        out.append(text(x + w / 2, y + h / 2 + (i - (total - 1) / 2) * 19 + 5, line, 14))
    return out


def arrow(x1, y1, x2, y2, label="", dashed=False):
    dash = ' stroke-dasharray="6 4"' if dashed else ""
    out = [
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="#71c4d8" '
        f'stroke-width="2" marker-end="url(#arrow)"{dash}/>'
    ]
    if label:
        out.append(text((x1 + x2) / 2, (y1 + y2) / 2 - 9, label, 11, "#b6d1e2"))
    return out


def write(name, width, height, body):
    target = ROOT / f"{name}.svg"
    target.write_text("\n".join(svg_open(width, height, name.replace("-", " ")) + body + ["</svg>"]) + "\n", encoding="utf-8")


def render_context():
    out = []
    out += box(30, 145, 170, 76, ["Разработчик", "джобы"], "gold")
    out += box(260, 145, 185, 76, ["Controller agent", "spec, ACL, schema"])
    out += box(510, 145, 150, 76, ["Exec node", "volume manager"])
    out += box(730, 75, 175, 76, ["NBD server", "block device"], "teal")
    out += box(970, 75, 185, 76, ["Динамическая", "таблица"], "teal")
    out += box(730, 225, 175, 76, ["Job proxy", "bind mount"])
    out += box(970, 225, 185, 76, ["Контейнер", "джобы"], "gold")
    out += arrow(200, 183, 260, 183, "YT API")
    out += arrow(445, 183, 510, 183, "job spec")
    out += arrow(660, 160, 730, 113)
    out += arrow(905, 113, 970, 113, "blocks")
    out += arrow(660, 200, 730, 263)
    out += arrow(905, 263, 970, 263)
    out.append(text(580, 343, "YTsaurus: controller agent, exec node, NBD, job proxy; Linux/Porto/NBD — внешняя среда", 13, "#a9bdd1"))
    write("D-01-context", 1190, 380, out)


def render_components():
    labels = [
        ["YSON-спека"], ["Валидация", "ACL / schema"], ["Job proto"],
        ["Workspace", "builder"], ["Volume", "manager"], ["NBD block", "device"],
        ["Dynamic", "table"], ["Porto volume"], ["Job proxy", "bind"],
        ["User job", "/slot/sandbox"],
    ]
    cols = [(35, 130), (205, 145), (390, 120), (550, 145), (735, 145)]
    out = []
    for i in range(5):
        x, w = cols[i]
        out += box(x, 91, w, 70, labels[i], "teal" if i == 4 else "blue")
        if i:
            px, pw = cols[i - 1]
            out += arrow(px + pw, 126, x, 126)
    for i in range(5):
        x, w = cols[i]
        out += box(x, 240, w, 70, labels[i + 5], "teal" if i in (0, 1) else "blue")
        if i:
            px, pw = cols[i - 1]
            out += arrow(px + pw, 275, x, 275)
    out += arrow(807, 161, 108, 240, "создать экспорт")
    out.append(text(455, 360, "NFR-002/003: проверка до запуска · NFR-001/004: блоки и flush · NFR-008: диагностика", 13, "#a9bdd1"))
    write("D-02-components", 925, 395, out)


def render_deployment():
    out = []
    out += box(35, 125, 165, 70, ["API / CLI", "клиент"], "gold")
    out += box(245, 125, 205, 70, ["Controller agent", "container"])
    out += box(505, 125, 190, 70, ["Exec node", "container"])
    out += box(745, 65, 175, 70, ["NBD server", "/dev/nbdX"], "teal")
    out += box(745, 210, 175, 70, ["Porto job", "container"])
    out += box(970, 65, 180, 70, ["YT dynamic", "table"], "teal")
    out += arrow(200, 160, 245, 160)
    out += arrow(450, 160, 505, 160)
    out += arrow(695, 145, 745, 100)
    out += arrow(695, 175, 745, 245)
    out += arrow(920, 100, 970, 100, "rows")
    out.append(text(590, 333, "Linux host: Porto, NBD kernel/client · секреты вне образа · версия образа = CI SHA/digest", 13, "#a9bdd1"))
    write("D-03-deployment", 1185, 370, out)


def render_sequence(name, participants, events):
    width = max(1050, len(participants) * 170 + 80)
    left = 80
    step = (width - 160) / (len(participants) - 1)
    x = {p: left + i * step for i, p in enumerate(participants)}
    height = 155 + len(events) * 43
    out = []
    for p in participants:
        out += box(x[p] - 73, 72, 146, 48, [p], "teal" if p in ("Dynamic table", "NBD device") else "blue")
        out.append(f'<line x1="{x[p]}" y1="122" x2="{x[p]}" y2="{height - 35}" stroke="#536f86" stroke-dasharray="5 5"/>')
    for i, (src, dst, label) in enumerate(events):
        y = 155 + i * 43
        out += arrow(x[src], y, x[dst], y)
        out.append(text((x[src] + x[dst]) / 2, y - 9, label, 11, "#dfedf9"))
    write(name, width, height, out)


def main():
    render_context()
    render_components()
    render_deployment()
    render_sequence(
        "D-04-success",
        ["User", "Controller", "Exec node", "NBD device", "Dynamic table", "Job proxy", "Job"],
        [
            ("User", "Controller", "start operation"),
            ("Controller", "Dynamic table", "ACL + schema"),
            ("Controller", "Exec node", "job spec"),
            ("Exec node", "NBD device", "device ID"),
            ("NBD device", "Dynamic table", "size / block_size"),
            ("Exec node", "Job proxy", "Porto volume"),
            ("Job proxy", "Job", "bind mount"),
            ("Job", "NBD device", "write + sync"),
            ("NBD device", "Dynamic table", "flush blocks"),
            ("User", "Controller", "restart, same ID"),
            ("Job", "NBD device", "read old file"),
        ],
    )
    render_sequence(
        "D-05-failure",
        ["User", "Controller", "Dynamic table", "Exec node"],
        [
            ("User", "Controller", "start operation"),
            ("Controller", "Dynamic table", "ACL + schema"),
            ("Dynamic table", "Controller", "denied / invalid"),
            ("Controller", "User", "error, no payload"),
        ],
    )


if __name__ == "__main__":
    main()
