---
title: Qashib
subtitle: A Kufic typeface in fresh garb
language: en-US
direction: ltr
---

Manuscript [Kufic] is a magnificent Arabic calligraphy style of epic proportions, lending any text written in it a sense of heritage and authority. However, some of its letter forms are so archaic that they are undecipherable to the untrained modern reader, which makes it unsuitable for use in modern contexts. _Qashib_ is an attempt to reimagine manuscript Kufic by replacing its most unfamiliar letter forms with alternatives that are closer to contemporary Arabic letter forms, while maintaining its distinctive spirit.

_Qashib_ means new or fresh (like in new garb), but it also means sharp-edged (like in a sharp sword), which is a nod to its fresh take on manuscript Kufic, as well as its sharp and clean-cut appearance.

_Qashib_ is a free, open-source project, and anyone is welcome to use and modify it under the terms of version 3 of the [GNU Affero General Public License].

![](/assets/images/qashib/qashib-01.svg)


## Character set
_Qashib_ supports Arabic and several extended Arabic-script languages, with Arabic digits and punctuation designed to match the spirit of _Qashib_ letters.

![Character set](/assets/images/qashib/qashib-08.svg "Character set")

### Letterforms
Some manuscript Kufic letterforms are difficult to read for those unfamiliar with them, because they can be confused with other letters in the styles of Arabic commonly used today. The following letters are, in my opinion, the hardest to read, so I have chosen alternate shapes for them in _Qashib_.

#### _Hah_
The isolated and final _hah_ in manuscript Kufic looks like a _hah_ with a returning _yeh_ attached to it. In _Qashib_ it is replaced with another form of _hah_ from the manuscript Kufic that was codified by the late Egyptian master of Arabic calligraphy _Mohammad Abdul Qadir_.

![Traditional and alternate forms of hah](/assets/images/qashib/qashib-02.svg "Traditional and alternate forms of hah")

#### _Ain_
The _ain_ in manuscript Kufic resembles the _hah_ in its isolated and initial forms. Also, in isolated position, it appears, similar to _hah_, as if a returning _yeh_ has been attached to it. In medial and final positions, its head takes an unfamiliar shape. In _Qashib_, the head of the isolated and initial _ain_ is replaced with a more familiar form seen in some Kufic Qur’ans, while the medial and final heads are borrowed from Qayrawani Kufic.

![Traditional and alternate forms of ain](/assets/images/qashib/qashib-03.svg "Traditional and alternate forms of ain")

#### _Kaf_
The _kaf_ in manuscript Kufic is written like _dal_ in its initial and medial positions (given that _dal_ never takes an initial or medial forms). In its isolated and final positions it differs from _dal_, but remains unfamiliar. In _Qashib_, _kaf_ takes a clearer, distinct form in all four positions, inspired by the _kaf_ of Qayrawani Kufic.

![Traditional and alternate forms of kaf](/assets/images/qashib/qashib-04.svg "Traditional and alternate forms of kaf")

#### _Qaf_
The isolated and final _qaf_ in manuscript Kufic appears as if a _yeh_ is attached to a _qaf_ head. In _Qashib_ it is replaced with a novel form derived from the shape of the _waw_, bringing it closer to its familiar shape.

![Traditional and alternate forms of qaf](/assets/images/qashib/qashib-05.svg "Traditional and alternate forms of qaf")

#### _Noon_
The isolated and final _noon_ in manuscript Kufic takes an archaic shape unfamiliar to contemporary readers. In _Qashib_ it is replaced with a less common form found in some Kufic Qur’ans, which is closer to its familiar shape.

![Traditional and alternate forms of noon](/assets/images/qashib/qashib-06.svg "Traditional and alternate forms of noon")

#### _Reh_
The isolated and final _reh_ in manuscript Kufic can be confused with modern _dal_. In _Qashib_ it is replaced with a form derived from its shape in Fatimid Kufic.

![Traditional and alternate forms of reh](/assets/images/qashib/qashib-07.svg "Traditional and alternate forms of reh")

### Contextual alternates
_Qashib_ contains contextual alternates that are enabled automatically, like raised tooth heights in sequences of three or more _beh_-like letters, or top attachemnent of letters to _hah_, or repositioning of dots to avoid clashes, or shape adjustments for certain letter sequences.

### Stylistic sets
It also includes a number of stylistic sets that can be enabled manually for richer designs:

`ss01` — Dot-less Letter Forms
: Removes dots, mirroring the dotless style of early Kufic Qur’ans.

`ss02` — Rectangular Dots
: Replaces the default round dots with the small rectangular dots characteristic of early Kufic manuscripts.

`ss03` — Historical Letter Forms
: Replaces _Qashib_’s reshaped letters with their traditional manuscript Kufic forms, without affecting the dot style.

### Historical forms
The `hist` feature switches _Qashib_ to a fully traditional manuscript Kufic appearance, undoing its reshaped letters and using historical dot styles. This is equivalent to enabling `ss02` and `ss03` together.

![Historical forms](/assets/images/qashib/qashib-10.svg "Historical forms")

### Stylistic alternates
The `salt` feature provides alternative shapes for selected glyphs.

![Stylistic alternates](/assets/images/qashib/qashib-09.svg "Stylistic alternates")

## Elongation
_Qashib_ is a variable font with an elongation axis, _Mashq_ (`MSHQ`), to elongate letters that can be elongated in Kufic, which are _dal_, _tah_, _kaf_, and _sad_, as well as _beh_, and _feh_ (only in their initial and medial positions). These letters can expand or shrink as needed. This can be used to justify text without expanding the space between words.

## Spacing
_Qashib_ also has a spacing axis, _Spacing_ (`SPAC`), to control the gap between unconnected letters. The wide Kufic default can be tightened or further widened.

[Kufic]: https://en.wikipedia.org/wiki/Kufic
[GNU Affero General Public License]: https://www.gnu.org/licenses/agpl-3.0.en.html
