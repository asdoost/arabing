"""Emoji category data and lookup helpers."""
from ._charsets import EmojiCharset

emoji = EmojiCharset(
    faces=(
        "😀😃😄😁😆😅😂🤣😊😇🙂🙃😉😌😍🥰😘😗😙😚😋😛😝😜🤪🤨🧐🤓😎🥸"
        "🤩🥳😏😒😞😔😟😕🙁☹️😣😖😫😩🥺😢😭😤😠😡🤬🤯😳🥵🥶😱😨😰😥😓"
        "🤗🤔🤭🤫🤥😶😐😑😬🙄😯😦😧😮😲🥱😴🤤😪😵🤐🥴🤢🤮🤧😷🤒🤕🤑🤠"
        "😈👿🤡💩👻💀☠️👽👾🤖🎃"
    ),
    emotions="💯💢💥💫💦💨🕳️💣💬🗨️🗯️💭💤",
    hand_gestures=(
        "👋🤚🖐️✋🖖👌🤌🤏✌️🤞🤟🤘🤙👈👉👆🖕👇☝️👍👎✊👊🤛🤜👏🙌👐🤲🤝🙏"
    ),
    hearts="❤️🧡💛💚💙💜🖤🤍🤎💔❣️💕💞💓💗💖💘💝💟",
    animals=(
        "🐶🐱🐭🐹🐰🦊🐻🐼🐨🐯🦁🐮🐷🐽🐸🐵🙈🙉🙊🐒🐔🐧🐦🐤🐣🐥🦆🦅🦉🦇"
        "🐺🐗🐴🦄🐝🐛🦋🐌🐞🐜🦟🦗🕷️🕸️🦂🐢🐍🦎🦖🦕🐙🦑🦐🦞🦀🐡🐠🐟🐬🐳"
        "🐋🦈🐊🐅🐆🦓🦍🐘🦛🦏🐪🐫🦒🦘🐃🐂🐄🐎🐖🐏🐑🦙🐐🦌🐕🐩🐈🐓🦃"
    ),
    food_and_drink=(
        "🍏🍎🍐🍊🍋🍌🍉🍇🍓🍈🍒🍑🥭🍍🥥🥝🍅🍆🥑🥦🥬🥒🌶️🌽🥕🧄🧅🥔🍠🥐"
        "🥯🍞🥖🥨🧀🥚🍳🧈🥞🧇🥓🥩🍗🍖🌭🍔🍟🍕🥪🥙🧆🌮🌯🥗🥘🥫🍝🍜🍲🍛"
        "🍣🍱🥟🦪🍤🍙🍚🍘🍥🥠🥮🍢🍡🍧🍨🍦🥧🧁🍰🎂🍮🍭🍬🍫🍿🍩🍪🌰🥜🍯"
        "🥛🍼☕🍵🧃🥤🍶🍺🍻🥂🍷🥃🍸🍹🧉🍾"
    ),
    activities=(
        "⚽🏀🏈⚾🥎🎾🏐🏉🥏🎱🪀🏓🏸🏒🏑🥍🏏🥅⛳🪁🏹🎣🤿🥊🥋🎽🛹🛼🛷⛸️"
        "🥌🎿⛷️🏂🏋️🤼🤸🤺🤾🏌️🏇🧘🏄🏊🤽🚣🧗🚵🚴🎪🎭🎨🎬🎤🎧🎼🎹🥁🎷🎺"
        "🎸🪕🎻🎲♟️🎯🎳🎮🎰🧩"
    ),
    travel_and_places=(
        "🚗🚕🚙🚌🚎🏎️🚓🚑🚒🚐🛻🚚🚛🚜🛴🚲🛵🏍️🛺🚨🚔🚍🚘🚖🚡🚠🚟"
        "🚃🚋🚞🚝🚄🚅🚈🚂🚆🚇🚊🚉✈️🛫🛬🛩️💺🛰️🚀🛸🚁🛶⛵🚤🛥️🛳️⛴️🚢⚓"
        "⛽🚧🚦🚥🗺️🗿🗽🗼🏰🏯🏟️🎡🎢🎠⛲⛱️🏖️🏝️🏜️🌋⛰️🏔️🗻🏕️⛺🏠🏡🏘️"
        "🏚️🏗️🏭🏢🏬🏣🏤🏥🏦🏨🏪🏫🏩💒🏛️⛪🕌🕍🛕🕋⛩️🗾🎑🏞️🌅🌄🌠🎇🎆"
    ),
    objects=(
        "⌚📱📲💻⌨️🖥️🖨️🖱️🖲️🕹️🗜️💽💾💿📀📼📷📸📹🎥📽️🎞️📞☎️📟📠📺📻"
        "🎙️🎚️🎛️🧭⏱️⏲️⏰🕰️⌛⏳📡🔋🔌💡🔦🕯️🪔🧯🛢️💸💵💴💶💷🪙💰💳💎"
        "⚖️🧰🔧🔨⚒️🛠️⛏️🔩⚙️🧱⛓️🧲🔫🧨🪓🔪🗡️⚔️🛡️🚬⚰️⚱️🏺🔮"
        "📿🧿💈⚗️🔭🔬💊💉🩸🩹🩺🚪🪞🛏️🛋️🪑🚽🚿🛁🪒🧴🧷🧹🧺🧻🧼🧽🛒"
    ),
    symbols=(
        "💠🔞📵🚭❗❕❓❔‼️⁉️💱💲🔱📛🔰⭕✅☑️✔️❌❎➕➖➗➰➿〽️✳️✴️❇️"
        "©️®️™️🔟🔢🔣🔤🅰️🆎🅱️🆑🆒🆓ℹ️🆔Ⓜ️🆕🆖🅾️🆗🅿️🆘🆙🆚"
        "🈁🈂️🈷️🈶🈯🉐🈹🈚🈲🉑🈸🈴🈳㊗️㊙️🈺🈵🔴🟠🟡🟢🔵🟣🟤⚫⚪"
        "🟥🟧🟨🟩🟦🟪🟫⬛⬜◼️◻️◾◽▪️▫️🔶🔷🔸🔹🔺🔻🔘🔳🔲"
    ),
    flags=(
        "🏁🚩🎌🏴🏳️🏳️‍🌈🏳️‍⚧️🏴‍☠️"
        "🇺🇳🇦🇫🇦🇱🇩🇿🇦🇷🇦🇲🇦🇺🇦🇹🇦🇿🇧🇭🇧🇩🇧🇪🇧🇴🇧🇦🇧🇷🇧🇬🇰🇭🇨🇦🇨🇱🇨🇳"
        "🇨🇴🇭🇷🇨🇺🇨🇾🇨🇿🇩🇰🇪🇬🇪🇪🇫🇮🇫🇷🇬🇪🇩🇪🇬🇭🇬🇷🇭🇹🇭🇳🇭🇰🇭🇺🇮🇸"
        "🇮🇳🇮🇩🇮🇷🇮🇶🇮🇪🇮🇱🇮🇹🇯🇵🇯🇴🇰🇿🇰🇪🇰🇼🇱🇦🇱🇧🇱🇾🇱🇹🇲🇾🇲🇽🇲🇦"
        "🇳🇱🇳🇿🇳🇬🇳🇴🇴🇲🇵🇰🇵🇸🇵🇦🇵🇾🇵🇪🇵🇭🇵🇱🇵🇹🇶🇦🇷🇴🇷🇺🇷🇼🇸🇦"
        "🇷🇸🇸🇬🇿🇦🇰🇷🇪🇸🇱🇰🇸🇩🇸🇪🇨🇭🇸🇾🇹🇼🇹🇭🇹🇷🇺🇦🇦🇪🇬🇧🇺🇸🇺🇾"
        "🇻🇪🇻🇳🇾🇪🇿🇲🇿🇼"
    ),
)

EMOJI_CATEGORIES = emoji.categories


def get_emoji_category(name):
    """
    Retrieve an emoji category's character string by name.

    Example:
        >>> get_emoji_category("hearts")
    """
    key = name.strip().lower()
    if key not in EMOJI_CATEGORIES:
        raise KeyError(
            f"Unknown emoji category: {name!r}. "
            f"Available categories: {sorted(EMOJI_CATEGORIES.keys())}"
        )
    return EMOJI_CATEGORIES[key]


def list_emoji_categories():
    """list[str]: Sorted list of supported emoji category names."""
    return sorted(EMOJI_CATEGORIES.keys())