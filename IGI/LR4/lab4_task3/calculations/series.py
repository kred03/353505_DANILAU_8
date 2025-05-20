import math

def calculate_arcsin_series(x, eps=1e-6, max_iterations=500):
    """
    Вычисляет arcsin(x) с помощью разложения в ряд
    """
    result = 0.0
    terms_used = 0
    for n in range(max_iterations):
        numerator = math.factorial(2 * n)
        denominator = (4 ** n) * (math.factorial(n) ** 2) * (2 * n + 1)
        term = (numerator / denominator) * (x ** (2 * n + 1))
        result += term
        terms_used += 1
        if abs(term) < eps:
            break
    return result, terms_used