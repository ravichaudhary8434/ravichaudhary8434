"""Render the animated neofetch-style info card for the profile README.

Writes assets/card-dark.svg and assets/card-light.svg. GitHub shows SVGs
through <img>, which keeps their CSS keyframe animations but strips scripts,
so everything here is plain SVG + CSS. Colours match ravichaudhary.dev.

Run:  python3 scripts/render_card.py
"""

from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"

PALETTES = {
    "dark": {
        "bg": "#09090b", "surface": "#151518", "line": "#27272a",
        "text": "#f4f3f0", "dim": "#b6b3ad", "mute": "#8d8a84",
        "accent": "#ff7a45", "accent2": "#f0508c", "accent3": "#8b5cf6",
    },
    "light": {
        "bg": "#f6f4ef", "surface": "#eeebe4", "line": "#dedad1",
        "text": "#181715", "dim": "#56524b", "mute": "#69645c",
        "accent": "#c2410c", "accent2": "#db2777", "accent3": "#6d28d9",
    },
}

NAME = "Ravi Chaudhary"
TAGLINE = "Fullstack Software Engineer · Noida, India"

# Backend and AI lead; frontend stays visible but lower down.
ROWS = [
    ("backend", "Go · Python (FastAPI) · Node.js"),
    ("ai", "OpenAI API · Claude Code · MCP"),
    ("infra", "AWS · Docker · Kubernetes · Redis"),
    ("data", "PostgreSQL · MySQL · OpenSearch"),
    ("frontend", "React · Redux · TypeScript"),
    ("recently", "TestMu AI (formerly LambdaTest)"),
    ("before", "LCX, crypto exchange"),
    ("shipped", "AI accessibility engine · trading UI"),
    ("off-clock", "mountains · Asphalt 9 · pop music"),
]

W = 520
PAD = 28
LINE = 25
FONT = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'Liberation Mono', monospace"


def card(p: dict) -> str:
    y0 = 78  # first content baseline, below the title bar
    rows_top = y0 + 3 * LINE + 16
    swatch_y = rows_top + len(ROWS) * LINE + 14
    prompt_y = swatch_y + 44
    h = prompt_y + 26

    lines = []
    step = 0.12

    def line(content: str, y: float) -> None:
        nonlocal step
        lines.append(f'<g class="l" style="animation-delay:{step:.2f}s">{content.format(y=y)}</g>')
        step += 0.12

    line(f'<text x="{PAD}" y="{{y}}" fill="{p["accent"]}">$ <tspan fill="{p["text"]}">neofetch</tspan></text>', y0)
    line(f'<text x="{PAD}" y="{{y}}" fill="{p["text"]}" font-weight="700">{NAME}</text>', y0 + LINE + 4)
    line(f'<text x="{PAD}" y="{{y}}" fill="{p["dim"]}">{escape(TAGLINE)}</text>', y0 + 2 * LINE + 4)
    lines.append(
        f'<line class="l" style="animation-delay:{step:.2f}s" x1="{PAD}" x2="{W - PAD}" '
        f'y1="{y0 + 2 * LINE + 20}" y2="{y0 + 2 * LINE + 20}" stroke="{p["line"]}" />'
    )
    step += 0.12

    for i, (k, v) in enumerate(ROWS):
        y = rows_top + i * LINE
        line(
            f'<text x="{PAD}" y="{{y}}"><tspan fill="{p["accent"]}">{k}</tspan>'
            f'<tspan x="{PAD + 112}" fill="{p["text"]}">{escape(v)}</tspan></text>',
            y,
        )

    swatches = "".join(
        f'<rect x="{PAD + i * 30}" y="{swatch_y}" width="22" height="12" rx="3" fill="{c}" />'
        for i, c in enumerate([p["accent"], p["accent2"], p["accent3"], p["dim"], p["mute"], p["line"]])
    )
    lines.append(f'<g class="l" style="animation-delay:{step:.2f}s">{swatches}</g>')
    step += 0.12
    lines.append(
        f'<g class="l" style="animation-delay:{step:.2f}s"><text x="{PAD}" y="{prompt_y}" fill="{p["accent"]}">$ '
        f'<tspan fill="{p["dim"]}">open ravichaudhary.dev</tspan>'
        # The cursor is a character, not a positioned box, so it always sits
        # right after the text whatever monospace font the viewer has.
        f'<tspan class="cursor" fill="{p["accent"]}"> ▋</tspan></text></g>'
    )

    dots = "".join(
        f'<circle cx="{PAD + i * 18}" cy="26" r="5.5" fill="{c}" />'
        for i, c in enumerate([p["accent"], p["accent2"], p["accent3"]])
    )

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="{NAME}: fullstack software engineer. Backend Go, Python, Node.js; AI with OpenAI API and Claude Code; most recently at TestMu AI (formerly LambdaTest).">
<style>
  text {{ font-family: {FONT}; font-size: 14px; }}
  .l {{ opacity: 0; animation: in .45s ease-out forwards; }}
  @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
  .cursor {{ animation: blink 1s steps(1) infinite; }}
  @keyframes blink {{ 50% {{ opacity: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{ .l {{ animation: none; opacity: 1; }} .cursor {{ animation: none; }} }}
</style>
<rect x="0.5" y="0.5" width="{W - 1}" height="{h - 1}" rx="14" fill="{p["bg"]}" stroke="{p["line"]}" />
<path d="M0.5 14.5a14 14 0 0 1 14-14h{W - 29}a14 14 0 0 1 14 14v37h-{W - 1}z" fill="{p["surface"]}" />
{dots}
<text x="{W / 2}" y="31" text-anchor="middle" fill="{p["mute"]}" font-size="12">ravi@ravichaudhary.dev: ~</text>
{"".join(lines)}
</svg>
'''


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for mode, p in PALETTES.items():
        (OUT / f"card-{mode}.svg").write_text(card(p), encoding="utf-8")
        print("wrote", OUT / f"card-{mode}.svg")


if __name__ == "__main__":
    main()
