#!/usr/bin/env python3
"""Render an HTML deck to PDF after all animations and images have settled.

The decks in this folder use a `<deck-stage>` web component where slides are
gated on the `[data-deck-active]` attribute and rely on opacity:0 → opacity:1
animations to reveal content. A naive `chrome --print-to-pdf` produces blank
or partial slides because:

  1. Only the currently-active slide has [data-deck-active], so animations on
     other slides never fire and their content stays at opacity:0.
  2. Section-scoped @keyframes (e.g. the Courtroom .ct-* effects) are gated
     on the same attribute and never trigger during print.

This script fixes both problems by:

  - Tagging every slide with `data-deck-active` before printing.
  - Injecting CSS that collapses every animation to 0.001ms with
    animation-fill-mode: forwards, so the "to" keyframe is the rendered state.
  - Forcing known opacity:0-by-default helper classes (anim-*, ct-*, leaf)
    to opacity:1 in case their animation rule never matched.

Usage:
  python3 deck_to_pdf.py path/to/deck.html [path/to/out.pdf]

If the output path is omitted, writes alongside the input with a .pdf suffix.

Requires:
  - playwright Python package: pip install playwright
  - Google Chrome installed at /Applications/Google Chrome.app
    (playwright's bundled chromium is not required)
"""
import argparse
import asyncio
import sys
from pathlib import Path

from playwright.async_api import async_playwright

CHROME_PATH = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

DESIGN_W = 1920
DESIGN_H = 1080

FINAL_STATE_CSS = """
*, *::before, *::after {
  animation-duration: 0.001ms !important;
  animation-delay: 0s !important;
  animation-iteration-count: 1 !important;
  animation-fill-mode: forwards !important;
  transition: none !important;
}
.anim-fade-up, .anim-fade-in, .anim-scale-in, .anim-slide-right {
  opacity: 1 !important;
  transform: none !important;
}
.ct-bg, .ct-beam, .ct-flash, .ct-exhibit, .ct-screen-on { opacity: 1 !important; }
.ct-exhibit { transform: none !important; }
.leaf { opacity: 1 !important; }
"""

SHADOW_CSS = """
::slotted(*) {
  opacity: 1 !important;
  visibility: visible !important;
  pointer-events: auto !important;
}
"""


async def render(src: Path, out: Path, width: int, height: int) -> None:
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            executable_path=CHROME_PATH,
        )
        ctx = await browser.new_context(
            viewport={"width": width, "height": height},
            device_scale_factor=2,
        )
        page = await ctx.new_page()

        await page.goto(src.as_uri(), wait_until="networkidle", timeout=90_000)

        await page.add_style_tag(content=FINAL_STATE_CSS)

        await page.evaluate(
            """({docCss, shadowCss}) => {
              for (const el of document.querySelectorAll('deck-stage')) {
                if (el.shadowRoot) {
                  const s = document.createElement('style');
                  s.textContent = docCss + '\\n' + shadowCss;
                  el.shadowRoot.appendChild(s);
                }
                for (const slide of el.children) {
                  slide.setAttribute('data-deck-active', '');
                  slide.classList.add('is-active');
                }
              }
            }""",
            {"docCss": FINAL_STATE_CSS, "shadowCss": SHADOW_CSS},
        )

        await page.evaluate("document.fonts && document.fonts.ready")
        await page.evaluate(
            """async () => {
              const imgs = Array.from(document.images);
              await Promise.all(imgs.map(img =>
                img.complete ? Promise.resolve()
                  : new Promise(res => { img.onload = img.onerror = res; })
              ));
            }"""
        )

        await page.wait_for_timeout(1500)

        await page.emulate_media(media="print")

        await page.pdf(
            path=str(out),
            width=f"{width}px",
            height=f"{height}px",
            margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
            print_background=True,
            prefer_css_page_size=True,
        )

        await browser.close()


def main() -> int:
    ap = argparse.ArgumentParser(description=(__doc__ or "").splitlines()[0])
    ap.add_argument("input", help="Path to HTML deck")
    ap.add_argument("output", nargs="?", help="Output PDF path (default: input with .pdf)")
    ap.add_argument("--width", type=int, default=DESIGN_W, help=f"Page width px (default {DESIGN_W})")
    ap.add_argument("--height", type=int, default=DESIGN_H, help=f"Page height px (default {DESIGN_H})")
    args = ap.parse_args()

    src = Path(args.input).expanduser().resolve()
    if not src.is_file():
        print(f"error: input not found: {src}", file=sys.stderr)
        return 2

    out = Path(args.output).expanduser().resolve() if args.output else src.with_suffix(".pdf")

    asyncio.run(render(src, out, args.width, args.height))
    print(f"wrote {out} ({out.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
