from alifTools.sample import (
    make_lines,
    TextRun,
    Font,
    parseFeatures,
    Features,
    Location,
    draw_lines,
)
import uharfbuzz as hb
import sys

FONTS = {50: Font(sys.argv[1])}
FONTS[50].size = 50

dark_palette_index = None
for i, palette in enumerate(FONTS[50].hbFont.face.color_palettes):
    if palette.flags & hb.OTColorPaletteFlags.USABLE_WITH_DARK_BACKGROUND:
        dark_palette_index = i
        break


def r(
    string: str,
    location: Location | None = None,
    features: str | None = None,
    font_size: int = 50,
    eot: bool = False,
):
    if features is not None:
        features: Features = parseFeatures(features)

    if location is None:
        location = dict()

    if font_size not in FONTS:
        font = FONTS[50].subfont()
        font.size = font_size
        FONTS[font_size] = font

    return TextRun(
        font=FONTS[font_size],
        string=string,
        features=features,
        location=location,
        eot=eot,
    )


samples = {
    "spacing-0": [
        [r("بسم الله الرحمن الرحيم")],
    ],
    "spacing-1": [
        [r("بسم الله الرحمن الرحيم", {"SPAC": -100})],
    ],
    "spacing-2": [
        [r("قُل هوَ ا للهُ أ حد", {"MSHQ": 37}), r("۝١"), r("ا", {"MSHQ": 37})],
        [r("للهُ ا لصمد", {"MSHQ": 48}), r("۝٢"), r("لَم", {"MSHQ": 48})],
        [r("يلد وَ لـم يُو", {"MSHQ": 53})],
        [r("لد", {"MSHQ": 46}), r("۝٣"), r("وَ لَم يكن لهُ", {"MSHQ": 46})],
        [r("كفو اً أحد", {"MSHQ": 43}), r("۝٤", eot=True)],
    ],
    "mashq-0": [
        [r("د "), r("د", {"MSHQ": 100}), r(" د", {"MSHQ": 0})],
        [r("ط "), r("ط", {"MSHQ": 100}), r(" ط", {"MSHQ": 0})],
        [r("ك "), r("ك", {"MSHQ": 100}), r(" ك", {"MSHQ": 0})],
        [r("ص "), r("ص", {"MSHQ": 100}), r(" ص", {"MSHQ": 0})],
        [r("ٮ "), r("ٮ", {"MSHQ": 100}), r(" ٮ", {"MSHQ": 0})],
        [r("ڡ "), r("ڡ", {"MSHQ": 100}), r(" ڡ", {"MSHQ": 0})],
    ],
    "mashq-1": [
        [r("ع "), r("ع", {"MSHQ": 100})],
        [r("ح "), r("ح", {"MSHQ": 100})],
    ],
    "mashq-2": [
        [r("ا "), r("ا", {"MSHQ": 100})],
    ],
    "mashq-3": [
        [r("سا يِلون", {}, "ss01")],
        [r("سايـِلون", {"MSHQ": 100}, "ss01")],
    ],
    "dots-0": [[r("◌َ ◌ً ◌ِ ◌ٍ ◌ُ ◌ٌ")]],
    "dots-1": [[r("طَ كَ لَ لَا")]],
    "dots-2": [[r("اَ اً")]],
    "dots-3": [[r("لِ ںِ ىِ لٍ ںٍ ىٍ", features="salt")]],
    "dots-4": [
        [r("قل ا عو ذ بر ب ا", {"MSHQ": 25})],
        [
            r("لفـلق", {"MSHQ": 22}),
            r("۝١"),
            r("من شر ما خلـق", {"MSHQ": 22}),
            r("۝٢"),
            r("و من", {"MSHQ": 22}),
        ],
        [r("شر غا سق ا ذ ا و قب", {"MSHQ": 13}), r("۝٣", eot=True)],
        [r("و من شر ا لنفا ثا ت في ا", {"MSHQ": 20})],
        [r("لعقد", {"MSHQ": 27}), r("۝٤"), r("و من شر حا سد", {"MSHQ": 27})],
        [r("ا ذ ا حسد", {"MSHQ": 47}), r("۝٥", eot=True)],
    ],
    "dots-5": [
        [r("قل ا عو ذ بر ب ا", {"MSHQ": 25}, "ss01")],
        [
            r("لفـلق", {"MSHQ": 22}, "ss01"),
            r("۝١"),
            r("من شر ما خلـق", {"MSHQ": 22}, "ss01"),
            r("۝٢"),
            r("و من", {"MSHQ": 22}, "ss01"),
        ],
        [r("شر غا سق ا ذ ا و قب", {"MSHQ": 13}, "ss01"), r("۝٣", eot=True)],
        [r("و من شر ا لنفا ثا ت في ا", {"MSHQ": 20}, "ss01")],
        [r("لعقد", {"MSHQ": 27}, "ss01"), r("۝٤"), r("و من شر حا سد", {"MSHQ": 27}, "ss01")],
        [r("ا ذ ا حسد", {"MSHQ": 47}, "ss01"), r("۝٥", eot=True)],
    ],
    "hamza-0": [[r("أ إ آ ؤ")]],
    "lam-alef-0": [[r("لأ لَا لإ لِأ لأُ")]],
    "ayah-0": [[r("۝١", font_size=100)]],
    "ayah-1": [[r("۝٥", font_size=100)]],
    "ayah-2": [
        [
            r("۝١٠", font_size=100),
            r(" "),
            r("۝٢٠", font_size=100),
            r(" "),
            r("۝٣٠", font_size=100),
        ]
    ],
    "ayah-3": [[r("۝٥", features="salt", font_size=100)]],
    "contextual-0": [[r("تثبتها ؞ سبها ؞ سن ؞ ينتن ؞ متثبتتان", features="ss01")]],
    "contextual-1": [[r("لله ؞ علل ؞ ظل ؞ ظاهر")]],
    "cursive-0": [
        [r("الحج ؞ "), r("المتـلجـلج ؞", {"MSHQ": 34})],
        [r("يضحكون", {"MSHQ": 69})],
    ],
    "yeh-0": [[r("سيء ؞ سِيء ؞ علي ؞ علِي ؞ حتى ؞ حبى")]],
    "yeh-1": [[r("ي ؞ لي ؞ في ؞ حي", features="salt")]],
    "yeh-2": [
        [r("أي ؞ على ؞ بني ؞", {}, "salt=2")],
        [r("إلي", {"MSHQ": 100}, "salt=2")],
    ],
    "yeh-3": [
        [r("أے ؞ علے ؞ بنے ؞")],
        [r("إلے", {"MSHQ": 100})],
    ],
    "meem-0": [[r("من ؞ مما ؞ علما")]],
    "contextual-2": [
        [r("ڡا ڡٮ ڡح ڡد ڡه ڡو ڡر")],
        [r("ڡط ڡی ڡك ڡل ڡم ڡں ڡس ڡع")],
        [r("ڡڡ ڡص ڡٯ ڡں")],
    ],
    "contextual-3": [
        [r("حا حٮ حح حد حه حو")],
        [r("حر حط حی حك حل حم")],
        [r("حں حس حع حڡ حص حق")],
    ],
    "contextual-4": [[r("علما ؞ بد ؞ سببا ؞ منها ؞ للسمع")]],
}

foreground = "000000"
background = "FFFAED"
dark_foreground = "D3D3D3"
dark_background = "000000"

margin = 2

for filename, text_lines in samples.items():
    text_lines = reversed([reversed(line) for line in text_lines])
    lines, _ = make_lines(
        text_lines,
        justify=False,
        x=0,
        y=0,
    )

    if dark_palette_index is not None:
        tree = draw_lines(
            lines=lines,
            foreground=foreground,
            background=background,
            dark_foreground=None,
            dark_background=None,
            margin=margin,
        )
        tree.write(f"{filename}.svg", pretty_print=True, xml_declaration=True)

        tree = draw_lines(
            lines=lines,
            foreground=dark_foreground,
            background=dark_background,
            dark_foreground=None,
            dark_background=None,
            margin=margin,
            palette=dark_palette_index,
        )
        tree.write(f"{filename}_dark.svg", pretty_print=True, xml_declaration=True)
    else:
        tree = draw_lines(
            lines=lines,
            foreground=foreground,
            background=background,
            dark_foreground=dark_foreground,
            dark_background=dark_background,
            margin=margin,
        )
        tree.write(f"{filename}.svg", pretty_print=True, xml_declaration=True)
