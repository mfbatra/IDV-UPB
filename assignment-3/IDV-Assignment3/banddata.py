import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

file1 = 'orion/i170b1h0_t0.txt'  # File Name
file2 = 'orion/i170b2h0_t0.txt'  # File Name
file3 = 'orion/i170b3h0_t0.txt'  # File Name
file4 = 'orion/i170b4h0_t0.txt'  # File Name

band1 = pd.read_csv(file1, header=None, sep=',')
band1 = np.flipud(band1)
band2 = pd.read_csv(file2, header=None, sep=',')
band2 = np.flipud(band2)
band3 = pd.read_csv(file3, header=None, sep=',')
band3 = np.flipud(band3)
band4 = pd.read_csv(file4, header=None, sep=',')
band4 = np.flipud(band4)

# Calculate Max,Min,Mean and Variance (a)
total = 0
mean = 0
variance = 0
value = 0
min = band2[0][0]
max = band2[0][0]

for row in range(len(band2)):
    for col in range(len(band2[0])):
        total = total + band2[row][col]
        if band2[row][col] < min:
            min = band2[row][col]
        elif band2[row][col] > max:
            max = band2[row][col]
            value = row
            valuec = col
mean = total / (len(band2) * len(band2))

total = 0
for row in range(len(band2)):
    for col in range(len(band2[0])):
        total = total + (band2[row][col] - mean) ** 2
variance = total / (len(band2) * len(band2))

print(min)
print(max)
print(mean)
print(variance)

# Profile Line (b)

line = []
line = band2[value]
plt.figure(1)
plt.title("Profile line of Band 2")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(line)
plt.savefig('profile_line-band2.png')

# Calculate Histogram (c)
unique = {}
for row in range(len(band2)):
    for col in range(len(band2[0])):
        data_value = band2[row][col]
        if data_value in unique:
            unique[data_value] += 1
        else:
            unique[data_value] = 1

plt.figure(2)
plt.title("Histogram")
plt.xlabel("x")
plt.ylabel("y")
plt.plot(*zip(*unique.items()))
plt.savefig("histogram-band2.png")

# Non Linear Transformation (d)
if max > 0:
    log_max = np.log(max)
else:
    log_max = 0
if min > 0:
    log_min = np.log(min)
else:
    log_min = 0

non_linear = np.zeros((len(band2), len(band2)))
for row in range(len(band2)):
    for col in range(len(band2[0])):
        data_value = band2[row][col]
        if data_value > 0:
            if np.log(data_value) > 0:
                non_linear[row][col] = ((np.log(data_value) - log_min) * (1 / (log_max - log_min) * 255))

plt.figure(3)
plt.title("Non Linear Transformation")
plt.plot(non_linear)
plt.savefig("non-linear-band2.png")


# Histogram Equalization (e)

# Calculate Probability of All Bands

def create_frequency(band2):
    unique = {}
    for row in range(len(band2)):
        for col in range(len(band2[0])):
            data_value = band2[row][col]
            if data_value in unique:
                unique[data_value] += 1
            else:
                unique[data_value] = 1
    return unique


def max_of(band2):
    max = 0


def cum_sum(band2):
    cdf = []
    cumsum = 0
    for elt in band2:
        cumsum += elt
        cdf.append(cumsum)
    return cdf


def max_of(band2):
    max = 0
    for key in band2:
        if key > max:
            max = key
    return max


def map_it(band2, final2):
    upper = 0
    inner = 0
    bandNew = np.zeros((500, 500))
    for i in band2:
        for j in i:
            bandNew[upper][inner] = final2[j]
            inner = inner + 1
        upper = upper + 1
        inner = 0
    return bandNew


# Calculate Frequency
frequency1 = create_frequency(band1)
frequency2 = create_frequency(band2)
frequency3 = create_frequency(band3)
frequency4 = create_frequency(band4)

# Calculate Probability

prob1 = {a: b / sum(frequency1.values()) for a, b in frequency1.items()}
prob2 = {a: b / sum(frequency2.values()) for a, b in frequency2.items()}
prob3 = {a: b / sum(frequency3.values()) for a, b in frequency3.items()}
prob4 = {a: b / sum(frequency4.values()) for a, b in frequency4.items()}


# Calculate CDF

cdf1 = cum_sum(np.array(list(prob1.values())))
cdf2 = cum_sum(np.array(list(prob2.values())))
cdf3 = cum_sum(np.array(list(prob3.values())))
cdf4 = cum_sum(np.array(list(prob4.values())))
# Calculate CDF * max
cdf1 = [int(i * max_of(prob1)) for i in cdf1]
cdf2 = [int(i * max_of(prob1)) for i in cdf2]
cdf3 = [int(i * max_of(prob3)) for i in cdf3]
cdf4 = [int(i * max_of(prob4)) for i in cdf4]

final1 = dict(zip(frequency1.keys(), cdf1))
final2 = dict(zip(frequency2.keys(), cdf2))
final3 = dict(zip(frequency3.keys(), cdf3))
final4 = dict(zip(frequency4.keys(), cdf4))

img1 = map_it(band1, final1)
img2 = map_it(band2, final2)
img3 = map_it(band3, final3)
img4 = map_it(band4, final4)
plt.figure(4)
plt.title("Images of Band 1")
plt.xlabel("x")
plt.ylabel("y")
plt.imshow(img1, cmap='gray')
plt.savefig("image-band1.png")

plt.figure(5)
plt.title("Images of Band 2")
plt.xlabel("x")
plt.ylabel("y")
plt.imshow(img2, cmap='gray')
plt.savefig("image-band2.png")

plt.figure(6)
plt.title("Images of Band 3")
plt.xlabel("x")
plt.ylabel("y")
plt.imshow(img3, cmap='gray')
plt.savefig("image-band3.png")

plt.figure(7)
plt.title("Images of Band 4")
plt.xlabel("x")
plt.ylabel("y")
plt.imshow(img4, cmap='gray')
plt.savefig("image-band4.png")

