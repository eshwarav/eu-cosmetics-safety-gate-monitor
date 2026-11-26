"""
Refresh the EU Safety Gate cosmetics alert extract.

Source : European Commission, Safety Gate - the EU rapid alert system for
         dangerous non-food products. https://ec.europa.eu/safety-gate-alerts/
         Public data; reuse allowed with attribution (Commission Decision
         2011/833/EU on the reuse of Commission documents).
Method : the same public JSON endpoints the portal's own search page calls.
           POST public/api/search            -> alert ids per year
           GET  public/api/notification/{id} -> full alert record
Output : data/raw/safety_gate_cosmetics_alerts.csv
         data/raw/safety_gate_cosmetics_measures.csv

Usage  : python scripts/fetch_safety_gate.py --years 2017-2026
Needs  : pip install requests
Be kind to the server: the default is 4 parallel requests with retries.
"""
import argparse
import csv
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import requests

BASE = "https://ec.europa.eu/safety-gate-alerts/"
SESSION = requests.Session()
SESSION.headers.update({"Content-Type": "application/json",
                        "User-Agent": "portfolio-research-script"})


def search(year, page, size=200):
    body = {
        "criteria": {"fullTextSearch": "", "productCategoryType": ["COSMETICS"], "year": [year]},
        "searchCriteriaForNotification": False, "isLaunched": True,
        "pagination": {"sortField": "PUBLICATION_DATE", "sortOrder": "DESC",
                       "totalElements": 0, "numberElements": size, "page": page},
        "searchResults": [], "displayDefaultResults": False,
        "displayTagsWithSelectedCriteria": [], "isForMostRecent": False,
        "isLaunchSearch": True, "fullTextSearch": "", "language": "en",
    }
    r = SESSION.post(BASE + "public/api/search", json=body, timeout=60)
    r.raise_for_status()
    return r.json()


def detail(alert_id):
    for attempt in range(3):
        try:
            r = SESSION.get(f"{BASE}public/api/notification/{alert_id}",
                            params={"language": "en"}, timeout=60)
            r.raise_for_status()
            return r.json()
        except requests.RequestException:
            time.sleep(2 * (attempt + 1))
    return None


def en(versions):
    versions = versions or []
    for v in versions:
        if (v.get("language") or {}).get("key") == "EN":
            return v
    return versions[0] if versions else {}


def clean(s):
    return " ".join(str(s).split()) if s is not None else ""


def name(obj):
    return (obj or {}).get("name") or ""


def flatten(d):
    p, r = d.get("product") or {}, d.get("risk") or {}
    mt, t, wr = d.get("measureTaken") or {}, d.get("traceability") or {}, d.get("webReport") or {}
    pv, rv = en(p.get("versions")), en(r.get("versions"))
    ms = mt.get("measures") or []
    recalls = mt.get("companyRecalls") or []
    barcodes = p.get("barcodes") or []
    reacting = d.get("reactingCountries") or []
    alert = {
        "alert_id": d["id"], "reference": d.get("reference"),
        "notification_type": (d.get("notificationType") or {}).get("code"),
        "notifying_country": name(d.get("country")),
        "notifying_country_code": (d.get("country") or {}).get("key"),
        "creation_date": (d.get("creationDate") or "")[:10],
        "publication_date": (d.get("publicationDate") or "")[:10],
        "web_report": wr.get("code"), "web_report_date": (wr.get("publicationDate") or "")[:10],
        "product_category": name(p.get("productCategory")),
        "product_type": clean(pv.get("name") or p.get("name")),
        "product_name": clean(p.get("nameSpecific")),
        "brand": clean(" | ".join(b.get("brand", "") for b in p.get("brands") or [])),
        "counterfeit": name(p.get("isCounterfeit")),
        "professional_product": p.get("professionalProduct"),
        "product_description": clean(pv.get("description")),
        "country_of_origin": name(t.get("countryOrigin")),
        "origin_code": (t.get("countryOrigin") or {}).get("key"),
        "sold_online": name(t.get("isSoldOnline")),
        "barcode": clean(barcodes[0].get("barcode")) if barcodes else "",
        "risk_types": "|".join(x.get("name", "") for x in r.get("riskType") or []),
        "risk_description": clean(rv.get("riskDescription")),
        "legal_provision": clean(rv.get("legalProvision")),
        "measures_count": len(ms),
        "measures_compulsory": sum(name(m.get("measureType")) == "COMPULSORY" for m in ms),
        "measures_voluntary": sum(name(m.get("measureType")) == "VOLUNTARY" for m in ms),
        "recall_published_online": name(mt.get("hasPublishedRecallOnline")),
        "company_recall_link": clean(recalls[0].get("link")) if recalls else "",
        "reacting_countries_count": len(reacting),
        "reacting_countries": "|".join((x.get("country") or {}).get("key", "") for x in reacting),
        "alert_url": f"{BASE}screen/webReport/alertDetail/{d['id']}?lang=en",
    }
    measures = []
    for m in ms:
        by = (m.get("measureVoluntaryEconomicOperator") or m.get("measureCompulsoryEconomicOperator")
              or m.get("measureVoluntaryAuthority") or m.get("measureCompulsoryAuthority"))
        measures.append({
            "alert_id": d["id"], "reference": d.get("reference"),
            "measure_category": name(m.get("measureCategory")),
            "measure_type": name(m.get("measureType")),
            "taken_by": name(by),
            "entry_into_force_date": (m.get("entryIntoForceDate") or "")[:10],
        })
    return alert, measures


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--years", default="2017-2026")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out", default="data/raw")
    a = ap.parse_args()
    y0, y1 = map(int, a.years.split("-"))

    ids = set()
    for year in range(y1, y0 - 1, -1):
        total = search(year, 0, 1)["totalElements"]
        for page in range((total + 199) // 200):
            ids.update(c["id"] for c in search(year, page)["content"])
        print(f"{year}: {total} alerts listed, {len(ids)} unique ids so far")

    with ThreadPoolExecutor(a.workers) as ex:
        records = [d for d in ex.map(detail, sorted(ids)) if d]
    print(f"details fetched: {len(records)} of {len(ids)}")

    alerts, measures = [], []
    for d in records:
        al, me = flatten(d)
        alerts.append(al)
        measures.extend(me)
    alerts.sort(key=lambda r: r["publication_date"], reverse=True)
    out = Path(a.out)
    write_csv(out / "safety_gate_cosmetics_alerts.csv", alerts)
    write_csv(out / "safety_gate_cosmetics_measures.csv", measures)
    print(f"wrote {len(alerts)} alerts and {len(measures)} measures to {out}")


if __name__ == "__main__":
    main()
