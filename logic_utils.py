"""
logic_utils.py
--------------
All game logic lives here, separated from the UI (app.py).
This makes the code easier to test and maintain.
"""


def get_range_for_difficulty(difficulty: str):
    """
    Return (low, high) inclusive range for a given difficulty.

    FIX: Hard was returning (1, 50) which is EASIER than Normal (1, 100).
    Harder difficulty = bigger range = harder to guess.
    """
    if difficulty == "Easy":
        return 1, 20       # small range -> easy to guess
    if difficulty == "Normal":
        return 1, 100      # medium range
    if difficulty == "Hard":
        return 1, 500      # FIX: large range -> actually hard
    return 1, 100          # default fallback


def parse_guess(raw: str):
    """
    Parse user input string into an integer guess.

    Returns a tuple: (ok, guess_int, error_message)
    - ok: True if input is valid, False otherwise
    - guess_int: the integer value, or None if invalid
    - error_message: a string if invalid, or None if valid

    No bugs here -- this function was correct already.
    """
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return (outcome, message).

    FIX 1: Hint messages were REVERSED.
        guess > secret = TOO HIGH -> tell user go LOWER
        guess < secret = TOO LOW  -> tell user go HIGHER

    FIX 2: Force int conversion so string comparisons never happen.
        Original app.py passed secret as str on even attempts,
        causing "6" > "50" = True (wrong! strings compare char by char).

    Returns: (outcome, message)
    """
    try:
        guess = int(guess)
        secret = int(secret)
    except (ValueError, TypeError):
        return "Error", "Invalid values for comparison."

    if guess == secret:
        return "Win", "Correct!"

    if guess > secret:
        return "Too High", "Go LOWER!"    # FIX: was "Go HIGHER!" (reversed)
    else:
        return "Too Low", "Go HIGHER!"    # FIX: was "Go LOWER!" (reversed)


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update and return new score based on outcome and attempt number.

    FIX: "Too High" on even attempts was giving +5 points (rewarding wrong guesses).
    Wrong guesses should always cost points.

    Scoring:
    - Win:   +100 minus 10 per attempt (min 10)
    - Wrong: -5 penalty
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High" or outcome == "Too Low":
        # FIX: always subtract -- original gave +5 on even attempts
        return current_score - 5

    return current_score
