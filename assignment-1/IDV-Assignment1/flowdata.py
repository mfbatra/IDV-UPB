import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm, colors

file = 'field2.irreg'  # File Name
header = 6  # header size
header_list = ["x", "y", "z", "u", "v", "w"]  # name of headers
column_remove = ["z", "w"]  # columns to remove
data = pd.read_csv(file, header=None, skiprows=header, delimiter=" ", names=header_list)  # Read file without header
data.drop(column_remove, axis=1, inplace=True)  # Remove z and dz since 2d
wv = plt.axes(xlabel="x", ylabel="y")  # Wind vector plotting axes with labels
Cmap = cm.ScalarMappable(cmap=plt.cm.jet)  # Create Mappable for colorbar creation
# calculate arrow length
for index, row in data.iterrows():
    length = np.sqrt(row.u * row.u + row.v * row.v)  # use any length formula to calculate length of arrow
    wv.arrow(row.x, row.y, row.u, row.v, color=cm.jet(length))  # draw arrows
plt.show()  # Display Plot
plt.colorbar(Cmap)