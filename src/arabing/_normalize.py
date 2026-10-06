"""Text normalization helpers."""
import re
from ._constants import ARABIC_DIACRITICS
from ._quranic_marks import *

__all__ = ["strip_diacritics", "normalize_alef"]

_DIACRITICS_TRANSLATION = {ord(c): None for c in ARABIC_DIACRITICS}

_UTHMANI_SIGNS = (
    QURANIC_EXTENDED_VOWEL_MARKS + 
    QURANIC_ANNOTATION_SIGNS + 
    QURANIC_HONORIFIC_SIGNS + 
    QURANIC_RECITATION_MARKS
    )

_UTHMANI_TRANSLATION = {ord(c): None for c in _UTHMANI_SIGNS}


def strip_diacritics(text):
    """
    Remove Arabic diacritical marks (tashkeel/harakat).

    Example:
        >>> strip_diacritics("مَرْحَبًا")
        'مرحبا'
    """
    return text.translate(_DIACRITICS_TRANSLATION)


def strip_uthmani_sign(text: str) -> str:
    """
    Remove Uthmani signs.
    Example:
        >>> strip_uthmani_sign("ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ")
        'ٱلحمد لله رب ٱلعلمين'
    """
    
    _UTHMANI_TRANSLATION.update(_DIACRITICS_TRANSLATION)
    
    text = text.translate(_UTHMANI_TRANSLATION)
    
    return re.sub(f'[{QURANIC_STRUCTURAL_MARKS}]+', ' ', text)
    

def normalize_alef(text):
    """
    Normalize Alef variants (أ, إ, آ) to bare Alef (ا).

    Example:
        >>> normalize_alef("أحمد إبراهيم آدم")
        'احمد ابراهيم ادم'
    """
    return re.sub(r"[أإآ]", "ا", text)


if __name__=="__main__":
    print(strip_uthmani_sign("ٱلۡحَمۡدُ لِلَّهِ رَبِّ ٱلۡعَٰلَمِينَ"))