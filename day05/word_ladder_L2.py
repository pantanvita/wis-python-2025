import random


# -----------------------
# Word Ladder Logic
# -----------------------

def one_letter_diff(word1: str, word2: str) -> bool:
    """Return True if the words differ by exactly one letter."""
    if len(word1) != len(word2):
        return False

    diff = sum(1 for a, b in zip(word1, word2) if a != b)
    return diff == 1


def is_valid_word(word: str, word_list: set) -> bool:
    """Check if a word exists in the dictionary of allowed words."""
    return word in word_list


def play_ladder_round(current_word: str, new_word: str, word_list: set):
    """
    Attempt to move from current_word to new_word.
    Returns (status, updated_word)
    status: "correct" or "invalid"
    """
    if not is_valid_word(new_word, word_list):
        return "invalid", current_word

    if not one_letter_diff(current_word, new_word):
        return "invalid", current_word

    return "correct", new_word


# -----------------------
# Load word list from file
# -----------------------

def load_word_list(wordlist_4Letter: str) -> set:
    """
    Load a text file containing one word per line.
    Returns a set of words (lowercase, stripped).
    """
    words = set()
    try:
        with open(wordlist_4Letter, "r") as file:
            for line in file:
                word = line.strip().lower()
                # Only include valid 4-letter alphabetic words
                if len(word) == 4 and word.isalpha():
                    words.add(word)
    except FileNotFoundError:
        print(f"Error: Cannot find {wordlist_4Letter}. Make sure it exists.")
        return set()

    return words


# -----------------------
# Main Game
# -----------------------

def main():
    print("Loading dictionary…")

    # Load all 4-letter English words from file
    word_list = load_word_list("wordlist_4Letter.txt")

    if not word_list:
        print("Word list is empty. Exiting.")
        return
    
    if len(word_list) < 10:
        print("ERROR: Your word list file does not contain enough 3-letter words.")
        return

    print(f"Loaded {len(word_list)} valid 4-letter words.\n")
    
    print("\nWelcome to the Word Ladder Game!")
    print("Rules:")
    print(" - Enter a new word that differs by ONE letter from the last word")
    print(" - Your word must be valid and approved by the Collins Dictionary list.")
    print(" - You get only 3 incorrect attempts.")
    print(" - The ladder ends after 8 total words.\n")

    # Choose random starting word
    current_word = random.choice(list(word_list))
    print(f"Starting word: {current_word}")

    ladder = [current_word]
    score = 0
    mistakes = 0
    steps = 1  # starting word counts as step 1

# Game loop
    while True:
        player_word = input("Enter the next word: ").strip().lower()

        if player_word not in word_list:
            mistakes += 1
            print("Invalid move: word not in dictionary. \n")
            print(f"Mistakes: {mistakes}/3 \n")
            
        elif not one_letter_diff(current_word, player_word):
            mistakes += 1
            print("Invalid move: word must differ by ONE letter. \n")
            print(f"Mistakes: {mistakes}/3 \n")
            
        else:
            # Valid move
            score += 1
            ladder.append(player_word)
            current_word = player_word
            print(f"Good! Ladder so far: {ladder}\n")

        # End conditions
        if mistakes == 3:
            print("You used all 3 incorrect attempts!")
            break

        if len(ladder) == 8:
            print("Great job! You completed a 8-word ladder!")
            break

    print("\nGame Over!")
    print(f"\nFinal ladder: {ladder}")
    print(f"Your final score: {score}")

# Run the game only when executed directly
if __name__ == "__main__":
    main()
