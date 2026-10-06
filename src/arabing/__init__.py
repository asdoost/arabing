"""
arabing
=======

A drop-in superset of the standard library's `string` module that adds
support for languages written in Arabic-script-based writing systems,
plus a categorized emoji character set.

    import arabing as string   # fully backward-compatible with `string`

Punctuation is exposed both as a combined string per language
(`<slug>_punctuation`) and broken into individual categories
(`<slug>_sentence_punctuation`, `<slug>_opening_brackets`,
`<slug>_closing_brackets`, `<slug>_quotation_marks`,
`<slug>_mathematical_signs`, `<slug>_special_signs`, `<slug>_tatweel`),
plus a Unicode-block-based split into `<slug>_native_punctuation` and
`<slug>_common_punctuation`.

Digit separators/signs (decimal separator, thousands separator, date
separator, percent sign) are intentionally NOT included in any
punctuation category -- removing them can change the meaning of a
number (e.g. "۲٫۷" -> "۲۷"). They're available separately via
`<slug>_digit_separators`.

See the project README for the full list of supported languages, emoji
categories, and utility functions.
"""
from string import *  # noqa: F401,F403
import string as _string

from ._charsets import LanguageCharset, QuranicCharset, EmojiCharset
from ._constants import (
    ARABIC_INDIC_DIGITS, EXTENDED_ARABIC_INDIC_DIGITS, ARABIC_DIACRITICS,
    ARABIC_DECIMAL_SEPARATOR, ARABIC_THOUSANDS_SEPARATOR,
    ARABIC_DATE_SEPARATOR, ARABIC_PERCENT_SIGN, ARABIC_DIGIT_SEPARATORS,
    ARABIC_SENTENCE_PUNCTUATION, COMMON_SENTENCE_PUNCTUATION,
    SENTENCE_PUNCTUATION, URDU_STYLE_FULL_STOP,
    OPENING_BRACKETS, CLOSING_BRACKETS, BRACKETS,
    MATHEMATICAL_SIGNS, QUOTATION_MARKS, SPECIAL_SIGNS, TATWEEL_SIGN,
    SHARED_PUNCTUATION, ZWNJ, ZWJ,
)
from ._quranic_marks import (
    QURANIC_ANNOTATION_SIGNS, QURANIC_STRUCTURAL_MARKS,
    QURANIC_RECITATION_MARKS, QURANIC_HONORIFIC_SIGNS,
)
from ._languages import (
    arabic, persian, urdu, pashto, kurdish_sorani, sindhi, uyghur,
    kashmiri, punjabi_shahmukhi, quranic,
    _ALL_LANGUAGE_OBJECTS, LANGUAGES, get_language, list_languages,
)
from ._emoji_data import (
    emoji, EMOJI_CATEGORIES, get_emoji_category, list_emoji_categories,
)
from ._detection import (
    is_arabing_char, contains_arabing,
    is_emoji_char, contains_emoji, strip_emojis, extract_emojis,
)
from ._digits import translate_digits
from ._normalize import strip_diacritics, normalize_alef
from ._aggregate import (
    arabing_alphabetic, arabing_digits, arabing_alphanumeric,
    arabing_digit_separators,
    arabing_sentence_punctuation, arabing_opening_brackets,
    arabing_closing_brackets, arabing_brackets, arabing_quotation_marks,
    arabing_mathematical_signs, arabing_special_signs, arabing_tatweel,
    arabing_punctuation, arabing_native_punctuation, arabing_common_punctuation,
    arabing_all_characters, arabing_printable, all_characters,
)

# ---------------------------------------------------------------------------
# Dynamically create module-level convenience variables, mirroring the
# naming style of the standard `string` module (e.g. `ascii_letters`).
# ---------------------------------------------------------------------------
_DYNAMIC_NAMES = []

# Maps <slug>_<public_name> -> LanguageCharset attribute name. Driving
# this from a single table (instead of manual per-name assignment) means
# a newly added attribute on LanguageCharset can't be silently forgotten
# from the generated globals.
_PER_LANGUAGE_ATTRS = {
    "letters": "alphabetic",
    "digits": "digits",
    "alphanumeric": "alphanumeric",
    "digit_separators": "digit_separators",
    "sentence_punctuation": "sentence_punctuation",
    "opening_brackets": "opening_brackets",
    "closing_brackets": "closing_brackets",
    "brackets": "brackets",
    "quotation_marks": "quotation_marks",
    "mathematical_signs": "mathematical_signs",
    "special_signs": "special_signs",
    "tatweel": "tatweel",
    "punctuation": "punctuation",
    "native_punctuation": "native_punctuation",
    "common_punctuation": "common_punctuation",
    "all_characters": "all_characters",
}

for _lang in _ALL_LANGUAGE_OBJECTS:
    for _public_name, _attr_name in _PER_LANGUAGE_ATTRS.items():
        globals()[f"{_lang.slug}_{_public_name}"] = getattr(_lang, _attr_name)
        _DYNAMIC_NAMES.append(f"{_lang.slug}_{_public_name}")
del _lang, _public_name, _attr_name

quranic_diacritics = quranic.diacritics
quranic_annotation_signs = quranic.annotation_signs
quranic_structural_marks = quranic.structural_marks
quranic_recitation_marks = quranic.recitation_marks
quranic_honorific_signs = quranic.honorific_signs
_DYNAMIC_NAMES.extend([
    "quranic_diacritics", "quranic_annotation_signs",
    "quranic_structural_marks", "quranic_recitation_marks",
    "quranic_honorific_signs",
])

for _cat_name, _cat_chars in emoji.categories.items():
    globals()[f"emoji_{_cat_name}"] = _cat_chars
    _DYNAMIC_NAMES.append(f"emoji_{_cat_name}")
del _cat_name, _cat_chars

emoji_all_characters = emoji.all_characters
_DYNAMIC_NAMES.append("emoji_all_characters")

# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------
__all__ = list(_string.__all__) + [
    "LanguageCharset", "QuranicCharset", "EmojiCharset",
    "LANGUAGES", "EMOJI_CATEGORIES",
    "arabic", "persian", "urdu", "pashto", "kurdish_sorani",
    "sindhi", "uyghur", "kashmiri", "punjabi_shahmukhi", "quranic",
    "emoji",
    "get_language", "list_languages",
    "get_emoji_category", "list_emoji_categories",
    "is_arabing_char", "contains_arabing",
    "is_emoji_char", "contains_emoji", "strip_emojis", "extract_emojis",
    "ARABIC_INDIC_DIGITS", "EXTENDED_ARABIC_INDIC_DIGITS", "translate_digits",
    "ARABIC_DIACRITICS", "strip_diacritics", "normalize_alef",
    "ARABIC_DECIMAL_SEPARATOR", "ARABIC_THOUSANDS_SEPARATOR",
    "ARABIC_DATE_SEPARATOR", "ARABIC_PERCENT_SIGN", "ARABIC_DIGIT_SEPARATORS",
    "ARABIC_SENTENCE_PUNCTUATION", "COMMON_SENTENCE_PUNCTUATION",
    "SENTENCE_PUNCTUATION", "URDU_STYLE_FULL_STOP",
    "OPENING_BRACKETS", "CLOSING_BRACKETS", "BRACKETS",
    "MATHEMATICAL_SIGNS", "QUOTATION_MARKS", "SPECIAL_SIGNS", "TATWEEL_SIGN",
    "SHARED_PUNCTUATION",
    "QURANIC_ANNOTATION_SIGNS", "QURANIC_STRUCTURAL_MARKS",
    "QURANIC_RECITATION_MARKS", "QURANIC_HONORIFIC_SIGNS",
    "ZWNJ", "ZWJ",
    "arabing_alphabetic", "arabing_digits", "arabing_alphanumeric",
    "arabing_digit_separators",
    "arabing_sentence_punctuation", "arabing_opening_brackets",
    "arabing_closing_brackets", "arabing_brackets", "arabing_quotation_marks",
    "arabing_mathematical_signs", "arabing_special_signs", "arabing_tatweel",
    "arabing_punctuation", "arabing_native_punctuation",
    "arabing_common_punctuation",
    "arabing_all_characters", "arabing_printable", "all_characters",
] + _DYNAMIC_NAMES


if __name__ == "__main__":
    print("Supported languages:", list_languages())
    print()

    number = "۲٫۷"
    print("Number with Arabic decimal separator:", number)
    print("Persian digit separators:", persian.digit_separators)
    print("Persian punctuation (excludes digit separators):", persian.punctuation)
    print()

    sample = "سال ۲۰۲۴، مَرْحَبًا! أحمد 😊👋"
    print("Sample text:", sample)
    print("Native punctuation used:", persian.native_punctuation)
    print("Common (Latin-derived) punctuation used:", persian.common_punctuation)
    print("Sentence punctuation:", persian.sentence_punctuation)
    print("Brackets:", persian.brackets)
    print("Contains emoji?", contains_emoji(sample))
    print("Extracted emojis:", extract_emojis(sample))