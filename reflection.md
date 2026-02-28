# Reflection: Game Glitch Investigator

## What I Did

I investigated an AI-generated Python guessing game, identified 8 bugs across two files,
fixed all of them, refactored the game logic into `logic_utils.py`, and wrote 16 automated
pytest tests to verify the fixes.

---

## Bugs Found and Fixed

| # | File | Bug Type | Description |
|---|------|----------|-------------|
| 1 | app.py | Logic | Hard difficulty range was (1, 50) — easier than Normal (1, 100) |
| 2 | app.py | Logic | Hint messages reversed: said "Go HIGHER" when guess was too high |
| 3 | app.py | Runtime | Secret cast to `str` on even attempts, causing broken string comparison |
| 4 | app.py | Logic | Wrong guesses on even attempts gave +5 points instead of -5 |
| 5 | app.py | Logic | `attempts` initialized to 1 instead of 0 |
| 6 | app.py | Logic | New Game always used range 1–100, ignoring selected difficulty |
| 7 | app.py | Logic | Info text hardcoded "between 1 and 100" regardless of difficulty |
| 8 | tests/ | Test | Tests expected a string return value, but `check_guess` returns a tuple |

---

## When I Accepted, Modified, or Rejected AI Suggestions

**Accepted:**
- The overall Streamlit UI structure was reasonable and clean.
- `parse_guess` had correct logic — no changes needed.
- Separating code into small, focused functions was a good design decision.

**Modified:**
- Hint messages needed to be reversed — the AI got the direction backwards.
- Hard difficulty range needed rethinking. Harder should mean a wider range, not smaller.
- The score function: removed the even/odd trick that added complexity with no real benefit.

**Rejected:**
- The string comparison trick on even attempts looked intentional but was completely wrong.
  The AI appeared to be adding "variety," but instead created a silent bug that made hints
  randomly incorrect every other guess — with no error message to indicate anything was wrong.

---

## The Most Interesting Bug

**Bug #3 (string comparison)** was the hardest to catch because it looked deliberate.

The code cast `secret` to `str` on even-numbered attempts before passing it to `check_guess`.
This caused Python to compare strings character-by-character instead of comparing integers:

```
"6" > "50"  →  True   (string comparison: "6" > "5" alphabetically)
 6  >  50   →  False  (integer comparison: correct)
```

The result: every other guess produced a completely wrong hint, with no visible error.

**Lesson:** AI-generated code can look intentional even when it is wrong.
Always run the code and test edge cases — do not just read it.

---

## Conclusion

AI is a fast first draft, not a final answer.
The developer's job shifts from "write everything" to "verify everything."
Human judgment is most valuable precisely where AI bugs are hardest to spot.
