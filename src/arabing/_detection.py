"""
Unicode-block based detection utilities for Arabic-script text and emoji.

Emoji handling is grapheme-cluster aware (via the third-party `regex`
package) so multi-codepoint sequences -- flags, ZWJ combinations, skin-
tone modifiers -- are treated, extracted, and stripped as single units
rather than being split into individual codepoints.
"""
import re

try:
    import regex as _regex
except ImportError as exc:  # pragma: no cover
    raise ImportError(
        "arabing requires the third-party 'regex' package for "
        "grapheme-cluster-aware emoji handling. Install it with "
        "`pip install regex`."
    ) from exc

__all__ = [
    "is_arabing_char", "contains_arabing",
    "is_emoji_char", "contains_emoji", "strip_emojis", "extract_emojis",
]

# ---------------------------------------------------------------------------
# Arabic-script detection
# ---------------------------------------------------------------------------
_ARABIC_UNICODE_RANGES = (
    (0x0600, 0x06FF), (0x0750, 0x077F), (0x0870, 0x089F), (0x08A0, 0x08FF),
    (0xFB50, 0xFDFF), (0xFE70, 0xFEFF), (0x10E60, 0x10E7F),
    (0x1EC70, 0x1ECBF), (0x1EE00, 0x1EEFF),
)

_ARABIC_PATTERN = re.compile(
    "[" + "".join(f"\\U{s:08X}-\\U{e:08X}" for s, e in _ARABIC_UNICODE_RANGES) + "]"
)


def is_arabing_char(ch):
    """bool: True if `ch` belongs to an Arabic-script Unicode block."""
    if not ch:
        return False
    codepoint = ord(ch)
    return any(s <= codepoint <= e for s, e in _ARABIC_UNICODE_RANGES)


def contains_arabing(text):
    """bool: True if `text` contains at least one Arabic-script character."""
    return bool(_ARABIC_PATTERN.search(text))


# ---------------------------------------------------------------------------
# Emoji detection
# ---------------------------------------------------------------------------
_EMOJI_UNICODE_RANGES = (
    (0x1F300, 0x1F5FF), (0x1F600, 0x1F64F), (0x1F680, 0x1F6FF),
    (0x1F700, 0x1F77F), (0x1F780, 0x1F7FF), (0x1F800, 0x1F8FF),
    (0x1F900, 0x1F9FF), (0x1FA00, 0x1FA6F), (0x1FA70, 0x1FAFF),
    (0x1F100, 0x1F1FF),  # enclosed alphanumeric supplement + regional indicators
    (0x1F200, 0x1F2FF),  # enclosed ideographic supplement
    (0x2300, 0x23FF),    # misc technical (⌚⏰⏱️...)
    (0x2460, 0x24FF),    # enclosed alphanumerics (Ⓜ️)
    (0x25A0, 0x25FF),    # geometric shapes (◼️◻️▪️...)
    (0x2600, 0x26FF), (0x2700, 0x27BF), (0x2B00, 0x2BFF),
    (0x3200, 0x32FF),    # enclosed CJK letters/months (㊗️㊙️)
    (0xFE00, 0xFE0F),    # variation selectors
    (0x200D, 0x200D),    # ZWJ
)

# One-off codepoints in otherwise "non-emoji" blocks.
_EMOJI_SINGLETONS = "\u00A9\u00AE\u2122\u2139\u203C\u2049\u303D"

_EMOJI_PATTERN = re.compile(
    "[" + "".join(f"\\U{s:08X}-\\U{e:08X}" for s, e in _EMOJI_UNICODE_RANGES)
    + re.escape(_EMOJI_SINGLETONS) + "]"
)

# Compiled once; walks text as user-perceived grapheme clusters.
_GRAPHEME_PATTERN = _regex.compile(r"\X")


def is_emoji_char(ch):
    """bool: True if `ch` belongs to an emoji-related Unicode block."""
    if not ch:
        return False
    if ch in _EMOJI_SINGLETONS:
        return True
    codepoint = ord(ch)
    return any(s <= codepoint <= e for s, e in _EMOJI_UNICODE_RANGES)


def contains_emoji(text):
    """bool: True if `text` contains at least one emoji character."""
    return bool(_EMOJI_PATTERN.search(text))


def _is_emoji_grapheme(grapheme):
    return any(is_emoji_char(ch) for ch in grapheme)


def strip_emojis(text):
    """
    Remove emoji (including multi-codepoint sequences) from `text`.

    Example:
        >>> strip_emojis("مرحبا 👋 يا صديقي 😊")
        'مرحبا  يا صديقي '
    """
    return "".join(
        g for g in _GRAPHEME_PATTERN.findall(text) if not _is_emoji_grapheme(g)
    )


def extract_emojis(text):
    """
    Extract emoji graphemes (flags, ZWJ sequences, etc. kept whole).

    Example:
        >>> extract_emojis("مرحبا 👋 يا صديقي 😊")
        ['👋', '😊']
    """
    return [g for g in _GRAPHEME_PATTERN.findall(text) if _is_emoji_grapheme(g)]