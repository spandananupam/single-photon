'''
Plotting code

Author: Spandan Anupam
Date: 29 Jan 2021
'''

from matplotlib import pyplot as plt
import matplotlib
import numpy as np
from scipy.optimize import curve_fit as fit
from scipy.special import factorial
from scipy.stats import poisson, chisquare
from math import log10, floor
matplotlib.rcParams['text.usetex'] = True


def curve(x, a, b, c):
    return a * np.exp((-a) * x + b) + c


def gaussian(x, a, b, c, d):
    return a * np.exp(-((x-b)**2/c)) + d


def poission(x, a):
    return poisson.pmf(x, a)


def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)


def diff(intensity):
    data = np.genfromtxt(f"data/diff_{intensity}.csv", delimiter=",")
    data = np.delete(data, np.argwhere(data <= 850))
    data = np.delete(data, np.argwhere(data > 9500))
    histdata, histedges = np.histogram(data, bins=70)
    x, y = histedges[:-1], histdata

    popt, pconv = fit(curve, x, y, p0=[0.001, 10, 1])
    perr = np.sqrt(np.diag(pconv))
    x_fit = np.linspace(x.min(), x.max(), num=100)
    y_fit = curve(x_fit, *popt)
    a, b, c = np.round_(popt, 3)
    da, db, dc = np.round_(perr, 4)

    plt.scatter(
        x,
        y,
        label="Experimental data",
        marker='o',
        c="gray"
    )
    plt.plot(
        x_fit,
        y_fit,
        label=r'Fit: ($%s \pm %s) \times e^{(-((%s) x + (%s \pm %s))} + (%s \pm %s)$' % (a, da, a, b, db, c, dc),
        linestyle='--',
        c="black"
    )
    plt.xlabel(r"Time between detection events ($\mu$s) at %s intensity" % (intensity))
    plt.ylabel("Number of occurences")
    plt.grid(True)
    plt.legend()
    plt.savefig(f'plots/plotdiff{intensity}.pgf')
    plt.show()


def num(pulse, intensity):
    data = np.genfromtxt(f"data/num_{intensity}_{pulse}.csv", delimiter=",")
    histdata, histedges = np.histogram(data, bins=45)
    x, y = histedges[:-1], histdata
    # # for low 10
    # p0 = [10, 15, 30, 10]
    # x = np.delete(x, np.argwhere(y <= 1))
    # y = np.delete(y, np.argwhere(y <= 1))
    p0 = [10, 1700, 30, 10]

    popt, pconv = fit(gaussian, x, y, p0=p0)
    x_fit = np.linspace(x.min(), x.max(), num=30)
    y_fit = gaussian(x_fit, *popt)
    y_opt = gaussian(x, *popt)
    chi, pval = chisquare(f_obs=y, f_exp=y_opt)
    fit_tuple = np.round_(popt, 2)

    label = r'Fit: $%s \times e^{-{(x-%s)}^2/%s} + (%s)$' % tuple(fit_tuple)

    plt.errorbar(
        x,
        y,
        yerr=np.sqrt(y),
        label="Experimental data",
        marker='o',
        fmt='o',
        ecolor='#d3d3d3',
        capsize=3,
        c="gray")
    plt.plot(
        x_fit,
        y_fit,
        label=label,
        linestyle='--',
        c="black"
    )
    plt.title(r"$\chi^2$ = %s and p-val = %s" % (round_sig(chi), round_sig(pval)))
    plt.xlabel(f"Counts per {pulse}ms at {intensity} intensity")
    plt.ylabel("Number of occurences")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"plots/plot{intensity}{pulse}.pgf")
    plt.show()


def pulse():
    data2 = np.genfromtxt("data/200.csv", delimiter=",")
    data5 = np.genfromtxt("data/500.csv", delimiter=",")
    data10 = np.genfromtxt("data/1000.csv", delimiter=",")
    fig, ax = plt.subplots(nrows=3, sharex=True)

    ax[0].plot(data2[:, 1], label=r'200k$\Omega$', color='black', linestyle='dotted')
    ax[0].get_yaxis().set_visible(False)
    ax[0].spines['bottom'].set_visible(False)
    ax[1].spines['top'].set_visible(False)
    ax[0].legend()
    ax[1].plot(data5[:, 1], label=r'500k$\Omega$', color='black', linestyle='dashed')
    ax[1].get_yaxis().set_visible(False)
    ax[1].spines['bottom'].set_visible(False)
    ax[2].spines['top'].set_visible(False)
    ax[1].legend()
    ax[2].plot(data10[:, 1], label=r'1M$\Omega$', color='black', linestyle='dashdot')
    ax[2].get_yaxis().set_visible(False)
    ax[2].legend()
    plt.xlim([-10, 500])
    ax[0].get_xaxis().set_visible(False)
    ax[1].get_xaxis().set_visible(False)
    ax[2].get_xaxis().set_visible(False)
    plt.subplots_adjust(hspace=.0)
    plt.grid(True)
    plt.savefig('plots/comp.pgf')
    plt.show()


# diff('lown')
num(100, "high")
# pulse()
