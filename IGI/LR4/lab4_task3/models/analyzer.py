from calculations.series import calculate_arcsin_series
from calculations.statistics import calculate_stats
from visualization.plotter import plot_comparison
import math

class ArcsinAnalyzer:
    def __init__(self):
        self.data = []
        self.x_values = []
        self.series_results = []
        self.math_results = []
    
    def calculate_for_range(self, start=-0.9, end=0.9, step=0.1, eps=1e-6):
        self.data = []
        self.x_values = []
        self.series_results = []
        self.math_results = []
        
        x = start
        while x <= end:
            fx, n = calculate_arcsin_series(x, eps)
            math_fx = math.asin(x)
            self.data.append({
                'x': x,
                'n': n,
                'F(x)': fx,
                'Math F(x)': math_fx,
                'eps': abs(fx - math_fx)
            })
            self.x_values.append(x)
            self.series_results.append(fx)
            self.math_results.append(math_fx)
            x = round(x + step, 2)
    
    def get_statistics(self):
        if not self.data:
            return None
        return calculate_stats(self.series_results)
    
    def visualize(self, save_path=None):
        if not self.data:
            raise ValueError("No data to plot. Run calculate_for_range() first.")
        stats = self.get_statistics()
        plot_comparison(
            self.x_values,
            self.series_results,
            self.math_results,
            stats,
            save_path
        )
    
    def print_results(self):
        if not self.data:
            print("No data available.")
            return
        
        print("\n| x | n | F(x) | Math F(x) | eps |")
        print("|---|---|------|-----------|-----|")
        for entry in self.data:
            print(f"| {entry['x']:.2f} | {entry['n']} | {entry['F(x)']:.6f} | {entry['Math F(x)']:.6f} | {entry['eps']:.2e} |")