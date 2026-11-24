"""Lab 7 - Hypothesis fuzz tests for password_policy.py.

Run:  pytest test_password_policy.py
"""
import string

from hypothesis import given, settings, strategies as st
from password_policy import first_character_type, split_credentials, digit_ratio

# Try more random inputs than the default 100 per test.
settings.register_profile("lab7", max_examples=300)
settings.load_profile("lab7")

NO_COLON = st.characters(exclude_characters=":")
USERS = st.text(alphabet=NO_COLON, min_size=1).filter(lambda u: u.strip())
PASSWORDS = st.text(min_size=1).filter(lambda p: p.strip())
BLANKS = st.text(alphabet=" \t")
NON_STRINGS = (st.integers() | st.floats() | st.booleans() | st.binary()
               | st.lists(st.text()) | st.dictionaries(st.text(), st.text()))


# ============================================================ first_character_type

@given(st.text() | st.none())
def test_first_character_type_no_crash(s):
    try:
        result = first_character_type(s)
    except Exception as e:
        assert False, f"first_character_type crashed with: {e!r}"
    assert result in {"digit", "letter", "symbol", "empty", "invalid"}


@given(st.text(min_size=1))
def test_first_character_type_classifies_first_char(s):
    if s[0].isdigit():
        expected = "digit"
    elif s[0].isalpha():
        expected = "letter"
    else:
        expected = "symbol"
    assert first_character_type(s) == expected


@given(NON_STRINGS)
def test_first_character_type_rejects_non_strings(value):
    assert first_character_type(value) == "invalid"


# ============================================================ split_credentials

@given(st.text() | st.none())
def test_split_credentials_no_crash(s):
    try:
        result = split_credentials(s)
    except Exception as e:
        assert False, f"split_credentials crashed with: {e!r}"
    assert result is None or (isinstance(result, tuple) and len(result) == 2)


@given(USERS, PASSWORDS)
def test_split_credentials_round_trip(user, password):
    # passwords may themselves contain ':' - only the first ':' separates
    assert split_credentials(f"{user}:{password}") == (user.strip(), password.strip())


@given(st.text(alphabet=NO_COLON))
def test_split_credentials_without_colon_is_rejected(s):
    assert split_credentials(s) is None


@given(BLANKS, USERS, PASSWORDS)
def test_split_credentials_blank_user_or_password_is_rejected(blank, user, password):
    assert split_credentials(f"{blank}:{password}") is None
    assert split_credentials(f"{user}:{blank}") is None


# ============================================================ digit_ratio

@given(st.text() | st.none())
def test_digit_ratio_no_crash(s):
    try:
        result = digit_ratio(s)
    except Exception as e:
        assert False, f"digit_ratio crashed with: {e!r}"
    assert 0.0 <= result <= 1.0


@given(st.text(min_size=1))
def test_digit_ratio_matches_definition(s):
    assert digit_ratio(s) == sum(c.isdigit() for c in s) / len(s)


@given(st.text(alphabet=string.digits, min_size=1))
def test_digit_ratio_of_only_digits_is_one(s):
    assert digit_ratio(s) == 1.0


@given(NON_STRINGS)
def test_digit_ratio_of_non_string_is_zero(value):
    assert digit_ratio(value) == 0.0
