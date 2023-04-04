from math import sqrt
import matplotlib.pyplot as plt
import numpy as np

PHI = (1.0 + sqrt(5)) / 2.0

formula = lambda t, p: (PHI ** -((t - 6 * p) / p)) / (PHI ** 6)

ps = [0.5, 1, 2, 5, 10, 20, 30, 50, 75, 100, 150, 200, 600, 1600]

x = np.linspace(0, 100, 10_000)

fig = plt.figure()
fig.set_size_inches(8.0, 5.0)

for p in ps:
    plt.plot(x, [formula(x_coord, p) for x_coord in x])

plt.title('Forgetting curves')

plt.xlabel('Delay in days')
plt.ylabel('Retention rate')

plt.savefig('prowess_ev_plot/curve_ev.jpg', format='jpg', dpi=1_000)

plt.show()