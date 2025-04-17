# Lab 3: Text Analysis
# Version: 1.0
# Developer: DZMITRY
# Date: 24.03.25

# Initialize the input string
input_string = "So she was considering in her own mind, as well as she could, for the hot day made her feel very sleepy and stupid, whether the pleasure of making a daisy-chain would be worth the trouble of getting up and picking the daisies, when suddenly a White Rabbit with pink eyes ran close by her."

# Function to clean the input string from punctuation
def clean_string(input_string):
    """
    Remove commas and other non-alphabetic characters from the string.
    :param input_string: The input string to clean.
    :return: A cleaned string with words separated by spaces.
    """
    cleaned_string = input_string.replace(",", "")
    return cleaned_string

# Function to count words with length equal to 3
def count_three_letter_words(words):
    """
    Count the number of words with exactly 3 letters.
    :param words: A list of words.
    :return: The count of 3-letter words.
    """
    count = 0
    for word in words:
        if len(word) == 3:
            count += 1
    return count

# Function to find words with equal number of vowels and consonants
def find_balanced_words(words):
    """
    Find words where the number of vowels equals the number of consonants.
    :param words: A list of words.
    :return: A list of tuples containing the word and its index.
    """
    vowels = "aeiou"
    balanced_words = []
    for index, word in enumerate(words):
        vowel_count = 0
        consonant_count = 0
        for char in word.lower():
            if char in vowels:
                vowel_count += 1
            elif char.isalpha():
                consonant_count += 1
        if vowel_count == consonant_count:
            balanced_words.append((word, index + 1))  # +1 to make index human-readable
    return balanced_words

# Function to sort words by length in descending order
def sort_words_by_length(words):
    """
    Sort the words by their length in descending order.
    :param words: A list of words.
    :return: A list of words sorted by length.
    """
    return sorted(words, key=len, reverse=True)

# Main function to run the program
def main():
    """
    Main function to execute the program.
    """
    cleaned_string = clean_string(input_string)
    words = cleaned_string.split()

    # Task a: Count words with length equal to 3
    three_letter_count = count_three_letter_words(words)
    print(f"Number of 3-letter words: {three_letter_count}")

    # Task b: Find words with equal number of vowels and consonants
    balanced_words = find_balanced_words(words)
    print("\nWords with equal number of vowels and consonants:")
    for word, index in balanced_words:
        print(f"Word: {word}, Position: {index}")

    # Task c: Sort words by length in descending order
    sorted_words = sort_words_by_length(words)
    print("\nWords sorted by length in descending order:")
    print(", ".join(sorted_words))

if __name__ == "__main__":
    main()