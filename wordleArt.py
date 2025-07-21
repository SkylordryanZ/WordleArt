def wordle_feedback(guess, target):
    result = ['n'] * 5  # default to 'n' (not in word)
    target_remaining = list(target)

    # First pass: green
    for i in range(5):
        if guess[i] == target[i]:
            result[i] = 'y'
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
        if expected == 'y' and c not in letter_pool:
            return False
        if expected == 'n' and c in letter_pool:
            return False
    # Must also match simulated feedback
    feedback = wordle_feedback(guess, word_of_day)
    for i in range(5):
        if feedback[i] != pattern[i]:
            return False
    return True


def find_matching_words_from_pool(word_list, word_of_day, pattern_str):
    if len(pattern_str) != 5:
        raise ValueError("Pattern must be 5 characters long")
    pattern = {i: pattern_str[i] for i in range(5)}
    matches = []
    for word in word_list:
        word = word.lower()
        if len(word) == 5 and word.isalpha():
            if matches_feedback_with_pool(word, word_of_day.lower(), pattern):
                matches.append(word)
    return matches


# === Example Usage ===
if __name__ == "__main__":
    sample_word_list = ["crane", "trace", "crate", "brace", "grape", "slate", "plane", "flame", "cater", "caste", "apple", "quiet"]

    word_of_day = input("Enter the Wordle word of the day (5 letters): ").lower()
    pattern_str = input("Enter the desired feedback pattern (use 'y' for present, 'n' for not-in-word): ").lower()

    if len(word_of_day) != 5 or len(pattern_str) != 5:
        print("Error: Both word and pattern must be exactly 5 letters.")
    else:
        results = find_matching_words_from_pool(sample_word_list, word_of_day, pattern_str)
        print("\nMatching words:")
        for word in results:
            print(word)
