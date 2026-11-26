# Data Quality & Reconciliation Log
**EU Cosmetics Safety Gate — Value Protection risk monitor**

Every transformation applied to the raw Safety Gate extract, with its row/count impact and a reconciliation to an independent reference ("answer key"). The reference dataset in `data/processed/` and the Python pipeline that produced it were built with AI assistance and are used only to *validate* the build; all Excel / Power Query / Power BI analysis is the author's own and is reconciled against that reference here.

**Extract:** pulled 16 Oct 2026 from the European Commission Safety Gate public API. As-of date pinned to **2026-10-15** (`pAsOfDate`).

---

## 1. Load (typed, Power Query)

| Table | Rows | Cols | Reconciles |
|---|---|---|---|
| `qAlerts` | 5,403 | 31 | ✓ = source extract |
| `qMeasures` | 6,638 | 6 | ✓ = source extract |

Type controls that prevent silent downstream errors:
- `barcode` → **Text** (leading zeros preserved — e.g. `080730012629` stays intact; as a number the zero is lost and the join key breaks).
- all dates → **Date** (enables month/lag maths).
- file read as **UTF-8** (`Encoding = 65001`) so accented authority/country names (Česko, Lietuva) survive the country join rather than becoming mojibake.

## 2. Cleaning & derivation

| Step | Rule | Before → After | Reconciliation |
|---|---|---|---|
| Standardise `product_type` | Trim, Clean, Lowercase, `-`→space | **542 → 511** distinct | ✓ 31 duplicates merged; rows unchanged (5,403). e.g. "Eau de Toilette"="Eau de toilette", "Skin-lightening cream"="Skin lightening cream" |
| `lag_days` | `publication_date − creation_date` (days) | — | ✓ **100%** match to reference `notification_lag_days` |
| `Year`, `month_start` | from `publication_date` (the KRI clock) | — | Year range **2016–2026** (note: README states 2017; data contains a stray 2016 record) |
| `country_dim` merges | Left Outer ×2 (notifying + origin) | **5,403 → 5,403** | ✓ no fan-out (lookup key is unique). `origin_region` null for 655 alerts (12.1%, XX = Unknown origin) — expected, not an error |
| Split `risk_types` | split on `\|` into rows | **5,403 → 5,433** rows | ✓ +30 = alerts carrying a 2nd risk type; 9 distinct types |

## 3. Classification (keyword lookups)

| Field | Method | Result vs reference | Notes |
|---|---|---|---|
| Primary substance — BMHCA (`S01`) | first-keyword match (SEARCH) | **4,192 vs 4,175 (+17)** | Over-count, *not* a coverage gap — 0 true BMHCA alerts missed. Cause: the lookup returns the first keyword in **table order** (BMHCA keywords sit first), not the first substance **named in the text**, so 17 secondary mentions get over-promoted. The reference ranks by text position |
| Product family — Fragrance | keyword rules, priority order | **2,156 vs 2,153 (+3)** | **99.5%** exact match across all 15 families. Regex rules were flattened to plain keywords (Excel's SEARCH can't read regex); the small diffs are regex features Excel can't replicate — word boundaries (`\b`), negative lookahead (`(?! …)`) |

**Documented keyword traps** (why first-match needs priority ordering):
- **"lead":** 91 text matches, of which **63** are the phrase "may lead to" (not the metal) → a naive match over-tags by ~63.
- **MI token:** 104 matches, of which **76** are the MCI/MI *mixture* (a distinct substance) and only 28 are pure MI → a naive match tags all 104 as MI.

## 4. KRI numerators

| KRI | Definition | Value | Reconciliation |
|---|---|---|---|
| **K03** Fragrance share | substance is fragrance-related | 4,298 (79.5%) | vs reference 4,305 (−7); rides the naive substance lookup, within tolerance |
| **K05** Compulsory-measure rate | alert has ≥1 compulsory measure | 4,860 (90.0%) | ✓ COUNTIFS against `qMeasures` |
| **K06** Recall/withdrawal rate | alert has ≥1 recall or withdrawal | 1,425 (26.4%) | reference figure (measure builds Day 16) |
| **K07** Notification lag | median days creation→publication | median **2**, P90 **8** | ✓ 105 alerts > 30 days |

## 5. Known data-quality caveats

- **Notification-lag tail:** median is 2 days but max is **1,729** and mean **7.7** — a thin tail of alerts where `creation_date` reflects an earlier system entry, not the drafting of that notification. K07 uses the **median** to stay robust to it; the tail is a data artefact, not a performance signal.
- **Enforcement intensity, not underlying risk:** Italy notifies **56.5%** of alerts but originates far fewer. The dataset measures *where market-surveillance authorities look*, not total market risk — every notification-count KRI inherits this bias. (Italy's 56.5% has no denominator of products actually on the Italian market.)
- **Classification coverage:** keyword lookups cover ~99% of alerts; unmatched alerts return `"none"`.
- **Missing fields:** 12.1% of alerts have XX (unknown) country of origin; `sold_online` is unknown for 81.8% (4,419 of 5,403).
- **Scheme change:** reference codes shift from `A12` (old GPSD serious-risk) to `SR` (new GPSR serious-risk) at the Dec 2024 regulation change; both denote serious-risk notifications — a change in legal basis, not severity.

## Method

All figures above are reconciled against `data/processed/alert_classified.csv`, an independent reference. That reference and the Python scripts in `/scripts` are AI-assisted validation material; the workbook analysis is the author's own work.
