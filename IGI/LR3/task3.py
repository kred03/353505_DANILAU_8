# Lab 3: Counting Digits in a String
# Version: 1.0
# Developer: DZMITRY
# Date: 24.03.25

# Function to count digits in a string
def count_digits(input_string):
    """
    Count the number of digits in the input string.
    :param input_string: The string to analyze.
    :return: The count of digits in the string.
    """
    count = 0
    for char in input_string:
        if char.isdigit():
            count += 1
    return count

# Main function to run the program
def main():
    """
    Main function to execute the program.
    """
    while True:
        input_string = input("Enter a string: ")
        digit_count = count_digits(input_string)
        print(f"The number of digits in the string is: {digit_count}")

        repeat = input("\nDo you want to analyze another string? (yes/no): ").strip().lower()
        if repeat != "yes":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()