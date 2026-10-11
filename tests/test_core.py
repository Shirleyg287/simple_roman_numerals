'''Tests for simple_roman_numerals.core.

These cover the documented edge cases: out-of-range inputs, non-int inputs,
empty strings, non-canonical numeral strings (IIII, IVI, repeated subtractive
forms), and the round-trip property on the full supported range.
'''

import unittest

from simple_roman_numerals.core import (
    RomanError,
    to_roman,
    from_roman,
    is_valid_roman,
)


class TestToRoman(unittest.TestCase):

    def test_basic_values(self):
        self.assertEqual(to_roman(1), "I")
        self.assertEqual(to_roman(4), "IV")
        self.assertEqual(to_roman(9), "IX")
        self.assertEqual(to_roman(40), "XL")
        self.assertEqual(to_roman(90), "XC")
        self.assertEqual(to_roman(400), "CD")
        self.assertEqual(to_roman(900), "CM")
        self.assertEqual(to_roman(49), "XLIX")
        self.assertEqual(to_roman(1994), "MCMXCIV")
        self.assertEqual(to_roman(2024), "MMXXIV")
        self.assertEqual(to_roman(3888), "MMMDCCCLXXXVIII")

    def test_boundaries(self):
        self.assertEqual(to_roman(1), "I")
        self.assertEqual(to_roman(3999), "MMMCMXCIX")

    def test_rejects_out_of_range(self):
        with self.assertRaises(RomanError):
            to_roman(0)
        with self.assertRaises(RomanError):
            to_roman(4000)
        with self.assertRaises(RomanError):
            to_roman(-1)

    def test_rejects_non_int(self):
        with self.assertRaises(RomanError):
            to_roman("5")
        with self.assertRaises(RomanError):
            to_roman(5.0)
        with self.assertRaises(RomanError):
            to_roman(None)

    def test_rejects_bool(self):
        # bool is a subclass of int; we reject it so callers do not get
        # surprising conversions like True -> "I".
        with self.assertRaises(RomanError):
            to_roman(True)
        with self.assertRaises(RomanError):
            to_roman(False)


class TestFromRoman(unittest.TestCase):

    def test_basic_values(self):
        self.assertEqual(from_roman("I"), 1)
        self.assertEqual(from_roman("IV"), 4)
        self.assertEqual(from_roman("IX"), 9)
        self.assertEqual(from_roman("XLIX"), 49)
        self.assertEqual(from_roman("MCMXCIV"), 1994)
        self.assertEqual(from_roman("MMXXIV"), 2024)
        self.assertEqual(from_roman("MMMDCCCLXXXVIII"), 3888)
        self.assertEqual(from_roman("MMMCMXCIX"), 3999)

    def test_rejects_empty_string(self):
        with self.assertRaises(RomanError):
            from_roman("")

    def test_rejects_non_string(self):
        with self.assertRaises(RomanError):
            from_roman(5)
        with self.assertRaises(RomanError):
            from_roman(None)
        with self.assertRaises(RomanError):
            from_roman(["I"])

    def test_rejects_additive_non_canonical(self):
        # IIII, XXXX, CCCC are the old additive forms; we reject them.
        with self.assertRaises(RomanError):
            from_roman("IIII")
        with self.assertRaises(RomanError):
            from_roman("XXXX")
        with self.assertRaises(RomanError):
            from_roman("CCCC")
        with self.assertRaises(RomanError):
            from_roman("VV")

    def test_rejects_repeated_subtractive(self):
        # Subtractive forms may not be repeated.
        with self.assertRaises(RomanError):
            from_roman("IVIV")
        with self.assertRaises(RomanError):
            from_roman("CMCM")

    def test_rejects_malformed_combinations(self):
        # These would parse structurally but are not canonical.
        with self.assertRaises(RomanError):
            from_roman("IVI")
        with self.assertRaises(RomanError):
            from_roman("IXI")
        with self.assertRaises(RomanError):
            from_roman("CMM")
        with self.assertRaises(RomanError):
            from_roman("IC")

    def test_rejects_unknown_chars(self):
        with self.assertRaises(RomanError):
            from_roman("XIZ")
        with self.assertRaises(RomanError):
            from_roman(" xi")
        with self.assertRaises(RomanError):
            from_roman("XI ")

    def test_case_sensitive(self):
        # We accept uppercase only. This is a deliberate simplification.
        with self.assertRaises(RomanError):
            from_roman("xiv")
        with self.assertRaises(RomanError):
            from_roman("mmxxiv")


class TestIsValidRoman(unittest.TestCase):

    def test_valid_returns_true(self):
        self.assertTrue(is_valid_roman("I"))
        self.assertTrue(is_valid_roman("IV"))
        self.assertTrue(is_valid_roman("MMMCMXCIX"))
        self.assertTrue(is_valid_roman("MMXXIV"))

    def test_invalid_returns_false(self):
        self.assertFalse(is_valid_roman("IIII"))
        self.assertFalse(is_valid_roman("IVI"))
        self.assertFalse(is_valid_roman("CMM"))
        self.assertFalse(is_valid_roman(""))
        self.assertFalse(is_valid_roman("xiv"))
        self.assertFalse(is_valid_roman(None))
        self.assertFalse(is_valid_roman(5))


class TestRoundTrip(unittest.TestCase):

    def test_all_in_range_round_trip(self):
        for n in range(1, 4000):
            self.assertEqual(from_roman(to_roman(n)), n)

    def test_round_trip_is_canonical(self):
        for n in [1, 4, 9, 40, 49, 90, 400, 900, 999, 1000, 1994, 2024, 3999]:
            self.assertEqual(to_roman(from_roman(to_roman(n))), to_roman(n))


if __name__ == "__main__":
    unittest.main()
