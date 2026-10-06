"""Per-language charset definitions and the language lookup registry."""
from ._charsets import LanguageCharset, QuranicCharset
from ._constants import (
    ARABIC_INDIC_DIGITS, EXTENDED_ARABIC_INDIC_DIGITS,
    ARABIC_DIGIT_SEPARATORS, SENTENCE_PUNCTUATION, URDU_STYLE_FULL_STOP,
    OPENING_BRACKETS, CLOSING_BRACKETS, QUOTATION_MARKS,
    MATHEMATICAL_SIGNS, SPECIAL_SIGNS, TATWEEL_SIGN, ARABIC_DIACRITICS,
)
from ._quranic_marks import (
    QURANIC_EXTENDED_VOWEL_MARKS, QURANIC_ANNOTATION_SIGNS,
    QURANIC_STRUCTURAL_MARKS, QURANIC_RECITATION_MARKS,
    QURANIC_HONORIFIC_SIGNS,
)

# Sentence punctuation for Urdu, Kashmiri, and Punjabi (Shahmukhi), which
# additionally use the native Arabic-block full stop (۔).
_URDU_FAMILY_SENTENCE_PUNCTUATION = SENTENCE_PUNCTUATION + URDU_STYLE_FULL_STOP

# Punctuation categories identical across every currently supported
# language (brackets/quotes/math/special-signs/tatweel/digit-separators).
_SHARED_PUNCTUATION_KWARGS = dict(
    opening_brackets=OPENING_BRACKETS,
    closing_brackets=CLOSING_BRACKETS,
    quotation_marks=QUOTATION_MARKS,
    mathematical_signs=MATHEMATICAL_SIGNS,
    special_signs=SPECIAL_SIGNS,
    tatweel=TATWEEL_SIGN,
    digit_separators=ARABIC_DIGIT_SEPARATORS,
)

quranic = QuranicCharset(
    name="Qur'anic Arabic (Uthmani Script)", code="quran", slug="quranic",
    alphabetic="ابتثجحخدذرزسشصضطظعغفقكلمنهويءأإؤئةىٱ",
    digits=ARABIC_INDIC_DIGITS,
    sentence_punctuation=SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
    diacritics=ARABIC_DIACRITICS + QURANIC_EXTENDED_VOWEL_MARKS,
    annotation_signs=QURANIC_ANNOTATION_SIGNS,
    structural_marks=QURANIC_STRUCTURAL_MARKS,
    recitation_marks=QURANIC_RECITATION_MARKS,
    honorific_signs=QURANIC_HONORIFIC_SIGNS,
)

arabic = LanguageCharset(
    name="Arabic", code="ar", slug="arabic",
    alphabetic="ابتثجحخدذرزسشصضطظعغفقكلمنهويءأإؤئةى",
    digits=ARABIC_INDIC_DIGITS,
    sentence_punctuation=SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

persian = LanguageCharset(
    name="Persian", code="fa", slug="persian",
    alphabetic="آبپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی" + "ائء",
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    sentence_punctuation=SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

urdu = LanguageCharset(
    name="Urdu", code="ur", slug="urdu",
    alphabetic="اآبپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوہھءیے",
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    sentence_punctuation=_URDU_FAMILY_SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

pashto = LanguageCharset(
    name="Pashto", code="ps", slug="pashto",
    alphabetic="اآبپتټثجځچڅحخدډذرړزژږسشښصضطظعغفقکګلمنڼوهءيیېۍ",
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    sentence_punctuation=SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

kurdish_sorani = LanguageCharset(
    name="Kurdish (Sorani)", code="ckb", slug="kurdish_sorani",
    alphabetic="ابپتجچحخدرڕزژسشعغفڤقکگلڵمنوۆهھیێء",
    digits=ARABIC_INDIC_DIGITS,
    sentence_punctuation=SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

sindhi = LanguageCharset(
    name="Sindhi", code="sd", slug="sindhi",
    alphabetic="ابٻڀتٿٽٺثجڄچڇحخدڌڊڏڍذرڙزسشصضطظعغفڦقکڪگڳڱلمنڻوھءيی",
    digits=ARABIC_INDIC_DIGITS,
    sentence_punctuation=SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

uyghur = LanguageCharset(
    name="Uyghur", code="ug", slug="uyghur",
    alphabetic="اەبپتجچخدرزژسشغفقكگڭلمنھوۇۆۈۋېىي",
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    sentence_punctuation=SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

kashmiri = LanguageCharset(
    name="Kashmiri", code="ks", slug="kashmiri",
    alphabetic="اآءبپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوہھیے",
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    sentence_punctuation=_URDU_FAMILY_SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

punjabi_shahmukhi = LanguageCharset(
    name="Punjabi (Shahmukhi)", code="pnb", slug="punjabi_shahmukhi",
    alphabetic="ابپتٹثجچحخدڈذرڑزژسشصضطظعغفقکگلمنںوہھءیے",
    digits=EXTENDED_ARABIC_INDIC_DIGITS,
    sentence_punctuation=_URDU_FAMILY_SENTENCE_PUNCTUATION,
    **_SHARED_PUNCTUATION_KWARGS,
)

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


def get_language(identifier):
    """
    Retrieve the LanguageCharset object for a given language name or code.

    Example:
        >>> get_language("fa").sentence_punctuation
    """
    key = identifier.strip().lower()
    if key not in LANGUAGES:
        raise KeyError(
            f"Unknown language identifier: {identifier!r}. "
            f"Available identifiers: {sorted(LANGUAGES.keys())}"
        )
    return LANGUAGES[key]


def list_languages():
    """list[str]: Sorted list of supported (unique) language names."""
    return sorted({lang.name for lang in _ALL_LANGUAGE_OBJECTS})