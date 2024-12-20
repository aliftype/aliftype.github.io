---
title: Qahiri
subtitle: A manuscript Kufic typeface
layout: font
language: en-US
direction: ltr
---
_Qahiri_ is a [Kufic][1] typeface based on the modernized and regularized old manuscript Kufic calligraphy style of the late master of Arabic calligraphy [_Mohammad Abdul Qadir_][2].

Following the convention of naming Kufic styles after the cities they appeared in, _Qahiri_ (قاهري) is named after the city of Cairo, Egypt (القاهرة).

_Qahiri_ is a free and open-source project, anyone is welcome to use and modify it under the terms of the [version 1.1 of SIL Open Font License][5].

## The app
The font provides many alternate shapes for many of its glyphs, which should be usable in any OpenType-savvy application. But since many apps have poor OpenType support or bad UI or don’t allow controlling features for single glyphs, _Qahiri_ comes with a web application that provides easy access to glyph alternates.

Visit the app [web page](./app/english) and type Arabic in the text area. Below the text will appear the alternates of the character before the text cursor (the gray bar). Clicking on an alternate form will cause it to be used instead of the current form:

![Screen shot of the app](/assets/images/qahiri/screenshot.png)

The slider and the input box next to it control the text size.

Two buttons control the dots, the ![remove dots](/assets/images/app/remove-dots.svg){:.button} button will remove all the dots, to get a dot-less version of the text resembling early Kufic manuscripts.

![Screenshot with no dots](/assets/images/qahiri/screenshot-dotless.png)

The ![rounded dots](/assets/images/app/round-dots.svg){:.button} button, on the other hand, replaces the default rectangular dots with more familiar rounded dots.

![Screenshot with rounded dots](/assets/images/qahiri/screenshot-rounded-dots.png)

The app allows exporting SVG files that can be further modified in any vector graphics application. Pressing *Export*{:.button} button will download the SVG. The SVG contains also the current text with the selected alternates, and can be loaded any time in the app again using the *Open*{:.button} button. Pressing the *Clear*{:.button} button will delete all the text.

## Font features
The font tries to remain faithful to the rules laid out by _Mohammad Abdul Qadir_, and one aspect of that is spacing. The space between letters, connected or not, as well as between words, is always about half the thickness of vertical stems. There is a distinction between inter-word and inter-letter spacing. Inserting more than one space character will increase the inter-word spacing.

![Screenshot showing spacing](/assets/images/qahiri/screenshot-spacing.png)

The letter forms used by default are designed to work together in harmony, but some of the alternate forms should be selected with care. For example, _returning ya’_ can clash with preceding letters with descenders and should be avoided in such cases. The font will try to solve clashes in such cases, but this does not always work.

![Screenshot showing clashing letters](/assets/images/qahiri/screenshot-clash.png)

## Issues
The font is built using some advanced OpenType techniques that are not equally supported by software, and this might result in the font being broken in certain applications.

The performance of the application is also far from being optimal, so pasting large amounts of text should be avoided. Also, it does not support multiple lines; it works with one line at a time.

[1]: https://en.wikipedia.org/wiki/Kufic
[2]: https://ar.wikipedia.org/wiki/محمد_عبد_القادر_عبد_الله_(خطاط)
[3]: https://github.com/aliftype/qahiri/releases/latest
[5]: https://github.com/aliftype/qahiri/blob/main/OFL.txt
