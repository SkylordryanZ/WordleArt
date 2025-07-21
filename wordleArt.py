import streamlit as st
import os


def wordle_feedback(guess, target):
    result = ['n'] * 5  # Default: 'n' = letter not in word
    target_remaining = list(target)

    # First pass: green (correct letter, correct place)
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'y'
            target_remaining[i] = None

    # Second pass: yellow (correct letter, wrong place)
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

        if expected == 'y' and c not in letter_pool:
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
        if len(word) == 5 and word.isalpha():
            if matches_feedback_with_pool(word, word_of_day, pattern):
                matches.append(word)
    return matches


def load_word_list():
    file_path = os.path.join(os.path.dirname(__file__), "valid-wordle-words.txt")
    if not os.path.isfile(file_path):
        st.error("Could not find 'valid-wordle-words.txt'. Please place it in the same folder as this app.")
        return []
    with open(file_path, "r") as f:
        return [line.strip().lower() for line in f if len(line.strip()) == 5 and line.strip().isalpha()]


# === Streamlit GUI ===

st.title("🟩 Wordle Pattern Matcher")
st.markdown("Enter the Wordle word of the day and a pattern using `'y'` (present in word) and `'n'` (not in word).")

word_of_day = st.text_input("Word of the Day (5 letters)", max_chars=5).lower()
pattern_input = st.text_input("Feedback Pattern (e.g. `ynnyn`)", max_chars=5).lower()

if word_of_day and pattern_input:
    if len(word_of_day) != 5 or len(pattern_input) != 5:
        st.warning("Both fields must be exactly 5 letters.")
    else:
        word_list = load_word_list()
        if word_list:
            matches = find_matching_words(word_list, word_of_day, pattern_input)
            st.subheader("🔍 Matching Words")
            if matches:
                st.write(f"Found {len(matches)} matching words:")
                st.write(", ".join(matches))
            else:
                st.info("No matching words found.")
