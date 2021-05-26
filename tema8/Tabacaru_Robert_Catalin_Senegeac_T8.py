from random import uniform
from math import sin


def get_x0(mini=0, maxi=10):
    x0 = input("Input x0 or type \"rand\":\n")
    if x0 == "rand":
        x0 = uniform(mini, maxi)
    else:
        x0 = float(x0)

    return x0


def get_h():
    exp = int(input("Please choose exponent for h (-5 or -6):\n"))

    while exp not in [-5, -6]:
        exp = int(input("Please choose exponent for h (-5 or -6):\n"))

    return 10 ** exp


def f1(x):
    return (1 / 3) * x ** 3 - 2 * x ** 2 + 2 * x + 3


def f2(x):
    return x ** 2 + sin(x)


def f3(x):
    return x ** 4 - 6 * x ** 3 + 13 * x ** 2 - 12 * x + 4


def approximate_derivative_1(func, h):
    def g(x):
        return (3 * func(x) - 4 * func(x - h) + func(x - 2 * h)) / (2 * h)

    return g


def approximate_derivative_2(func, h):
    def g(x):
        return (-func(x + 2 * h) + 8 * func(x + h) - 8 * func(x - h) + func(x - 2 * h)) / (12 * h)

    return g


def approximate_second_derivative(func, x, h):
    return (-func(x + 2 * h) + 16 * func(x + h) - 30 * func(x) + 16 * func(x - h) - func(x - 2 * h)) / (12 * h ** 2)


def get_z_deltax(x_curr, g):
    z = x_curr + (g(x_curr) ** 2 / (g(x_curr + g(x_curr)) - g(x_curr)))
    delta_x = (g(x_curr) * (g(z) - g(x_curr))) / (g(x_curr + g(x_curr)) - g(x_curr))

    return z, delta_x


def dehgan_hajarian(g, eps=10 ** (-10), k_max=10_000):
    x = get_x0()
    k = 0

    if abs(g(x + g(x)) - g(x)) <= eps:
        return x
    z, delta_x = get_z_deltax(x, g)
    x -= delta_x
    k += 1

    while eps <= abs(delta_x) <= 10 ** 8 and k <= k_max:
        if abs(g(x + g(x)) - g(x)) <= eps:
            return x
        z, delta_x = get_z_deltax(x, g)
        x -= delta_x
        k += 1

    if abs(delta_x) < eps:
        return x
    else:
        return "divergence"


if __name__ == '__main__':
    test_functions = [f1, f2, f3]
    deriv_aproximators = [approximate_derivative_1, approximate_derivative_2]
    h = get_h()
    for i, f in enumerate(test_functions):
        print("Testing function ", i + 1)
        for j, aprox in enumerate(deriv_aproximators):
            print("Aproximation method: ", j + 1)
            g = aprox(f, h)
            result = dehgan_hajarian(g)
            print("X* = ", result)