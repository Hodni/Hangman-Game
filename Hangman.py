import random

# Define variables
HANGMAN_ASCII_ART = """
Welcome to the game Hangman
 _                                             
| |                                            
| |__   __ _ _ __   __ _ _ __ ___   __ _ _ __  
| '_ \ / _` | '_ \ / _` | '_ ` _ \ / _` | '_ \ 
| | | | (_| | | | | (_| | | | | | | (_| | | | |
|_| |_|\__,_|_| |_|\__, |_| |_| |_|\__,_|_| |_|
                    __/ |                      
                   |___/                       
"""
MAX_TRIES = 6  # The maximum number of tries a player has in the game

# Dictionary to hold hangman photos
HANGMAN_PHOTOS = {
    1: """
         -----
        |     |
        |
        |
        |
        |
      -------""",
    2: """
         -----
        |     |
        |     O
        |
        |
        |
      -------""",
    3: """
         -----
        |     |
        |     O
        |     |
        |
        |
      -------""",
    4: """
         -----
        |     |
        |     O
        |    /|\\
        |
        |
      -------""",
    5: """
         -----
        |     |
        |     O
        |    /|\\
        |    /
        |
      -------""",
    6: """
         -----
        |     |
        |     O
        |    /|\\
        |    / \\
        |
      -------"""
}


def choose_word(file_path, index):
    """
    Choose a word from a file at a specified index.

    Args:
    file_path (str): Path to the file containing the list of words.
    index (int): Index of the word to choose.

    Returns:
    tuple: A tuple containing the total number of unique words in the file
    and the chosen word at the specified index.
    """
    with open(file_path, 'r') as file:
        word_list = file.read().split()
        unique_words = set(word_list)
        total_unique_words = len(unique_words)
        chosen_index = index % total_unique_words  # Handle circular indexing
        chosen_word = list(unique_words)[chosen_index]
        return total_unique_words, chosen_word


def print_hangman(num_of_tries):
    """
    Print the hangman image corresponding to the number of tries.

    Args:
    num_of_tries (int): Number of incorrect guesses made by the player.
    """
    if num_of_tries in HANGMAN_PHOTOS:
        print(HANGMAN_PHOTOS[num_of_tries])
    else:
        print("Game over! You have reached the maximum number of attempts.")


def check_valid_input(letter_guessed):
    """
    Check if the guessed letter is valid.

    Args:
    letter_guessed (str): The letter guessed by the player.

    Returns:
    bool: True if the input is valid, False otherwise.
    """
    if len(letter_guessed) != 1 or not letter_guessed.isalpha():
        print("X")
        print("Invalid input! Please enter a single alphabetical character.")
        return False
    return True


def try_update_letter_guessed(letter_guessed, old_letters_guessed):
    """
    Update the list of guessed letters.

    Args:
    letter_guessed (str): The letter guessed by the player.
    old_letters_guessed (list): List of previously guessed letters.

    Returns:
    bool: True if the update was successful, False otherwise.
    """
    if not check_valid_input(letter_guessed):
        return False

    if letter_guessed in old_letters_guessed:
        print("You already guessed this letter. Try again.")
        old_letters_guessed = list(set(old_letters_guessed))  # Remove duplicates
        print("X\n" + " -> ".join(sorted(old_letters_guessed)))
        return False
    else:
        old_letters_guessed.append(letter_guessed)
        old_letters_guessed.sort()
        return True


def show_hidden_word(secret_word, old_letters_guessed):
    """
    Display the progress of the word.

    Args:
    secret_word (str): The word to be guessed.
    old_letters_guessed (list): List of previously guessed letters.

    Returns:
    str: The word with guessed letters revealed and others hidden.
    """
    display_word = ""
    for letter in secret_word:
        if letter.lower() in old_letters_guessed:
            display_word += letter + " "
        else:
            display_word += "_ "
    return display_word.strip()


def check_win(secret_word, old_letters_guessed):
    """
    Check if the player has won.

    Args:
    secret_word (str): The word to be guessed.
    old_letters_guessed (list): List of previously guessed letters.

    Returns:
    bool: True if the player has guessed all the letters in the word, False otherwise.
    """
    return all(letter.lower() in old_letters_guessed for letter in secret_word)


def play_hangman():
    """
    Play the Hangman game.
    """
    word = choose_word(r"D:\YodGimel\wordsForHangman.txt", 1)[1]  # Choose a word from the file
    guessed_letters = []  # List to store guessed letters
    wrong_attempts = 0  # Counter for wrong attempts

    print("Welcome to Hangman!")
    print(HANGMAN_ASCII_ART)  # Display the Hangman ASCII art

    # Game loop
    while wrong_attempts < MAX_TRIES:
        print("\nWord:", show_hidden_word(word, guessed_letters))  # Show the progress of the word
        print("\n")

        # Take input from user
        guess = input("Guess a letter: ").lower()  # Convert guess to lowercase

        # Update guessed letters
        if not try_update_letter_guessed(guess, guessed_letters):
            continue

        # Check if the guessed letter is in the word
        if guess in word:
            guessed_letters.append(guess)
            print("Correct guess!")
        else:
            wrong_attempts += 1
            print("Wrong guess!")
            print_hangman(wrong_attempts)

        # Check if the player has won
        if check_win(word, guessed_letters):
            print("\nCongratulations! You guessed the word:", word)
            break

    # If the player runs out of attempts
    if wrong_attempts == MAX_TRIES:
        print("\nSorry, you ran out of attempts. The word was:", word)


def main():
    play_hangman()


if __name__ == "__main__":
    main()
