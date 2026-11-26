"""
Classify each Safety Gate cosmetics alert by substance and product family.

Reads : data/raw/safety_gate_cosmetics_alerts.csv, data/raw/safety_gate_cosmetics_measures.csv
Writes: data/processed/alert_substance.csv   (bridge: one row per alert x substance)
        data/processed/alert_classified.csv  (one row per alert, derived fields)
        data/reference/substance_dictionary.csv, data/reference/product_family_rules.csv

This is the REFERENCE ANSWER. Build your own version in Power Query first
(Days 3-6 of the plan), then compare your counts with this output.
Usage : python scripts/classify_alerts.py
"""
import re
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).parent))
import families as F  # noqa: E402
import substances as S  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RAW, REF, OUT = ROOT / "data/raw", ROOT / "data/reference", ROOT / "data/processed"


def sid(name):
    return "S" + str([d[0] for d in S.DICT].index(name) + 1).zfill(2)


def main():
    a = pd.read_csv(RAW / "safety_gate_cosmetics_alerts.csv", encoding="utf-8-sig", keep_default_na=False)
    m = pd.read_csv(RAW / "safety_gate_cosmetics_measures.csv", encoding="utf-8-sig", keep_default_na=False)
    REF.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    sd = pd.DataFrame([{"substance_id": sid(s), "substance": s, "substance_group": g,
                        "fragrance_related": f, "regulatory_note": n, "regex": p}
                       for s, g, f, n, p in S.DICT])
    sd = pd.concat([sd, pd.DataFrame([{"substance_id": "S99", "substance": "Other / unclassified",
                                       "substance_group": "Other / unclassified", "fragrance_related": "N",
                                       "regulatory_note": "", "regex": ""}])])
    sd.to_csv(REF / "substance_dictionary.csv", index=False, encoding="utf-8-sig")
    pd.DataFrame([{"priority": i + 1, "product_family": f, "regex": p} for i, (f, p) in enumerate(F.RULES)]) \
        .to_csv(REF / "product_family_rules.csv", index=False, encoding="utf-8-sig")

    bridge, rows = [], []
    for r in a.itertuples(index=False):
        hits = S.match(r.risk_description + " " + r.legal_provision)
        for rank, (_, s, g, f, n) in enumerate(hits, 1):
            bridge.append({"alert_id": r.alert_id, "substance_id": sid(s), "match_rank": rank})
        if not hits:
            bridge.append({"alert_id": r.alert_id, "substance_id": "S99", "match_rank": 1})
        rows.append({
            "alert_id": r.alert_id,
            "product_family": F.family(r.product_type),
            "primary_substance_id": sid(hits[0][1]) if hits else "S99",
            "substances_found": len(hits),
            "fragrance_related": "Y" if any(h[3] == "Y" for h in hits) else "N",
        })
    b = pd.DataFrame(bridge)
    b.to_csv(OUT / "alert_substance.csv", index=False, encoding="utf-8-sig")

    c = pd.DataFrame(rows)
    pub = pd.to_datetime(a.publication_date)
    cre = pd.to_datetime(a.creation_date)
    c["notification_lag_days"] = (pub - cre).dt.days.values
    comp = m[m.measure_type == "COMPULSORY"].alert_id.unique()
    rw = m[m.measure_category.isin(["PRODUCT_RECALL_FROM_CONSUMERS", "PRODUCT_WITHDRAWAL_FROM_MARKET"])].alert_id.unique()
    c["has_compulsory_measure"] = c.alert_id.isin(comp).map({True: "Y", False: "N"})
    c["has_recall_or_withdrawal"] = c.alert_id.isin(rw).map({True: "Y", False: "N"})
    c.to_csv(OUT / "alert_classified.csv", index=False, encoding="utf-8-sig")
    print(f"{len(c)} alerts classified; {len(b)} alert-substance rows; "
          f"coverage {(c.substances_found > 0).mean():.1%}")


if __name__ == "__main__":
    main()
