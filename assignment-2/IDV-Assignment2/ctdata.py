import numpy as np
import matplotlib.pyplot as plt


size = 512
file = 'slice150.raw'  # File Name
data = np.fromfile(file, dtype=np.short)  # load 12-bit data as short (16-bit integer)
data = np.reshape(data, (-1, size))  # reshape data

# Mean and Variance
total = 0  # sum
mean = 0  # mean
variance = 0  # variance
min = data[0][0]  # minimum
max = data[0][0]  # maximum
filters = 11  # 11x11 Filter
# Calculate Mean
for row in range(len(data)):
    for col in range(len(data[0])):
        total = total + data[row][col]
        if data[row][col] < min:
            min = data[row][col]
        elif data[row][col] > max:
            max = data[row][col]
mean = total / (size * size)
print(mean)

# Calculate Variance
for xi in data:
    variance = variance + sum((xi - mean) * (xi - mean)) / (size * size)
print(variance)

# Calculate Profile Line
line = []
value = 255
line = data[value]
plt.figure(1)
plt.title("Profile line")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(line)
plt.savefig('profile_line.png')

# Calculate Histogram
unique = {}
for row in range(len(data)):
    for col in range(len(data[0])):
        data_value = data[row][col]
        if data_value in unique:
            unique[data_value] += 1
        else:
            unique[data_value] = 1

plt.figure(2)
plt.title("Histogram")
plt.xlabel("x")
plt.ylabel("y")
plt.bar(*zip(*unique.items()))
plt.savefig("histogram.png")

# Linear Transformation

linear = []
linear = ((data - min) * (1 / (max - min) * 255))
plt.figure(3)
plt.title("Linear Transformation")
plt.imshow(linear, cmap='gray')
plt.savefig("linear.png")
# Non Linear Transformation
if max > 0:
    log_max = np.log(max)
else:
    log_max = 0
if min > 0:
    log_min = np.log(min)
else:
    log_min = 0

non_linear = np.zeros((size, size))
for row in range(len(data)):
    for col in range(len(data[0])):
        data_value = data[row][col]
        if data_value > 0:
            if np.log(data_value) > 0:
                non_linear[row][col] = ((np.log(data_value) - log_min) * (1 / (log_max - log_min) * 255))

plt.figure(4)
plt.title("Non Linear Transformation")
plt.imshow(non_linear, cmap='gray')
plt.savefig("non-linear.png")

# Box Car Filter
boxcar = []
for row in range(len(data)):
    for col in range(len(data[0])):
        if col + filters <= len(data[0]) and row + filters <= len(data):
            temp = sum(map(sum, data[row:row + filters, col:col + filters]))
            boxcar.append(temp / (filters * filters))

boxcar = np.reshape(boxcar, (-1, size - filters + 1))  # reshape data
plt.figure(4)
plt.title("Box Car Filter")
plt.imshow(boxcar, cmap='gray')
plt.savefig("box-car.png")
# Median Filter
index = filters // 2
median = []
for row in range(len(data)):
    for col in range(len(data[0])):
        if col + filters <= len(data[0]) and row + filters <= len(data):
            temp = np.sort(data[row:row + filters, col:col + filters])
            median.append(temp[index][index])
median = np.reshape(median, (-1, size - filters + 1))  # reshape data
plt.figure(5)
plt.title("Median Filter")
plt.imshow(median, cmap='gray')
plt.savefig("median.png")
