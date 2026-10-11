"""Core conversion logic for simple_roman_numerals.

We use the "standard" subtractive forms: IV, IX, XL, XC, CD, CM.
We do NOT support the deprecated additive-only forms (IIII for 4, XXXX for 40,
etc.) nor any medieval shorthand (no 4=IVI, no exotic large-value notation).
This keeps the parser unambiguous: there is exactly one canonical string per
integer, and exactly one integer per canonical string.

Range is 1..3999. The Romans had no symbol for zero, and without a vinculum
(overline) convention, 4000 and above cannot be expressed. Supporting
vinculum notation adds parsing complexity (including validating the parser
against itself) for a rare use case, so we chose the classical range.
"""


class RomanError(ValueError):
    """Raised when a value cannot be converted to or from a Roman numeral.

    Subclasses ValueError so that input-validation code can catch either the
    specific case or the general value error.
    """


# Ordered so that greedy subtraction produces the canonical form.
# Each entry is (value, symbol). Tuples chosen over a dict for stable,
# declaration-order iteration (though dicts preserve insertion order in 3.7+,
# tuples make the ordering intent explicit and impossible to disturb).
_SYMBOLS = [
    (1000, "M"),
    (900, "CM"),
    (500, "D"),
    (400, "CD"),
    (100, "C"),
    (90, "XC"),
    (50, "L"),
    (40, "XL"),
    (10, "X"),
    (9, "IX"),
    (5, "V"),
    (4, "IV"),
    (1, "I"),
]

# Inverted lookup for parsing. Multiple-character subtractive pairs are
# listed first so that longest-match parsing is the natural result.
_VALUE_OF = {
    "CM": 900,
    "CD": 400,
    "XC": 90,
    "XL": 40,
    "IX": 9,
    "IV": 4,
    "M": 1000,
    "D": 500,
    "C": 100,
    "L": 50,
    "X": 10,
    "V": 5,
    "I": 1,
}


def to_roman(n):
    """Convert an integer to its canonical Roman-numeral string.

    Raises RomanError if n is not an integer or falls outside 1..3999.
    We check int-ness via the type to avoid silently accepting bools or
    floats; bool is a subclass of int, so we reject it explicitly.
    """
    if isinstance(n, bool) or not isinstance(n, int):
        raise RomanError("to_roman requires an int, got %r" % type(n).__name__)
    if n < 1 or n > 3999:
        raise RomanError("to_roman requires 1..3999, got %d" % n)

    result = []
    remaining = n
    for value, symbol in _SYMBOLS:
        count, remaining = divmod(remaining, value)
        result.append(symbol * count)
    return "".join(result)


def from_roman(s):
    """Parse a canonical Roman-numeral string to an integer.

    Raises RomanError if s is not a string or is not a valid Roman numeral.
    We reject empty strings and non-string inputs outright, and we do a
    strict canonical check after computing the value. The canonical check
    guarantees that from_roman(to_roman(x)) == x and that strings like IIII
    or IVI are rejected rather than silently accepted with an off value.
    """
    if not isinstance(s, str):
        raise RomanError("from_roman requires a str, got %r" % type(s).__name__)
    if s == "":
        raise RomanError("from_roman received an empty string")

    value = _parse_roman(s)
    if to_roman(value) != s:
        raise RomanError("%r is not a canonical Roman numeral" % s)
    return value


def is_valid_roman(s):
    """Return True if s is a canonical Roman numeral, else False.

    This never raises; it is the non-throwing counterpart to from_roman.
    """
    if not isinstance(s, str) or s == "":
        return False
    parsed = _parse_roman(s)
    if parsed is None:
        return False
    return to_roman(parsed) == s


def _parse_roman(s):
    """Greedy longest-match parser.

    Returns None on any unrecognized character or structural oddity that
    leaves the string unconsumed. Canonicality is then verified by the
    caller, so this function focuses on producing an integer when the
    string is structurally plausible.
    """
    value = 0
    i = 0
    while i < len(s):
        # Try two-character subtractive forms first (longest match),
        # then single characters. We do not use a regex; an explicit scan
        # is easier to reason about and avoids re as a dependency.
        matched = False
        for length in (2, 1):
            piece = s[i:i + length]
            if piece in _VALUE_OF:
                value += _VALUE_OF[piece]
                i += length
                matched = True
                break
        if not matched:
            return None
    return value
