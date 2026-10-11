# simple_roman_numerals

Convert between integers and Roman numerals in both directions.

```python
from simple_roman_numerals import to_roman, from_roman, is_valid_roman, RomanError

to_roman(1994)        # "MCMXCIV"
from_roman("MCMXCIV") # 1994
is_valid_roman("IIII") # False
is_valid_roman("IV")    # True
try:
    to_roman(4000)
except RomanError:
    pass
```

The library exists because Python's standard library does not include a Roman-numeral converter, and ad-hoc implementations typically fail to reject non-canonical strings such as `IIII`, `IVI`, or `CMM`. Here, `to_roman` produces the canonical subtractive form, and `from_roman` validates against that same canonical form, so `from_roman(to_roman(n)) == n` and non-canonical inputs raise `RomanError`.

The supported range is 1..3999. The Romans had no symbol for zero, and without an overline (vinculum) convention for thousands, 4000 and above cannot be expressed. Supporting vinculum notation adds parsing complexity for a rare use case, so this library deliberately does not cover it. Input is case-sensitive: only uppercase letters are accepted.


## Exported names

- `to_roman(n)` — `int` → `str`; raises `RomanError` if `n` is not an int or falls outside 1..3999. Rejects `bool` explicitly.
- `from_roman(s)` — `str` → `int`; raises `RomanError` on empty string, non-string input, unrecognized characters, or any non-canonical numeral.
- `is_valid_roman(s)` — `str` → `bool`; never raises; returns `False` for non-string input.
- `RomanError` — a `ValueError` subclass.


## Awkward edge

`to_roman(True)` raises `RomanError`. Since `bool` subclasses `int`, a naive type check would accept `True` as `1`; we reject it so that surprises like `to_roman(True) == "I"` do not pass silently. If you want that behavior, cast explicitly with `to_roman(int(True))`.
