# arabing 🕌🔤

**arabing** (Arabic+string) is a Python library that extends the standard `string` module with full character-set support for languages written in **Arabic-derived scripts** — Arabic, Persian, Urdu, Pashto, Kurdish, Sindhi, Uyghur, Kashmiri, and Punjabi (Shahmukhi).

It is a **drop-in replacement** for Python's built-in `string` module: everything you already use (`ascii_letters`, `digits`, `punctuation`, `capwords()`, `Template`, etc.) works exactly the same, plus you get equivalent letter/digit/punctuation data for Arabic-script languages, along with useful text-processing utilities (digit conversion, diacritic stripping, Alef normalization, script detection).

---

## ✨ Features

- 🔤 **Per-language character sets** — letters, digits, punctuation, and combined sets for 10 languages/scripts
- 📿 **Qur'anic (Uthmani script) support** — dedicated categories for tashkeel, waqf/pause signs, structural marks, recitation marks, and honorific signs
- 🌍 **Aggregate constants** — union of all Arabic-script letters/digits/punctuation across every supported language
- 🧩 **100% compatible with the standard `string` module** — `ascii_letters`, `whitespace`, `printable`, `capwords()`, `Formatter`, `Template` all included
- 🔎 **Script detection** — check if a character or string contains Arabic-script text
- 🔢 **Digit conversion** — convert between Latin, Arabic-Indic (٠١٢), and Extended Arabic-Indic (۰۱۲) digit systems
- 🧹 **Text normalization** — strip diacritics (tashkeel), normalize Alef variants
- 📚 **Language registry** — look up any language by name or ISO 639 code
- 🪶 **Zero dependencies** — pure Python standard library only

---

## 📦 Installation

```bash
pip install arabing
```

Or, since it's a single-file library, just download `arabing.py` and drop it into your project:

```bash
curl -O https://raw.githubusercontent.com/<your-username>/arabing/main/arabing.py
```

---

## 🚀 Quick Start

```python
import arabing

# Works exactly like the standard `string` module
print(arabing.ascii_uppercase)          # ABCDEFGHIJKLMNOPQRSTUVWXYZ
print(arabing.capwords("hello world"))  # Hello World

# Arabic-script language support
print(arabing.arabic_letters)           # ابتثجحخد...ءأإؤئةى
print(arabing.persian_digits)           # ۰۱۲۳۴۵۶۷۸۹
print(arabing.urdu_punctuation)         # ،؛؟٪٫٬ـ«»۔
print(arabing.pashto_all_characters)    # letters + digits + punctuation combined
```

---

## 🌐 Supported Languages

| Language                          | ISO Code | Slug (variable prefix) |
|-----------------------------------|----------|--------------------------|
| Arabic                            | `ar`     | `arabic`                 |
| Persian / Farsi                   | `fa`     | `persian`                |
| Urdu                              | `ur`     | `urdu`                   |
| Pashto                            | `ps`     | `pashto`                 |
| Kurdish (Sorani)                  | `ckb`    | `kurdish_sorani`         |
| Sindhi                            | `sd`     | `sindhi`                 |
| Uyghur                            | `ug`     | `uyghur`                 |
| Kashmiri                          | `ks`     | `kashmiri`               |
| Punjabi (Shahmukhi)               | `pnb`    | `punjabi_shahmukhi`      |
| Qur'anic Arabic (Uthmani Script)  | `quran`  | `quranic`                |

> ℹ️ The Qur'anic entry can also be looked up via `"quranic"`, `"uthmani"`, or `"ar-quran"`.

For **every** language, four constants are auto-generated using the slug:

```python
<slug>_letters          # alphabetic characters
<slug>_digits           # native digit characters
<slug>_punctuation      # script-specific punctuation
<slug>_all_characters   # letters + digits + punctuation combined
```

Example:

```python
arabing.arabic_letters
arabing.persian_digits
arabing.urdu_punctuation
arabing.kurdish_sorani_all_characters
```

---

## 📖 API Reference

### Language Objects

Each language is also available as a `LanguageCharset` object with richer access:

```python
arabing.arabic
arabing.persian
arabing.urdu
arabing.pashto
arabing.kurdish_sorani
arabing.sindhi
arabing.uyghur
arabing.kashmiri
arabing.punjabi_shahmukhi
```

Each object exposes:

| Attribute         | Description                                  |
|-------------------|-----------------------------------------------|
| `.name`           | Human-readable language name                  |
| `.code`           | ISO 639 language code                         |
| `.alphabetic`     | Alphabetic characters                         |
| `.digits`         | Native digit characters                       |
| `.punctuation`    | Script-specific punctuation                   |
| `.all_characters` | Combined letters + digits + punctuation       |
| `.printable`      | `all_characters` + ASCII whitespace           |

```python
fa = arabing.persian
print(fa.name)            # Persian
print(fa.alphabetic)      # ابپتثجچحخد...
print("ا" in fa)          # True (supports `in` operator)
```

---

### Language Registry

```python
arabing.get_language(identifier)
```
Look up a `LanguageCharset` by name or ISO code (case-insensitive).

```python
arabing.get_language("fa")       # Persian
arabing.get_language("Urdu")     # Urdu
arabing.get_language("ckb")      # Kurdish (Sorani)
```

```python
arabing.list_languages()
```
Returns a sorted list of all supported language names.

```python
>>> arabing.list_languages()
['Arabic', 'Kashmiri', 'Kurdish (Sorani)', 'Pashto', 'Persian',
 'Punjabi (Shahmukhi)', 'Sindhi', 'Urdu', 'Uyghur']
```

---

### Aggregate Constants

Union of character sets across **all** supported languages:

| Constant                          | Description                                   |
|-----------------------------------|-----------------------------------------------|
| `arabing_alphabetic`        | Union of all letters across all languages     |
| `arabing_digits`            | Union of all digits across all languages      |
| `arabing_punctuation`       | Union of all punctuation across all languages |
| `arabing_all_characters`    | All of the above combined                     |
| `arabing_printable`         | `arabing_all_characters` + whitespace   |
| `all_characters`                  | ASCII `printable` + `arabing_all_characters` |

```python
print(arabing.arabing_alphabetic)
print(len(arabing.all_characters))
```

---

### Qur'anic Character Categories

The Qur'an (in Uthmani script) uses many special Unicode characters beyond
the standard Arabic alphabet — recitation (tajweed) vowel marks, waqf
(pause) signs, structural markers, and honorific signs. `arabing` exposes
these as **separate categories** rather than lumping them into generic
"punctuation", since each serves a distinct purpose.

| Constant                     | Description                                                        |
|-------------------------------|---------------------------------------------------------------------|
| `quranic_letters`             | Base Uthmani letters (Arabic alphabet + alef wasla `ٱ`)             |
| `quranic_digits`               | Arabic-Indic digits (٠١٢٣٤٥٦٧٨٩)                                    |
| `quranic_punctuation`          | Common Arabic-script punctuation                                    |
| `quranic_diacritics`           | Tashkeel/harakat + extended Qur'anic vowel marks                    |
| `quranic_annotation_signs`     | Waqf (pause/stop) signs: `ۖ ۗ ۘ ۙ ۚ ۛ ۜ`                            |
| `quranic_structural_marks`     | End-of-ayah `۝`, start-of-rub-el-hizb `۞`, place-of-sajdah `۩`      |
| `quranic_recitation_marks`     | Fine-grained small high/low recitation marks                        |
| `quranic_honorific_signs`      | Honorific signs (e.g. ﷺ-style annotations: SAW, AS, RA, etc.)       |
| `quranic_all_characters`       | All of the above categories combined                                |

```python
import arabing

# Access via flat constants:
print(arabing.quranic_annotation_signs)   # ۖۗۘۙۚۛۜ
print(arabing.quranic_structural_marks)   # ۝۞۩
print(arabing.quranic_honorific_signs)    # ؘؙؚؐؑؒؓؔؕؖؗ

# Access via the QuranicCharset object (richer, includes .name/.code):
q = arabing.quranic
print(q.name)               # Qur'anic Arabic (Uthmani Script)
print(q.diacritics)         # tashkeel + extended vowel marks
print(q.annotation_signs)   # waqf signs
print(q.all_characters)     # every category combined

# Registry lookup also works:
q2 = arabing.get_language("quran")
assert q2 is q

# Identifying waqf signs in a Qur'anic text sample:
sample = "وَقَالَ الَّذِينَ كَفَرُوا۟ لَن نُّؤْمِنَ ۖ بِهَـٰذَا الْقُرْءَانِ"

waqf_found = [ch for ch in sample if ch in arabing.quranic_annotation_signs]
print(waqf_found)  # ['ۖ']
```

### Script Detection

```python
arabing.is_arabing_char(ch)
```
Check if a single character belongs to an Arabic-script Unicode block.

```python
>>> arabing.is_arabing_char("ا")
True
>>> arabing.is_arabing_char("A")
False
```

```python
arabing.contains_arabing(text)
```
Check if any character in a string is Arabic-script.

```python
>>> arabing.contains_arabing("Hello مرحبا")
True
```

---

### Digit Conversion

```python
arabing.translate_digits(text, to="latin", from_=None)
```
Convert digits between digit systems: `"latin"`, `"arabic_indic"` (٠١٢٣٤٥٦٧٨٩), `"extended_arabic_indic"` (۰۱۲۳۴۵۶۷۸۹).

```python
>>> arabing.translate_digits("سال 2024", to="extended_arabic_indic")
'سال ۲۰۲۴'

>>> arabing.translate_digits("۱۲۳", to="latin")
'123'
```

---

### Text Normalization

```python
arabing.strip_diacritics(text)
```
Remove Arabic diacritics (tashkeel/harakat) — e.g. for search/indexing.

```python
>>> arabing.strip_diacritics("مَرْحَبًا")
'مرحبا'
```

```python
arabing.normalize_alef(text)
```
Normalize Alef variants (أ, إ, آ) to bare Alef (ا).

```python
>>> arabing.normalize_alef("أحمد إبراهيم آدم")
'احمد ابراهيم ادم'
```

---

### Full `string`-module Compatibility

Since `arabing` re-exports everything from the standard `string` module, you can use it as a direct replacement:

```python
import arabing as string

string.ascii_letters
string.digits
string.punctuation
string.whitespace
string.printable
string.capwords("hello world")
string.Template("Hello $name").substitute(name="World")
```

---

## 🧪 Full Example

```python
import arabing

sample = "سال ۲۰۲۴ مَرْحَبًا أحمد"

print("Contains Arabic script?", arabing.contains_arabing(sample))
print("Digits → Latin:", arabing.translate_digits(sample, to="latin"))
print("Diacritics stripped:", arabing.strip_diacritics(sample))
print("Alef normalized:", arabing.normalize_alef(sample))

persian = arabing.get_language("fa")
print(f"{persian.name} letters:", persian.alphabetic)
print(f"{persian.name} digits:", persian.digits)
```

**Output:**
```
Contains Arabic script? True
Digits → Latin: سال 2024 مَرْحَبًا أحمد
Diacritics stripped: سال ۲۰۲۴ مرحبا أحمد
Alef normalized: سال ۲۰۲۴ مَرْحَبًا احمد
```

---

## ⚠️ Notes & Caveats

- Character inventories reflect **commonly used, practical** letter/digit/punctuation sets for each language. Some languages have regional or historical orthographic variants.
- For linguistically critical applications (e.g. NLP corpora, government documents), validate character sets against an authoritative orthographic standard for your specific use case/dialect.
- Diacritic stripping and Alef normalization are lossy operations intended for search/matching — not for preserving original text fidelity.
- The Qur'anic (`quranic`) character set reflects standard Unicode-encoded
  Uthmani script marks. Different Mus'haf printings (e.g. Madinah Mus'haf,
  IndoPak style) may use slightly different subsets of recitation marks —
  verify against your target Mus'haf edition for recitation-critical apps.
---

## 🤝 Contributing

Contributions are welcome! If you'd like to:
- Add a new Arabic-script language
- Improve/correct a character set
- Add new utility functions

Please open an issue or submit a pull request.

### Adding a new language
1. Define a new `LanguageCharset` instance following the existing pattern.
2. Add it to `_ALL_LANGUAGE_OBJECTS` and the `LANGUAGES` registry dict.
3. Submit a PR with sources/references for the character set used.

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

## 🙏 Acknowledgments

Inspired by Python's built-in [`string`](https://docs.python.org/3/library/string.html) module, extended to serve the ~1.5 billion+ speakers of languages written in Arabic-derived scripts.