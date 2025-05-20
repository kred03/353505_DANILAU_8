def input_float(prompt: str) -> float:
    """Запрашивает у пользователя ввод числа с плавающей точкой с проверкой ошибок."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def input_nonempty_string(prompt: str) -> str:
    """Запрашивает у пользователя непустую строку."""
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("Input cannot be empty.")
