import numpy as np
from input import *
import model
from priors import Priors2

pri=Priors2()


class Priors:

    def __init__(self, ndim, nparams):

        self.ndim = ndim
        self.nparams = nparams

    def prior(self, cube, ndim, n_params):

        for param in parameters:
            i = parameters.index(param)

            if param == 'log_xhcn':             # implementing limit on XH2O + XHCN + XNH3 =< 1
                h2o_index = parameters.index('log_xh2o')
                h2o_abundance = 10**cube[h2o_index]
                new_lim = np.log10(1-h2o_abundance)
                diff = priors[param][0] + new_lim
                cube[i] = cube[i]*diff + priors[param][1]
            elif param == 'log_xnh3':
                if 'log_xhcn' in parameters:
                    h2o_index = parameters.index('log_xh2o')
                    h2o_abundance = 10**cube[h2o_index]
                    hcn_index = parameters.index('log_xhcn')
                    hcn_abundance = 10**cube[hcn_index]
                    new_lim = np.log10(1 - h2o_abundance - hcn_abundance)
                    diff = priors[param][0] + new_lim
                    cube[i] = cube[i]*diff + priors[param][1]
                else:
                    h2o_index = parameters.index('log_xh2o')
                    h2o_abundance = 10**cube[h2o_index]
                    new_lim = np.log10(1 - h2o_abundance)
                    diff = priors[param][0] + new_lim
                    cube[i] = cube[i]*diff + priors[param][1]
            elif param == 'G':    # set gaussian priors for planetary gravity 
                try:
                    cube[i] = pri.GaussianPrior(cube[i], g, g_uncertainty)
                except:
                    cube[i] = pri.GaussianPrior(cube[i], g, (g_uperr + g_loerr)/2)
            elif param == 'Rstar':    # set gaussian priors for stellar radius
                try:
                    cube[i] = pri.GaussianPrior(cube[i], rstar, rstar_uncertainty)
                except:
                    cube[i] = pri.GaussianPrior(cube[i], rstar, (rstar_uperr + rstar_loerr)/2)
            else:
                cube[i] = cube[i]*priors[param][0] + priors[param][1]  # set uniform priors based on values in input



    def loglike(self, cube, ndim, n_params, loglike_args):
        for param in parameters:
            i = parameters.index(param)
            parameter_dict[param] = cube[i]     # set priors

        x = model.Model(loglike_args[0], loglike_args[1], loglike_args[2], parameter_dict, loglike_args[3])
        ymodel = x.binned_model()


        # ymodel = self.model.binned_model(loglike_args[0], loglike_args[1], loglike_args[2], parameter_dict, loglike_args[3])   # evaluate binned model
        loglikelihood = (-0.5 * ((ymodel - loglike_args[4]) / loglike_args[5])**2 - np.log(abs(loglike_args[5])*np.sqrt(2*np.pi))).sum()     # evaluate loglikelihood

        return loglikelihood
