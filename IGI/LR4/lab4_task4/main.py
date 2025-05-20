from geometry import Pentagon
from draw import draw_pentagon

def get_positive_float(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                raise ValueError
            return value
        except ValueError:
            print("Please enter a positive number.")

def main():
    print("=== Pentagon Generator ===")
    side = get_positive_float("Enter side length: ")
    color = input("Enter color (e.g., 'blue', '#FF5733'): ")
    label = input("Enter label text: ")

    pent = Pentagon(side, color)
    print(pent.describe())

    draw_pentagon(side, color, label, save_path="pentagon.png")
    print("Pentagon saved as pentagon.png")

if __name__ == "__main__":
    main()
