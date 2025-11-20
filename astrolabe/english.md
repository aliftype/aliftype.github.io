---
title: Astrolabe
subtitle: A Kufic typeface inspired by old sciences
layout: font
language: en-US
direction: ltr
---

_Astrolabe_ is a [Kufic](https://en.wikipedia.org/wiki/Kufic) typeface inspired by Arabic inscription on old scientific instruments like [Astrolabes](https://en.wikipedia.org/wiki/Astrolabe) and [Quadrants](https://en.wikipedia.org/wiki/Quadrant_(instrument)). The main source of inspiration is quadrants made by [Shams al‐Din al-Mizzī](https://islamsci.mcgill.ca/RASI/BEA/Mizzi_BEA.htm) (690–750 AH / 1291–1349 CE), like the one in Cairo Museum of Islamic Art, and [another one](https://www.britishmuseum.org/collection/object/W_1888-1201-276) in The The British Museum.

_Astrolabe_ is a free, open-source project, and anyone is welcome to use and modify it under the terms of version 3 of [GNU Affero General Public License](https://www.gnu.org/licenses/agpl-3.0.en.html).

![](/assets/images/astrolabe/astrolabe-01.svg)

## Character set
_Astrolabe_ supports Arabic languages, with Arabic digits and punctuation designed to match the spirit of _Astrolabe_ letters.
![](/assets/images/astrolabe/astrolabe-03.svg)

### Contextual alternates
_Astrolabe_ contains contextual alternates that are enabled automatically, like high middle _beh_ tooth in sequences of three or more _beh_-like letters, or wider variants of some letters to avoid dot clash, or shallower versions of letters with descenders where necessary:
![](/assets/images/astrolabe/astrolabe-07.svg)

### Stylistic sets
It also includes an number of stylistic sets that can be enabled manually for richer designs:
![](/assets/images/astrolabe/astrolabe-08.svg)

`ss01` — Dot-less Letter Forms
: Losses the dots of dotted letters like _beh_, _teh_, etc.

`ss02` — Alternate isolated/final “hah”
: Alternate isolated and final _hah_-like letters (_hah_, _khah_, _jeem_) with straight ending and no descender. This resembles the form of _jeem_ used in scientific and mathematical contexts.

`ss03` — Alternate medial/final “ain”
: Alternate medial and final _ain_ and _ghain_ with a rounded instead of flaring ending.

`ss04` — Alternate medial/final “feh”
: Alternate, circular, medial _feh_ and _qaf_, and final _feh_.

`ss05` — Alternate isolated/final “lam”
: Alternate isolated and final _lam_ without a descender.

`ss06` — Alternate isolated/final “meem”
: Alternate, longer, isolated and final _meem_.

`ss07` — Alternate isolated “yeh”
: Alternate, returning, isolated _yeh_.

### Tabular figures
_Astrolabe_ supports also tabular figures feature (`tnum`) for uses where fixed width digits are more appropriate, like tables:
![](/assets/images/astrolabe/astrolabe-09.svg)

## Elongation
_Astrolabe_ is a variable font with an elongation axis, _Mashq_ (`MSHQ`), to elongate letters that can be elongated in Kufic, which are _dal_, _tah_, _kaf_, and _sad_, as well as _beh_, and _feh_ (only in their initial and medial positions). These letters can expand or shrink as needed. This can be used to justify text without expanding the space between words.

In this example, there is a comparison between justifying text with spaces without elongation, as well as using elongation, with several variations in the use of elongations in attempt to achieve more balanced paragraph color:
![](/assets/images/astrolabe/astrolabe-04.svg)

The places of elongation is highlighted below, the the _Mashq_ axis values of each line next to it:
![](/assets/images/astrolabe/astrolabe-05.svg)

This is another example of use of elongation to balance the text:
![](/assets/images/astrolabe/astrolabe-02.svg)