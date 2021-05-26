from math import sin, cos
from random import uniform
from numpy.linalg import solve
import matplotlib.pyplot as plt


def function_1(x):
    return x ** 2 - 12 * x + 30


def function_2(x):
    return sin(x) - cos(x)


def function_3(x):
    return 2 * (x ** 3) - 3 * x + 15


def read_x0_xn():
    try:
        x0 = float(input("Input the value for x0:\n"))
        xn = float(input("Input the value for xn:\n"))
        m = int(input("Input the number of desired values (>=2):\n"))
    except:
        raise ValueError("Invalid user input!")

    if x0 >= xn:
        raise ValueError("x0 should be smaller than xn")
    if m < 2:
        raise ValueError("m should be bigger than 0")

    return x0, xn, m


def generate_x_values(epsilon=0.01):
    x0, xn, m = read_x0_xn()
    x_values = [x0]
    current_min = x0 + epsilon
    for _ in range(2, m):
        current_value = round(uniform(current_min, xn - epsilon), 3)
        x_values.append(current_value)
        current_min = current_value + epsilon

    x_values.append(xn)
    return x_values


def generate_y_values(x_values, fun):
    y_values = []
    for x in x_values:
        y_values.append(fun(x))
    return y_values


def horner(poly, x):
    result = poly[0]
    n = len(poly)
    for i in range(1, n):
        result = result * x + poly[i]

    return result


def reverse(lst):
    return [ele for ele in reversed(lst)]


def generate_x_matrix(x_values):
    n = len(x_values)
    x_matrix = []

    for x in x_values:
        x_matrix.append(reverse([x ** i for i in range(0, n)]))

    return x_matrix


def solve_system(x_matrix, y_values):
    return solve(x_matrix, y_values)



def spline_method(x_values, y_values, x, d_a):
    if x < x_values[0] or x > x_values[-1]:
        raise ValueError("Invalid x")

    i0 = 0
    a_values = [d_a]
    a_prev = d_a
    h_i = x_values[i0 + 1] - x_values[i0]
    a_current = -a_prev + 2 * (y_values[i0 + 1] - y_values[0]) / h_i
    a_values.append(a_current)
    a_prev = a_current

    while x > x_values[i0 + 1]:
        i0 += 1
        h_i = x_values[i0 + 1] - x_values[i0]
        a_current = -a_prev + 2 * (y_values[i0 + 1] - y_values[0]) / h_i
        a_values.append(a_current)
        a_prev = a_current

    return (a_values[-1] - a_values[-2]) / (2 * (x_values[i0 + 1] - x_values[i0])) * (x - x_values[i0]) ** 2 + a_values[i0] * (x - x_values[i0]) + y_values[i0]


if __name__ == '__main__':
    functions = [function_1, function_2, function_3]
    # functions = [function_1]
    iter = 1
    for f in functions:
        print("Function %d:" % iter)
        print("Least squares method.")
        x_values = generate_x_values()
        y_values = generate_y_values(x_values, f)
        # print(x_values, y_values)
        print("X_VALUES GENERATED:\n", x_values)
        x_matrix = generate_x_matrix(x_values)
        coefs = solve_system(x_matrix, y_values)
        print(coefs)
        new_x = float(input("Now let's test the result in a new point:\n"))
        print("Actual result for new x vs computed result: ", abs(horner(coefs, new_x) - f(new_x)))
        sum_norms = 0
        for i in range(len(x_values)):
            sum_norms += abs(horner(coefs, x_values[i]) - y_values[i])

        print("The sum of differences for the generated dataset is: ", sum_norms)
        graph_x = [*x_values, new_x]
        graph_x.sort()
        graph_y = [*[f(x) for x in graph_x]]
        plot1 = plt.figure(1)
        plt.plot(graph_x, graph_y)
        plt.title('Actual graph')

        graph_y2 = [*[horner(coefs, x) for x in graph_x]]
        plot2 = plt.figure(2)
        plt.plot(graph_x, graph_y2)
        plt.title('Least squares graph')
        print('-------------------------')
        print("Spline method")
        iter += 1
        d_a = float(input("Derivative value in %f:\n" % x_values[0]))
        spl_result = spline_method(x_values, y_values, new_x, d_a)
        print("Spline result: %f\n" % spl_result)
        print("Difference: %f" % abs(spl_result - f(new_x)))
        graph_y3 = [*[spline_method(x_values, y_values, x, d_a) for x in graph_x]]
        plot3 = plt.figure(3)
        plt.plot(graph_x, graph_y3)
        plt.title('Spline graph')
        plt.show()