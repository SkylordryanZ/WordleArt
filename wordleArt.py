import streamlit as st
import os


def wordle_feedback(guess, target):
    result = ['n'] * 5
    target_remaining = list(target)

    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'g'
            target_remaining[i] = None

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
st.set_page_config(page_title="Wordle Art Tool", layout="centered")
st.title("🔹 Wordle Art Generator")

word_list = load_word_list()

if "patterns" not in st.session_state:
    st.session_state.patterns = [list("nnnnn") for _ in range(6)]
if "word_of_day" not in st.session_state:
    st.session_state.word_of_day = ""

# Word of the day input
st.subheader("Step 1: Enter the Wordle answer")
word_of_day = st.text_input("Wordle Answer (5 letters)", max_chars=5).lower()
if len(word_of_day) == 5:
    st.session_state.word_of_day = word_of_day

# Colors
color_map = {
    "n": "#787c7e",
    "y": "#c9b458",
    "g": "#6aaa64"
}

# Grid UI: 5 x 6 board
st.subheader("Step 2: Set feedback pattern for each row")

for row in range(6):
    cols = st.columns(5)
    pattern = st.session_state.patterns[row]
    matches = find_matching_words(word_list, st.session_state.word_of_day, "".join(pattern)) if len(st.session_state.word_of_day) == 5 else []
    top_word = matches[0] if matches else ""

    for col in range(5):
        tile_key = f"tile_{row}_{col}"

        if tile_key not in st.session_state:
            st.session_state[tile_key] = "n"

        def toggle(row=row, col=col):
            key = f"tile_{row}_{col}"
            current = st.session_state[key]
            next_state = {'n': 'y', 'y': 'g', 'g': 'n'}
            new_state = next_state[current]
            st.session_state[key] = new_state
            st.session_state.patterns[row][col] = new_state

        color = color_map[st.session_state[tile_key]]
        letter = top_word[col].upper() if len(top_word) == 5 else ""

        with cols[col]:
            st.markdown(
                f"""
                <div style="background-color: {color}; color: white; height: 70px; width: 100%; 
                            display: flex; align-items: center; justify-content: center; 
                            font-size: 32px; font-weight: bold; border-radius: 6px;">
                    {letter}
                </div>
                """,
                unsafe_allow_html=True
            )
            st.button(" ", key=f"btn_{row}_{col}", on_click=toggle, help="Click to cycle colors", use_container_width=True)

# Matching section
if len(st.session_state.word_of_day) == 5:
    st.markdown("---")
    st.subheader("🔍 Top Matches per Row")

    for row in range(6):
        pattern = "".join(st.session_state.patterns[row])
        if pattern == "nnnnn":
            continue
        matches = find_matching_words(word_list, st.session_state.word_of_day, pattern)
        top_word = matches[0] if matches else "(no match)"
        st.markdown(f"**Row {row + 1}** — Pattern: `{pattern}` → **{top_word}**")

    st.markdown("---")
    st.subheader("📊 All Matching Words")

    for row in range(6):
        pattern = "".join(st.session_state.patterns[row])
        if pattern == "nnnnn":
            continue
        matches = find_matching_words(word_list, st.session_state.word_of_day, pattern)
        with st.expander(f"Row {row + 1} ({pattern}) - {len(matches)} matches"):
            st.write(", ".join(matches))
else:
    st.info("Please enter a valid 5-letter Wordle answer.")
