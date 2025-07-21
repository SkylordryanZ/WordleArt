import streamlit as st
import os


def wordle_feedback(guess, target):
    result = ['n'] * 5
    target_remaining = list(target)

    # First pass: green
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'g'
            target_remaining[i] = None

    # Second pass: yellow
    for i in range(5):
        if result[i] == 'n' and guess[i] in target_remaining:
            result[i] = 'y'
            target_remaining[target_remaining.index(guess[i])] = None

    return result


def matches_feedback_with_pool(guess, word_of_day, pattern):
    letter_pool = set(word_of_day)
    for i in range(5):
        c = guess[i]
        expected = pattern[i]

        if expected in ['y', 'g'] and c not in letter_pool:
            return False
        if expected == 'n' and c in letter_pool:
            return False

    feedback = wordle_feedback(guess, word_of_day)
    for i in range(5):
        if feedback[i] != pattern[i]:
            return False

    return True


def find_matching_words(word_list, word_of_day, pattern):
    matches = []
    for word in word_list:
        word = word.lower()
        if len(word) == 5 and word.isalpha():
            if matches_feedback_with_pool(word, word_of_day, pattern):
                matches.append(word)
    return matches


def load_word_list():
    file_path = os.path.join(os.path.dirname(__file__), "valid-wordle-words.txt")
    if not os.path.isfile(file_path):
        st.error("Could not find 'valid-wordle-words.txt'. Please place it in the same folder.")
        return []
    with open(file_path, "r") as f:
        return [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]


# === Streamlit UI ===

st.set_page_config(page_title="Wordle Solver", page_icon="🟩", layout="centered")
st.title("🟩 Wordle Pattern Matcher (Green + Yellow + Gray Tiles)")

# Session state
if "letters" not in st.session_state:
    st.session_state.letters = [""] * 5

if "feedback" not in st.session_state:
    st.session_state.feedback = ["n"] * 5

if "clicked_index" not in st.session_state:
    st.session_state.clicked_index = -1


def cycle_feedback(i):
    current = st.session_state.feedback[i]
    next_state = {'n': 'y', 'y': 'g', 'g': 'n'}
    st.session_state.feedback[i] = next_state[current]


# Colors for states
color_map = {
    "n": "#787c7e",  # Gray
    "y": "#c9b458",  # Yellow
    "g": "#6aaa64",  # Green
}

# --- Input letters ---
st.markdown("### Step 1: Enter the Wordle Answer (5 letters)")

cols = st.columns(5)
for i, col in enumerate(cols):
    st.session_state.letters[i] = col.text_input(
        f"Letter {i+1}",
        value=st.session_state.letters[i],
        max_chars=1,
        key=f"letter_input_{i}",
        label_visibility="collapsed",
        placeholder=" ",
    ).lower()

# --- Feedback Buttons ---
st.markdown("### Step 2: Click tiles to toggle feedback (gray → yellow → green)")

feedback_cols = st.columns(5)
for i, col in enumerate(feedback_cols):
    letter = st.session_state.letters[i].upper() if st.session_state.letters[i] else " "
    color = color_map[st.session_state.feedback[i]]

    if col.button(letter, key=f"feedback_button_{i}", use_container_width=True):
        st.session_state.clicked_index = i

    # Show colored tile below button
    col.markdown(
        f"<div style='height:50px; background-color:{color}; color:white; font-weight:bold; text-align:center; "
        f"line-height:50px; border-radius:6px; margin-top:5px'>{letter}</div>",
        unsafe_allow_html=True
    )

# Handle tile click after render
if st.session_state.clicked_index != -1:
    idx = st.session_state.clicked_index
    cycle_feedback(idx)
    st.session_state.clicked_index = -1
    st.rerun()
    
# --- Logic to search ---
st.markdown("---")

word_of_day = "".join(st.session_state.letters)
pattern = "".join(st.session_state.feedback)

if len(word_of_day) == 5 and all(c in "ygn" for c in pattern):
    word_list = load_word_list()
    if word_list:
        matches = find_matching_words(word_list, word_of_day, pattern)
        st.subheader("🔍 Matching Words")
        if matches:
            st.success(f"Found {len(matches)} matching words:")
            st.write(", ".join(matches))
        else:
            st.info("No matching words found.")
else:
    st.info("Enter all 5 letters and click feedback buttons to set color.")
