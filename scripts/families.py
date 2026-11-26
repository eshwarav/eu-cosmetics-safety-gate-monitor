import re
# priority order matters: first match wins
RULES = [
 ("Oral care", r"tooth|teeth|mouth ?wash|dental"),
 ("Skin lightening", r"lighten|whiten|bleaching cream|brightening"),
 ("Nail", r"nail|manicure|acrylic powder|gel polish"),
 ("Hair colouring", r"hair ?dye|hair colou?r|colou?ring|henna|tint|bleach"),
 ("Fragrance (incl. body sprays)", r"perfum|parfum|toilette|cologne|after ?shave|body mist|body spray|scented body|fragrance|eau de"),
 ("Deodorant", r"deodorant|antiperspirant|roll-on"),
 ("Sun care", r"\bsun|spf|tanning|bronz"),
 ("Shaving", r"shav"),
 ("Make-up", r"mascara|eye ?liner|lip|foundation|eyeshadow|eye shadow|make-?up(?! remover)|face paint|blush|concealer|kohl|kajal|eyebrow|highlighter|glitter|body paint|lash"),
 ("Hair care", r"hair|shampoo|conditioner|scalp|beard"),
 ("Bath & shower", r"shower|bath|soap|wash|foam"),
 ("Wipes", r"wipe"),
 ("Skin care", r"cream|lotion|serum|milk|oil|mask|toner|tonic|balm|butter|gel|scrub|moistur|cleans|skin|face|body|ointment|remover|powder|peel"),
 ("Sets & kits", r"\bset\b|\bkit\b|gift"),
]
COMPILED = [(f, re.compile(p)) for f, p in RULES]
def family(t):
    t = (t or "").lower()
    for f, rx in COMPILED:
        if rx.search(t): return f
    return "Other"
