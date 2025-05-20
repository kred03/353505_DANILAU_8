from models.analyzer import ArcsinAnalyzer
from utils.helpers import get_user_input

def main():
    analyzer = ArcsinAnalyzer()
    
    print("1. Calculate for default range (-0.9 to 0.9)")
    print("2. Calculate for single value")
    choice = input("Choose option (1 or 2): ").strip()
    
    if choice == '1':
        # Расчет для диапазона
        print("\nCalculating for range -0.9 to 0.9...")
        analyzer.calculate_for_range()
        analyzer.print_results()
        analyzer.visualize(save_path="arcsin_comparison_range.png")
        
    elif choice == '2':
        # Расчет для одного значения
        x, eps = get_user_input()
        print(f"\nCalculating for x = {x} with precision {eps}...")
        
        # Для графика используем 3 точки: x-0.1, x, x+0.1
        start = max(-1.0, x - 0.1)
        end = min(1.0, x + 0.1)
        analyzer.calculate_for_range(start=start, end=end, step=0.1, eps=eps)
        
        analyzer.print_results()
        analyzer.visualize(save_path=f"arcsin_single_{x}.png")
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()