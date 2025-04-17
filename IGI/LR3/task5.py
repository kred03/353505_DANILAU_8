# Lab 3: Processing Real-Valued Lists
# Version: 1.0
# Developer: DZMITRY
# Date: 24.03.25

# Function to input a list of real numbers
def input_list():
    """
    Prompt the user to input a list of real numbers.
    :return: A list of real numbers.
    """
    while True:
        try:
            input_string = input("Enter a list of real numbers separated by spaces: ")
            numbers = list(map(float, input_string.split()))
            return numbers
        except ValueError:
            print("Invalid input. Please enter real numbers only.")

# Function to count positive even numbers in the list
def count_positive_even(numbers):
    """
    Count the number of positive even numbers in the list.
    :param numbers: The list of real numbers.
    :return: The count of positive even numbers.
    """
    count = 0
    for num in numbers:
        if num > 0 and num % 2 == 0:
            count += 1
    return count

# Function to calculate the sum of elements after the last zero
def sum_after_last_zero(numbers):
    """
    Calculate the sum of elements after the last occurrence of zero.
    :param numbers: The list of real numbers.
    :return: The sum of elements after the last zero.
    """
    try:
        last_zero_index = len(numbers) - 1 - numbers[::-1].index(0)
        return sum(numbers[last_zero_index + 1:])
    except ValueError:
        return 0  # If there is no zero in the list

# Function to print the list
def print_list(numbers):
    """
    Print the list of numbers.
    :param numbers: The list of real numbers.
    """
    print("List:", numbers)

# Main function to run the program
def main():
    """
    Main function to execute the program.
    """
    while True:
        numbers = input_list()
        print_list(numbers)

        # Task a: Count positive even numbers
        positive_even_count = count_positive_even(numbers)
        print(f"Number of positive even numbers: {positive_even_count}")

        # Task b: Sum of elements after the last zero
        sum_after_zero = sum_after_last_zero(numbers)
        print(f"Sum of elements after the last zero: {sum_after_zero}")

        repeat = input("\nDo you want to process another list? (yes/no): ").strip().lower()
        if repeat != "yes":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()