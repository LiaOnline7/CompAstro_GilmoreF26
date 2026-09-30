#Assuming circular orbits, and assuming that the Earth
# is much more massive than either the Moon or the satellite,
# show that the distance r from the center of the Earth to
# the L1 point satisfies

# GM/r^2 - GM/ (R-r)^2 = omega^2r   <-- fifth-order polynomial equation in r

#where M and m are the Earth and Moon masses,
# G is Newton’s gravitational constant, and ω is the
# angular velocity of both the Moon and the satellite.

# Write a program that uses either Newton’s method or
# the secant method to solve for the distance r from the Earth
# to the L1 point. Compute a solution accurate to at least
# four significant figures.


from astropy import constants as const
import astropy.units as u
import numpy as np
import matplotlib.pyplot as plt

G = const.G.value
Me = const.M_earth.value
Mm = 7.348e22 #*u.kg
R = 3.844e8 #* u.m
omega = 2.662e-6 #*(1/ u.s)

def P(r):
    return (G*Me)/(r**2) - (G*Mm)/((R-r)**2) - (omega**2)*r

def newtons_method(r):
    tolerance = 1e-4
    delta_x = 5
    while np.abs(delta_x) > tolerance:
        fr = P(r)
        dfdr = -2*(G*Me)/(r**3) - 2*(G*Mm)/((R-r)**3) - (omega**2)

        delta_x = fr / dfdr
        r = r - delta_x

    return round(r, 5)

#print("Roots = ", newtons_method(R/2)/const.au.value)

import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="L1 Lagrange Point",
        description="")

    parser.add_argument("-r",
                                  default=R/2,
                                  type=float,
                                  help="change the initial guess for the distance r to L1, default is R/2")

    parser.add_argument("-units",
                        type = str,
                        choices = ['au', 'percent', 'km', 'm'],
                        default = 'R',
                        help="changes the units of the result, default is normalized to Earth-Moon distance")

    parser.add_argument("-round",
                        nargs = "?",
                        const = 4,
                        type = int,
                        help = 'rounds the output to a specified place')

    parser.add_argument("-format",
                        nargs = "?",
                        const= 2,
                        type = int,
                        help="prints in scientific notation. FOR DEFAULT UNITS, prints as a percent of Earth-Moon distance")

    parser.add_argument("-graph",
                        action= 'store_true',
                        help="prints a graph of the Earth-Moon system and "
                             "the L1 Lagrange point labeled in the specified distance units. Graph axes stay in default normalized r/R units.")

    args = parser.parse_args()

    if args.units == 'au':
        if args.round:
            if args.format:
                R_text = format(round(R/const.au.value, args.round), f".{args.format}e")
                Roots = format(round(newtons_method(args.r)/const.au.value, args.round), f".{args.format}e")
                print("Roots = ", Roots, 'au')
            else:
                R_text = round(R/const.au.value, args.round)
                Roots = round(newtons_method(args.r)/const.au.value, args.round)
                print("Roots = ", Roots, 'au')
        else:
            if args.format:
                R_text =  format(R/const.au.value, f".{args.format}e")
                Roots = format(newtons_method(args.r)/const.au.value, f".{args.format}e")
                print("Roots = ", Roots, 'au')
            else:
                R_text = R / const.au.value
                Roots = newtons_method(args.r) / const.au.value
                print("Roots = ", Roots, 'au')

    elif args.units == 'km':
        if args.round:
            if args.format:
                R_text = format(round(R/1e3, args.round), f".{args.format}e")
                Roots = format(round(newtons_method(args.r)/1e3, args.round), f".{args.format}e")
                print("Roots = ", Roots, 'kilometers')
            else:
                R_text = round(R/1e3, args.round)
                Roots = round(newtons_method(args.r)/1e3, args.round)
                print("Roots = ", Roots, 'kilometers')
        else:
            if args.format:
                R_text = format(R/1e3, f".{args.format}e")
                Roots = format(newtons_method(args.r)/1e3, f".{args.format}e")
                print("Roots = ", Roots, 'kilometers')
            else:
                R_text = R / 1e3
                Roots = newtons_method(args.r) / 1e3
                print("Roots = ",Roots, 'kilometers')
    elif args.units == 'm':
        if args.round:
            if args.format:
                R_text = format(round(R, args.round), f".{args.format}e")
                Roots = format(round(newtons_method(args.r), args.round), f".{args.format}e")
                print("Roots = ", Roots, 'meters')
            else:
                R_text = round(R, args.round)
                Roots = round(newtons_method(args.r), args.round)
                print("Roots = ",Roots, 'meters')
        else:
            if args.format:
                R_text = format(R, f".{args.format}e")
                Roots = format(newtons_method(args.r), f".{args.format}e")
                print("Roots = ", Roots, 'meters')
            else:
                R_text = R
                Roots = newtons_method(args.r)
                print("Roots = ", Roots, 'meters')
    else:
        if args.round:
            if args.format:
                args.units = '%'
                R_text = 100
                Roots = round(newtons_method(args.r)/R, args.round)*100
                print("Roots = ", round(newtons_method(args.r)/R, args.round), '% of Earth-moon distance')
            else:
                R_text = 1
                Roots = round(newtons_method(args.r)/R, args.round)
                print("Roots = ", round(newtons_method(args.r)/R, args.round), 'r/R')
        else:
            if args.format:
                args.units = '%'
                R_text = 100
                Roots = (newtons_method(args.r)/R)*100
                print("Roots = ", newtons_method(args.r)/R, '% of Earth-moon distance')
            else:
                R_text = 1
                Roots = newtons_method(args.r)/R
                print("Roots = ", newtons_method(args.r)/R, 'r/R')

    if args.graph:
        fig, ax = plt.subplots(figsize=(5, 5))
        ax.set_xlabel(r"$\frac{x}{R}$")
        ax.set_ylabel(r"$\frac{y}{R}$")

        ax.axhline(0, c='k')
        ax.plot(newtons_method(args.r) / R, 0, "rv", label="$L_1$")

        pi_2 = Mm / (Me + Mm)

        orbit = plt.Circle((0, 0), 1, color='b', fill=False, alpha=0.65)

        ax.add_patch(orbit)

        ax.text(0.12, -0.165, f"{Roots} {args.units}", color = 'r')
        ax.annotate(" ", xytext=(0, -0.1), xy=(0.8482, -0.1),
                    arrowprops=dict(color = 'r', arrowstyle="<->", lw = 2))

        ax.text(0.12, 0.125, f"{R_text} {args.units}", color='b')
        ax.annotate(" ", xytext=(0, 0.1), xy=(1, 0.1),
                    arrowprops=dict(arrowstyle="<->", color = 'b'))

        ax.plot(-pi_2, 0, "bo", markersize=15, label="$Earth$")
        ax.plot(1 - pi_2, 0, color = 'grey', markersize=8, marker = "o", label="$Moon$")

        ax.legend()
        plt.show()