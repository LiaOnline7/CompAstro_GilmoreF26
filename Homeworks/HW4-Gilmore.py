# One of the strongest time varying signals are occulting binaries,
# when two orbiting stars pass in front of one-another. This website has data from the
# TESS machine that observed hundreds of nearby stars. You can download the data for a light curve
# as a fits file from the site after you choose a star. You can read the file using astropy:

import matplotlib.pyplot as plt
import numpy as np
from astropy.timeseries import LombScargle
from astropy.io import fits

# Note that these files contain errors on the measured fluxes that we will not use in Fourier analysis.
# Choose an epoch with lots of observations and reduce your
# data to just that range. Create the Fourier transform for that range and plot the power spectrum.
# See how few coefficients you can use to capture the behavior of the eclipsing binary looking at
# the inverse transform. You can check a different region of the light curve and redo the analysis to see
# if you get the same results.


#TIC 10393493

TIC_10393493 = fits.open('tic0010393493.fits')[1]
t = TIC_10393493.data['times']
y = TIC_10393493.data['fluxes']
dy = TIC_10393493.data['ferrs']

frequency, power = LombScargle(t, y, dy).autopower()
dominant_frequency = frequency[np.argmax(power)]
print(" ** TIC_10393493 has a symmetric light curve, as such the calculated values have been doubled/halved accordingly **")

import argparse
if __name__ == "__main__":
    print('The LombScargle period is =', round(2./dominant_frequency, 5),'days, or (',round(24*2./dominant_frequency, 3), 'hours)')
    parser = argparse.ArgumentParser(
        prog="Fourier Transform",
        description="Calculates the period, frequency of eclipsing binary TIC 10393493 using TESS data. "
                    "Plots the lightcurve.")

    parser.add_argument('-plot',
                        action='store_true',
                        help = "plots all of the availible TESS data for TIC 10393493")

    parser.add_argument('-plot_fit',
                        action='store_true',
                        help = 'plots the phase folded data and the best fit for the light curve')

    parser.add_argument('-range',
                        nargs=2,
                        default=[t.min(), t.max()],
                        type=float,
                        help = 'use with any of the plotting args IF you want to specify a range')

    parser.add_argument('--dom_freq',
                        action='store_true',
                        help = 'prints the dominant frequency of the eclipsing binary')

    parser.add_argument('-phase_fold',
                        nargs = '?',
                        const = 0.36046,
                        default = 0.36046,
                        type = float,
                        help = 'plots the phase folded data for some "initial guess" '
                               '(taken from TESS website, f = 0.36046, as such is the default)'
                        )

    parser.add_argument('-plot_power_spect',
                        action= 'store_true',
                        help = 'plots the power spectrum')

    args = parser.parse_args()

    if args.plot:
        min, max = args.range
        ind = (t >= min) & (t < max)
        plt.scatter(t[ind], y[ind], s=5, marker="o")
        plt.xlabel('Truncated Barycentric Julian Date')
        plt.ylabel('Normalized PDC flux')
        plt.show()

    elif args.plot_fit:
        min, max = args.range
        ind = (t > min) & (t <= max)
        t_ind, y_ind = (t[ind], y[ind])

        period = 2.0 / dominant_frequency

        t_fit = np.linspace(0, period, 100)
        ls = LombScargle(t_ind, y_ind)
        y_fit = ls.model(t_fit, dominant_frequency)
        phase_fold = args.phase_fold
        phases = np.remainder(t_ind, period) / period

        plt.figure(figsize=(12, 8))

        plt.scatter(phases, y_ind, s=15, marker="o", label='Phase-Folded Observational Data')
        plt.plot(t_fit / period, y_fit, color='r', linewidth=2, alpha=0.5, label='Lomb-Scargle Model')

        plt.gca().invert_yaxis()
        plt.xlabel('Phase')
        plt.ylabel('Normalized PDC flux')
        plt.title(f'TIC_10393493 Light Curve (P = {period:.5f} days)')
        plt.legend(loc='lower right', fontsize=14)
        plt.show()

    elif args.plot_power_spect:
        plt.plot(frequency/2, power)
        plt.xlabel('Frequency')
        plt.ylabel('Power')
        plt.xlim(0, 10)
        plt.show()

    elif args.dom_freq:
        print('Dominant Frequency = ', frequency[np.argmax(power)]/2)

    elif args.phase_fold is not None:
        plt.gca().invert_yaxis()
        phases = np.remainder(t, args.phase_fold) / args.phase_fold
        plt.scatter(phases, y, s=5, marker="o")
        plt.xlabel('Phase')
        plt.ylabel('Normalized PDC flux')
        plt.show()




