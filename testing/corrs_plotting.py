from typing import List, Tuple
from math import sqrt

import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

def normalize(series: List[int | float] | Tuple[int | float], element: int | float = None) -> List[float] | float:
    if not isinstance(series, (list, tuple)):
        raise ValueError('Invalid series.')
    
    mean = sum(series) / len(series)

    std = sqrt(sum([(data_point - mean) ** 2 for data_point in series]) / len(series))

    return (element - mean) / std if element is not None else [(data_point - mean) / std for data_point in series]

data = {1.25: {0: {'pearson': 0.027513905543997814, 'spearman': 0.05258261145846417, 'kendall': 0.04396425882056702}}, 1.5: {0: {'pearson': 0.0034270069914200166, 'spearman': 0.05242458760851476, 'kendall': 0.0437763865981264}}, 1.618: {0: {'pearson': -0.0011499512287737284, 'spearman': 0.05237788443716579, 'kendall': 0.04371984057905841}}, 1.75: {0: {'pearson': -0.003343003545414519, 'spearman': 0.05232436081227296, 'kendall': 0.043658947731015176}}, 2: {0: {'pearson': -0.004640916192098909, 'spearman': 0.05226458933049234, 'kendall': 0.04358665881927977}}, 2.718: {0: {'pearson': -0.005033629196490749, 'spearman': 0.05215412963642344, 'kendall': 0.04345871221318035}}, 3.142: {0: {'pearson': -0.005044509841031803, 'spearman': 0.05209535619779018, 'kendall': 0.04339665911897364}}}


rdt = {'pearson': {}, 'spearman': {}, 'kendall': {}}

for n in data:
    ks = tuple(data[n].keys())
    
    rdt['pearson'][n] = {1: data[n][ks[0]]['pearson']}
    rdt['spearman'][n] = {1: data[n][ks[0]]['spearman']}
    rdt['kendall'][n] = {1: data[n][ks[0]]['kendall']}


#plt.figure(figsize=(1536, 754))

fig, ax = plt.subplots()

x = ['1.25', '1.5', 'φ', '1.75', '2', 'e', 'π']
x_values = list(rdt['pearson'].keys())
methods = {}

colors = ['royalblue', 'firebrick', 'indigo']

for method in rdt:
    if not x:
        x = list(rdt[method].keys())
    
    methods[method] = [data_dict[1] for data_dict in rdt[method].values()]

for method in methods:
    y = normalize(methods[method])
    smooth_y = interp1d(x_values, y)
    
    color = colors.pop(0)
    
    plt.plot(x, smooth_y(x_values), color=color, label=method.capitalize())
    
    plt.scatter(x, y, color=color)


plt.title('Normalized correlations per base')

plt.xlabel('Bases')
plt.ylabel('Normalized correlations')

plt.yticks([-1.5, 0, 1.5])

plt.ylim(top=3, bottom=-2.25)

plt.legend()



# We need to draw the canvas, otherwise the labels won't be positioned and 
# won't have values yet.
fig.set_size_inches(8.0, 5.0)
fig.canvas.draw()

#labels = [item.get_text() for item in ax.get_yticklabels()]
labels = ['-1.5σ', '0', '1.5σ']

ax.set_yticklabels(labels)

plt.savefig('testing/normalized_correlations.jpg', format='jpg', dpi=1_000)

plt.show()