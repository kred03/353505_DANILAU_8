# Lab 3: Sum of Every Second Number
# Version: 1.0
# Developer: DZMITRY
# Date: 24.03.25

# Function to calculate the sum of every second number
def sum_every_second_number():
    numbers = []
    print("Enter integers one by one. Enter 0 to finish:")
    
    while True:
        try:
            num = int(input("Enter a number: "))
            if num == 0:
                break
            numbers.append(num)
        except ValueError:
            print("Invalid input. Please enter a valid integer.")
    
    # Calculate the sum of every second number
    total_sum = sum(numbers[::2])
    return total_sum, numbers

# Main function to run the program
def main():
    while True:
        total_sum, numbers = sum_every_second_number()
        print("\nEntered numbers:", numbers)
        print("Sum of every second number:", total_sum)
        
        repeat = input("\nDo you want to calculate again? (yes/no): ").strip().lower()
        if repeat != "yes":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()