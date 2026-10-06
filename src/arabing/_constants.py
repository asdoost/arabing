"""
Shared low-level Unicode building blocks for Arabic-script charsets.

These are intentionally split into narrow, single-purpose constants so
language definitions (see `_languages.py`) can compose exactly the
categories they need, and so package users can import individual
punctuation classes (sentence punctuation, brackets, quotation marks,
etc.) instead of only a single flat "punctuation" blob.

DESIGN NOTES
------------
* Digit separators/signs (`ARABIC_DIGIT_SEPARATORS`) are kept
  deliberately SEPARATE from punctuation. Unlike ordinary punctuation,
  removing these characters can change the meaning of a number, e.g.
  stripping "٫" from "۲٫۷" (2.7) turns it into "۲۷" (27) -- a different
  value entirely. Because of this, digit separators are exposed as
  their own category (`LanguageCharset.digit_separators`) and are
  NEVER included in any `*_punctuation` constant/attribute, so generic
  punctuation-stripping code never accidentally corrupts numbers.

* Only ONE canonical form is provided per semantic punctuation role.
  Arabic-script languages have dedicated Arabic-block equivalents for
  the comma, semicolon, and question mark (، ؛ ؟), so the ASCII forms
  ("," ";" "?") are intentionally NOT duplicated anywhere in this
  module. Do not add them elsewhere -- this avoids ambiguity for
  consumers (no need to check "is this the Arabic or Latin comma?").
"""

# ---------------------------------------------------------------------------
# Digits
# ---------------------------------------------------------------------------
# Arabic-Indic digits (U+0660-U+0669).
ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

# Extended Arabic-Indic digits (U+06F0-U+06F9) - Persian, Urdu, Pashto, etc.
EXTENDED_ARABIC_INDIC_DIGITS = "۰۱۲۳۴۵۶۷۸۹"

# ---------------------------------------------------------------------------
# Digit signs / separators - NOT punctuation (see module docstring).
# ---------------------------------------------------------------------------
ARABIC_DECIMAL_SEPARATOR = "\u066B"    # ٫ ARABIC DECIMAL SEPARATOR
ARABIC_THOUSANDS_SEPARATOR = "\u066C"  # ٬ ARABIC THOUSANDS SEPARATOR
ARABIC_DATE_SEPARATOR = "\u060D"       # ؍ ARABIC DATE SEPARATOR
ARABIC_PERCENT_SIGN = "\u066A"         # ٪ ARABIC PERCENT SIGN

ARABIC_DIGIT_SEPARATORS = (
    ARABIC_DECIMAL_SEPARATOR + ARABIC_THOUSANDS_SEPARATOR +
    ARABIC_DATE_SEPARATOR + ARABIC_PERCENT_SIGN
)

# ---------------------------------------------------------------------------
# Sentence punctuation
# ---------------------------------------------------------------------------
# Arabic comma, semicolon, question mark (canonical forms - see the
# module docstring note about deliberately excluding ASCII "," ";" "?").
ARABIC_SENTENCE_PUNCTUATION = "،؛؟"

# Period, colon, exclamation mark - no widely-used Arabic-block
# equivalents. (Urdu/Kashmiri/Punjabi additionally use a native full
# stop; see `URDU_STYLE_FULL_STOP`, composed in per-language definitions.)
COMMON_SENTENCE_PUNCTUATION = ".:!"

SENTENCE_PUNCTUATION = ARABIC_SENTENCE_PUNCTUATION + COMMON_SENTENCE_PUNCTUATION

# ۔ = Urdu/Kashmiri/Punjabi full stop (danda-style period, U+06D4).
URDU_STYLE_FULL_STOP = "۔"

# ---------------------------------------------------------------------------
# Brackets
# ---------------------------------------------------------------------------
# NOTE: «» (guillemets, U+00AB/U+00BB) are in the Latin-1 Supplement
# block, not an Arabic block, despite being commonly used as Arabic
# quotation marks. The native/common punctuation split in
# `LanguageCharset` is strictly Unicode-block based, so these will be
# classified as "common" punctuation.
OPENING_BRACKETS = "([{«"
CLOSING_BRACKETS = ")]}»"
BRACKETS = OPENING_BRACKETS + CLOSING_BRACKETS

# ---------------------------------------------------------------------------
# Other punctuation categories
# ---------------------------------------------------------------------------
MATHEMATICAL_SIGNS = "-+×=<>"
QUOTATION_MARKS = "\"'`"
SPECIAL_SIGNS = "@#$^&*_|~\\/"

# Tatweel (kashida) - elongation character used for justification. Purely
# cosmetic: removing it does not change a text's meaning, so (unlike
# digit separators) it's safe to treat as ordinary, strippable punctuation.
TATWEEL_SIGN = "ـ"

# Convenience flat union of every punctuation category above (excludes
# digit separators). Provided for callers who just want a single string;
# `LanguageCharset` instances compose their own `.punctuation` from the
# individual category parameters rather than consuming this directly.
SHARED_PUNCTUATION = (
    SENTENCE_PUNCTUATION + BRACKETS + MATHEMATICAL_SIGNS +
    QUOTATION_MARKS + SPECIAL_SIGNS + TATWEEL_SIGN
)

# ---------------------------------------------------------------------------
# Zero-width joiners required for correct Perso-Arabic rendering.
# ---------------------------------------------------------------------------
ZWNJ = "\u200c"
ZWJ = "\u200d"

# ---------------------------------------------------------------------------
# Common Arabic diacritical marks (tashkeel / harakat).
# ---------------------------------------------------------------------------
ARABIC_DIACRITICS = (
    "\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652"
    "\u0653\u0654\u0655\u0656\u0670"
)