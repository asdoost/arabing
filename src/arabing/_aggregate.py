"""Aggregate constants across all supported languages and emoji."""
from string import printable, whitespace
from ._languages import _ALL_LANGUAGE_OBJECTS, quranic
from ._emoji_data import emoji

__all__ = [
    "arabing_alphabetic", "arabing_digits", "arabing_alphanumeric",
    "arabing_digit_separators",
    "arabing_sentence_punctuation", "arabing_opening_brackets",
    "arabing_closing_brackets", "arabing_brackets", "arabing_quotation_marks",
    "arabing_mathematical_signs", "arabing_special_signs", "arabing_tatweel",
    "arabing_punctuation", "arabing_native_punctuation",
    "arabing_common_punctuation",
    "arabing_all_characters", "arabing_printable", "all_characters",
]


def _dedup_concat(strings):
    """Concatenate strings, preserving order, removing duplicate chars."""
    seen = set()
    result = []
    for s in strings:
        for ch in s:
            if ch not in seen:
                seen.add(ch)
                result.append(ch)
    return "".join(result)


arabing_alphabetic = _dedup_concat(l.alphabetic for l in _ALL_LANGUAGE_OBJECTS)
arabing_digits = _dedup_concat(l.digits for l in _ALL_LANGUAGE_OBJECTS)
# Alphabetic and digit character sets never overlap, so a plain
# concatenation (rather than a fresh dedup pass) is sufficient here.
arabing_alphanumeric = arabing_alphabetic + arabing_digits

arabing_digit_separators = _dedup_concat(
    l.digit_separators for l in _ALL_LANGUAGE_OBJECTS
)

arabing_sentence_punctuation = _dedup_concat(
    l.sentence_punctuation for l in _ALL_LANGUAGE_OBJECTS
)
arabing_opening_brackets = _dedup_concat(
    l.opening_brackets for l in _ALL_LANGUAGE_OBJECTS
)
arabing_closing_brackets = _dedup_concat(
    l.closing_brackets for l in _ALL_LANGUAGE_OBJECTS
)
arabing_brackets = arabing_opening_brackets + arabing_closing_brackets
arabing_quotation_marks = _dedup_concat(
    l.quotation_marks for l in _ALL_LANGUAGE_OBJECTS
)
arabing_mathematical_signs = _dedup_concat(
    l.mathematical_signs for l in _ALL_LANGUAGE_OBJECTS
)
arabing_special_signs = _dedup_concat(
    l.special_signs for l in _ALL_LANGUAGE_OBJECTS
)
arabing_tatweel = _dedup_concat(l.tatweel for l in _ALL_LANGUAGE_OBJECTS)

arabing_punctuation = _dedup_concat(l.punctuation for l in _ALL_LANGUAGE_OBJECTS)
arabing_native_punctuation = _dedup_concat(
    l.native_punctuation for l in _ALL_LANGUAGE_OBJECTS
)
arabing_common_punctuation = _dedup_concat(
    l.common_punctuation for l in _ALL_LANGUAGE_OBJECTS
)

arabing_all_characters = (
    arabing_alphabetic + arabing_digits + arabing_digit_separators +
    arabing_punctuation +
    quranic.diacritics + quranic.annotation_signs +
    quranic.structural_marks + quranic.recitation_marks +
    quranic.honorific_signs
)
arabing_printable = arabing_all_characters + whitespace

all_characters = _dedup_concat(
    [printable, arabing_all_characters, emoji.all_characters]
)