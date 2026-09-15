"""
arabing.py
=================

A drop-in superset of the standard library's `string` module that adds
support for languages written in **Arabic-script-based** writing systems
(i.e. scripts belonging to the Unicode "Arabic" block and its extensions).

WHY THIS EXISTS
----------------
The built-in `string` module only exposes ASCII-based constants
(`ascii_letters`, `digits`, `punctuation`, etc.). This module keeps 100%
of that functionality (via `from string import *`) and adds equivalent
data structures for Arabic-script languages, following the same naming
philosophy as the standard module.

SUPPORTED LANGUAGES
--------------------
    - Arabic              (ar)
    - Persian / Farsi     (fa)
    - Urdu                (ur)
    - Pashto              (ps)
    - Kurdish - Sorani    (ckb)
    - Sindhi              (sd)
    - Uyghur              (ug)
    - Kashmiri            (ks)
    - Punjabi (Shahmukhi) (pnb)
    - Qur'anic Arabic (Uthmani Script) (quran)

WHAT YOU GET
------------
For every language:
    <slug>_letters          -> alphabetic characters
    <slug>_digits            -> native digit characters (0-9 equivalents)
    <slug>_punctuation       -> script-specific punctuation marks
    <slug>_all_characters    -> letters + digits + punctuation

For Qur'anic Arabic specifically, additional categorized character sets
are provided (since Qur'anic orthography uses many special marks not
found in standard Arabic):
    quranic_diacritics         -> tashkeel/harakat + extended vowel marks
    quranic_annotation_signs   -> waqf (pause/stop) signs
    quranic_structural_marks   -> end-of-ayah, rub-el-hizb, sajdah signs
    quranic_recitation_marks   -> small high/low recitation marks
    quranic_honorific_signs    -> honorific signs (SAW, AS, RA, etc.)

Also:
    LANGUAGES                 -> dict registry, lookup by name or ISO code
    get_language(id)          -> fetch a LanguageCharset object
    list_languages()          -> list all supported language names
    arabing_alphabetic        -> union of all Arabic-script letters
    arabing_digits            -> union of all Arabic-script digits
    arabing_punctuation       -> union of all Arabic-script punctuation
    arabing_all_characters
    arabing_printable
    all_characters            -> ASCII printable + all Arabic-script chars

Utility functions:
    is_arabing_char(ch)
    contains_arabing(text)
    translate_digits(text, to=..., from_=...)
    strip_diacritics(text)
    normalize_alef(text)

FULL ASCII / `string`-MODULE COMPATIBILITY
-------------------------------------------
Everything the standard `string` module offers (ascii_letters,
ascii_lowercase, ascii_uppercase, digits, hexdigits, octdigits,
punctuation, whitespace, printable, capwords(), Formatter, Template)
is re-exported unchanged, so this module can be used as a direct
replacement for `string` in existing code:

    import arabing as string

CAVEAT
------
The character sets below reflect commonly used, practical letter/digit/
punctuation inventories for each language. Some languages have regional
orthographic variants; for linguistically critical applications, verify
against an authoritative orthographic standard for your use case.
"""

# ---------------------------------------------------------------------------
# Re-export the entire standard `string` module so this library is a
# fully backward-compatible drop-in replacement for ASCII use cases.
# ---------------------------------------------------------------------------
from string import *          # noqa: F401,F403  (ascii_letters, digits, ...)
import string as _string       # kept for internal, explicit references
import re


# ---------------------------------------------------------------------------
# Core data container
# ---------------------------------------------------------------------------
class LanguageCharset:
    """
    Holds the character inventory for a single Arabic-script-based language.

    Attributes:
        name (str): Human-readable language name (e.g. "Arabic").
        code (str): ISO 639 language code (e.g. "ar").
        slug (str): Python-identifier-friendly name used to build the
                    module-level convenience variables (e.g. "arabic").
        alphabetic (str): The language's alphabetic characters.
        digits (str): The language's native digit characters (0-9).
        punctuation (str): Punctuation marks commonly used in the language.
    """

    __slots__ = ("name", "code", "slug", "alphabetic", "digits", "punctuation")

    def __init__(self, name, code, slug, alphabetic, digits, punctuation):
        self.name = name
        self.code = code
        self.slug = slug
        self.alphabetic = alphabetic
        self.digits = digits
        self.punctuation = punctuation

    @property
    def all_characters(self):
        """str: Concatenation of alphabetic + digits + punctuation."""
        return self.alphabetic + self.digits + self.punctuation

    @property
    def printable(self):
        """str: All characters plus ASCII whitespace (spaces, tabs, etc.)."""
        return self.all_characters + whitespace

    def __repr__(self):
        return f"<LanguageCharset {self.name!r} ({self.code})>"

    def __contains__(self, ch):
        """Allow `'a' in some_language_charset` checks."""
        return ch in self.all_characters


class QuranicCharset(LanguageCharset):
    """
    Extends LanguageCharset with additional category-specific character
    sets unique to Qur'anic (Uthmani) orthography.

    The Qur'an uses many special Unicode characters beyond the standard
    Arabic alphabet, digits, and punctuation — including recitation
    (tajweed) vowel marks, waqf (pause) signs, structural markers
    (end-of-ayah, sajdah, hizb), and honorific signs. This subclass keeps
    those categories separate rather than lumping them into generic
    "punctuation", since each serves a distinct linguistic/liturgical
    function.

    Attributes (in addition to those inherited from LanguageCharset):
        diacritics (str): Tashkeel/harakat plus extended Qur'anic vowel
                           and recitation marks.
        annotation_signs (str): Waqf (pause/stop) signs used to guide
                           recitation (e.g. ۖ ۗ ۘ ۙ ۚ ۛ ۜ).
        structural_marks (str): End-of-ayah (۝), start-of-rub-el-hizb (۞),
                           and place-of-sajdah (۩) markers.
        recitation_marks (str): Fine-grained small high/low marks used
                           in various Mus'haf printing styles.
        honorific_signs (str): Signs marking honorific phrases (e.g.
                           sallallahu 'alayhi wasallam, radi allahu anhu).
    """

    __slots__ = (
        "diacritics", "annotation_signs", "structural_marks",
        "recitation_marks", "honorific_signs",
    )

    def __init__(self, name, code, slug, alphabetic, digits, punctuation,
                 diacritics, annotation_signs, structural_marks,
                 recitation_marks, honorific_signs):
        super().__init__(name, code, slug, alphabetic, digits, punctuation)
        self.diacritics = diacritics
        self.annotation_signs = annotation_signs
        self.structural_marks = structural_marks
        self.recitation_marks = recitation_marks
        self.honorific_signs = honorific_signs

    @property
    def all_characters(self):
        """str: Every Qur'anic character category combined."""
        return (
            self.alphabetic + self.digits + self.punctuation +
            self.diacritics + self.annotation_signs +
            self.structural_marks + self.recitation_marks +
            self.honorific_signs
        )
        

# ---------------------------------------------------------------------------
# Shared digit systems used across several Arabic-script languages
# ---------------------------------------------------------------------------
# Arabic-Indic digits (U+0660-U+0669) - used by Arabic, Kurdish, Sindhi, etc.
ARABIC_INDIC_DIGITS = "٠١٢٣٤٥٦٧٨٩"

# Extended Arabic-Indic digits (U+06F0-U+06F9) - used by Persian, Urdu,
# Pashto, Uyghur, Kashmiri, Punjabi (Shahmukhi), etc.
EXTENDED_ARABIC_INDIC_DIGITS = "۰۱۲۳۴۵۶۷۸۹"


# ---------------------------------------------------------------------------
# Shared punctuation common to most Arabic-script languages
# ---------------------------------------------------------------------------
# ، = Arabic comma        ؛ = Arabic semicolon     ؟ = Arabic question mark
# ٪ = percent sign        ٫ = decimal separator    ٬ = thousands separator
# ـ = tatweel (kashida)   « » = guillemets (quotation marks)
_COMMON_ARABIC_PUNCTUATION = "،؛؟٪٫٬ـ«»"

# ۔ = Urdu/Kashmiri/Punjabi full stop (danda-style period)
_URDU_STYLE_FULL_STOP = "۔"

# Zero-width joiners frequently required for correct Perso-Arabic rendering.
ZWNJ = "\u200c"   # ZWNJ - e.g. Persian "می‌روم"
ZWJ = "\u200d"       # ZWJ

# Common Arabic diacritical marks (tashkeel / harakat).
ARABIC_DIACRITICS = (
    "\u064B"  # FATHATAN
    "\u064C"  # DAMMATAN
    "\u064D"  # KASRATAN
    "\u064E"  # FATHA
    "\u064F"  # DAMMA
    "\u0650"  # KASRA
    "\u0651"  # SHADDA
    "\u0652"  # SUKUN
    "\u0653"  # MADDAH ABOVE
    "\u0654"  # HAMZA ABOVE
    "\u0655"  # HAMZA BELOW
    "\u0656"  # SUBSCRIPT ALEF
    "\u0670"  # SUPERSCRIPT ALEF (Alef Khanjariyah)
)

# ---------------------------------------------------------------------------
# Qur'anic (Uthmani script) - specific Unicode marks
#
# These characters live in the Arabic Unicode block but are specific to
# Qur'anic recitation/orthography and are not used in everyday Arabic,
# Persian, Urdu, etc. They are grouped by function.
# ---------------------------------------------------------------------------

# Extended vowel/recitation marks (beyond basic tashkeel in ARABIC_DIACRITICS)
_QURANIC_EXTENDED_VOWEL_MARKS = (
    "\u0657"  # ARABIC INVERTED DAMMA
    "\u0658"  # ARABIC MARK NOON GHUNNA
    "\u0659"  # ARABIC ZWARAKAY
    "\u065A"  # ARABIC VOWEL SIGN SMALL V ABOVE
    "\u065B"  # ARABIC VOWEL SIGN INVERTED SMALL V ABOVE
    "\u065C"  # ARABIC VOWEL SIGN DOT BELOW
    "\u065D"  # ARABIC REVERSED DAMMA
    "\u065E"  # ARABIC FATHA WITH TWO DOTS
    "\u065F"  # ARABIC WAVY HAMZA BELOW
)

# Waqf (pause/stop) annotation signs - guide the reciter on where/how to pause
QURANIC_ANNOTATION_SIGNS = (
    "\u06D6"  # ۖ SMALL HIGH LIGATURE SAD WITH LAM WITH ALEF MAKSURA (sila)
    "\u06D7"  # ۗ SMALL HIGH LIGATURE QAF WITH LAM WITH ALEF MAKSURA (qif)
    "\u06D8"  # ۘ SMALL HIGH MEEM INITIAL FORM (compulsory stop)
    "\u06D9"  # ۙ SMALL HIGH LAM ALEF (no stop)
    "\u06DA"  # ۚ SMALL HIGH JEEM (permissible stop)
    "\u06DB"  # ۛ SMALL HIGH THREE DOTS (one of two stops)
    "\u06DC"  # ۜ SMALL HIGH SEEN (saktah / brief pause)
)

# Structural markers - denote textual divisions of the Mus'haf
QURANIC_STRUCTURAL_MARKS = (
    "\u06DD"  # ۝ END OF AYAH
    "\u06DE"  # ۞ START OF RUB EL HIZB
    "\u06E9"  # ۩ PLACE OF SAJDAH
)

# Fine-grained recitation marks used across different Mus'haf print styles
QURANIC_RECITATION_MARKS = (
    "\u06DF"  # ۟ SMALL HIGH ROUNDED ZERO
    "\u06E0"  # ۠ SMALL HIGH UPRIGHT RECTANGULAR ZERO
    "\u06E1"  # ۡ SMALL HIGH DOTLESS HEAD OF KHAH
    "\u06E2"  # ۢ SMALL HIGH MEEM ISOLATED FORM
    "\u06E3"  # ۣ SMALL LOW SEEN
    "\u06E4"  # ۤ SMALL HIGH MADDA
    "\u06E5"  # ۥ SMALL WAW
    "\u06E6"  # ۦ SMALL YEH
    "\u06E7"  # ۧ SMALL HIGH YEH
    "\u06E8"  # ۨ SMALL HIGH NOON
    "\u06EA"  # ۪ EMPTY CENTRE LOW STOP
    "\u06EB"  # ۫ EMPTY CENTRE HIGH STOP
    "\u06EC"  # ۬ ROUNDED HIGH STOP WITH FILLED CENTRE
    "\u06ED"  # ۭ SMALL LOW MEEM
)

# Honorific signs (e.g. sallallahu 'alayhi wasallam, radi allahu 'anhu)
QURANIC_HONORIFIC_SIGNS = (
    "\u0610"  # ؐ SIGN SALLALLAHOU ALAYHE WASSALLAM
    "\u0611"  # ؑ SIGN ALAYHE ASSALLAM
    "\u0612"  # ؒ SIGN RAHMATULLAH ALAYHE
    "\u0613"  # ؓ SIGN RADI ALLAHOU ANHU
    "\u0614"  # ؔ SIGN TAKHALLUS
    "\u0615"  # ؕ SMALL HIGH TAH
    "\u0616"  # ؖ SMALL HIGH LIGATURE ALEF WITH LAM WITH YEH
    "\u0617"  # ؗ SMALL HIGH ZAIN
    "\u0618"  # ؘ SMALL FATHA
    "\u0619"  # ؙ SMALL DAMMA
    "\u061A"  # ؚ SMALL KASRA
)

# ---------------------------------------------------------------------------
# Per-language definitions
# ---------------------------------------------------------------------------

# --- Qur'anic Arabic - Uthmani Script (quran) ---------------------------------------
quranic = QuranicCharset(
    name="Qur'anic Arabic (Uthmani Script)",
    code="quran",
    slug="quranic",
    alphabetic=(
        "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"   # 28 base letters
        "ءأإؤئةى"                          # hamza forms, taa marbuta, alef maksura
        "ٱ"                                # alef wasla (Uthmani-specific)
    ),
    digits=ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION,
    diacritics=ARABIC_DIACRITICS + _QURANIC_EXTENDED_VOWEL_MARKS,
    annotation_signs=QURANIC_ANNOTATION_SIGNS,
    structural_marks=QURANIC_STRUCTURAL_MARKS,
    recitation_marks=QURANIC_RECITATION_MARKS,
    honorific_signs=QURANIC_HONORIFIC_SIGNS,
)

# --- Arabic (ar) ------------------------------------------------------------
arabic = LanguageCharset(
    name="Arabic",
    code="ar",
    slug="arabic",
    alphabetic=(
        "ابتثجحخدذرزسشصضطظعغفقكلمنهوي"   # 28 base letters
        "ءأإؤئةى"                          # hamza forms, taa marbuta, alef maqsura
    ),
    digits=ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION,
)

# --- Persian / Farsi (fa) ----------------------------------------------------
persian = LanguageCharset(
    name="Persian",
    code="fa",
    slug="persian",
    alphabetic=(
        "آبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی" "اء"
    ),
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION,
)

# --- Urdu (ur) ----------------------------------------------------------------
urdu = LanguageCharset(
    name="Urdu",
    code="ur",
    slug="urdu",
    alphabetic=(
        "اآبپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوہھءیے"
    ),
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION + _URDU_STYLE_FULL_STOP,
)

# --- Pashto (ps) ---------------------------------------------------------------
pashto = LanguageCharset(
    name="Pashto",
    code="ps",
    slug="pashto",
    alphabetic=(
        "اآبپتټثجځچڅحخدډذرړزژږسشښصضطظعغفقکګلمنڼوهءيیېۍ"
    ),
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION,
)

# --- Kurdish - Sorani (ckb) -----------------------------------------------------
kurdish_sorani = LanguageCharset(
    name="Kurdish (Sorani)",
    code="ckb",
    slug="kurdish_sorani",
    alphabetic=(
        "ابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆهھیێء"
    ),
    digits=ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION,
)

# --- Sindhi (sd) -----------------------------------------------------------------
sindhi = LanguageCharset(
    name="Sindhi",
    code="sd",
    slug="sindhi",
    alphabetic=(
        "ابٻڀتٿٽٺثجڄچڇحخدڌڊڏڍذرڙزسشصضطظعغفڦقکڪگڳڱلمنڻوھءيی"
    ),
    digits=ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION,
)

# --- Uyghur (ug) -------------------------------------------------------------------
uyghur = LanguageCharset(
    name="Uyghur",
    code="ug",
    slug="uyghur",
    alphabetic=(
        "اەبپتجچخدرزژسشغفقكگڭلمنھوۇۆۈۋېىي"
    ),
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION,
)

# --- Kashmiri (ks) --------------------------------------------------------------------
kashmiri = LanguageCharset(
    name="Kashmiri",
    code="ks",
    slug="kashmiri",
    alphabetic=(
        "اآءبپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوہھیے"
    ),
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION + _URDU_STYLE_FULL_STOP,
)

# --- Punjabi - Shahmukhi (pnb) -----------------------------------------------------------
punjabi_shahmukhi = LanguageCharset(
    name="Punjabi (Shahmukhi)",
    code="pnb",
    slug="punjabi_shahmukhi",
    alphabetic=(
        "ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوہھءیے"
    ),
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    punctuation=_COMMON_ARABIC_PUNCTUATION + _URDU_STYLE_FULL_STOP,
)


# ---------------------------------------------------------------------------
# Registry: lookup any language by its full name or ISO code (case-insensitive)
# ---------------------------------------------------------------------------
_ALL_LANGUAGE_OBJECTS = [
    arabic, persian, urdu, pashto, kurdish_sorani,
    sindhi, uyghur, kashmiri, punjabi_shahmukhi, quranic,
]

LANGUAGES = {
    "arabic": arabic, "ar": arabic,
    "persian": persian, "farsi": persian, "fa": persian,
    "urdu": urdu, "ur": urdu,
    "pashto": pashto, "ps": pashto,
    "kurdish": kurdish_sorani, "sorani": kurdish_sorani, "ckb": kurdish_sorani,
    "sindhi": sindhi, "sd": sindhi,
    "uyghur": uyghur, "ug": uyghur,
    "kashmiri": kashmiri, "ks": kashmiri,
    "punjabi": punjabi_shahmukhi, "shahmukhi": punjabi_shahmukhi, "pnb": punjabi_shahmukhi,
    "quranic": quranic, "quran": quranic, "uthmani": quranic, "ar-quran": quranic,
}


# ---------------------------------------------------------------------------
# Dynamically create module-level convenience variables, mirroring the
# naming style of the standard `string` module (e.g. `ascii_letters`).
#
# This produces, for every language, four globals:
#   <slug>_letters, <slug>_digits, <slug>_punctuation, <slug>_all_characters
#
# e.g. arabic_letters, arabic_digits, arabic_punctuation, arabic_all_characters
#      persian_letters, persian_digits, ...
# ---------------------------------------------------------------------------
_DYNAMIC_NAMES = []
for _lang in _ALL_LANGUAGE_OBJECTS:
    globals()[f"{_lang.slug}_letters"] = _lang.alphabetic
    globals()[f"{_lang.slug}_digits"] = _lang.digits
    globals()[f"{_lang.slug}_punctuation"] = _lang.punctuation
    globals()[f"{_lang.slug}_all_characters"] = _lang.all_characters
    _DYNAMIC_NAMES.extend([
        f"{_lang.slug}_letters",
        f"{_lang.slug}_digits",
        f"{_lang.slug}_punctuation",
        f"{_lang.slug}_all_characters",
    ])
del _lang

# ---------------------------------------------------------------------------
# Extra category-specific constants unique to Qur'anic orthography
# (these have no equivalent in the plain LanguageCharset class, so they
# are not produced by the generic dynamic-generation loop above).
# ---------------------------------------------------------------------------
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

# ---------------------------------------------------------------------------
# Aggregate constants across ALL supported Arabic-script languages
# ---------------------------------------------------------------------------
def _dedup_concat(strings):
    """
    Concatenate multiple strings, preserving first-seen order while
    removing duplicate characters.

    Args:
        strings (iterable[str]): Strings to combine.
    Returns:
        str: Combined, de-duplicated string.
    """
    seen = set()
    result = []
    for s in strings:
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                result.append(ch)
    return "".join(result)


# Union of every language's letters / digits / punctuation.
arabing_alphabetic = _dedup_concat(l.alphabetic for l in _ALL_LANGUAGE_OBJECTS)
arabing_digits = _dedup_concat(l.digits for l in _ALL_LANGUAGE_OBJECTS)
arabing_punctuation = _dedup_concat(l.punctuation for l in _ALL_LANGUAGE_OBJECTS)
arabing_all_characters = (
    arabing_alphabetic + arabing_digits + arabing_punctuation +
    quranic.diacritics + quranic.annotation_signs +
    quranic.structural_marks + quranic.recitation_marks +
    quranic.honorific_signs
)
arabing_printable = arabing_all_characters + whitespace

# Grand union: ASCII (from the standard `string` module) + all Arabic-script
# languages combined - the "everything" constant.
all_characters = printable + arabing_all_characters


# ---------------------------------------------------------------------------
# Language lookup helpers
# ---------------------------------------------------------------------------
def get_language(identifier):
    """
    Retrieve the LanguageCharset object for a given language name or code.

    Args:
        identifier (str): Language name (e.g. "Arabic") or ISO 639 code
                           (e.g. "ar"). Case-insensitive.

    Returns:
        LanguageCharset: The matching language's character data.

    Raises:
        KeyError: If no matching language is found.

    Example:
        >>> get_language("fa").alphabetic
        'ابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهیء'
    """
    key = identifier.strip().lower()
    if key not in LANGUAGES:
        raise KeyError(
            f"Unknown language identifier: {identifier!r}. "
            f"Available identifiers: {sorted(LANGUAGES.keys())}"
        )
    return LANGUAGES[key]


def list_languages():
    """
    List all supported (unique) language names.

    Returns:
        list[str]: Sorted list of human-readable language names.
    """
    return sorted({lang.name for lang in _ALL_LANGUAGE_OBJECTS})


# ---------------------------------------------------------------------------
# Unicode-block based detection utilities
# ---------------------------------------------------------------------------
# Unicode block ranges that cover Arabic-script writing systems.
_ARABIC_UNICODE_RANGES = (
    (0x0600, 0x06FF),    # Arabic
    (0x0750, 0x077F),    # Arabic Supplement
    (0x0870, 0x089F),    # Arabic Extended-B
    (0x08A0, 0x08FF),    # Arabic Extended-A
    (0xFB50, 0xFDFF),    # Arabic Presentation Forms-A
    (0xFE70, 0xFEFF),    # Arabic Presentation Forms-B
    (0x10E60, 0x10E7F),  # Rumi Numeral Symbols
    (0x1EC70, 0x1ECBF),  # Indic Siyaq Numbers
    (0x1EE00, 0x1EEFF),  # Arabic Mathematical Alphabetic Symbols
)


def is_arabing_char(ch):
    """
    Check whether a single character belongs to a Unicode block used by
    Arabic-script writing systems.

    Args:
        ch (str): A single character.

    Returns:
        bool: True if the character is part of an Arabic-script block.
    """
    if not ch:
        return False
    codepoint = ord(ch)
    return any(start <= codepoint <= end for start, end in _ARABIC_UNICODE_RANGES)


def contains_arabing(text):
    """
    Check whether any character in `text` belongs to an Arabic-script block.

    Args:
        text (str): Text to inspect.

    Returns:
        bool: True if at least one Arabic-script character is present.
    """
    return any(is_arabing_char(ch) for ch in text)


# ---------------------------------------------------------------------------
# Digit conversion utilities
# ---------------------------------------------------------------------------
_DIGIT_SYSTEMS = {
    "latin": _string.digits,                                # 0123456789
    "arabic_indic": ARABIC_INDIC_DIGITS,                    # ٠١٢٣٤٥٦٧٨٩
    "extended_arabic_indic": EXTENDED_ARABIC_INDIC_DIGITS,  # ۰۱۲۳۴۵۶۷۸۹
}


def translate_digits(text, to="latin", from_=None):
    """
    Convert digit characters within `text` from one digit system to another.

    Args:
        text (str): Input text possibly containing digits.
        to (str): Target digit system. One of:
                  'latin', 'arabic_indic', 'extended_arabic_indic'.
        from_ (str, optional): Restrict conversion to a specific source
                  digit system. If None (default), digits from *all* known
                  systems are converted to the target system.

    Returns:
        str: `text` with digits translated to the target system.

    Raises:
        ValueError: If `to` (or `from_`) is not a recognized digit system.

    Example:
        >>> translate_digits("سال 2024", to="extended_arabic_indic")
        'سال ۲۰۲۴'
        >>> translate_digits("۱۲۳", to="latin")
        '123'
    """
    if to not in _DIGIT_SYSTEMS:
        raise ValueError(
            f"Unknown target digit system: {to!r}. "
            f"Choose from {list(_DIGIT_SYSTEMS.keys())}"
        )

    sources = [from_] if from_ else list(_DIGIT_SYSTEMS.keys())
    for source in sources:
        if source not in _DIGIT_SYSTEMS:
            raise ValueError(
                f"Unknown source digit system: {source!r}. "
                f"Choose from {list(_DIGIT_SYSTEMS.keys())}"
            )

    target_digits = _DIGIT_SYSTEMS[to]
    translation_map = {}
    for source in sources:
        source_digits = _DIGIT_SYSTEMS[source]
        for src_char, tgt_char in zip(source_digits, target_digits):
            translation_map[ord(src_char)] = tgt_char

    return text.translate(translation_map)


# ---------------------------------------------------------------------------
# Text normalization helpers
# ---------------------------------------------------------------------------
_DIACRITICS_TRANSLATION = {ord(c): None for c in ARABIC_DIACRITICS}


def strip_diacritics(text):
    """
    Remove Arabic diacritical marks (tashkeel/harakat) from `text`.

    Useful for normalizing text before search, comparison, or indexing,
    since diacritics are often optional and inconsistently applied.

    Args:
        text (str): Input text.

    Returns:
        str: Text with diacritics removed.

    Example:
        >>> strip_diacritics("مَرْحَبًا")
        'مرحبا'
    """
    return text.translate(_DIACRITICS_TRANSLATION)


def normalize_alef(text):
    """
    Normalize variant forms of Alef (أ, إ, آ) to the bare Alef (ا).

    A common preprocessing step for Arabic/Persian/Urdu search and
    comparison, since spelling variants are frequently used interchangeably.

    Args:
        text (str): Input text.

    Returns:
        str: Text with Alef variants normalized.

    Example:
        >>> normalize_alef("أحمد إبراهيم آدم")
        'احمد ابراهيم ادم'
    """
    return re.sub(r"[أإآ]", "ا", text)


# ---------------------------------------------------------------------------
# Public API surface
# ---------------------------------------------------------------------------
__all__ = list(_string.__all__) + [
    # Core classes & registry
    "LanguageCharset", "QuranicCharset", "LANGUAGES",
    # Language objects
    "arabic", "persian", "urdu", "pashto", "kurdish_sorani",
    "sindhi", "uyghur", "kashmiri", "punjabi_shahmukhi", "quranic",
    # Lookup helpers
    "get_language", "list_languages",
    # Detection utilities
    "is_arabing_char", "contains_arabing",
    # Digit systems & conversion
    "ARABIC_INDIC_DIGITS", "EXTENDED_ARABIC_INDIC_DIGITS", "translate_digits",
    # Normalization
    "ARABIC_DIACRITICS", "strip_diacritics", "normalize_alef",
    # Qur'anic-specific constants
    "QURANIC_ANNOTATION_SIGNS", "QURANIC_STRUCTURAL_MARKS",
    "QURANIC_RECITATION_MARKS", "QURANIC_HONORIFIC_SIGNS",
    # Special formatting characters
    "ZWNJ", "ZWJ",
    # Aggregates
    "arabing_alphabetic", "arabing_digits",
    "arabing_punctuation", "arabing_all_characters",
    "arabing_printable", "all_characters",
] + _DYNAMIC_NAMES


# ---------------------------------------------------------------------------
# Demonstration (only runs when executed directly, not on import)
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("Supported languages:", list_languages())
    print()

    for lang in _ALL_LANGUAGE_OBJECTS:
        print(f"--- {lang.name} ({lang.code}) ---")
        print("Letters     :", lang.alphabetic)
        print("Digits      :", lang.digits)
        print("Punctuation :", lang.punctuation)
        print()

    print("ASCII letters (from standard string module):", ascii_letters)
    print("Arabic-script union alphabetic:", arabing_alphabetic)
    print("Full all_characters length:", len(all_characters))

    sample = "سال ۲۰۲۴ مَرْحَبًا أحمد"
    print("\nSample text:", sample)
    print("Contains Arabic script?", contains_arabing(sample))
    print("Digits -> Latin:", translate_digits(sample, to="latin"))
    print("Diacritics stripped:", strip_diacritics(sample))
    print("Alef normalized:", normalize_alef(sample))
