#!/usr/bin/env python
# -*- coding: utf8 -*-

'''Create scatter plot'''

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress


# Data with epoch number
cc100 = [[3.45, 1], [3.75, 1], [8.8, 1], [17.2, 1.5], [28.1, 1.75]]
macocu = [[3.2, 2.0], [3.2, 3.0], [6.6, 3.25], [26.2, 2.75], [23.1, 1.00]]
mc4 =[[7.1, 3.5], [7.7, 3.5], [3.3, 1.75], [7.8, 2.5], [11.5, 1.75]]
oscar = [[24.9, 4.0], [24.9, 3.5], [96.3, 2.5], [37.2, 2.5], [53.1, 2.5]]
combined = [[1.3, 1.0], [4.2, 1.5], [1.8, 2.25], [4.2, 3.25], [5.6, 2.25]]

# Data with GB size
cc100 = [[10.3, 1], [11.3, 1], [4.2, 1], [2.1, 1.5], [1.3, 1.75]]
macocu = [[12.1, 2.0], [12.1, 3.0], [4.7, 3.25], [1.4, 2.75], [1.6, 1.00]]
mc4 =[[4.7, 3.5], [5.1, 3.5], [11.0, 1.75], [4.6, 2.5], [2.9, 1.75]]
oscar = [[1.4, 4.0], [1.4, 3.5], [0.4, 2.5], [0.9, 2.5], [0.6, 2.5]]
combined = [[29.2, 1.0], [29.2, 1.5], [20.1, 2.25], [9.0, 3.25], [6.3, 2.25]]

data = [cc100, macocu, mc4, oscar, combined]

# Create scatter plots
fig, ax = plt.subplots()

# Using a circle and a square as shapes
shapes = ['o', 's', "^", "d", "*"]
shape_names = ["Croatian", "Serbian", "Slovene", "Albanian", "Icelandic"]
colors = ['moccasin', 'lightblue', 'lightgreen', 'lightcoral', "mediumpurple"]
color_names = ["CC100", "MaCoCu", "MC4", "OSCAR", "Comb"]

# Plot for GB
# Plot each corpus with a unique color and shape combinations
flat_x = []
flat_y = []
for idx, corpus in enumerate(data):
    for j, (x, y) in enumerate(corpus):
        ax.scatter(x, y, c=colors[idx], marker=shapes[j], label="", edgecolors= "black", s=150)
        flat_x.append(x)
        flat_y.append(y)

# Add the regression line
x = np.array(flat_x)
y = np.array(flat_y)
slope, intercept, r_value, p_value, std_err = linregress(x, y)

# Calculate values for ticks
x_vals = np.linspace(0.25, 25, 500)
plt.plot(x_vals, slope*x_vals + intercept, 'k--', linewidth=1)

# Adjust the legend
for idx, color in enumerate(colors):
    ax.plot([], [], color=color, label=color_names[idx], linewidth=3)

# Then, add legend for shape
for idx, shape in enumerate(shapes):
    ax.scatter([], [], c='gray', marker=shape, label=shape_names[idx])
legend = plt.legend(loc="upper right", fontsize=12.3, ncol=2, columnspacing=-0.1)

# Less space after the shapes
# Adjust space in the second column
for i, text in enumerate(legend.get_texts()):
    if i >= 5:
        text.set_position((text.get_position()[0] - 10.0, text.get_position()[1]))

# Adjusting x-axis to 2-log scale
ax.set_xscale('log', base=2)
ax.set_xlim(0.25, 36)
ax.set_ylim(0.75, 5.5)
ax.set_xticks([0.5, 1, 2, 4, 8, 16, 32])
ax.set_xticklabels([0.5, 1, 2, 4, 8, 16, 32], fontsize=15)
ax.set_yticks(np.arange(1, 6))
ax.set_yticklabels(np.arange(1, 6), fontsize=15)

ax.set_xlabel('Corpus size (GB)', fontsize=15, labelpad=0)
ax.set_ylabel('Position', fontsize=17, labelpad=3)

# Save as PDF
plt.savefig("scatter_gb.pdf", format='pdf')
plt.close()
