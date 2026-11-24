# Lab 6 – Code and Branch Coverage Report

**Name:** Prathith Shetty  **SRN:** PES2UG24AM121
**Application:** `password_policy.py` (`check_password`, `strength`, `suggest_fix`)
**Tools:** Python 3.12.10, pytest 9.2.0, coverage 7.17.5

## Results

| Test file | Tests | Line coverage | Branch coverage | Screenshot |
|-----------|------:|--------------:|----------------:|------------|
| `test_password_policy.py` (starter) | 2 | 55% (21 of 47 lines missed) | 52% (9 of 36 branches partial) | – |
| `CodeCoverageTest_PES2UG24AM121_password_policy.py` | 15 | **100%** | 100% | [code_coverage.png](screenshots/code_coverage.png) |
| `BranchCoverageTest_PES2UG24AM121_password_policy.py` | 40 | **100%** | **100%** (36 / 36 branches) | [branch_coverage.png](screenshots/branch_coverage.png) |

The full terminal output for each screenshot is in [`screenshots/code_coverage_output.txt`](screenshots/code_coverage_output.txt) and [`screenshots/branch_coverage_output.txt`](screenshots/branch_coverage_output.txt).

### Commands

```
pip install coverage pytest

# code (line) coverage
coverage run -m pytest CodeCoverageTest_PES2UG24AM121_password_policy.py
coverage report -m

# branch coverage
coverage run --branch -m pytest BranchCoverageTest_PES2UG24AM121_password_policy.py
coverage report -m
```

## 1. Starting point (starter tests)

The two starter tests use only one valid password, `"Abcdef1!"`, so `coverage report -m` listed these lines as never executed:

| Missing lines | Code not reached |
|---------------|------------------|
| 7, 9, 11 | the `too short`, `too long` and `common` issues |
| 23, 25, 27, 29 | the `no uppercase / lowercase / digit / special` issues |
| 37, 39–41 | the `strong`, `weak` and `very weak` ratings |
| 45–54 | all of `suggest_fix` |

## 2. Code coverage tests → 100% line coverage

`CodeCoverageTest_PES2UG24AM121_password_policy.py` adds one test aimed at each missing line, and each test is labelled with the line it covers:

- **check_password:** a 4-character password (`too short`), a 68-character password (`too long`), `"password"` (`common`), `"12345678"` (no uppercase/lowercase/special) and `"Abcdefg!"` (no digit).
- **strength:** a 14-character valid password (`strong`), an 8-character one (`good`), one issue (`weak`) and four issues (`very weak`).
- **suggest_fix:** an empty list plus one list for each kind of first issue, which reaches every `return`, including the last one, `"shorten it"`.

Result: **47 / 47 statements executed (100%)**.

## 3. Branch coverage tests → 100% branch coverage

Line coverage only asks whether each line ran. Branch coverage asks whether every decision went **both ways**. `password_policy.py` has 36 branch outcomes: the `if`/`elif` tests, the `for` loop, and the `isupper → islower → isdigit → else` chain.

`BranchCoverageTest_PES2UG24AM121_password_policy.py` drives each decision True **and** False, at its exact boundary where there is one:

| Decision (line) | True case | False case |
|-----------------|-----------|------------|
| `len(pw) < 8` (6) | 7 characters | 8 characters |
| `len(pw) > 64` (8) | 65 characters | 64 characters; and a short password, where the `elif` is skipped |
| `pw.lower() in COMMON` (10) | all 4 common passwords + `"PassWord"`, `"QWERTY"` (case-insensitive) | `"Zebra#2024"` |
| `for ch in pw` (13) | any non-empty password | `""`, where the loop body never runs |
| `isupper / islower / isdigit / else` (14–21) | one password missing each class; space and Unicode (`É`, `١`) characters | the fully valid password |
| `upper/lower/digit/special == 0` (22–29) | one password missing each class | `"Abcdef1!"` |
| `not issues` (35) / `len(pw) >= 14` (36) | 14 characters → `strong` | 13 characters → `good` |
| `len(issues) <= 2` (39) | 1 and exactly 2 issues → `weak` | 3 issues → `very weak` |
| `suggest_fix` checks (45, 48, 50, 52) | each kind of first issue | `["too long"]` → `"shorten it"` |

It also checks `check_password` → `suggest_fix` end to end, and that `suggest_fix` only looks at the **first** issue.

Result: **36 / 36 branches taken, 0 partial (100%)**.

## 4. Observations

- **Line vs branch.** With only the starter tests, line coverage (55%) was higher than branch coverage (52%) because 9 decisions had only gone one way. Here, the line-coverage suite already reached 100% branch coverage as well. Almost every `if` in this module either returns or appends an issue, so reaching every line also forces the opposite outcome somewhere else. The branch suite still adds value: it pins every decision at its boundary (7/8, 64/65, 13/14 characters, 2/3 issues). An off-by-one change such as `<` becoming `<=` would pass the line tests but fail these.
- **Path coverage is not 100%.** Every branch is taken, but not every combination of branches is. For example, there is no "too long **and** common" password, because no common password is longer than 64 characters, so that path can never run.
- **Behaviour worth knowing.** Spaces and other non-alphanumeric characters count as "special", and Unicode letters and digits count toward the uppercase/lowercase/digit rules. `suggest_fix` only reports the first issue, so a password that is too short *and* has no digit only gets "add more characters".
