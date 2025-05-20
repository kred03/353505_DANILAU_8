def get_user_input():
    """
    Получает и валидирует пользовательский ввод
    """
    while True:
        try:
            x = float(input("Enter x (|x| <= 1): "))
            if abs(x) > 1:
                print("Error: |x| must be ≤ 1")
                continue
            eps = float(input("Enter precision (eps): "))
            return x, eps
        except ValueError:
            print("Invalid input. Please enter numbers.")