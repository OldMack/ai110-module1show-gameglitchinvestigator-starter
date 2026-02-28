import random
import streamlit as st

# FIX: Import logic from logic_utils.py (separation of concerns)
from logic_utils import (
    get_range_for_difficulty,
    parse_guess,
    check_guess,
    update_score,
)

st.set_page_config(page_title="Glitchy Guesser", page_icon="?")
st.title("? Game Glitch Investigator")
st.caption("AI-generated guessing game -- now de-glitched.")

st.sidebar.header("Settings")
difficulty = st.sidebar.selectbox("Difficulty", ["Easy", "Normal", "Hard"], index=1)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)
st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 0   # FIX: was 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")
# FIX: show actual range, not hardcoded "1 to 100"
st.info(f"Guess a number between {low} and {high}. Attempts left: {attempt_limit - st.session_state.attempts}")

with st.expander("Developer Debug Info"):
    st.write("Secret:", st.session_state.secret)
    st.write("Attempts:", st.session_state.attempts)
    st.write("Score:", st.session_state.score)

raw_guess = st.text_input("Enter your guess:", key=f"guess_input_{difficulty}")

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button("Submit Guess")
with col2:
    new_game = st.button("New Game")
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if new_game:
    st.session_state.attempts = 0
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.secret = random.randint(low, high)  # FIX: use difficulty range
    st.session_state.score = 0
    st.session_state.status = "playing"
    st.session_state.history = []
    st.success("New game started.")
    st.rerun()

if st.session_state.status != "playing":
    if st.session_state.status == "won":
        st.success("You already won! Start a new game.")
    else:
        st.error("Game over. Start a new game.")
    st.stop()

if submit:
    st.session_state.attempts += 1
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    else:
        st.session_state.history.append(guess_int)
        # FIX: always pass secret as int, never cast to str
        secret = st.session_state.secret
        outcome, message = check_guess(guess_int, secret)

        if show_hint:
            st.warning(message)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.success(f"You won! Secret was {st.session_state.secret}. Score: {st.session_state.score}")
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.error(f"Out of attempts! Secret was {st.session_state.secret}. Score: {st.session_state.score}")

st.divider()
st.caption("Now actually production-ready.")
