"""Password helpers: classify the first character of a password, split
'user:password' credentials and measure how many characters are digits.

Hardened after fuzz testing with Hypothesis: every function now handles
empty strings, None, non-string values and missing or extra ':' separators
without crashing.
"""


def first_character_type(pw):
    """Return 'digit', 'letter' or 'symbol' for the first character of pw.

    Returns 'empty' for an empty string and 'invalid' for anything that is
    not a string (for example None, numbers, bytes or lists).
    """
    if not isinstance(pw, str):
        return 'invalid'
    if not pw:
        return 'empty'
    ch = pw[0]
    if ch.isdigit():
        return 'digit'
    if ch.isalpha():
        return 'letter'
    return 'symbol'


def split_credentials(text):
    """Split 'user:password' into a (user, password) tuple.

    Only the first ':' separates the two parts, so a password may itself
    contain ':'. Returns None when text is not a string, has no ':', or the
    user name or password is blank.
    """
    if not isinstance(text, str):
        return None
    user, sep, password = text.partition(':')
    user, password = user.strip(), password.strip()
    if not sep or not user or not password:
        return None
    return user, password


def digit_ratio(pw):
    """Return the fraction of characters in pw that are digits (0.0 to 1.0).

    Returns 0.0 for an empty string or a value that is not a string.
    """
    if not isinstance(pw, str) or not pw:
        return 0.0
    return sum(c.isdigit() for c in pw) / len(pw)


def read_line(prompt):
    """Read one line of input; return '' instead of crashing if input ends."""
    try:
        return input(prompt)
    except EOFError:
        print()
        return ''


def main():
    print("==== Running first_character_type ====")
    user_input = read_line("Enter a password: ")
    result = first_character_type(user_input)
    print("First Character Type:", result)

    print("\n==== Running split_credentials ====")
    user_input = read_line("Enter user:password (e.g. alice:Secret1): ")
    result = split_credentials(user_input)
    if result is None:
        print("User and Password: invalid input, expected user:password")
    else:
        print("User and Password:", result)

    print("\n==== Running digit_ratio ====")
    user_input = read_line("Enter a password to measure: ")
    result = digit_ratio(user_input)
    print("Digit Ratio:", result)


if __name__ == "__main__":
    main()
