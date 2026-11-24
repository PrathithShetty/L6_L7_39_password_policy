"""Lab 6 - Branch coverage tests for password_policy.py.

Goal: drive every decision (if / elif / for) both ways - True and False -
using boundary values, so no branch is left untested.

Run:
    coverage run --branch -m pytest BranchCoverageTest_PES2UG24AM121_password_policy.py
    coverage report -m
"""
import pytest

from password_policy import COMMON, check_password, strength, suggest_fix

STRONG_14 = "Abcdefghijk1!x"   # 14 chars, every character class
GOOD_13 = "Abcdefghij1!x"      # 13 chars, every character class
LONG_PW = "Ab1!" * 17          # 68 chars, every character class


# ============================================================ check_password

# line 6 `len(pw) < 8` and line 8 `len(pw) > 64`, both directions,
# checked at the exact boundary values 7/8 and 64/65.
@pytest.mark.parametrize("pw, too_short", [
    ("Abcd1!x", True),    # 7 chars  -> line 6 True
    ("Abcde1!x", False),  # 8 chars  -> line 6 False
])
def test_minimum_length_boundary(pw, too_short):
    assert ("too short" in check_password(pw)) is too_short


@pytest.mark.parametrize("length, too_long", [
    (64, False),          # line 8 False
    (65, True),           # line 8 True
])
def test_maximum_length_boundary(length, too_long):
    assert ("too long" in check_password(LONG_PW[:length])) is too_long


def test_short_password_is_never_also_too_long():
    # elif: when line 6 is True, line 8 is not evaluated at all
    assert "too long" not in check_password("Ab1!")


# line 10 `pw.lower() in COMMON`: True for every common password,
# in any letter case, and False for an uncommon one.
@pytest.mark.parametrize("pw", sorted(COMMON) + ["PassWord", "QWERTY"])
def test_common_password_detected_case_insensitively(pw):
    assert "common" in check_password(pw)


def test_uncommon_password_not_flagged():
    assert "common" not in check_password("Zebra#2024")


# lines 13-21: the for loop and the isupper / islower / isdigit / else chain,
# and lines 22-29: each "no ..." check both True and False.
@pytest.mark.parametrize("pw, issues", [
    ("abcdefg1!", ["no uppercase"]),
    ("ABCDEFG1!", ["no lowercase"]),
    ("Abcdefgh!", ["no digit"]),
    ("Abcdefgh1", ["no special"]),
    ("Abcdef1!", []),
    ("12345678", ["no uppercase", "no lowercase", "no special"]),
])
def test_each_character_class(pw, issues):
    assert check_password(pw) == issues


def test_space_counts_as_special_character():
    assert check_password("Abcdef 1") == []


def test_unicode_letters_and_digits_are_classified():
    # 'É' is uppercase and '١' (Arabic-Indic one) is a digit
    assert check_password("Ébcdef١!") == []


def test_empty_password_skips_the_loop():
    # for loop on line 13 runs zero times -> every class is missing
    assert check_password("") == [
        "too short", "no uppercase", "no lowercase", "no digit", "no special"]


# ============================================================ strength

@pytest.mark.parametrize("pw, expected", [
    (STRONG_14, "strong"),    # line 35 True,  line 36 True  (14 chars)
    (GOOD_13, "good"),        # line 35 True,  line 36 False (13 chars)
    ("Abcdefg!", "weak"),     # line 35 False, line 39 True  (1 issue)
    ("abcdefg!", "weak"),     # line 39 True at the boundary  (2 issues)
    ("abcdefgh", "very weak"),  # line 39 False               (3 issues)
    ("", "very weak"),        # 5 issues
])
def test_strength_levels(pw, expected):
    assert strength(pw) == expected


# ============================================================ suggest_fix

@pytest.mark.parametrize("issues, expected", [
    ([], "none needed"),                                  # line 45 True
    (["too short", "no digit"], "add more characters"),   # line 48 True
    (["common", "no digit"], "avoid common passwords"),   # line 50 True
    (["no uppercase"], "add uppercase"),                  # line 52 True
    (["no lowercase"], "add lowercase"),
    (["no digit"], "add digit"),
    (["no special"], "add special"),
    (["too long"], "shorten it"),                         # line 52 False
])
def test_suggest_fix_uses_first_issue(issues, expected):
    assert suggest_fix(issues) == expected


# ============================================================ end to end

@pytest.mark.parametrize("pw, expected", [
    ("Abcdef1!", "none needed"),
    ("Ab1!", "add more characters"),
    ("password", "avoid common passwords"),
    ("abcdefg1!", "add uppercase"),
    (LONG_PW, "shorten it"),
])
def test_check_then_suggest(pw, expected):
    assert suggest_fix(check_password(pw)) == expected
