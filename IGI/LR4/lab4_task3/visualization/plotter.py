import matplotlib.pyplot as plt

def plot_comparison(x_values, series_results, math_results, stats, save_path=None):
    plt.figure(figsize=(10, 6))
    
    # Основные графики
    plt.plot(x_values, series_results, 'bo-', label='Series Approximation', markersize=5)
    plt.plot(x_values, math_results, 'r--', label='Math.asin()')
    
    # Особый случай для одной точки
    if len(x_values) == 1:
        plt.plot(x_values[0], series_results[0], 'bo', markersize=10, label='Single Point')
    
    plt.xlabel('x')
    plt.ylabel('arcsin(x)')
    plt.title('Arcsin Calculation Comparison')
    plt.legend()
    plt.grid(True)
    
    # Аннотация
    if stats:
        stats_text = f"Statistics for x ∈ [{min(x_values):.2f}, {max(x_values):.2f}]:\n"
        stats_text += f"Mean: {stats['mean']:.6f}\nMedian: {stats['median']:.6f}"
        
        if len(x_values) >= 2:
            stats_text += f"\nVariance: {stats['variance']:.6f}\nStd Dev: {stats['stdev']:.6f}"
        
        plt.annotate(stats_text, xy=(0.02, 0.98), xycoords='axes fraction',
                    bbox=dict(boxstyle="round", fc="w"), verticalalignment='top')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    plt.show()