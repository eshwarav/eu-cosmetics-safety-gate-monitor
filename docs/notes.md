## Day 1 

## Alerts reviewed

1. [325698](https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/325698?lang=en), Skin cream, 2018, Ireland, MI (ref A12/1113/18)
2. [10091838](https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/10091838?lang=en), Eau de parfum, 2024, Italy, BMHCA (ref SR/03832/24)
3. [10119076](https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/10119076?lang=en), Gel nail polish, 2026, Italy, TPO (ref SR/02766/26)
4. [10119263](https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/10119263?lang=en), Shampoo, 2026, Sweden, PPD +3 (ref SR/02952/26)
5. [10118533](https://ec.europa.eu/safety-gate-alerts/screen/webReport/alertDetail/10118533?lang=en), Perfume, 2026, Czechia, counterfeit, French origin (ref SR/02205/26)

## Observations

Observation 1, substance naming is inconsistent; the acronym is the reliable key.
Comparing alerts #2 and #5 (both BMHCA), the chemical name isn’t written the same way, #2 has a space inside “tert- butylbenzyl,” #5 doesn’t. The full IUPAC string is therefore unreliable as a match key, but the parenthetical “(BMHCA)” is identical in both. Implication for my Week 2 lookup: anchor on the acronym token, not the chemical name, or I’ll undercount.

Observation 2, these are labelling-compliance alerts, not toxicology findings.
Every modern alert uses the phrase “according to the list of ingredients, the product contains X, which is prohibited.” The authority is reading the declared INCI list, not reporting a measured dose or an injury. So this dataset captures regulatory/labelling non-compliance surfacing through market surveillance, a formulation and artwork problem, which is squarely Value Protection’s remit. I should describe my KRIs as compliance-breach indicators, not consumer-harm counts, to avoid overclaiming.

Observation 3, there are two eras of phrasing, and my lookup has to survive both.
The 2018 alert (#1) is terse, “The cream contains methylisothiazolinone (MI).”, no “prohibited,” no harm clause, while the 2024–26 alerts are rigid boilerplate. The template standardised somewhere in between. A keyword lookup tuned on recent language will likely under-match 2017–2019 text, so that’s where my coverage gaps will hide. (Also: #1 is MI, the substance the data dictionary flags for mis-tagging inside MCI/MI mixtures; one to watch on Day 9.)

Observation 4, same violation, different measure, and that split is itself a signal.
The same breach (a banned ingredient) drew different responses: alert #1 got a voluntary withdrawal, #2–5 got compulsory measures. That compulsory-vs-voluntary split feeds K05 (compulsory rate) and K06 (recall/withdrawal rate), and it tracks how aggressively a given member state enforces as much as the underlying risk. It’s the measures-side version of the “Italy notified 57%” caveat: my KRIs partly measure enforcement intensity, not danger.

Observation 5, “lag” means two different clocks; keep them separate.
Notification lag on my five alerts is tiny (0, 4, 2, 2, 1 days), so K07 (creation→publication lag) isn’t a “how fast did they catch it” signal for recent alerts, it’s near-zero. The lag behind my headline finding is a different clock entirely: ban date → publication date (the ~31-month BMHCA tail). I have to keep these two lags labelled separately or I’ll mis-describe K07 versus the ban-tail story.

Observation 6, the alert reference number is structured metadata: PREFIX / serial / year.
Every reference has three parts, e.g. SR/03832/24. The prefix is a regime code, A12 (old GPSD serious-risk, 2016–2026) vs SR (new GPSR serious-risk, from 2024); both are serious-risk, so the prefix marks era/legal basis, not severity, and the A12→SR switch reflects the GPSR becoming applicable in Dec 2024. The middle part is a sequential serial within the year; the suffix is the 2-digit year. That year tracks the creation year, not publication, they differ in 34 alerts, so I’ll keep using publication_date for monthly KRIs and treat the reference only as an ID + a regime flag. This is the same “two eras / two clocks” pattern as Obs 3 and 5, visible in the numbering.


## Day 2, Column → regulation mapping

**Headline:** the 31 alert columns split three ways, product law (Reg. 1223/2009),
surveillance law (GPSD/RAPEX → GPSR), and plain system metadata, and the two columns
that fit *none* of them, `brand` and `counterfeit`, are exactly where Value Protection
lives: the seam between product-safety law and brand/IP protection.

### A, Product law · Regulation (EC) 1223/2009 (what the product is / contains / declares)
| Column(s) | Concept |
|---|---|
| `product_category` | Art. 2, scope (qualifies as a "cosmetic product") |
| `product_type`, `product_name` | Art. 13, notification category / name (CPNP) |
| `product_description` | Art. 19, product as presented |
| `risk_description` | **The breach**, Annex II (prohibited) / Annex III (restricted) |
| `legal_provision` | Cited legal basis (usually 1223/2009 + annex) |
| `professional_product` | Annex III use-conditions / Art. 19 professional-use labelling |
| `country_of_origin`, `origin_code` | **Dual home**, Art. 13 (notify import origin) *and* Art. 19 (label it) |

### B, Surveillance law · GPSD/RAPEX → GPSR (Reg. 2023/988, from 13 Dec 2024)
| Column(s) | Concept |
|---|---|
| `reference`, `notification_type` | Notification identity + severity code (A12 → SR = the regime shift) |
| `notifying_country`, `notifying_country_code` | Which market-surveillance authority notified |
| `risk_types` | Hazard taxonomy (CHEMICAL/MICRO…), classifies the hazard, not the substance |
| `measures_count`, `measures_compulsory`, `measures_voluntary` | Enforcement response → **K05 / K06** |
| `recall_published_online`, `company_recall_link` | Recall transparency |
| `reacting_countries`, `reacting_countries_count` | Cross-border reaction → **K08** |
| `sold_online` | Sales channel (in scope under GPSR) → **K09** |

### C, System metadata (no regulatory concept, just the record)
| Column(s) | Note |
|---|---|
| `alert_id`, `web_report`, `web_report_date`, `alert_url` | Identifiers / links |
| `creation_date`, `publication_date` | Timestamps, `publication_date` is the **KRI clock** |
| `barcode` | GS1/GTIN identifier, the **join key** |

### Outside both safety regimes, brand protection / IP
| Column | Concept |
|---|---|
| `brand` | Legal identity under 1223/2009 is the *Responsible Person* (Art. 4), not the brand, brand is commercial |
| `counterfeit` | IP / anti-counterfeiting (customs Reg. 608/2013) → **K10**. No home in either safety regulation, which is *why* it's a Value Protection signal |

## Six of these columns feed KRIs directly (K05/K06/K08/K09/K10). The mapping isn't academic, it's where half the KRIs come from, and it frames what VP owns (the A↔B seam and the brand/IP columns) vs. what regulatory compliance owns (A and B proper).


## Day 3, Typed load with Power Query

**What I built:** two queries, `qAlerts` (5,403 × 31) and `qMeasures` (6,638), that refresh in one click and never lose a leading zero, driven by a single `FilePath` parameter so the model survives the folder being moved or handed to someone else.

**The pipeline (Applied Steps), read left to right:**
| Step | What it does | Why it matters |
|---|---|---|
| Source | `Csv.Document(..., Encoding = 65001)` reads the file | 65001 = UTF-8; without it, accented authority names (Česko, Lietuva) load as mojibake and fail the country join later |
| Promoted | first row → headers | columns get real names instead of Column1 |
| BlanksToNull | `""` → null | COUNTA and filters treat empty-string as *present*; null as *absent*, gets "unknown" counts right |
| Typed | sets every column's data type | the step that carries the project's reliability |

**The three type decisions that are silent-failure risks:**
- `barcode` → **Text**: as a number Excel drops the leading zero (080730012629 → 80730012629) and the join key is broken forever.
- dates → **Date**: wrong type kills every month, lag, and time-intelligence calculation downstream.
- correct **locale**: so DD/MM never silently flips to MM/DD.

**Check:** qAlerts = 5,403 rows loaded, qMeasures = 6,638, FilePath/pAsOfDate = Connection only.
**Lesson:** the load is where correctness is decided. A wrong type here surfaces three weeks later as a nonsensical KRI with no obvious cause.


## Day 4, Standardise product_type

**What I did:** four cleaning operations on `product_type`, each fixing a specific way the same value hides as two:
| Operation | Fixes |
|---|---|
| Trim | leading/trailing spaces (`perfume ` ≠ `perfume`) |
| Clean | invisible control characters |
| Lowercase | `Perfume` = `perfume` |
| Replace `-` → space | `skin-lightening` = `skin lightening` (data-dictionary trap #3) |

**Result:** distinct `product_type` fell **542 → 511**, 31 phantom categories collapsed. Real examples merged: `Eau de Toilette`=`Eau de toilette`, `Skin-lightening cream`=`Skin lightening cream`, `hair-dye`=`Hair dye`. Each of those would otherwise have fragmented a pivot and split a KRI, which is why cleaning precedes any counting.

**Correction to the manual:** its "replace XX with Unknown" step does **not** apply to `product_type`, zero XX values here; XX is the Unknown marker for the *origin* columns (handled Day 6). Habit: verify an instruction against the data before following it.


## Day 5, Time and lag columns

**Columns added:**
| Column | Definition | Note |
|---|---|---|
| `Year` | year of `publication_date` | publication_date is the KRI clock, *not* creation_date (Obs 5) |
| `month_start` | `Date.StartOfMonth(publication_date)` | the grouping key for every monthly KRI |
| `lag_days` | `publication − creation` | reproduces the reference answer key **exactly (100%)** |

**Parameter:** `pAsOfDate = 2026-10-15`, pinning "today" to the extract date so any "months since ban" or trailing-window figure stays reproducible instead of drifting when recomputed in December.

**Lag distribution:** median **2 days**, but a long tail, max **1,729 days**, and 105 alerts over 30 days, zero negatives. This is exactly why K07 is defined on the **median**: a handful of multi-year outliers (an alert created in 2023, published in 2026) would wreck a mean. The big lags trace to `creation_date` reflecting an earlier system entry, not the drafting of that specific notification, a data-quality note for Day 27.


## Day 6, Country merges and the enforcement pivot

**What I built:** merged `country_dim` onto the alerts twice, once on notifying country, once on origin, with **Left Outer** joins, bringing in region and EU27 flag for each side.

**Validation:** row count held at **exactly 5,403** after both merges, confirming no fan-out. (A left join multiplies rows if the lookup key has duplicates; `country_dim` is unique on `country_code`, so rows are safe, the same watchlist-join risk I knew from screening.)

**Notifying-country pivot (% of all alerts):**
| Country | Alerts | % |
|---|---|---|
| Italy | 3,055 | 56.5% |
| Czechia | 565 | 10.5% |
| Hungary | 548 | 10.1% |
| Sweden | 191 | 3.5% |
| Germany | 170 | 3.1% |

**The insight:** Italy notifies **56.5%** of all EU cosmetics alerts but originates far fewer, so this data measures *enforcement intensity* (where authorities look) as much as underlying risk. This is the measures-side of Obs 4, now backed by a column I can pivot.

**Trap caught:** Excel defaulted the value field to *Sum of alert_id* and returned a plausible-but-wrong **59.3%**, because newer alerts have larger IDs and Italy has many recent ones, so summing inflated its share. *Count* gives the true 56.5%. Never sum an identifier.


## Day 7, What surprised me
1. The same substance is written three different ways across alerts, the parenthetical acronym is the only reliable match key.
2. One country, Italy, drives more than half the dataset, so the KRIs partly measure who enforces, not what is dangerous.
3. A naive first-match lookup produces a plausible wrong answer, not an obvious error, which is the dangerous kind.


## Day 8, Normalise risk_types

**What I built:** `qRiskTypes`, referenced `qAlerts`, kept `alert_id` + `risk_types`, split `risk_types` on "|" into **rows**. Result: **5,433 rows** (30 more than 5,403, the alerts carrying a second risk type), **9 distinct** types.

**Distribution:**
| Risk type | Count |
|---|---|
| CHEMICAL | 5,219 |
| MICROBIOLOGICAL | 127 |
| HEALTH_RISK_OTHER | 31 |
| ENVIRONMENT / CHOKING | 22 / 22 |
| BURNS / CUTS / DAMAGE_TO_SIGHT / INJURIES | 7 / 3 / 1 / 1 |

**Check:** `COUNTIF(risk_types, "*CHEMICAL*")` = **5,219 (96.6%)**. The `*` wildcards matter, without them, plain `"CHEMICAL"` misses the ~28 multi-type alerts like `CHEMICAL|MICROBIOLOGICAL` and undercounts.

**Finding:** the hazard-type dimension is almost flat for cosmetics, 96.6% chemical, everything else marginal. It carries little information and doesn't warrant a dashboard tile, unlike toys/electronics where hazard type genuinely varies.

**Also solved:** a Power Query hang where a *referenced* query (qRiskTypes → qAlerts, which combines CSV + merges) tripped the Formula Firewall's privacy check and "loaded" for 20 minutes. Fix: workbook → Query Options → Ignore Privacy Levels.


## Day 9, Substance lookup and the BMHCA gap

**What I built:** `substance_naive`, for each alert, `XLOOKUP(TRUE, ISNUMBER(SEARCH(keyword, risk_description)), substance_id, "none")` finds the first keyword present in the text and returns its substance id.

**The result and the gap:** naive BMHCA (S01) = **4,192** vs reference **4,175** → **+17 over-count**. Explaining it *is* the deliverable:
- The formula returns the first keyword in **table order** (BMHCA's keywords sit first), not the first substance named in the **text**. So 17 alerts that mention BMHCA only secondarily get over-promoted to S01.
- Zero true BMHCA alerts were *missed* (all 4,175 caught), so it's pure over-count, not a coverage gap, the four keyword forms (`bmhca` 4,170, `butylbenzyl` 3,796, `butylphenyl methylpropional` 393, `lilial` 53) are comprehensive.

**The two traps, same root cause (order & specificity):**
| Trap | Numbers | Effect |
|---|---|---|
| "lead" | 91 matches, 63 are "may lead to" | naive over-tags lead by ~63 false positives |
| MCI/MI | 104 MI matches, 76 are the MCI/MI *mixture*, 28 pure MI | naive tags all 104 as MI |

The reference avoids all of it by ranking on **position in the text** (match_rank). This is the same screen-and-triage problem as sanctions screening: a watchlist token matching too broadly ("lead"), and a specific designation hiding inside a generic one (the mixture).

**Debugging lessons banked:** `[@column]` structured references only resolve inside a *genuine* table member (use a plain cell reference otherwise); French Excel still accepts commas (tested with `=SUM(1,2)`); and isolating each piece of a formula in its own cell is the fastest way to find the broken part.


## Day 10, Product family and the fragrance flag

**The problem:** the supplied `Product_Family_Rules` table is **regex** (`\b`, `|`, `(?! …)`), which Excel's `SEARCH` cannot read. So I rebuilt it as a plain-keyword table in **priority order** (96 keywords across 15 families, specific families like Hair colouring before general ones like Hair care, the same first-match ordering lesson as Day 9) and ran the Day-9 engine against `product_type`.

**Validation:** reproduces the reference at **99.5%** exact match. Top families:
| Family | Mine | Ref |
|---|---|---|
| Fragrance (incl. body sprays) | 2,156 | 2,153 |
| Skin care | 606 | 618 |
| Hair care | 609 | 610 |
| Bath & shower | 536 | 537 |

The small diffs are the regex niceties Excel can't do (negative lookahead on "makeup remover", word boundaries on "sun"/"set").

**Fragrance flag:** `frag_flag` looks each alert's substance up in the dictionary's `fragrance_related` field → 1/0. This column **is KRI K03 (fragrance share)** = **4,298, ~80%**.

**Two findings:** perfumes and body sprays are **40%** of all alerts; **80%** are fragrance-related. Fragrance is the exposed category for a major fragrance house, which is exactly why the 31 July 2028 allergen-labelling deadline is the risk to watch.


## Day 11, Compulsory-measure flag (K05 numerator)

**What I built:** `has_compulsory`, a 1/0 flag per alert, via `COUNTIFS(qMeasures[alert_id],[@alert_id],qMeasures[measure_type],"COMPULSORY")>0`, reaching across to the measures table to ask "does this alert carry at least one authority-*forced* measure?" **SUM = 4,860 (90.0%).**

**Method note / lesson:** this runs 5,403 COUNTIFS, each scanning 6,638 measure rows, deliberately heavy. The lesson is architectural: a per-row cross-table lookup is fine for a one-off check but belongs in a pre-aggregated Power Query **Group By** for production. (Also re-hit the Day-9 trap: `[@alert_id]` wouldn't resolve because the column wasn't a true table member; a plain `A2` cell reference fixed it.)

**Finding:** 90% of alerts carry a compulsory measure, authorities *force* action nine times in ten. This is the measures-side twin of the Italy-56.5% finding: both measure enforcement posture, not underlying danger.


## Day 12, Lag analysis (K07)

**What I built:** four summary stats on `lag_days`, plus data bars to see the distribution at a glance.
| Statistic | Value |
|---|---|
| Median lag | **2 days** |
| P90 (`PERCENTILE.INC`, 0.9) | **8 days** |
| Alerts > 30 days | **105** |
| Mean | 7.7 |
| Max | 1,729 |

**Finding / lesson:** 90% of alerts are published within **8 days** of creation (median just 2), authorities publish fast. But the **mean is 7.7, nearly 4× the median**, dragged up by a thin tail (max 1,729 days, where `creation_date` reflects an earlier system entry). That median-vs-mean gap is the concrete, on-my-own-data argument for defining K07 on the **median**, robust to the outliers that would otherwise make the lag look far worse than it is.


## Day 13, The KRI tracker (K01–K10), the monthly monitor

**Headline:** the monitor itself, a monthly table (Jan-23 → Sep-26, 45 rows) that computes all ten KRIs off the alert model, with RAG colour driven by **editable threshold cells** so a user can re-tune amber/red without touching a formula.

**The engine (three techniques):**
- `COUNTIFS` / `SUMIFS` aggregate the alert columns **by publication month** (a `>=` month-start, `<` next-month window).
- `EDATE(month, -12)` builds the **trailing-12-month window** for the K02 surge ratio, it has to reach back *before* the tracker's first row, so it reads the raw dates, not the K01 column.
- `MEDIAN(FILTER(lag_days, month-condition))` gives a **conditional median** for K07, there is no `MEDIANIFS`, so `FILTER` isolates the month and `MEDIAN` takes it.

| KRI | Definition | Method |
|---|---|---|
| K01 Alerts | count per month | COUNTIFS on publication_date window |
| K02 vs T12M | this month ÷ trailing-12M avg | K01 ÷ (COUNTIFS over prior 12 mo / 12) |
| K03 Fragrance share | fragrance-related ÷ alerts | SUMIFS(frag_flag) ÷ K01 |
| K05 Compulsory rate | ≥1 compulsory measure ÷ alerts | SUMIFS(has_compulsory) ÷ K01 |
| K06 Recall/withdrawal | ≥1 recall/withdrawal ÷ alerts | SUMIFS(has_recall) ÷ K01 |
| K07 Median lag | median days creation→publication | MEDIAN(FILTER(...)) |
| K08 Cross-border % | reacting countries > 0 ÷ alerts | COUNTIFS(...,rcc>0) ÷ K01 |
| K10 Counterfeit | counterfeit = YES, count | COUNTIFS(...,"YES") |

**Reconciliation:** the Jan-2023 row reproduces the reference answer row exactly, K01 **53**, K02 **3.06**, K05 **89%**, K06 **28%**, K07 **19**, K08 **13%**, K10 **0**. Only K03 is off by one (51 vs 52), the documented −7 drift from the naive substance lookup.

**Three findings the tracker surfaces:**
1. **K03 fragrance share collapses through 2026**, from ~66% in January to 15–28% mid-year. The TPO / gel-nail wave (non-fragrance) is displacing BMHCA fragrance alerts: the *exposed category is shifting from fragrance to nail products*.
2. **K06 recall/withdrawal rate climbs in 2026** (up to ~46%), authorities escalating from market withdrawal toward consumer recall as the banned back-catalogue clears.
3. **K10 counterfeit ≈ 0 everywhere**, only 17 counterfeit alerts in the entire dataset. Counterfeit barely surfaces in *official* EU alerts: a blind spot in the data, not an absence of the problem, and precisely why brand-protection needs sources beyond Safety Gate.

**Top-substance column + a debug lesson:** the "most-common substance per month" needed a modal lookup, and it surfaced a real Excel limit, `COUNTIF`/`SUMIF` require genuine worksheet **ranges, not in-memory arrays**. A `FILTER`-then-`COUNTIF(s,s)` approach failed silently (the `IFERROR` turned the error into a blank); the fix was to push the month condition *into* `COUNTIFS` against the real columns and take the max count. The column also names the story: the top substance flips from **S01 (BMHCA) to S05 (TPO) in mid-2026**, the fragrance-to-nail shift, pinned to the substance.


## Day 14, Power BI star schema

**What I built:** the whole model skeleton, six tables wired into a star, a DAX date table marked and sorted, and seven relationships including the two inactive "role-playing" links the time and country measures switch on later. The authorship decision stands: the fact tables are **my own Excel queries** (`qAlerts` → `fAlerts`, `qMeasures` → `fMeasures`), not the AI reference merge, so every number traces back to work I did by hand.

**The six tables:**
| Table | Source | Rows | Role |
|---|---|---|---|
| `fAlerts` | my Excel `qAlerts` | 5,403 | fact |
| `fMeasures` | my Excel `qMeasures` | 6,638 | fact |
| `dCountry` | `country_dim.csv` | 79 | dimension (role-playing) |
| `dSubstance` | `substance_dictionary.csv` | 35 | dimension |
| `dDate` | DAX `CALENDAR` | Dec-2016 → Dec-2026 | date dimension |
| `dBan` | Enter Data (S01, S05) | 2 | ban-date spine (Day 25) |

**The date table (the piece that unlocks time intelligence):** `dDate = ADDCOLUMNS(CALENDAR(DATE(2016,12,1), DATE(2026,12,31)), …)` with `Year`, `Month No`, `Month` (display "Jan 2023"), `Month Start`, `YearMonth` (sortable integer). Two settings make it behave: **Mark as Date Table** on `[Date]` (what activates the time-intelligence functions), and **Sort `Month` by `YearMonth`** so months sort chronologically, not alphabetically.

**The seven relationships:**
| From (one) | To (many) | State |
|---|---|---|
| `dDate[Date]` | `fAlerts[publication_date]` | active |
| `dDate[Date]` | `fAlerts[creation_date]` | inactive |
| `dCountry[country_code]` | `fAlerts[notifying_country_code]` | active |
| `dCountry[country_code]` | `fAlerts[origin_code]` | inactive |
| `dSubstance[substance_id]` | `fAlerts[substance_naive]` | active |
| `fAlerts[alert_id]` | `fMeasures[alert_id]` | active |
| `dBan[substance_id]` | `dSubstance[substance_id]` | active |

**Why the two inactive links matter:** you can't have two active paths between the same pair of tables, Power BI greys the second to avoid an ambiguous filter. The dotted `creation_date` and `origin_code` links are parked deliberately, to be switched on inside specific measures with `USERELATIONSHIP`. This is the modelling version of the Day-6 notifying-vs-origin split: one fact table, two lenses (who *flagged* it vs. where it *came from*).

**Four load traps caught:**
| Trap | Symptom | Fix |
|---|---|---|
| `barcode` auto-typed Whole Number | import threw 70 errors | retype to Text (the Day-3 leading-zero lesson, re-surfacing in Power BI) |
| stray blank row | import showed 5,404, not 5,403 | filtered on `alert_id` null → back to 5,403 |
| dimension headers | `dSubstance`/`dCountry`/`dBan` loaded as `Column1, Column2…` | Use First Row as Headers; dropped `dSubstance`'s regex column |
| fact-table name | alerts loaded as `qAlerts` | renamed `fAlerts` so the `f`/`d` prefixes mark fact vs. dimension at a glance |

**Lesson:** a star schema isn't decoration, it's what lets one `dDate` or `dCountry` filter the whole fact table cleanly. Get the relationships and the marked date table right and every measure downstream inherits correct filtering; get them wrong and the error hides three steps later in a nonsensical trend. Same principle as Day 3: correctness is decided at the model layer, not the visual.


## Day 15, Core DAX, base measures

**What I built:** the base measure layer, the nine measures every KRI and visual sits on, validated to the digit against the Excel tracker. The transferable skill is one skeleton: `DIVIDE(CALCULATE(COUNTROWS(fAlerts), <filter>), [Alerts])`. Learn it once and K03, K05, K08, K09, K10 are all just a different `<filter>`.

**The measures:**
| Measure | Logic | Validates to |
|---|---|---|
| `Alerts` | `COUNTROWS(fAlerts)` | 5,403 |
| `Fragrance Share %` | `DIVIDE(SUM(frag_flag), [Alerts])` | 87.6% (2025) |
| `Compulsory Alerts` | `CALCULATE(COUNTROWS, has_compulsory=1)` | 4,860 |
| `Compulsory Rate %` | `DIVIDE([Compulsory Alerts], [Alerts])` | 90.0% |
| `Median Lag Days` | `MEDIAN(lag_days)` | 2 |
| `Cross-border %` | `DIVIDE(CALCULATE(COUNTROWS, rcc>0), [Alerts])` | K08 |
| `Online Share %` | `DIVIDE(YES, YES+NO)`, known channel only | K09 |
| `Counterfeit Alerts` | `CALCULATE(COUNTROWS, counterfeit="YES")` | K10 |
| `Alerts by Origin` | `CALCULATE([Alerts], USERELATIONSHIP(country_code, origin_code))` | re-lens to origin |

**Two correctness decisions, not just syntax:**
- **Online Share denominator excludes `UNKNOWN`.** 82% of alerts have unknown channel; dividing by all 5,403 would understate online share massively. "Share of *known* channel" (denominator = YES + NO = 984) is the only honest read, the same "don't let missing data masquerade as a zero" instinct as the Day-6 origin nulls.
- **`Alerts by Origin` fires the inactive link.** `[Alerts]` counts by *notifying* country (Italy huge); wrapping it in `USERELATIONSHIP` flips it to *origin* for that measure only. This is the model-layer proof of the Day-6 enforcement-vs-risk caveat, the mechanism that stops anyone reading Italy's 57% as "Italy makes the most dangerous cosmetics."

**Three bugs, each a real DAX lesson:**
| Bug | Symptom | Root cause |
|---|---|---|
| One box, three measures | "syntax for 'Compulsory' is incorrect" | pasted three measures into one New-measure box; one box = one name = one measure |
| Circular dependency | "circular dependency detected: [Compulsory Alerts]" | the mashed paste left a measure referencing *itself*; fixed by deleting and rebuilding base-first |
| Measure vs. column | `Fragrance Share %` showed "Sum of… 23,222,094" | accidentally built as a calculated column: 4,298 fragrance alerts × 5,403 rows = 23.2M. A column computes per-row and the visual sums all 5,403; a measure computes *once*, in context |

**The validation that mattered most:** dropping a `dDate[Year]` slicer and clicking 2025 drove Fragrance Share % from 0.80 (all years) to 0.88 (87.6%). The number *moving* is the proof that the `dDate → publication_date` relationship is live, the one thing that could have silently broken every trend downstream. It works.

**Lesson:** measure vs. calculated column is *the* Power BI distinction. KRIs are always measures, they react to filters and compute in the visual's context; a column is baked per-row at load and gets summed. The "Sum of" prefix and an impossibly large number are the tell. Worth knowing cold for the Phase B rebuild.


## Day 16, Time intelligence, the trend and surge layer

**What I built:** seven measures that turn static counts into trends and build the surge detector, `Alerts PY`, `Alerts YoY %`, `Alerts YTD`, `Alerts R12M`, `T12M Monthly Avg`, `Alerts vs T12M`, and `K02 Colour`. This is the layer the whole dashboard's time logic sits on, and it only works because `dDate` was marked as a date table on Day 14, the functions below (`SAMEPERIODLASTYEAR`, `TOTALYTD`, `DATESINPERIOD`) refuse to run on an unmarked table. That one Day-14 setting is what this day cashes in.

**The measures:**
| Measure | Logic | Does |
|---|---|---|
| `Alerts PY` | `CALCULATE([Alerts], SAMEPERIODLASTYEAR(dDate[Date]))` | shifts context back one year |
| `Alerts YoY %` | `DIVIDE([Alerts]-[Alerts PY], [Alerts PY])` | year-over-year change |
| `Alerts YTD` | `TOTALYTD([Alerts], dDate[Date])` | running year-to-date total |
| `Alerts R12M` | `CALCULATE([Alerts], DATESINPERIOD(dDate[Date], MAX(dDate[Date]), -12, MONTH))` | rolling 12 months, inclusive |
| `T12M Monthly Avg` | `DIVIDE(CALCULATE([Alerts], DATESINPERIOD(dDate[Date], MIN(dDate[Date])-1, -12, MONTH)), 12)` | avg month of the *prior* 12 |
| `Alerts vs T12M` | `DIVIDE([Alerts], [T12M Monthly Avg])` | the K02 surge ratio |
| `K02 Colour` | `SWITCH(TRUE(), ... )` | RAG flag for the dashboard |

**The one distinction that matters:** `R12M` looks *back from* the current month and includes it; `T12M Monthly Avg` looks at the 12 months *before* this month. The anchor `MIN(dDate[Date]) - 1` sets the baseline window to end the day before the current period, so **a surge month can't contaminate its own baseline**. That's the difference between a surge detector that works and one that quietly dampens every spike by averaging it into its own benchmark.

**Reconciliation:** `Alerts R12M` at **Sep-2026 = 864**, and `Alerts vs T12M` at **Jan-2023 = 3.06** (53 alerts ÷ 17.33 trailing average), both tie exactly to the Excel K02 column. Same numbers, two engines, one more confirmation the Power BI model counts what the workbook counts.

**Lesson:** "trailing average" is a trap unless you say *trailing from when*. Anchoring the baseline window to end before the current period, not at it, is the whole game, the same discipline as the Day-5 as-of-date parameter: pin the window or the number drifts.


## Day 17, K04 emerging substance and the what-if parameter

**What I built:** the early-warning measure, `K04 Emerging Flag`, plus a what-if parameter that makes the surge thresholds a user-draggable slider instead of a hard-coded number.

**K04 logic:**
```
K04 Emerging Flag =
VAR Recent3M = CALCULATE([Alerts], DATESINPERIOD(dDate[Date], MAX(dDate[Date]), -3, MONTH))
VAR BaselineEnd = EOMONTH(MAX(dDate[Date]), -3)
VAR PriorAvg = DIVIDE(CALCULATE([Alerts], DATESINPERIOD(dDate[Date], BaselineEnd, -12, MONTH)), 12)
RETURN IF(AND(Recent3M >= 5, Recent3M > 2 * PriorAvg), 1, 0)
```
It flags a substance when its trailing-3-month count is both **≥ 5** (noise floor) and **more than double** its prior-12-month monthly average. `EOMONTH(…, -3)` anchors the baseline to end just before the 3-month window, the same don't-contaminate-your-own-baseline rule as Day 16. It's the `Alerts vs T12M` surge test from yesterday, sliced per substance instead of applied to the whole dataset, which is exactly why the general version was built first.

**The design insight:** for a substance emerging from zero (TPO had ~0 alerts before late 2025), `PriorAvg ≈ 0`, so `2 × PriorAvg ≈ 0` and the comparison is trivially true. That means the **minimum-5 guard is the real trigger** for anything new, the flag fires the moment a from-nothing substance first clears 5 alerts in a rolling quarter. Without that floor, one stray alert against a zero baseline would fire a false positive every time.

**Validation, the headline of the whole project:** filtered to S05 (TPO), K04 first fires in **November 2025**, holds through **August 2026**, then switches back to 0 as the baseline catches up. That on/off shape is correct, an "emerging" flag *should* stop firing once the thing has become the new normal. In plain terms: **this monitor would have flagged TPO in November 2025, seven months before it peaked at 96 alerts in June 2026.** That is the case for building a leading-indicator monitor at all.

**Upgrade C, the what-if parameter:** two numeric-range parameters, `Surge Red Threshold` (default 2.0) and `Surge Amber Threshold` (default 1.5), each auto-creating a slicer and a `[… Value]` measure. `K02 Colour` was rewired to read them:
```
K02 Colour =
VAR Ratio = [Alerts vs T12M]
RETURN SWITCH(TRUE(),
    Ratio >= [Surge Red Threshold Value], "Red",
    Ratio >= [Surge Amber Threshold Value], "Amber",
    "Green")
```
Dragging the red slider re-tunes the whole dashboard's RAG live, no formula editing. The order matters: the parameter measures must exist before the measure that references them, or the names red-underline.

**Debug lesson, the Jan-2023 trap:** the first validation matrices showed K04 = 0 for TPO everywhere and looked like a broken measure. It wasn't, the visuals were pinned to a stray Jan-2023 filter (a month when TPO didn't exist), so of course the flag was 0. The fix was to read the flag on the all-months matrix, where it fired correctly. The lesson is the Power BI twin of the Day-9 formula-isolation habit: **a measure reading 0 inside a filtered visual is not a broken measure, check the visual's filter context before rewriting the DAX.** Most "wrong number" moments in Power BI are filter-context, not formula.


## Day 18, Dashboard pages 1 and 2

**What I built:** the first two dashboard pages and the drill-through that connects them, KRI Overview (six KPI cards + a RAG surge chart), Substance Watch (a substance × year heatmap + a K04 emerging leaderboard), and an Alert Detail page you reach by right-clicking a substance. Every visual runs off measures already built and validated, so this day was assembly, not new logic, exactly the payoff for front-loading the model and DAX.

**Page 1, KRI Overview:**
| Element | Build |
|---|---|
| 6 KPI cards | `[Alerts]` 5,403, `[Fragrance Share %]`, `[Compulsory Rate %]`, `[Median Lag Days]`, `[Cross-border %]`, `[Counterfeit Alerts]` 17 |
| Surge chart | column chart, `dDate[Month]` × `[Alerts]`, each bar coloured by `[K02 Colour]` |
| Slicer | `dDate[Year]` |

**The one real gotcha, `K02 Colour` had to return hex, not words.** The measure returned "Red"/"Amber"/"Green", but field-value conditional formatting reads the string as a CSS colour, and **"Amber" is not a valid CSS colour** (only "Red" and "Green" are), so amber bars rendered black. Swapped the words for hex (`#C0392B` / `#E67E22` / `#27AE60`). The chart now paints each month by its surge ratio: red spikes at **Aug-2024 and Apr-2025** (the BMHCA ban-tail peak), green baseline. The page reads the state of the system in ten seconds, which is the whole point of an overview.

**Re-hit the measure-vs-column trap (Day 15) in card form:** the cards first came in as column charts, and converting one to the *new* Card visual hid the Display-units control, so "5403" showed as "5K". Fix was the classic Card → Callout value → Display units → None. Same lesson, new surface: pick the right visual *type* first, formatting second.

**Page 2, Substance Watch, and the insight the heatmap forced:**
The substance × year heatmap (matrix, `[Alerts]` with a gradient background) immediately showed its own limitation. **BMHCA's magnitude swamps the colour scale**, S01 hits 1,006 → 1,405 → 1,458 in 2023-25, so every other substance, including the emerging TPO (S05, 53 → 182), washes out to pale. That washout *is* the argument for K04: **absolute heat shows what's biggest; it cannot show what's accelerating**, because a substance exploding from 3 to 182 is still tiny next to BMHCA. You need both a "what's biggest" view (the heatmap) and a "what's accelerating" view (the normalised flag).

So I built the leaderboard. New measure:
```
K04 Months Flagged = SUMX ( VALUES ( dDate[Month Start] ), [K04 Emerging Flag] )
```
It counts, per substance, how many months it has ever tripped the emerging flag. Sorted descending, filtered > 0: **S01 (42) → S07 (29) → S11 (23) → S23 (23) → S08 (16) → S05/TPO (10)**. TPO sits firmly on the watchlist, which the absolute heatmap could never have surfaced. (Note for the README: this ranks all-time persistence; a last-12-months version would rank *current* emergence and push TPO to the top.)

**Drill-through, the step that makes it a tool:** an Alert Detail page listing `reference`, `publication_date`, `product_type`, `substance_naive`, `risk_description`, and `alert_url` (set to **Data category = Web URL** so it's a live clickable link to the official Safety Gate page). Dragging `dSubstance[substance_id]` into the page's Drill-through well makes it a target; right-click any substance → Drill through → land on just its alerts.

**Debug lesson, the "drill target shows everything" trap:** after it worked once, drilling "stopped working", the Alert Detail page showed the complete list. It wasn't broken: **a drill-through target shows all data by default and only filters when reached via the right-click drill, not when opened by clicking its tab.** The Filters pane confirms it (`substance_id is S01` appears only after a real drill). This is the Day-17 Jan-2023 trap wearing a new coat, a visual looking wrong because of filter context, not formula. In Power BI, "it shows the wrong rows" is almost always context, not code.

**Lesson:** assembly is where the earlier discipline pays back. Two polished, interactive pages in one sitting, with no new measures except one helper, because the model, the relationships, the date table and the KRIs were already built and validated. Front-load correctness and the dashboard is just plumbing.


## Day 19, Page 3, final polish, and the write-up

**What I built:** the last dashboard page (Markets & Enforcement), a final polish pass across all three pages, and the full write-up: README, backtest, reconciliation and limitations. I also cleaned the repository before publishing. That closes Upgrades B, C and D.

**Page 3, Markets & Enforcement:**
| Visual | Build | What it shows |
|---|---|---|
| Notifying country | bar, `dCountry[country_name]` × `[Alerts]`, Top 10 | who *files* alerts: Italy 3,055 (56.5%) |
| Origin country | same bar, `[Alerts by Origin]` | where products *come from*: Italy roughly half as many; France and Germany move up |
| Measure mix | bar, `fMeasures[measure_category]` × count | the enforcement hierarchy: ban on marketing far ahead, then withdrawal, recall, destruction |
| Lag distribution | column, `lag_days` binned at 5 days, filtered ≤ 30 | a steep spike at 0–5 days: authorities publish fast |

The origin chart is the first place the inactive relationship is visible on a page. The two country bars use the same fact table, and `USERELATIONSHIP` switches which country column it filters through. If the two charts had come out identical, the measure wouldn't be firing. They differ sharply, which is the enforcement-vs-origin point from Day 6, now on the page itself.

**Final polish:**
| Fix | Why |
|---|---|
| `%` measures formatted as Percentage (79.55% / 89.95% / 7.92%) | the cards showed 0.80 under a "%" label |
| Alert Detail page hidden | drill-through still works, but viewers don't land on a raw table |
| What-if sliders re-added as slicers | I had deleted the visuals. The parameters survived (the chart kept its RAG colours), so only the control needed restoring. They render as tiles, not a slider. That's fine: they work and show the selected threshold. |

**The write-up, structured like a consulting deliverable:** an executive summary with the answer first. The governing thought is that a ban date starts a two-to-three-year recall tail rather than ending the risk, followed by three supporting messages. Section headings state the takeaway rather than the topic. Screenshots are numbered exhibits with source lines. Each recommendation names the KRI that tracks it. Method, reconciliation, KRI definitions and limitations go in an appendix so they support the argument without cluttering it.

**Upgrade B, the K04 backtest:** across 2016–2026 the flag fires in **83 substance-months across 15 substances**. S01 BMHCA leads with 42, then S07 (29), S11 (23), S23 (23), and S05 TPO with 10. TPO first fired in Nov 2025, seven months before its June 2026 peak. The minimum-count guard of 5 keeps it from firing against near-zero baselines, so the flag is selective enough to act on.

**Upgrade D, limitations:** six caveats.
- Enforcement intensity is not the same as underlying risk.
- Keyword classification picks the first match.
- 12% of alerts have no origin and 82% have no sales channel.
- These are compliance breaches, not measured harm.
- The A12 → SR code change marks a change of legal basis, not severity.
- The lag tail makes the median the right statistic.

**Repository clean-up before publishing:**
| Issue | Fix |
|---|---|
| The starter workbook (template with answer-key check values) was in `excel/` | deleted. It isn't my work and shouldn't be public |
| Working file named `P1_Eshwar_Working.xlsx` | renamed `P1_SafetyGate_Analysis.xlsx` |
| Excel and Power BI data sources used **absolute paths** containing a private folder name | moved the project to a neutral folder and re-pointed the Excel `FilePath` parameter and every Power BI source. Re-validated `[Alerts]` = 5,403 after refresh |
| README listed files that weren't in the repo | repository tree rewritten to match the actual contents |

**Lesson:** publishing is a data-governance step, not a formality. An absolute file path is metadata. It travels inside the `.pbix` and the workbook, and anyone who opens Power Query can read it. Before a file goes public, check what it says about you as well as what it shows. In screening terms, sanitise the record before it leaves the building.
