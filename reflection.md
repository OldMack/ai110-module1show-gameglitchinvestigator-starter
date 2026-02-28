# Reflection: Game Glitch Investigator

## What I Did

I investigated an AI-generated Python guessing game and found 8 bugs across two files.
I fixed them, refactored the logic into `logic_utils.py`, and wrote automated pytest tests.

---

## Bugs Found and Fixed

| # | File | Bug Type | Description |
|---|------|----------|-------------|
| 1 | app.py | Logic | Hard difficulty range (1-50) was easier than Normal (1-100) |
| 2 | app.py | Logic | Hint messages were reversed: "Go HIGHER" when guess was too high |
| 3 | app.py | Runtime | Secret was cast to `str` on even attempts, causing broken string comparison |
| 4 | app.py | Logic | Wrong guesses on even attempts gave +5 points instead of -5 |
| 5 | app.py | Logic | `attempts` initialized to 1 instead of 0 |
| 6 | app.py | Logic | New Game always used range 1-100, ignoring selected difficulty |
| 7 | app.py | Logic | Info text hardcoded "between 1 and 100" regardless of difficulty |
| 8 | tests/ | Test | Tests expected a string return but `check_guess` returns a tuple |

---

## What I Learned About AI-Generated Code

**When I accepted AI suggestions:**
- The overall structure of the game was reasonable (session state, Streamlit UI layout)
- The `parse_guess` function logic was correct and clean
- The separation into functions was a good idea, even if the functions had bugs

**When I modified AI suggestions:**
- The hint messages needed to be reversed — the AI got the logic backwards
- The difficulty ranges needed rethinking (Hard should mean harder, not smaller range)
- The score function needed the even/odd trick removed — it added complexity with no benefit

**When I rejected AI suggestions:**
- The string comparison trick on even attempts was completely wrong.
  It seemed like the AI was trying to add variety but instead introduced a silent bug
  that made the hints randomly incorrect every other guess.

---

## The Most Interesting Bug

Bug #3 (the string comparison) was the hardest to spot because it looked intentional.
The code `secret = str(st.session_state.secret)` on even attempts appeared purposeful.
But the result was that Python compared strings character-by-character:
- `"6" > "50"` evaluates to `True` (because `"6" > "5"`)
- But `6 > 50` evaluates to `False` (correct integer comparison)

This meant every other guess gave a completely wrong hint — a subtle, hard-to-catch bug.

**Lesson:** AI-generated code can look intentional even when it is wrong.
Always run the code and test edge cases, not just read it.

---

## Human Judgment in AI-Assisted Development

The AI was helpful for:
- Scaffolding the Streamlit UI quickly
- Generating test structure and boilerplate

The AI required human correction for:
- Business logic (what "Hard" difficulty should actually mean)
- Edge cases (what happens with string vs int comparison)
- Consistency (why does New Game ignore difficulty?)

**Conclusion:** AI is a fast first draft, not a final answer.
The developer's job shifts from "write everything" to "verify everything."
