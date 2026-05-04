# AvS Deck — Reviewer Feedback Plan

Plan to address reviewer feedback on `AvS.html` (Apple vs. Samsung presentation).
Status: documented — awaiting reviewer's decision on Option A vs B for forward P/E before implementation.

## Context

- **Deck file:** `/Users/hossein/Downloads/MBA-GBS/ECEB/Gh_ECEB/AvS.html`
- **Original case:** `/Users/hossein/Downloads/MBA-GBS/ECEB/Apple vs Samsung.pdf` (Ivey 9B13A009, 20 pages)
- **Current structure:** 11 main slides + 2 appendix slides
  - A1: Samsung Financials 2006–2011 in **KRW billions** (replicates case Exhibit 9 verbatim)
  - A2: 2016 & 2018 Aftermath
- **Reviewer's three asks:**
  1. Financial figures for Apple AND Samsung at company level AND phone segment, **USD only — no KRW**
  2. Normalized share price chart, both firms, since financial crisis, with lawsuit dates marked
  3. 12M forward P/E ratio chart, both firms, same period

## What the case PDF covers (audited 2026-05-03)

| Reviewer ask | In case? |
|---|---|
| Apple financials (any level) | **No** |
| Samsung company financials | Yes — Exhibit 9, KRW only, 2006–2011, K-GAAP/K-IFRS break at 2009 |
| Phone-segment financials (either firm) | **No** — only narrative crumbs (Q2 2012 mobile = ~60% of Samsung profit; $6B Apple→Samsung in 2010 = 4% of Samsung revenue) |
| Share prices | **No** |
| P/E ratios | **No** |

**Conclusion:** all three asks require external data. Current A1 is the case Exhibit 9 verbatim — that's why it's KRW.

## Pending decision (blocker)

Reviewer chooses one of:
- **Option A:** User pulls 12M forward P/E (monthly, Jan 2009–Dec 2018, AAPL + 005930 KS) from school terminal (Bloomberg / FactSet / Capital IQ) and sends CSV → exact match to reviewer's ask.
- **Option B:** Use trailing 12M P/E from public sources (macrotrends), labeled and footnoted "forward not accessible without terminal" → partial concession.

Implementation kicks off once Option A or B is confirmed.

## Implementation Plan

### Step 1 — Replace A1 with USD financial snapshot (both firms, both levels)

**Layout:** one slide, two side-by-side blocks (Apple left, Samsung right).

**Data (FY2009 → FY2018, USD billions):**
- Per firm, company-level rows: Revenue · Operating Income · Net Income · R&D · R&D % of Revenue
- Per firm, phone-segment rows:
  - **Apple iPhone:** net sales (10-K product-revenue disclosure), units shipped — *no operating profit available, Apple did not disclose product-level segment profit before 2020*
  - **Samsung IM (IT & Mobile Comm.):** segment revenue, segment operating profit, units shipped

**Currency conversion:**
- Income statement: KRW → USD at **period-average** (Federal Reserve H.10 KRW/USD)
- Note Samsung's K-GAAP→K-IFRS transition at FY2009; start the table at FY2009.

**On-slide quote (from case p. 2, faculty-proof):**
> "In 2011, Apple and Google each spent more on lawsuits than on research and development."

**Sources cited on-slide:**
- Apple 10-K filings (apple.com/investor)
- Samsung Electronics audit reports (samsung.com/global/ir)
- FRB H.10 historical exchange rates

### Step 2 — New A2: Normalized share price

**Chart:** inline SVG, two lines, rebased to **100 on 2 Jan 2009**, daily through 31 Dec 2018.

**Tickers:** AAPL (NASDAQ), 005930.KS (KRX) — both adjusted close (handles dividends + Samsung's 2018 50:1 split).

**Lawsuit event markers (vertical lines + labels):**
1. **15 Apr 2011** — Apple files suit (case p. 3)
2. **24 Aug 2012** — Jury verdict, $1.05B (case p. 7)
3. **6 Dec 2016** — SCOTUS 8–0 design-patent ruling
4. **27 Jun 2018** — Confidential settlement

**Annotations (the "did this matter?" punchline):**
- Cumulative return at each marker, end-period return for both names.
- One-line takeaway: "Litigation news did/did not measurably move either stock."

**Source:** Yahoo Finance adjusted close.

### Step 3 — New A3: 12M forward P/E (or trailing, per pending decision)

**Chart:** inline SVG, two lines, monthly, Jan 2009 → Dec 2018, same event markers as A2.

**If Option A (forward P/E):** label "12M Forward P/E (consensus)" — source Bloomberg/FactSet/CapIQ via user-supplied CSV.

**If Option B (trailing P/E):** label "Trailing 12M P/E" with footnote *"Forward consensus P/E history requires Bloomberg/FactSet; trailing shown as proxy."* — source macrotrends.

**Annotations:** median multiple over period for each name; multiple at verdict (Aug 2012) and at settlement (Jun 2018) — supports a "investors did not re-rate either name on litigation news" reading.

### Step 4 — Speaker notes and navigation

- Rewrite A1 speaker note (currently says "trillion KRW") to match the new USD content.
- Add 1-2 sentence speaker notes for new A2 and A3 tying each to the main thesis.
- Renumber: A1 (Financials) · A2 (Share price) · A3 (P/E) · A4 (Aftermath — currently A2).
- Update slide footer counters.

### Step 5 — Verify

- Open `AvS.html` in browser at presentation aspect ratio.
- Check chart rendering, event-marker positioning, no title-area collisions.
- Walk speaker view to confirm note coherence.

## Data sources reference

| Need | Source | Free? |
|---|---|---|
| Apple financials (10-K, 2009–2018) | apple.com/investor | Yes |
| Samsung financials (audit reports, K-IFRS, 2009–2018) | samsung.com/global/ir | Yes |
| KRW/USD period-average exchange rates | federalreserve.gov/releases/H10 | Yes |
| Apple iPhone net sales (10-K product disclosure) | 10-Ks | Yes |
| Samsung IM segment data | Samsung audit reports | Yes |
| AAPL adjusted close | Yahoo Finance | Yes |
| 005930.KS adjusted close | Yahoo Finance | Yes |
| Trailing P/E history | macrotrends.net | Yes |
| **12M forward P/E history** | **Bloomberg / FactSet / Capital IQ** | **No — requires terminal** |

## Key dates (cross-checked vs case)

- Aug 2010 — Apple/Samsung cross-license talks; Apple PowerPoint (case p. 3, Exhibit 4)
- 15 Apr 2011 — Apple files suit (case p. 3)
- 22 Apr 2011 — Samsung counter-claims (case p. 4 cite)
- 24 Aug 2012 — Jury verdict, $1.05B, 21 hours of deliberation (case p. 7)
- 5 Oct 2012 — Samsung iPhone 5 counter-suit (case p. 7)
- 6 Dec 2016 — SCOTUS 8–0
- 27 Jun 2018 — Settlement

## Slide-count math

- Before: 11 main + 2 appendix = 13 sections
- After: 11 main + 4 appendix (A1 financials USD, A2 price, A3 P/E, A4 aftermath) = 15 sections
- Net: +2 slides (we replace old A1, add A2 and A3, demote old A2 to A4)

## Open questions for reviewer

1. Forward P/E source: Option A (terminal CSV) or Option B (trailing fallback)? **— message drafted, awaiting answer**
2. (Implicit) Period 2009–2018 OK, or trim to 2009–2014?
3. (Implicit) 4 backup slides OK, or compress?

## Resume instructions for next session

1. Read this file.
2. Check whether reviewer answered Option A or B.
3. If Option A: ask user for the forward-P/E CSV path; build A1, A2 in parallel; build A3 once CSV in hand.
4. If Option B: build all three slides in sequence using public sources only.
5. Keep currency rule strict: USD only on every visible number; period-average for flow items, period-end for stock items.
6. Cite sources on-slide for faculty defensibility.
