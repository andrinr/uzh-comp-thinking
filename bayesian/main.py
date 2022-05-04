from enum import unique
import numpy as np
import matplotlib.pyplot as plt
import math
import random as rnd
from scipy.stats import norm    
from scipy.stats import multivariate_normal
from sklearn.model_selection import train_test_split

nLabels, minSamples, maxSamples, testSamples = 5, 200, 400, 20

for i in range(nLabels):

    n = minSamples + round((maxSamples-minSamples) * rnd.random())
    means = [6*(rnd.random()-0.5), 6*(rnd.random()-0.5)]
    cov = [[rnd.random()-0.5,rnd.random()-0.5], [rnd.random()-0.5,rnd.random()-0.5]]
    sample = np.random.multivariate_normal(means, cov, size=n)

    labels = np.full((n,1), i)
    sample = np.hstack((sample, labels))

    if i == 0:
        samples = sample
    else:
        samples = np.concatenate((samples, sample), axis=0)


X = samples[:,0:2]
y = samples[:,2]


def bayes_class_ind(x_train, y_train, x):
    maxP, maxLabel = 0, -1

    unq, counts = np.unique(y_train, return_counts=True)
    rows, cols = np.shape(x_train)


    for i in range(len(unq)):
        label = round(unq[i])
        p_label = counts[i] / rows

        p_xi = 1.0
        for j in range(cols):

            p_xi *= norm.pdf(
                x[j], 
                loc=np.mean(x_train[y_train == label, j]), 
                scale=np.var(x_train[y_train == label, j])
                )

        p = p_label * p_xi

        if (p > maxP):
            maxP = p
            maxLabel = label

    return maxLabel

def bayes_class(x_train, y_train, x):
    maxP, maxLabel = 0, -1

    unq, counts = np.unique(y_train, return_counts=True)
    rows, cols = np.shape(x_train)

    for i in range(len(unq)):
        label = round(unq[i])
        p_label = counts[i] / rows

        mn = multivariate_normal(
            np.mean(x_train[y_train == label, :], axis=0), 
            np.cov(x_train[y_train == label, :], rowvar=False)
            )

        p_xi = mn.pdf(x)

        p = p_label * p_xi

        if (p > maxP):
            maxP = p
            maxLabel = label

    return maxLabel

X_train, X_test, y_train, y_test = train_test_split( X, y, test_size=0.33, random_state=42)


y_pred_ind = np.zeros(len(X_test))
for i in range(len(X_test)):
    y_pred_ind[i] = bayes_class_ind(X_train, y_train, X_test[i])



fig, ax = plt.subplots()
ax.scatter(X_train[:,0], X_train[:,1], c=y_train)
ax.scatter(X_test[:,0], X_test[:,1], c=y_pred_ind,  marker="x")
ax.set_title("Assuming ind. normal distr.")

print("Percentage of incorrect classifications with ind. distr.: " , np.sum(y_pred_ind != y_test) / len(y_test))

y_pred = np.zeros(len(X_test))
for i in range(len(X_test)):
    y_pred[i] = bayes_class(X_train, y_train, X_test[i])

fig, ax = plt.subplots()
ax.scatter(X_train[:,0], X_train[:,1], c=y_train)
ax.scatter(X_test[:,0], X_test[:,1], c=y_pred,  marker="x")
ax.set_title("Assuming multivariate normal distr.")


print("Percentage of incorrect classifications with multivariate distr.: " , np.sum(y_pred != y_test) / len(y_test))


plt.show()