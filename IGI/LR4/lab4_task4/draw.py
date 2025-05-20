import matplotlib.pyplot as plt
import math

def draw_pentagon(side, color, label_text, save_path=None):
    angles = [2 * math.pi * i / 5 for i in range(5)]
    radius = side / (2 * math.sin(math.pi / 5))
    x = [radius * math.cos(a) for a in angles] + [radius * math.cos(0)]
    y = [radius * math.sin(a) for a in angles] + [radius * math.sin(0)]

    fig, ax = plt.subplots()
    ax.fill(x, y, color=color, edgecolor='black')
    ax.text(0, 0, label_text, fontsize=12, ha='center', va='center', color='white')
    ax.set_aspect('equal')
    ax.axis('off')

    if save_path:
        plt.savefig(save_path)
    plt.show()
