#Consider the integral:
#E(x) = int(0,x)e^(-t^2)dt

#a) Write a program to calculate E(x)
# for values of x from 0 to 3 in steps of 0.1.
# Choose for yourself what method you will use for
# performing the integral and a suitable number of slices.

#b) When you are convinced your program is working,
# extend it further to make a graph of E(x) as a function of x.

#Note: that there is no known way to perform this particular
# integral analytically, so numerical approaches are the only way forward.

import numpy as np
import matplotlib.pyplot as plt

def f(t):
    return np.exp(-t**2)
def simp_rule(a,b, N):
    sum_even = 0
    sum_odd = 0
    n = int(N/2)
    delta_x = (b-a)/N
    for k in range (1, n):
        point_e = a + (2*k-1)*delta_x
        sum_even = sum_even + f(point_e)

    for k in range (1, (n-1)):
        point_o = a + (2*k)*delta_x
        sum_odd = sum_odd +f(point_o)

    return (delta_x/3) * (f(a) + f(b) + 4*(sum_even) + 2*(sum_odd))

#print(simp_rule(0,3,300))


def error_func(a,b,N):
    return (1/90)* ((b-a)/N)**4 *np.abs((12*a**2) - (12*b**2))

#print(error_func(0,3, 20))

#x_range = np.arange(-3,3,0.1)

#plt.plot(x_range, simp_rule(0, x_range, 300), label= r'$E(x) = \int_{0}^{x} e^{-t^{2}} dt$', color='blue')
#plt.plot(x_range, f(x_range), label = r'$f(x) = e^{-t^{2}}$')
#plt.xlim(-2, 2)
#plt.ylim(-1.5, 1.5)

plt.xlabel('')
plt.ylabel('')
plt.title('')
plt.grid(True)

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="Integrate",
        description="Calculates the numerical integral E(x) = int(0,x)e^(-t^2)dt using Simpson's method. "
                    "Default calculation of this integral sets x from 0 to 3 in steps of 0.1. "
                    "Can also plot the graph of E(x) and its integral.")

    parser.add_argument("-a",
                        default = 0,
                        type=float,
                        help="change lower limit of the integral, default is 0")

    parser.add_argument('-b',
                        default=3,
                        type=float,
                        help="change upper limit of the integral, default is 3")

    parser.add_argument("-N",
                        default=300,
                        type=int,
                        help="change number of steps, default is 300")

    parser.add_argument("-error",
                        nargs= '?',
                        const = 20,
                        type = int,
                        help="estimate of the error with x steps, default is 20")

    parser.add_argument("-round",
                        type = int,
                        help = 'rounds the output to a specified place')

    parser.add_argument("-graph",
                        action= 'store_true',
                        help="prints a graph of E(x) and its integrand "
                             "with the area underneath the curve specified by the integral shaded")

    args = parser.parse_args()

    #print((simp_rule(args.a, args.b, args.N)))

    if args.graph:
        x_range = np.arange(-args.b, args.b,0.1)

        plt.plot(x_range, simp_rule(0, x_range, 300),
                 label= r'$E(x) = \int_{0}^{x} e^{-t^{2}} dt$', color='blue')
        plt.plot(x_range, f(x_range),
                 label = r'$f(x) = e^{-t^{2}}$', color = 'grey', alpha = 0.5)
        plt.xlim(-2, 2)
        plt.ylim(-1.5, 1.5)

        section = np.arange(args.a, args.b, 1 / 20.)
        plt.fill_between(section, f(section), hatch = '|||', edgecolor = 'r', alpha = 0.5,
                         facecolor = 'none',
                         label = r'$E(x) = \int_{a}^{b}' r'e^{-t^{2}} dt ~ $')

        plt.legend()
        plt.show()

    if args.error:
        if args.round:
            print(r'$E(x) = \int_' fr'{args.a}' r'^' fr'{args.b}' r'e^{-t^{2}} dt ~ $',
                  f"{round((simp_rule(args.a, args.b, args.N)), args.round)}",
                  'error =', f"{round(error_func(args.a, args.b, args.error), args.round)}")
        else:
            print(r'$E(x) = \int_' fr'{args.a}' r'^' fr'{args.b}' r'e^{-t^{2}} dt ~ $',
                  simp_rule(args.a, args.b, args.N),
                  'error =', error_func(args.a, args.b, args.error))

    else:
        if args.round:
            print(r'$E(x) = \int_' fr'{args.a}' r'^' fr'{args.b}' r'e^{-t^{2}} dt ~ $', f"{ round( simp_rule(args.a, args.b, args.N), args.round) }")
        else:
            print(r'$E(x) = \int_' fr'{args.a}' r'^' fr'{args.b}' r'e^{-t^{2}} dt ~ $',
                  simp_rule(args.a, args.b,args.N))