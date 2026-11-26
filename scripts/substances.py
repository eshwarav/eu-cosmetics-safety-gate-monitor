import re
# (substance, group, fragrance_related, regulatory_note, regex)
DICT = [
 ("Butylphenyl methylpropional (BMHCA, lilial)","Fragrance ingredient - prohibited (CMR)","Y","Annex II since 1 Mar 2022, Reg. (EU) 2021/1902", r"butylphenyl ?methylpropional|tert-?butylbenzyl\)? ?(?:propionaldehyde|methylpropional)|\bbmhca\b|lilial"),
 ("Hydroxyisohexyl 3-cyclohexene carboxaldehyde (HICC, lyral)","Fragrance ingredient - prohibited","Y","Annex II, Reg. (EU) 2017/1410", r"hydroxyisohexyl ?3-?cyclohexene|\bhicc\b|lyral"),
 ("Atranol / chloroatranol","Fragrance ingredient - prohibited","Y","Annex II, Reg. (EU) 2017/1410", r"\batranol|chloroatranol"),
 ("Labelled fragrance allergen (undeclared or excess)","Fragrance allergen - labelling","Y","Annex III labelling (Reg. (EU) 2023/1545 extends the list)", r"limonene|linalool|geraniol|citronellol|hexyl ?cinnamal|benzyl (?:alcohol|salicylate|benzoate|cinnamate)|coumarin|eugenol|citral\b|cinnamal|cinnamyl alcohol|hydroxycitronellal|amyl ?cinnam|farnesol|anise alcohol|methyl 2-octynoate|alpha-isomethyl ionone|evernia|oak ?moss|tree ?moss|allergenic fragrance"),
 ("TPO (trimethylbenzoyl diphenylphosphine oxide)","Nail product chemical - prohibited (CMR)","N","Annex II since 1 Sep 2025, Reg. (EU) 2025/877", r"diphenyl ?\(2|trimethylbenzoyl ?diphenyl|\btpo\b"),
 ("Other nail acrylates (TMPTA, HEMA, etc.)","Nail product chemical","N","Check the CosIng entry", r"trimethylolpropane triacrylate|tmpta|hydroxyethyl methacrylate|\bhema\b|di-hema|methacrylate|acrylate"),
 ("Hydroquinone","Skin-lightening agent - prohibited","N","Annex II (except professional artificial-nail systems)", r"hydroquinone"),
 ("Mercury","Heavy metal - prohibited","N","Annex II", r"mercury"),
 ("Clobetasol propionate / corticosteroids","Medicinal active - prohibited","N","Annex II (corticosteroids)", r"clobetasol|betamethasone|corticosteroid|dexamethasone"),
 ("Kojic acid","Skin-lightening agent - restricted","N","Check the CosIng entry", r"kojic"),
 ("Methylisothiazolinone (MI)","Preservative - restricted","N","Banned in leave-on, Reg. (EU) 2016/1198", r"methylisothiazolinone(?! and)|\bmi\)"),
 ("MCI/MI mixture","Preservative - restricted","N","Rinse-off only, Reg. (EU) No 1003/2014", r"methylchloroisothiazolinone|\bmci\b"),
 ("Formaldehyde / releasers","Preservative - restricted","N","Check the CosIng entry", r"formaldehyde|dmdm hydantoin"),
 ("Parabens (prohibited types)","Preservative - prohibited","N","Annex II, Reg. (EU) No 358/2014", r"isobutylparaben|isopropylparaben|phenylparaben|benzylparaben|pentylparaben|propylparaben|butylparaben"),
 ("p-Phenylenediamine and hair-dye amines","Hair dye - restricted","N","Annex III (hair dye entries)", r"phenylenediamine|\bppd\b|aminophenol|toluene-2,5-diamine|resorcinol|amino-m-cresol"),
 ("PFAS (perfluorononyl dimethicone, PFOA, PFNA)","PFAS / persistent organic pollutant","N","Reg. (EU) 2019/1021 (POPs)", r"perfluoro|pfoa|pfna|pfas|polyfluoro"),
 ("Cyclosiloxanes (D4, D5, D6)","Siloxane - restricted","N","REACH Annex XVII", r"cyclotetrasiloxane|cyclopentasiloxane|cyclohexasiloxane|\bd4\b|\bd5\b"),
 ("Phthalates","Phthalate - prohibited","N","Annex II", r"phthalate"),
 ("Lead","Heavy metal - prohibited","N","Annex II", r"\blead\b(?! to\b)(?! the\b)(?!ing)"),
 ("Other heavy metals (antimony, arsenic, cadmium, nickel, barium, chromium)","Heavy metal - prohibited","N","Annex II", r"antimony|arsenic|cadmium|nickel|barium|chromium"),
 ("Prostaglandin analogues (eyelash serums)","Medicinal active - prohibited","N","Medicinal substance; not a cosmetic ingredient", r"prostaglandin|bimatoprost|cloprostenol|latanoprost|travoprost|dechloro"),
 ("Peroxides and borates","Bleaching / boron compound","N","Annex III limits or Annex II (borates)", r"hydrogen peroxide|perborate|tetraborate|boric acid|\bborate|barium peroxide|carbamide peroxide"),
 ("Microbial contamination","Microbiological","N","Art. 3 safety; GMP", r"bacteri|micro-?organism|mould|yeast|pseudomonas|microbial|fungi|burkholderia|klebsiella|enterobacter|staphylococcus"),
 ("Asbestos","Contaminant - prohibited","N","Annex II", r"asbestos"),
 ("Benzophenone and UV filters","UV filter / photoinitiator","N","Check the CosIng entry", r"benzophenone|octocrylene|homosalate"),
 ("Salicylic acid (excess)","Restricted ingredient","N","Annex III/V limits", r"salicylic acid"),
 ("Prohibited colourants","Colourant - prohibited","N","Annex IV / Annex II", r"\bci \d{5}|solvent (?:yellow|red|orange)|sudan|rhodamine|colourant|colorant|dye(?:stuff)? not"),
 ("Sun protection claim not met (SPF/UVA)","Claim / labelling - sun protection","N","Art. 20 claims; Recommendation 2006/647/EC", r"protection factor|\bspf\b|uva protection|uv-?filter and do|announced level|level of protection|protection level"),
 ("Nitrosamines","Contaminant - prohibited","N","Annex II", r"nitroso"),
 ("Lawsone and henna-type colourants","Hair dye - restricted","N","Annex III (hair dye entries)", r"naphthoquinone|lawsone"),
 ("Aniline","Contaminant - prohibited","N","Annex II", r"\baniline"),
 ("Food imitation (look-alike product)","Product presentation risk","N","Directive 87/357/EEC (food-imitating products)", r"mistaken (?:with|for) (?:food|foodstuff)|characteristic appearance|appearance, (?:form|colour|color)|resembl\w* food"),
 ("Labelling, documentation or GMP failure","Labelling / documentation","N","Arts 8, 11, 19 (GMP, PIF, labelling)", r"label of the product does not|not labelled|no documentation|product information file|not manufactured according|good manufacturing|responsible person|safety (?:assessment|report)|lack of labelling|missing label|warnings? (?:are|is) missing"),
 ("Cannabinoids (THC, CBD)","Narcotic / medicinal - prohibited","N","Annex II", r"tetrahydrocannabinol|\bthc\b|cannabidiol|\bcbd\b"),
]
COMPILED = [(s,g,f,n,re.compile(p)) for s,g,f,n,p in DICT]

def norm(t):
    t = (t or "").lower()
    t = re.sub(r"-\s+", "-", t)
    return t

def match(text):
    t = norm(text)
    out = []
    for s,g,f,n,rx in COMPILED:
        m = rx.search(t)
        if m: out.append((m.start(), s, g, f, n))
    out.sort()
    return out
