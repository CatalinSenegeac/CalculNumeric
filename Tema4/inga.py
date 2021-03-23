import numpy as np
import matplotlib.pyplot as plt


class MatriciRare:

    def readWhile(self, f):
        x = []
        while True:
            line = f.readline()
            if not line or line == "\n":
                break
            x.append(float(line))
        return x

    def readAndParse(self, test_data):

        path_a = "inputs/a" + str(test_data) + ".txt"
        path_f = "inputs/f" + str(test_data) + ".txt"
        f_a = open(path_a, 'r');
        f_f = open(path_f, 'r')

        self.dim = int(f_a.readline())
        self.p = int(f_a.readline())
        self.eps = 10 ** (-self.p)
        self.q = int(f_a.readline())
        f_a.readline()
        self.a = np.array(self.readWhile(f_a))
        self.b = np.array(self.readWhile(f_a))
        self.c = np.array(self.readWhile(f_a))
        print(len(self.a), len(self.b), len(self.c))

        self.dim_f = int(f_f.readline())
        f_f.readline()
        self.f = self.readWhile(f_f)
        print(len(self.f))

    def check_zeros(self):
        if np.all(abs(self.a) > self.eps):
            return True
        return False

    def generate_gs_vector(self, xp):
        for i in range(self.dim):
            tmp_sum1 = tmp_sum2 = 0
            if i != 0:
                tmp_sum1 = self.b[i - 1] * xp[i - 1]
            if i < self.dim - 2:
                tmp_sum2 = self.c[i] * xp[i + 1]
            if (i < len(self.f)):
                xp[i] = (self.f[i] - tmp_sum1 - tmp_sum2) / self.a[i]
        return xp

    def generate_gs_vector_bonus(self, xp):
        for i in range(self.dim):
            tmp_sum1 = tmp_sum2 = 0
            if i >= q:
                tmp_sum1 = self.b[i - 1] * xp[i - q]
            if i < self.dim - p:
                tmp_sum2 = self.c[i] * xp[i + p]
            if (i < len(self.f)):
                xp[i] = (self.f[i] - tmp_sum1 - tmp_sum2) / self.a[i]
        return xp

    def solve_gauss_seidel(self):
        xc = xp = np.zeros_like(self.a)
        delta_x = 0
        k_max = 10000
        k = 1
        xc = self.generate_gs_vector(xp)
        delta_x = np.linalg.norm(xc - xp)
        while (delta_x >= self.eps and k < k_max and delta_x < 10 ** 8):
            xp = xc
            xc = self.generate_gs_vector_bonus(xp)
            delta_x = np.linalg.norm(xc - xp)
            print(delta_x)
            k += 1
        if delta_x < self.eps:
            return xc
        else:
            return "divergenta"


service = MatriciRare()
data = []
for i in range(1, 6):
    service.readAndParse(i)
    print("for zeros", service.check_zeros())
    print(service.solve_gauss_seidel())
    # data.append(service.solve_gauss_seidel()) # plotting by columns
    plt.plot(service.solve_gauss_seidel())
    plt.show()