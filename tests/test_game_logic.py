"""
test_game_logic.py - 16 pytest tests for logic_utils.py

Run: pytest tests/ -v
"""
from logic_utils import check_guess, parse_guess, get_range_for_difficulty, update_score

# check_guess tests
def test_winning_guess():
    outcome, message = check_guess(50, 50)   # FIX: unpack tuple
    assert outcome == "Win"

def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message    # FIX: original said HIGHER (reversed)

def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message   # FIX: original said LOWER (reversed)

def test_string_secret_still_works():
    outcome, message = check_guess(50, "50")  # FIX: int conversion
    assert outcome == "Win"

def test_string_comparison_trap():
    # Bug: "6" > "50" is True (string), but 6 > 50 is False (int)
    # Our fix forces int conversion so this returns Too Low correctly
    outcome, message = check_guess(6, "50")
    assert outcome == "Too Low"   # NOT "Too High" like the buggy version

# parse_guess tests
def test_parse_valid():
    ok, value, err = parse_guess("42")
    assert ok == True and value == 42

def test_parse_decimal():
    ok, value, err = parse_guess("5.0")
    assert ok == True and value == 5

def test_parse_empty():
    ok, value, err = parse_guess("")
    assert ok == False

def test_parse_none():
    ok, value, err = parse_guess(None)
    assert ok == False

def test_parse_letters():
    ok, value, err = parse_guess("hello")
    assert ok == False and err == "That is not a number."

# get_range_for_difficulty tests
def test_easy_range():
    low, high = get_range_for_difficulty("Easy")
    assert low == 1 and high == 20

def test_normal_range():
    low, high = get_range_for_difficulty("Normal")
    assert low == 1 and high == 100

def test_hard_is_harder_than_normal():
    # FIX: Hard must have bigger range than Normal
    _, hard_high = get_range_for_difficulty("Hard")
    _, normal_high = get_range_for_difficulty("Normal")
    assert hard_high > normal_high

# update_score tests
def test_win_gives_points():
    assert update_score(0, "Win", 1) > 0

def test_wrong_guess_loses_points():
    # FIX: even-numbered attempts used to give +5 for Too High
    assert update_score(100, "Too High", 2) < 100
    assert update_score(100, "Too Low", 2) < 100

def test_win_minimum_10():
    assert update_score(0, "Win", 20) >= 10
