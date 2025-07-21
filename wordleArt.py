import os
import streamlit as st

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

        if expected in ['y', 'g', 'h'] and c not in letter_pool:
            return False
        if expected == 'n' and c in letter_pool:
            return False

    feedback = wordle_feedback(guess, word_of_day)
    for i in range(5):
        if pattern[i] == 'h' and feedback[i] not in ['y', 'g']:
            return False
        elif pattern[i] != 'h' and feedback[i] != pattern[i]:
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
