# Reflection: Game Glitch Investigator

## What I Did

Investigated an AI-generated Python guessing game, found 8 bugs, fixed them,
refactored all logic into logic_utils.py, and wrote 16 automated pytest tests.

---

## Bugs Found and Fixed

| # | File | Bug Type | Description |
|---|------|----------|-------------|
| 1 | app.py | Logic | Hard difficulty range (1-50) was EASIER than Normal (1-100) |
| 2 | app.py | Logic | Hint messages reversed: said "Go HIGHER" when guess was too high |
| 3 | app.py | Runtime | Secret cast to str on even attempts, broke comparison logic |
| 4 | app.py | Logic | Wrong guesses on even attempts gave +5 points (should lose points) |
| 5 | app.py | Logic | attempts initialized to 1 instead of 0 |
| 6 | app.py | Logic | New Game always used range 1-100, ignored selected difficulty |
| 7 | app.py | Logic | Info text hardcoded "between 1 and 100" regardless of difficulty |
| 8 | tests/ | Test | Tests expected string return but check_guess returns a tuple |

---

## When I Accepted, Modified, or Rejected AI Suggestions

**Accepted:**
- Overall Streamlit UI structure was reasonable
- parse_guess function logic was correct
- Separating code into functions was a good pattern

**Modified:**
- Hint messages needed to be reversed
- Hard difficulty range needed rethinking (bigger = harder)
- Score function: removed the even/odd trick that added complexity with no benefit

**Rejected:**
- The string comparison trick on even attempts looked intentional but was completely broken.
  The AI appeared to be adding "variety" but instead created a silent bug where hints
  were randomly wrong every other guess.

---

## Most Interesting Bug

Bug #3 (string comparison) was hardest to catch because it looked deliberate.
The code cast secret to str on even attempts, causing:
  "6" > "50" = True  (string comparison, wrong!)
  6 > 50 = False     (integer comparison, correct)

This meant every other guess gave a wrong hint with no error message.

**Lesson:** AI code can appear intentional even when it is wrong.
Always test edge cases, not just read the code.

---

## Conclusion

AI is a fast first draft, not a final answer.
The developers job shifts from "write everything" to "verify everything."
