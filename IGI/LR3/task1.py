# Lab 3: Calculation of arcsin(x) using a power series
# Version: 1.0
# Developer: DZMITRY
# Date: 24.03.25

import math

# Decorator to demonstrate its usage
def debug_decorator(func):
    """
    A decorator to log function calls and their results.
    """
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__} with args: {args}, kwargs: {kwargs}")
        result = func(*args, **kwargs)
        print(f"Function {func.__name__} returned: {result}")
        return result
    return wrapper

# Function to calculate factorial
def factorial(n):
    """
    Calculate the factorial of a number using math.factorial.
    """
    return math.factorial(n)

# Function to calculate arcsin(x) using a power series
@debug_decorator
def arcsin_series(x, eps=1e-6, max_iterations=500):
    """
    Calculate arcsin(x) using a power series expansion.
    :param x: The input value for arcsin(x), |x| <= 1.
    :param eps: The precision for the calculation.
    :param max_iterations: Maximum number of iterations to prevent infinite loops.
    :return: A tuple containing the calculated value of arcsin(x) and the number of terms used.
    """
    result = 0.0
    for n in range(max_iterations):
        numerator = factorial(2 * n)
        denominator = (4 ** n) * (factorial(n) ** 2) * (2 * n + 1)
        term = (numerator / denominator) * (x ** (2 * n + 1))
        result += term
        if abs(term) < eps:
            break
    return result, n + 1

# Function to get user input with validation
def get_user_input():
    """
    Get user input for x and eps with validation.
    :return: A tuple containing x and eps.
    """
    while True:
        try:
            x = float(input("Enter x (|x| <= 1): "))
            if abs(x) > 1:
                print("Error: |x| must be less than or equal to 1.")
                continue
            eps = float(input("Enter precision (eps): "))
            return x, eps
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# Function to print the result in a table format
def print_result(x, n, fx, math_fx, eps):
    """
    Print the result in a table format.
    :param x: The input value x.
    :param n: The number of terms used in the series.
    :param fx: The calculated value of arcsin(x).
    :param math_fx: The value of arcsin(x) from the math module.
    :param eps: The precision used in the calculation.
    """
    print("\n| x | n | F(x) | Math F(x) | eps |")
    print("|---|---|------|-----------|-----|")
    print(f"| {x} | {n} | {fx:.6f} | {math_fx:.6f} | {eps} |")

# Main function to run the program
def main():
    """
    Main function to execute the program.
    """
    while True:
        x, eps = get_user_input()
        fx, n = arcsin_series(x, eps)
        math_fx = math.asin(x)
        print_result(x, n, fx, math_fx, eps)

        repeat = input("Do you want to calculate again? (yes/no): ").strip().lower()
        if repeat != "yes":
            print("Exiting the program. Goodbye!")
            break

if __name__ == "__main__":
    main()