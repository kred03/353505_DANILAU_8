from statistics import mean, median, variance, stdev
from collections import Counter

def calculate_stats(values):
    """
    Вычисляет статистические показатели
    """
    if len(values) < 1:
        return None
    
    rounded_values = [round(v, 4) for v in values]
    counts = Counter(rounded_values)
    mode_value = counts.most_common(1)[0][0]
    
    stats = {
        'mean': mean(values),
        'median': median(values),
        'mode': mode_value,
    }
    
    # Добавляем дисперсию и СКО только если есть достаточное количество точек
    if len(values) >= 2:
        stats['variance'] = variance(values)
        stats['stdev'] = stdev(values)
    else:
        stats['variance'] = None
        stats['stdev'] = None
    
    return stats