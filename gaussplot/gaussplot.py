from math import e
import numpy as np
import matplotlib.pyplot as plt

a, b, c = 2.0, 2.0, 2.0

w1 = lambda tarari, x: tarari * a * (e ** (-((x - b) ** 2) / (2 * (c ** 2)))) + 2
w2 = lambda tarari, x: w1(tarari, x) / 2
w3 = lambda tarari, x: tarari * (a / 4) + 0.25 if tarari * (a / 4) + 0.25 <= 0.8 else 0.8

def get_w_function(n: int):
    match n:
        case 1: return w1
        case 0: return w2
        case -1: return w3
    
    return None


x = np.linspace(-6, 6, 10_000) #np.linspace(-6, 6, 10_000)


tararis = {0.1: ('-', 'grey'), 0.5: (':', 'black'), 1.0: ('-.', 'black'), 1.5: ('--', 'black'), 2.0: ('-', 'black')}

letter = {1: 'A', 0: 'B', -1: 'C'}

for r in (1, 0, -1):
    for t in tararis:
        if not t in (0.1, 0.5, 1.0, 1.5, 2.0):
            continue
        
        w = lambda x: get_w_function(r)(t, x)
        plt.plot(x, list(map(w, x)), tararis[t][0], color=tararis[t][1], label=f'Ease factor = {t}')

    plt.legend()

    plt.title(f'({letter[r]}) Gauss function ω with response r = {r}.')

    plt.xticks([0, b] if r != -1 else [])

    if r != -1:
        plt.axvline(x=0, ls='-.', color='lightgrey')

    plt.savefig(f'gaussplot/w{r}.jpg', format='jpg', dpi=1_000)

    plt.show()
