"""
Core charset container classes used throughout `arabing`.
"""
from string import whitespace

from ._detection import is_arabing_char

__all__ = ["LanguageCharset", "QuranicCharset", "EmojiCharset"]


def _split_by_script(chars):
    """Partition `chars` into (native, common) by Arabic-block membership."""
    native = "".join(ch for ch in chars if is_arabing_char(ch))
    common = "".join(ch for ch in chars if not is_arabing_char(ch))
    return native, common


class LanguageCharset:
    """
    Character inventory for a single Arabic-script-based language.
    ...
    Attributes:
        ...
        alphabetic (str): The language's alphabetic characters.
        digits (str): The language's native digit characters (0-9).
        alphanumeric (str): alphabetic + digits (does NOT include
                    `digit_separators`; see below).
        digit_separators (str): Decimal/thousands/date separators and
                    percent sign used alongside digits. NOT punctuation.
        ...
    """

    __slots__ = (
        "name", "code", "slug",
        "alphabetic", "digits", "alphanumeric", "digit_separators",
        "sentence_punctuation", "opening_brackets", "closing_brackets",
        "quotation_marks", "mathematical_signs", "special_signs", "tatweel",
        "punctuation", "native_punctuation", "common_punctuation",
        "all_characters",
    )

    def __init__(self, name, code, slug, alphabetic, digits,
                 sentence_punctuation, opening_brackets, closing_brackets,
                 quotation_marks, mathematical_signs, special_signs, tatweel,
                 digit_separators):
        self.name = name
        self.code = code
        self.slug = slug
        self.alphabetic = alphabetic
        self.digits = digits
        self.alphanumeric = alphabetic + digits
        self.digit_separators = digit_separators

        self.sentence_punctuation = sentence_punctuation
        self.opening_brackets = opening_brackets
        self.closing_brackets = closing_brackets
        self.quotation_marks = quotation_marks
        self.mathematical_signs = mathematical_signs
        self.special_signs = special_signs
        self.tatweel = tatweel

        self.punctuation = (
            sentence_punctuation + opening_brackets + closing_brackets +
            quotation_marks + mathematical_signs + special_signs + tatweel
        )
        self.native_punctuation, self.common_punctuation = _split_by_script(
            self.punctuation
        )

        self.all_characters = (
            alphabetic + digits + digit_separators + self.punctuation
        )

    @property
    def brackets(self):
        """str: Opening and closing brackets combined."""
        return self.opening_brackets + self.closing_brackets

    @property
    def printable(self):
        """str: All characters plus ASCII whitespace."""
        return self.all_characters + whitespace

    def __repr__(self):
        return f"<LanguageCharset {self.name!r} ({self.code})>"

    def __contains__(self, ch):
        return ch in self.all_characters


class QuranicCharset(LanguageCharset):
    """
    Extends LanguageCharset with category-specific character sets unique
    to Qur'anic (Uthmani) orthography: recitation vowel marks, waqf
    (pause) signs, structural markers, fine-grained recitation marks,
    and honorific signs. These are liturgical/structural marks, not
    punctuation, and remain separate categories just as before.
    """

    __slots__ = (
        "diacritics", "annotation_signs", "structural_marks",
        "recitation_marks", "honorific_signs",
    )

    def __init__(self, name, code, slug, alphabetic, digits,
                 sentence_punctuation, opening_brackets, closing_brackets,
                 quotation_marks, mathematical_signs, special_signs, tatweel,
                 digit_separators,
                 diacritics, annotation_signs, structural_marks,
                 recitation_marks, honorific_signs):
        super().__init__(
            name, code, slug, alphabetic, digits,
            sentence_punctuation, opening_brackets, closing_brackets,
            quotation_marks, mathematical_signs, special_signs, tatweel,
            digit_separators,
        )
        self.diacritics = diacritics
        self.annotation_signs = annotation_signs
        self.structural_marks = structural_marks
        self.recitation_marks = recitation_marks
        self.honorific_signs = honorific_signs
        self.all_characters += (
            diacritics + annotation_signs + structural_marks +
            recitation_marks + honorific_signs
        )


class EmojiCharset:
    """
    Categorized emoji character inventory.

    Emojis aren't tied to a single "language", so instead of
    alphabetic/digit/punctuation groupings, this class organizes emoji
    by common semantic category (faces, hearts, animals, flags, etc.).
    """

    __slots__ = (
        "faces", "emotions", "hand_gestures", "hearts", "animals",
        "food_and_drink", "activities", "travel_and_places",
        "objects", "symbols", "flags", "all_characters",
    )

    def __init__(self, faces, emotions, hand_gestures, hearts, animals,
                 food_and_drink, activities, travel_and_places,
                 objects, symbols, flags):
        self.faces = faces
        self.emotions = emotions
        self.hand_gestures = hand_gestures
        self.hearts = hearts
        self.animals = animals
        self.food_and_drink = food_and_drink
        self.activities = activities
        self.travel_and_places = travel_and_places
        self.objects = objects
        self.symbols = symbols
        self.flags = flags
        self.all_characters = (
            faces + emotions + hand_gestures + hearts + animals +
            food_and_drink + activities + travel_and_places +
            objects + symbols + flags
        )

    @property
    def categories(self):
        """dict[str, str]: category name -> character string."""
        return {
            name: getattr(self, name)
            for name in self.__slots__
            if name != "all_characters"
        }

    def __repr__(self):
        return f"<EmojiCharset {len(self.all_characters)} codepoints>"

    def __contains__(self, ch):
        return ch in self.all_characters