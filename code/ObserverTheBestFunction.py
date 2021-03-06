import code.estimators_selectors.CalculatorModelValues as CalculatorModelValues
from numpy import  sum, isnan, inf,  nan, transpose, errstate
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import axes3d, Axes3D
from pylab import figure, plot, ion, linspace, arange, sin, pi
import time

def observer_the_best_function(population, data_to_fit, iter = 0):
    """
    Draw on the same plot initial and predicted values
    Inputs:
     population     - set of the best approximating functions for 'data_to_fit'
     data_to_fit    - initial values to be approximated
    Author: Kulunchakov Andrei, MIPT
    """
    if (data_to_fit.shape[1] == 2):
        draw_2d_plot_updating(population, data_to_fit, iter)

    if (data_to_fit.shape[1] == 3):
        draw_3d_plot(population, data_to_fit)


def draw_2d_plot(population, data_to_fit, iter = 0):
    independent_var = data_to_fit[:,1:]
    independent_var = transpose(independent_var)
    dependent_var = data_to_fit[:,0]

    model = population[0]

    dependent_var_estimation = CalculatorModelValues.calculate_model_values(model,independent_var)
    dependent_var            = dependent_var.reshape(1,-1)
    dependent_var_estimation = dependent_var_estimation.reshape(1,-1)

    plt.plot(independent_var[0], dependent_var[0], 'r--', independent_var[0], dependent_var_estimation[0], 'b')
    plt.title(model.handle)
    plt.show()


def draw_2d_plot_updating(population, data_to_fit, iter = 0):
    import warnings

    def fxn():
        warnings.warn("deprecated", DeprecationWarning)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        fxn()
        independent_var = data_to_fit[:,1:]
        independent_var = transpose(independent_var)
        dependent_var = data_to_fit[:,0]

        model = population[0]

        dependent_var_estimation = CalculatorModelValues.calculate_model_values(model,independent_var)
        dependent_var            = dependent_var.reshape(1,-1)
        dependent_var_estimation = dependent_var_estimation.reshape(1,-1)

        plt.clf()
        plt.plot(independent_var[0], dependent_var[0], 'r--', independent_var[0], dependent_var_estimation[0], 'b')
        plt.title(model.handle)
        plt.draw()
        plt.pause(0.01)

def draw_3d_plot(population, data_to_fit):

    independent_var = data_to_fit[:,1:]
    dependent_var = data_to_fit[:,0]

    dependent_var            = dependent_var.reshape(1,-1)

    fig = plt.figure(2)

    ax = Axes3D(fig)
    X0 = independent_var[:,0]
    Y0 = independent_var[:,-1]
    limitsX = [min(X0), max(X0), 20]
    limitsY = [min(Y0), max(Y0), 20]


    X = np.linspace(*limitsX)
    Y = np.linspace(*limitsY)
    X, Y = np.meshgrid(X, Y)
    Z = CalculatorModelValues.calculate_model_values(population[0],np.vstack([X.ravel(), Y.ravel()]))
    Z = Z.reshape(limitsX[2], limitsY[2])



    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=cm.coolwarm,
                           linewidth=0, antialiased=False)
    ax.set_zlim(0, np.max(list(Z)))

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)
    ax.scatter(X0, Y0, dependent_var)

    ax.set_xlabel('x label')
    ax.set_ylabel('y label')
    ax.set_zlabel('z label')
    plt.show()

