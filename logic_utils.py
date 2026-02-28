"""
logic_utils.py - All game logic, separated from UI (app.py)
"""

def get_range_for_difficulty(difficulty: str):
    """
    Return (low, high) range for a given difficulty.
    FIX: Hard was 1-50 (easier than Normal 1-100). Now 1-500.
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 500   # FIX: was 1,50 which is easier than Normal
    return 1, 100


def parse_guess(raw: str):
    """
    Parse user input into an integer.
    Returns: (ok: bool, value: int|None, error: str|None)
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
    Compare guess to secret.
    FIX 1: Hint messages were reversed (said HIGHER when should say LOWER).
    FIX 2: Force int conversion - original passed secret as str on even attempts,
           causing broken string comparison e.g. "6" > "50" = True (wrong!).
    Returns: (outcome, message)
    """
    try:
        guess = int(guess)
        secret = int(secret)
    except (ValueError, TypeError):
        return "Error", "Invalid values."

    if guess == secret:
        return "Win", "Correct!"
    if guess > secret:
        return "Too High", "Go LOWER!"    # FIX: was "Go HIGHER!" (reversed)
    else:
        return "Too Low", "Go HIGHER!"    # FIX: was "Go LOWER!" (reversed)


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    FIX: Too High on even attempts was giving +5 (rewarding wrong guesses).
    Wrong guesses always lose 5 points now.
    """
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points
    if outcome == "Too High" or outcome == "Too Low":
        return current_score - 5   # FIX: always subtract, never add
    return current_score
