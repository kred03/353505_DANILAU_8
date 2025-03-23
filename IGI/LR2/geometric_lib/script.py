# script.py
from circle import area as circle_area, perimeter as circle_perimeter
from square import area as square_area, perimeter as square_perimeter

# Пример использования
circle_radius = 5
square_side = 4

print(f"Area of circle: {circle_area(circle_radius)}")
print(f"Perimeter of circle: {circle_perimeter(circle_radius)}")
print(f"Area of square: {square_area(square_side)}")
print(f"Perimeter of square: {square_perimeter(square_side)}")