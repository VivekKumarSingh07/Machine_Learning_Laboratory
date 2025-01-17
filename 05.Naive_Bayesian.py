"""
5. Write a program to implement the naïve Bayesian classifier for a sample training
data set stored as a .CSV file. Compute the accuracy of the classifier, considering few
test data sets.
"""

import csv
import math


def mean(numbers):
    return sum(numbers) / float(len(numbers))


def stdev(numbers):
    avg = mean(numbers)
    variance = sum([pow(x - avg, 2) for x in numbers]) / float(len(numbers) - 1)
    return math.sqrt(variance)


def summarize(dataset):
    summaries = [(mean(attribute), stdev(attribute))
                 for attribute in zip(*dataset)]
    del summaries[-1]
    return summaries


def calcProb(summary, item):
    prob = 1
    for i in range(len(summary)):
        x = item[i]
        mean, stdev = summary[i]
        exponent = math.exp(-math.pow(x - mean, 2) / (2 * math.pow(stdev, 2)))
        final = exponent / (math.sqrt(2 * math.pi) * stdev)
        prob *= final
    return prob


with open('ds3.csv') as csvFile:
    data = [line for line in csv.reader(csvFile)]
for i in range(len(data)):
    data[i] = [float(x) for x in data[i]]
split = int(0.90 * len(data))

train = data[:split]
test = data[split:]
print("{} input rows is split into {} training and {} testing datasets".format(
    len(data), len(train), len(test)))
print("\nThe values assumed for the concept learning attributes are\n")
print(
    "OUTLOOK=> Sunny=1 Overcast=2 Rain=3\nTEMPERATURE=> Hot=1 Mild=2 Cool=3\nHUMIDITY=> High=1 Normal=2\nWIND=> Weak=1 Strong=2")
print("TARGET CONCEPT:PLAY TENNIS=> Yes=10 No=5")
print("\nThe Training set are:")
for x in train:
    print(x)
print("\nThe Test data set are:")
for x in test:
    print(x)
yes = []
no = []
for i in range(len(train)):
    if data[i][-1] == 5.0:
        no.append(data[i])
    else:
        yes.append(data[i])
yes = summarize(yes)
no = summarize(no)
predictions = []
for item in test:
    yesProb = calcProb(yes, item)
    noProb = calcProb(no, item)
    predictions.append(10.0 if (yesProb > noProb) else 5.0)
correct = 0
for i in range(len(test)):
    if (test[i][-1] == predictions[i]):
        correct += 1
print("\nActual values are:")
for i in range(len(test)):
    print(test[i][-1], end=" ")
print("\nPredicted values are:")
for i in range(len(predictions)):
    print(predictions[i], end=" ")
print("\nAccuracy is {}%".format(float(correct / len(test) * 100)))

"""
Output:

16 input rows is split into 14 training and 2 testing datasets

The values assumed for the concept learning attributes are

OUTLOOK=> Sunny=1 Overcast=2 Rain=3
TEMPERATURE=> Hot=1 Mild=2 Cool=3
HUMIDITY=> High=1 Normal=2
WIND=> Weak=1 Strong=2
TARGET CONCEPT:PLAY TENNIS=> Yes=10 No=5

The Training set are:
[1.0, 1.0, 1.0, 1.0, 5.0]
[1.0, 1.0, 1.0, 2.0, 5.0]
[2.0, 1.0, 1.0, 2.0, 10.0]
[3.0, 2.0, 1.0, 1.0, 10.0]
[3.0, 3.0, 2.0, 1.0, 10.0]
[3.0, 3.0, 2.0, 2.0, 5.0]
[2.0, 3.0, 2.0, 2.0, 10.0]
[1.0, 2.0, 1.0, 1.0, 5.0]
[1.0, 3.0, 2.0, 1.0, 10.0]
[3.0, 2.0, 2.0, 2.0, 10.0]
[1.0, 2.0, 2.0, 2.0, 10.0]
[2.0, 2.0, 1.0, 2.0, 10.0]
[2.0, 1.0, 2.0, 1.0, 10.0]
[3.0, 2.0, 1.0, 2.0, 5.0]

The Test data set are:
[1.0, 2.0, 1.0, 2.0, 10.0]
[1.0, 2.0, 1.0, 2.0, 5.0]

Actual values are:
10.0 5.0 
Predicted values are:
5.0 5.0 
Accuracy is 50.0%
"""
