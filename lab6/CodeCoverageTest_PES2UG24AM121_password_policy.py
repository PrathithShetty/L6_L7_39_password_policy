"""Lab 6 - Code (line) coverage tests for password_policy.py.

Goal: execute every line of password_policy.py at least once.

Run:
    coverage run -m pytest CodeCoverageTest_PES2UG24AM121_password_policy.py
    coverage report -m
"""
from password_policy import check_password, strength, suggest_fix


# ---------------------------------------------------------------- check_password

def test_valid_password_has_no_issues():
    assert check_password("Abcdef1!") == []


def test_too_short_password():                        # line 7
    assert "too short" in check_password("Ab1!")


def test_too_long_password():                         # line 9
    assert "too long" in check_password("Ab1!" * 17)  # 68 characters


def test_common_password():                           # line 11
    assert "common" in check_password("password")


def test_password_without_letters_or_special():       # lines 23, 25, 29
    assert check_password("12345678") == [
        "no uppercase", "no lowercase", "no special"]


def test_password_without_digit():                    # line 27
    assert check_password("Abcdefg!") == ["no digit"]


# ---------------------------------------------------------------- strength

def test_strong_password():                           # line 37
    assert strength("Abcdefghijk1!x") == "strong"     # 14 characters


def test_good_password():                             # line 38
    assert strength("Abcdef1!") == "good"


def test_weak_password():                             # lines 39-40
    assert strength("Abcdefg!") == "weak"             # one issue


def test_very_weak_password():                        # line 41
    assert strength("abc") == "very weak"             # four issues


# ---------------------------------------------------------------- suggest_fix

def test_suggest_fix_none_needed():                   # lines 45-46
    assert suggest_fix([]) == "none needed"


def test_suggest_fix_too_short():                     # lines 47-49
    assert suggest_fix(["too short"]) == "add more characters"


def test_suggest_fix_common():                        # lines 50-51
    assert suggest_fix(["common"]) == "avoid common passwords"


def test_suggest_fix_missing_class():                 # lines 52-53
    assert suggest_fix(["no digit"]) == "add digit"


def test_suggest_fix_too_long():                      # line 54
    assert suggest_fix(["too long"]) == "shorten it"
