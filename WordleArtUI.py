import streamlit as st
from WordleArt import load_word_list, find_matching_words

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
    "g": "#6aaa64",
    "h": "linear-gradient(90deg, #6aaa64 50%, #c9b458 50%)"
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
            next_state = {'n': 'h', 'h': 'y', 'y': 'g', 'g': 'n'}
            new_state = next_state[current]
            st.session_state[key] = new_state
            st.session_state.patterns[row][col] = new_state

        color = color_map[st.session_state[tile_key]]
        letter = top_word[col].upper() if len(top_word) == 5 else ""

        with cols[col]:
            st.markdown(
                f"""
                <div style="background: {color}; color: white; height: 80px; width: 100%; 
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
