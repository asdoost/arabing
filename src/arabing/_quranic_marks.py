"""
Qur'anic (Uthmani script) specific Unicode marks.

These live in the Arabic Unicode block but are specific to Qur'anic
recitation/orthography and aren't used in everyday Arabic, Persian, etc.
"""

# Extended vowel/recitation marks (beyond basic tashkeel).
QURANIC_EXTENDED_VOWEL_MARKS = (
    "\u0657\u0658\u0659\u065A\u065B\u065C\u065D\u065E\u065F"
)

# Waqf (pause/stop) annotation signs.
QURANIC_ANNOTATION_SIGNS = "\u06D6\u06D7\u06D8\u06D9\u06DA\u06DB\u06DC"

# End-of-ayah, rub-el-hizb, sajdah markers.
QURANIC_STRUCTURAL_MARKS = "\u06DD\u06DE\u06E9"

# Fine-grained recitation marks across Mus'haf printing styles.
QURANIC_RECITATION_MARKS = (
    "\u06DF\u06E0\u06E1\u06E2\u06E3\u06E4\u06E5\u06E6"
    "\u06E7\u06E8\u06EA\u06EB\u06EC\u06ED"
)

# Honorific signs (sallallahu 'alayhi wasallam, radi allahu 'anhu, etc.).
QURANIC_HONORIFIC_SIGNS = (
    "\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0617\u0618\u0619\u061A"
)