"""Render the "Selected work" tiles for the profile README.

One SVG per case study and theme: assets/work-<slug>-<mode>.svg. Static on
purpose (no animation), so they read the same in every viewer. Text and
numbers mirror the case studies on ravichaudhary.dev.

Run:  python3 scripts/render_tiles.py
"""

from pathlib import Path
from textwrap import wrap
from xml.sax.saxutils import escape

from render_card import PALETTES, OUT

SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

# Backend first, matching the order recruiters should read them in.
TILES = [
    {
        "slug": "ai-accessibility-engine",
        "kicker": "AI · BACKEND · TESTMU AI",
        "title": "AI Accessibility Engine",
        "text": "GPT judges the WCAG rules static scanners can't, and suggests a fix for each issue.",
        "metric": "5",
        "label": "WCAG rules judged",
        "stack": "Python · FastAPI · Go · OpenAI API",
    },
    {
        "slug": "real-device-offline-mode",
        "kicker": "REAL-TIME · INFRA · TESTMU AI",
        "title": "Offline Mode, Real Devices",
        "text": "Switch off the network on real iPhones and Android phones in the middle of a session.",
        "metric": "E2E",
        "label": "stream, relay, UI, API",
        "stack": "WebRTC · Nginx/Lua · Redis · Node.js",
    },
    {
        "slug": "crypto-trading-interface",
        "kicker": "FINTECH · REAL-TIME · LCX",
        "title": "Crypto Trading Interface",
        "text": "The exchange's trading screen, built from scratch, with WebSocket push. 50K+ traders at peak.",
        "metric": "−50%",
        "label": "trade execution time",
        "stack": "React · Redux · WebSockets · TradingView",
    },
    {
        "slug": "accessibility-devtools",
        "kicker": "PRODUCT · BROWSER · TESTMU AI",
        "title": "Accessibility DevTools",
        "text": "A Chrome DevTools panel that finds accessibility issues and highlights them on the page.",
        "metric": "3K+",
        "label": "users · 4.9★ rating",
        "stack": "Chrome MV3 · React · TypeScript",
    },
]

W, H, PAD = 440, 200, 22


def tile(t: dict, p: dict) -> str:
    body = "".join(
        f'<text x="{PAD}" y="{106 + i * 20}" fill="{p["dim"]}" font-family="{SANS}" font-size="14">{escape(l)}</text>'
        for i, l in enumerate(wrap(t["text"], 54)[:2])
    )
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(t["title"])}: {escape(t["text"])}">
<defs><linearGradient id="g" x1="0" x2="1"><stop offset="0" stop-color="{p["accent"]}"/><stop offset=".5" stop-color="{p["accent2"]}"/><stop offset="1" stop-color="{p["accent3"]}"/></linearGradient></defs>
<rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="14" fill="{p["bg"]}" stroke="{p["line"]}"/>
<rect x="{PAD}" y="0.5" width="64" height="3" rx="1.5" fill="url(#g)"/>
<text x="{PAD}" y="34" fill="{p["accent"]}" font-family="{MONO}" font-size="11" letter-spacing=".6">{escape(t["kicker"])}</text>
<text x="{PAD}" y="64" fill="{p["text"]}" font-family="{SANS}" font-size="20" font-weight="600">{escape(t["title"])}</text>
<text x="{W - PAD}" y="64" text-anchor="end" fill="url(#g)" font-family="{SANS}" font-size="26" font-weight="700">{escape(t["metric"])}</text>
{body}
<line x1="{PAD}" x2="{W - PAD}" y1="{H - 52}" y2="{H - 52}" stroke="{p["line"]}"/>
<text x="{PAD}" y="{H - 26}" fill="{p["mute"]}" font-family="{MONO}" font-size="11">{escape(t["stack"])}</text>
<text x="{W - PAD}" y="84" text-anchor="end" fill="{p["mute"]}" font-family="{SANS}" font-size="11">{escape(t["label"])}</text>
</svg>
'''


def main() -> None:
    OUT.mkdir(exist_ok=True)
    for t in TILES:
        for mode, p in PALETTES.items():
            path = OUT / f"work-{t['slug']}-{mode}.svg"
            path.write_text(tile(t, p), encoding="utf-8")
            print("wrote", path.name)


if __name__ == "__main__":
    main()
