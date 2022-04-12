import matplotlib.pyplot as plt
import numpy as np


def square_func(a, b, c):
    def f(x):
        return a * x ** 2 + b * x + c

    return f


f = np.poly1d([-1, 10, 5])
X = np.arange(-10, 10, 0.1)
Y = f(X)

plt.plot(X, Y)
plt.savefig('plt.png')
