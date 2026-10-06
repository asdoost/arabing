# arabing 🕌🔤

**A drop-in superset of Python's standard `string` module for Arabic-script
languages — with categorized punctuation, digit-script handling, and emoji.**

**arabing** (_Arabic + string_) keeps 100% of the standard library's `string` module
(`ascii_letters`, `digits`, `punctuation`, `Template`, `capwords()`, etc.)
and adds ready-to-use, well-organized character-set constants and text
utilities for languages written in Arabic-script-based writing systems,
plus a categorized emoji character set for real-world text.

```python
import arabing as string

print(string.ascii_letters)     # everything from the stdlib still works
print(string.arabic_letters)    # 'ابتثجحخدذرزسشصضطظعغفقكلمنهويءأإؤئةى'
print(string.persian_digits)    # '۰۱۲۳۴۵۶۷۸۹'
print(string.emoji_hearts)      # '❤️🧡💛💚💙💜🖤🤍🤎💔❣️💕💞💓💗💖💘💝💟'
```

## Table of contents

- [Why?](#why)
- [Installation](#installation)
- [Supported languages](#supported-languages)
- [Quick start](#quick-start)
- [Per-language character sets](#per-language-character-sets)
- [Punctuation categories](#punctuation-categories)
- [Digit separators are not punctuation](#digit-separators-are-not-punctuation)
- [Qur'anic (Uthmani) specific character sets](#quranic-uthmani-specific-character-sets)
- [Emoji](#emoji)
- [Aggregates](#aggregates)
- [Utility functions](#utility-functions)
- [Design notes](#design-notes)
- [Full `string`-module compatibility](#full-string-module-compatibility)
- [Requirements](#requirements)
- [License](#license)
- [Contributing](#contributing)

## Why?

The built-in `string` module only exposes ASCII-based constants. Projects
dealing with Arabic, Persian, Urdu, Pashto, Kurdish, Sindhi, Uyghur,
Kashmiri, Punjabi (Shahmukhi), or Qur'anic Uthmani script end up
re-implementing the same character-set constants, digit-conversion logic,
punctuation classification, and emoji-handling regexes over and over.
`arabing` centralizes all of that in one well-documented,
`string`-module-compatible package.

## Installation

```bash
pip install arabing
```

## Supported languages

| Language | Code |
|---|---|
| Arabic | `ar` |
| Persian / Farsi | `fa` |
| Urdu | `ur` |
| Pashto | `ps` |
| Kurdish (Sorani) | `ckb` |
| Sindhi | `sd` |
| Uyghur | `ug` |
| Kashmiri | `ks` |
| Punjabi (Shahmukhi) | `pnb` |
| Qur'anic Arabic (Uthmani Script) | `quran` |

## Quick start

```python
from arabing import get_language, list_languages

list_languages()
# ['Arabic', 'Kashmiri', 'Kurdish (Sorani)', 'Pashto', 'Persian',
#  "Qur'anic Arabic (Uthmani Script)", 'Punjabi (Shahmukhi)',
#  'Sindhi', 'Urdu', 'Uyghur']

fa = get_language("fa")          # by ISO code
fa = get_language("Persian")     # or by name (case-insensitive)

print(fa.alphabetic)             # letters
print(fa.digits)                 # '۰۱۲۳۴۵۶۷۸۹'
print(fa.punctuation)            # combined punctuation
print("پ" in fa)                 # LanguageCharset supports `in`
```

## Per-language character sets

For every supported language, module-level constants are generated
automatically, named `<slug>_<category>` (e.g. `persian_letters`,
`urdu_digits`, `pashto_sentence_punctuation`):

```python
import arabing as string

string.arabic_letters
string.urdu_digits
string.pashto_punctuation
string.kurdish_sorani_all_characters
```

Each language is also available as a `LanguageCharset` object exposing
the same data as attributes:

| Attribute | Description |
|---|---|
| `alphabetic` | Alphabetic characters |
| `digits` | Native digit characters (0-9 equivalents) |
| `alphanumeric` | `alphabetic + digits` |
| `digit_separators` | Decimal/thousands/date separators + percent sign (see [below](#digit-separators-are-not-punctuation)) |
| `sentence_punctuation` | Comma/semicolon/question mark/period/colon/exclamation |
| `opening_brackets` / `closing_brackets` | Bracket/parenthesis/quote-opening and closing characters |
| `brackets` | `opening_brackets + closing_brackets` |
| `quotation_marks` | Quotation mark characters |
| `mathematical_signs` | Mathematical operator/comparison signs |
| `special_signs` | Miscellaneous signs (`@`, `#`, `$`, etc.) |
| `tatweel` | The tatweel/kashida elongation character |
| `punctuation` | All punctuation categories combined (excludes `digit_separators`) |
| `native_punctuation` | Subset of `punctuation` in an Arabic Unicode block |
| `common_punctuation` | Subset of `punctuation` outside an Arabic Unicode block |
| `all_characters` | Every character category combined |
| `printable` | `all_characters` + ASCII whitespace |

```python
fa.sentence_punctuation   # '،؛؟.:!'
fa.brackets               # '([{«)]}»'
fa.native_punctuation     # subset in an Arabic Unicode block, e.g. '،؛؟٫٬؍٪ـ'
fa.common_punctuation     # subset outside, e.g. '.!()[]{}«»-+×=<>"\'`@#$^&*_|~\\/'
```

## Punctuation categories

Punctuation is available both as a single combined string per language
and broken into individually-accessible categories, per language *and*
as cross-language unions:

```python
from arabing import (
    arabing_sentence_punctuation, arabing_opening_brackets,
    arabing_closing_brackets, arabing_brackets, arabing_quotation_marks,
    arabing_mathematical_signs, arabing_special_signs, arabing_tatweel,
    arabing_punctuation, arabing_native_punctuation,
    arabing_common_punctuation,
)
```

The lower-level building blocks used to compose these are also exported
directly:

```python
from arabing import (
    ARABIC_SENTENCE_PUNCTUATION, COMMON_SENTENCE_PUNCTUATION,
    SENTENCE_PUNCTUATION, OPENING_BRACKETS, CLOSING_BRACKETS, BRACKETS,
    MATHEMATICAL_SIGNS, QUOTATION_MARKS, SPECIAL_SIGNS, TATWEEL_SIGN,
    URDU_STYLE_FULL_STOP, SHARED_PUNCTUATION,
)
```

## Digit separators are not punctuation

The Arabic decimal separator (٫), thousands separator (٬), date
separator (؍), and percent sign (٪) are kept in their own category
(`digit_separators`), **deliberately excluded** from every punctuation
constant/attribute. Unlike ordinary punctuation, stripping these
characters can change the *meaning* of a number:

```python
"٫" in fa.punctuation        # False
"٫" in fa.digit_separators   # True
```

```
"۲٫۷"  (i.e. 2.7)  --[naively strip punctuation]-->  "۲۷"  (i.e. 27)
```

so any code that does bulk punctuation stripping via `arabing` will
never accidentally corrupt a number.

```python
from arabing import (
    ARABIC_DECIMAL_SEPARATOR, ARABIC_THOUSANDS_SEPARATOR,
    ARABIC_DATE_SEPARATOR, ARABIC_PERCENT_SIGN, ARABIC_DIGIT_SEPARATORS,
    arabing_digit_separators,
)
```

## Qur'anic (Uthmani) specific character sets

Qur'anic orthography uses many special Unicode marks not found in
standard Arabic. These are exposed separately since they serve distinct
liturgical/linguistic functions:

```python
from arabing import (
    quranic_diacritics,         # tashkeel/harakat + extended vowel marks
    quranic_annotation_signs,   # waqf (pause/stop) signs
    quranic_structural_marks,   # end-of-ayah, rub-el-hizb, sajdah signs
    quranic_recitation_marks,   # small high/low recitation marks
    quranic_honorific_signs,    # honorific signs (SAW, AS, RA, etc.)
)
```

## Emoji

Because emoji frequently appear alongside Arabic-script text in
real-world content (chat, social media, reviews), `arabing` ships a
categorized emoji character set:

```python
from arabing import (
    emoji_faces, emoji_emotions, emoji_hand_gestures, emoji_hearts,
    emoji_animals, emoji_food_and_drink, emoji_activities,
    emoji_travel_and_places, emoji_objects, emoji_symbols, emoji_flags,
    emoji_all_characters,
)
from arabing import get_emoji_category, list_emoji_categories

list_emoji_categories()
# ['activities', 'animals', 'emotions', 'faces', 'flags',
#  'food_and_drink', 'hand_gestures', 'hearts', 'objects',
#  'symbols', 'travel_and_places']

get_emoji_category("hearts")
```

Emoji detection/extraction/stripping is **grapheme-cluster aware**, so
multi-codepoint sequences (flags, ZWJ combinations) are treated as
single units rather than being split into individual codepoints:

```python
from arabing import contains_emoji, extract_emojis, strip_emojis

contains_emoji("Hello 👋")                    # True
extract_emojis("Go Resistance 🇵🇸 🇮🇷 🇮🇶 🇾🇪 🇱🇧")             # ['🇵🇸', '🇮🇷', '🇮🇶', '🇾🇪', '🇱🇧']
strip_emojis("مرحبا 👋 يا صديقي 😊")           # 'مرحبا  يا صديقي '
```

## Aggregates

Cross-language unions covering every supported language at once:

```python
from arabing import (
    arabing_alphabetic, arabing_digits, arabing_alphanumeric,
    arabing_digit_separators, arabing_punctuation,
    arabing_native_punctuation, arabing_common_punctuation,
    arabing_all_characters, arabing_printable,
    all_characters,   # ASCII printable + all Arabic-script chars + all emoji
)
```

## Utility functions

```python
from arabing import (
    is_arabing_char, contains_arabing,
    is_emoji_char, contains_emoji, strip_emojis, extract_emojis,
    translate_digits, strip_diacritics, normalize_alef,
)

contains_arabing("Hello مرحبا")          # True

translate_digits("سال 2024", to="extended_arabic_indic")  # 'سال ۲۰۲۴'
translate_digits("۱۲۳", to="latin")                        # '123'

strip_diacritics("مَرْحَبًا")               # 'مرحبا'
normalize_alef("أحمد إبراهيم آدم")         # 'احمد ابراهيم ادم'
```

## Design notes

A few deliberate policies worth knowing about:

- **Native vs. common punctuation is determined by Unicode block
  membership**, not by subjective "feel." `native_punctuation` is
  whatever `is_arabing_char()` recognizes as belonging to an Arabic
  Unicode block; everything else in `punctuation` is `common_punctuation`.
  One consequence: guillemets (`«»`) are technically in the Latin-1
  Supplement block, so they're classified as *common* punctuation even
  though they're commonly used as Arabic quotation marks.
- **Only one canonical form per punctuation role.** Arabic-script
  languages have dedicated equivalents for the comma, semicolon, and
  question mark (، ؛ ؟), so the ASCII forms (`,` `;` `?`) are
  intentionally *not* duplicated anywhere in `arabing`'s data.
- **Digit separators are never punctuation** (see above) — this is the
  one category deliberately excluded from `punctuation` so that
  stripping punctuation can never corrupt a number.

## Full `string`-module compatibility

Everything the standard `string` module offers (`ascii_letters`,
`ascii_lowercase`, `ascii_uppercase`, `digits`, `hexdigits`, `octdigits`,
`punctuation`, `whitespace`, `printable`, `capwords()`, `Formatter`,
`Template`) is re-exported unchanged, so `arabing` can be used as a
direct replacement for `string` in existing code:

```python
import arabing as string
```

## Requirements

- Python >= 3.8
- [`regex`](https://pypi.org/project/regex/) (for grapheme-cluster-aware
  emoji extraction/stripping)

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues and pull requests are welcome, especially for:
- Additional/regional orthographic variants
- Additional emoji categories or corrections
- Additional Arabic-script languages not yet covered

## Caveat

The character sets in this package reflect commonly used, practical
letter/digit/punctuation inventories for each language. Some languages
have regional orthographic variants; for linguistically critical
applications, verify against an authoritative orthographic standard for
your use case.