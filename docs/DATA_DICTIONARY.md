# Data dictionary

All files are UTF-8 with BOM (Excel opens them correctly). Dates are ISO `YYYY-MM-DD`.

## safety_gate_cosmetics_alerts.csv (one row per alert)

| Column | Type | Notes |
| --- | --- | --- |
| alert_id | integer | Safety Gate internal id. Primary key |
| reference | text | Official alert number, e.g. `SR/01038/25` |
| notification_type | text | `A12` = serious-risk notification (portal key: Art. 12 GPSD / Art. 22 Reg. 765/2008), `A11` = non-serious risk, `INFO` = for information |
| notifying_country, notifying_country_code | text | Authority that notified. `XI` = UK in respect of Northern Ireland |
| creation_date | date | When the notification was created in the system |
| publication_date | date | When it was published on the public portal. Use this for monthly KRIs |
| web_report, web_report_date | text, date | Weekly report the alert appeared in |
| product_category | text | Always `COSMETICS` here |
| product_type | text | Generic product type as written by the authority. 542 distinct, messy values |
| product_name | text | Specific product name, often blank |
| brand | text | Brand(s), separated by ` \| ` |
| counterfeit | text | YES / NO / UNKNOWN |
| professional_product | boolean | Professional-use product |
| product_description | text | Free text |
| country_of_origin, origin_code | text | `XX` = Unknown |
| sold_online | text | YES / NO / UNKNOWN |
| barcode | text | First barcode listed. Keep as text, since leading zeros matter |
| risk_types | text | One or more of CHEMICAL, MICROBIOLOGICAL, ... separated by `\|` |
| risk_description | text | What was found. Source for substance classification |
| legal_provision | text | Legal basis cited (inconsistent wording, a cleaning exercise) |
| measures_count, measures_compulsory, measures_voluntary | integer | Counts from the measures table |
| recall_published_online | text | YES / NO / UNKNOWN |
| company_recall_link | text | First recall URL if any |
| reacting_countries_count, reacting_countries | integer, text | Other countries that found the same product |
| alert_url | text | Link to the official alert page. Use it as a drill-through web URL |

## safety_gate_cosmetics_measures.csv (one row per measure)

| Column | Notes |
| --- | --- |
| alert_id | Foreign key to alerts |
| reference | Alert number |
| measure_category | BAN_MARKETING_OF_PRODUCT, PRODUCT_WITHDRAWAL_FROM_MARKET, PRODUCT_RECALL_FROM_CONSUMERS, DESTRUCTION_OF_PRODUCT, STOP_OF_SALES, IMPORT_REJECTED_AT_BORDER, ... |
| measure_type | COMPULSORY / VOLUNTARY |
| taken_by | Economic operator or authority type, when given |
| entry_into_force_date | Often blank |

## Reference and processed tables

- **substance_dictionary.csv**: `substance_id` (S01–S34, S99 = other), substance, group, `fragrance_related` (Y/N), regulatory note, regex used by the script.
- **substance_keywords_excel.csv**: keyword → substance_id, with `priority` = the substance number. The table is in naive id order on purpose: a first-match lookup will tag MCI/MI mixtures as MI (S11). Re-order it so specific keywords come first, then re-run.
- **product_family_rules.csv**: priority, family, regex. The first match wins.
- **country_dim.csv**: country_code, country_name, is_eu27, region.
- **alert_substance.csv**: alert_id, substance_id, match_rank (1 = first substance named in the text).
- **alert_classified.csv**: alert_id, product_family, primary_substance_id, substances_found, fragrance_related, notification_lag_days, has_compulsory_measure, has_recall_or_withdrawal.

## Known data traps (they are deliberate learning points)

1. "lead" in "may **lead** to" is not the metal. The script excludes it; a naive SEARCH("lead") does not.
2. "methylchloroisothiazolinone and methylisothiazolinone" contains the MI keyword. Check the MCI/MI mixture first.
3. "Skin lightening" and "Skin-lightening" are the same product type.
4. One alert can name several substances. Count alerts with DISTINCTCOUNT, not rows of the bridge table.
5. Search filters on the portal overlap years, so 75 alerts appear under two years. The extract is de-duplicated on alert_id.
