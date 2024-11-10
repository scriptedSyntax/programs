#It generates random keywords that match the words provided. still under making only accept 3 words

import random
import string
from itertools import permutations


def random_case(word):
    """Randomly change the case of each letter in the word."""
    return ''.join(random.choice([char.lower(), char.upper()]) for char in word)


def generate_combinations(base_words):
    """Generate all unique combinations of the base words."""
    combinations = set()

    # Include all permutations of the base words
    for r in range(1, len(base_words) + 1):  # Include single words to all combinations
        for combo in permutations(base_words, r):
            combined_word = ''.join(combo)  # Merge words without symbols
            if 5 <= len(combined_word) <= 15:
                combinations.add(random_case(combined_word))

    # Also include the combination of all words together
    all_combined = ''.join(base_words)
    if 5 <= len(all_combined) <= 15:
        combinations.add(random_case(all_combined))

    return list(combinations)


def generate_passwords(base_words, count=10):
    # Generate combinations of base words
    word_combinations = generate_combinations(base_words)

    # Define all possible symbols
    symbols = string.punctuation + string.digits

    for _ in range(count):
        # Randomly select a combination
        if word_combinations:
            selected_word = random.choice(word_combinations)
        else:
            continue

        # Randomly decide how many symbols to insert (0 to 3)
        num_symbols = random.randint(0, 3)

        # Create password with symbols either at the beginning or end
        prefix_symbols = ''.join(random.choices(symbols, k=num_symbols))
        suffix_symbols = ''.join(random.choices(symbols, k=num_symbols))

        password = f"{prefix_symbols}{selected_word}{suffix_symbols}"

        # Ensure final password length is between 5 and 15 characters
        if 5 <= len(password) <= 15:
            print(password)


# Example usage
base_words = ["test", "with", "me"]

generate_passwords(base_words)