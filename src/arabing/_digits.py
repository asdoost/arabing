"""Digit-system conversion utilities."""
import string as _string
from ._constants import ARABIC_INDIC_DIGITS, EXTENDED_ARABIC_INDIC_DIGITS

__all__ = ["translate_digits"]

_DIGIT_SYSTEMS = {
    "latin": _string.digits,
    "arabic_indic": ARABIC_INDIC_DIGITS,
    "extended_arabic_indic": EXTENDED_ARABIC_INDIC_DIGITS,
}


def translate_digits(text, to="latin", from_=None):
    """
    Convert digits in `text` between digit systems.

    Args:
        text (str): Input text.
        to (str): 'latin', 'arabic_indic', or 'extended_arabic_indic'.
        from_ (str, optional): Restrict conversion to one source system.

    Example:
        >>> translate_digits("سال 2024", to="extended_arabic_indic")
        'سال ۲۰۲۴'
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
        for src_char, tgt_char in zip(_DIGIT_SYSTEMS[source], target_digits):
            translation_map[ord(src_char)] = tgt_char

    return text.translate(translation_map)