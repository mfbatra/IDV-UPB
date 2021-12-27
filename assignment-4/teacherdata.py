import pandas as pd
import numpy as np
from pandas.plotting import scatter_matrix
from pandas.plotting import parallel_coordinates
import matplotlib.pyplot as plt
#Read File and columns
file = 'DataWeierstrass.csv'
df = pd.read_csv(file, sep=';')
cols = ['overall impression', 'professional expertise', 'motivation', 'clear presentation']

# Parallel Coordinates (b)
parallel_coordinates(df, class_column='professor', cols=cols)
plt.gca().invert_yaxis()
plt.legend(
    loc=6, bbox_to_anchor=(1.05, 0.56),
    frameon=False,  # reverse legend
    fontsize=4.0)
plt.savefig('parallel-coordinates.png')

#Scatter Matrix
plt.figure(2)
scatter_matrix(df, alpha=0.2,  diagonal='hist', figsize=(10, 10))
plt.savefig('scatter-matrix.png')
