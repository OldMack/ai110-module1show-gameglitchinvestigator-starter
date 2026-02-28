"""
test_game_logic.py
------------------
Automated tests for logic_utils.py using pytest.

HOW TO RUN:
    cd D:\codepath\ai110-module1show-gameglitchinvestigator-starter-main
    pytest tests/ -v

WHY TESTS?
    Tests prove your fixes actually work.
    They also catch future bugs if someone changes the code later.
"""

from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score


# ── check_guess tests ────────────────────────────────────────────────

def test_winning_guess():
    # Guess equals secret -> should win
    outcome, message = check_guess(50, 50)   # FIX: unpack tuple (was just "result == Win")
    assert outcome == "Win"

def test_guess_too_high():
    # Guess is higher than secret -> outcome is "Too High", hint says go LOWER
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message    # FIX: original hint was reversed (said "HIGHER")

def test_guess_too_low():
    # Guess is lower than secret -> outcome is "Too Low", hint says go HIGHER
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message   # FIX: original hint was reversed (said "LOWER")

def test_check_guess_with_string_secret():
    # FIX: even if secret is passed as string "50", should still compare correctly
    # (Original bug: even-numbered attempts passed secret as str)
    outcome, message = check_guess(50, "50")
    assert outcome == "Win"

def test_string_comparison_trap():
    # This was the sneaky bug: "6" > "50" is True in Python (string comparison)
    # but 6 > 50 is False (int comparison). Our fix forces int conversion.
    outcome, message = check_guess(6, "50")   # 6 < 50, should be Too Low
    assert outcome == "Too Low"               # NOT "Too High" like the buggy version


# ── parse_guess tests ────────────────────────────────────────────────

def test_parse_valid_integer():
    ok, value, err = parse_guess("42")
    assert ok == True
    assert value == 42
    assert err is None

def test_parse_decimal_input():
    # "5.0" should be accepted and converted to 5
    ok, value, err = parse_guess("5.0")
    assert ok == True
    assert value == 5

def test_parse_empty_string():
    ok, value, err = parse_guess("")
    assert ok == False
    assert err == "Enter a guess."

def test_parse_none_input():
    ok, value, err = parse_guess(None)
    assert ok == False

def test_parse_non_numeric():
    ok, value, err = parse_guess("hello")
    assert ok == False
    assert err == "That is not a number."


# ── get_range_for_difficulty tests ───────────────────────────────────

def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1
    assert high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1
    assert high == 100

def test_hard_range_is_actually_hard():
    # FIX: Hard range must be LARGER than Normal, not smaller
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high    # Hard should be harder than Normal


# ── update_score tests ───────────────────────────────────────────────

def test_win_gives_points():
    new_score = update_score(0, "Win", attempt_number=1)
    assert new_score > 0

def test_wrong_guess_loses_points():
    # FIX: wrong guesses should NEVER give points
    score_after_high = update_score(100, "Too High", attempt_number=2)  # even attempt
    score_after_low  = update_score(100, "Too Low",  attempt_number=2)
    assert score_after_high < 100   # must go DOWN
    assert score_after_low  < 100   # must go DOWN

def test_win_minimum_score():
    # Even if you win on the last attempt, score should be at least 10
    new_score = update_score(0, "Win", attempt_number=20)
    assert new_score >= 10
