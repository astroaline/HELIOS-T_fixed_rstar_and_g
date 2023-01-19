import numpy as np
import os


## Constants ##
kboltz = 1.38064852e-16    # Boltzmann's constant
amu = 1.660539040e-24      # atomic mass unit
gamma = 0.57721
rjup = 7.1492e9            # equatorial radius of Jupiter
rsun = 6.9566e10           # solar radius
rearth = 6.378e8            # earth radius
pressure_probed = 1e-2      # probed pressure in bars
# pressure_cia = 1e-2         # pressure for cia in bars
# m = 2.4*amu                 # assummed hydrogen-dominated atmosphere
m_water = 18.0*amu          # mean molecular mass of any molecules you want to consider
m_cyanide = 27.0*amu
m_ammonia = 17.0*amu
m_methane = 16.0*amu
m_carbon_monoxide = 28.0*amu
solar_h2 = 0.5
solar_he = 0.085114


## Planet Data ##

planet_name = 'HAT-P-1b'

g = 746
g_uncertainty = 17 
rstar = 1.115
rstar_uncertainty = 0.050
r0 = 1.213   # Rp = [1.166,1.284]
r0_uncertainty = 0.12   # R0 = [1.093,1.333]

wavelength_bins = np.array([1.1107999999999998,1.1416,1.1709,1.1987999999999999,1.2257,1.2522,1.2791,1.3058,1.3321,1.3586,1.3860000000000001,1.414,1.4425,1.4718999999999998,1.5027,1.5345,1.5682,1.6042,1.6431999999999998])
transit_depth = np.array([1.3785912796371758,1.3634339735782401,1.3714679828179623,1.373148386405245,1.3699109038399175,1.3574237907953184,1.3609673540965737,1.374844682524226,1.3762843049082327,1.3663591695378419,1.3947965892180652,1.3994997200411854,1.3837274855970783,1.3925272785860114,1.381690250960784,1.3767625604254765,1.363290868688746,1.352030600681179])
transit_depth_error = np.array([0.008896843844690984,0.010193032357077029,0.007945293065908042,0.00918047643223376,0.008468270965652083,0.008987853023422655,0.0074570312178861885,0.008268250942310271,0.0071528810915148155,0.009458862576029773,0.007905102869558187,0.008662763572214691,0.00860645235315381,0.007806406027125861,0.007466646174739144,0.009222555475364953,0.010198236533669318,0.008009469882268788])


## Retrieval info ##
model_name = 'cloudfree_fixed_rstar_and_g_rayleigh_cia'
approach_name = 'isobaric'

molecules = ["01"]
parameters = ["T", "log_xh2o", "R0"]
res = 5         # resolution used for opacities
live = 1000     # live points used in nested sampling
wavenumber=True     # True if opacity given in terms of wavenumber, False if wavelength

priors = {"T": [2800, 100], "log_xh2o": [13,-13], "log_xhcn": [13,-13], "log_xnh3": [13,-13], "log_xch4": [13,-13], "log_kappa_cloud": [14,-12], "log_P0": [4,-1], "log_kappa_0": [9,-10], "Q0": [99,1], "a": [3,3], "log_r_c": [6,-7], "log_p_cia": [3,-3], "R0": [2*r0_uncertainty,r0-r0_uncertainty], "line": [5,0]} # priors for all possible parameters


## Info for all possible parameters ##
molecular_abundance_dict = {"01":"log_xh2o", "23":"log_xhcn", "11":"log_xnh3", "06":"log_xch4"}  # dictionary list of all possible molecules and corresponding abundance names

parameter_dict = {"T": 1000, "log_xh2o": "Off", "log_xhcn": "Off", "log_xnh3": "Off", "log_xch4": "Off", "log_kappa_cloud": "Off", "R0": r0, "log_P0": 1, "log_kappa_0": "Off", "Q0": "Off", "a": "Off", "log_r_c": "Off", "log_p_cia": -2, "Rstar": rstar, "G": g, "line": "Off"}    # default parameter values used if not retrieved

molecular_mass_dict = {"01": m_water, "23": m_cyanide, "11": m_ammonia, "06": m_methane}   # dictionary of molecules and their mean molecular masses
temperature_array = np.r_[50:700:50, 700:1500:100, 1500:3100:200]
temp_dict = {'01': temperature_array, '23': temperature_array, '11': temperature_array[:22], '06': temperature_array}   # temperature values for corresponding opacity tables
temperature_array_cia = np.r_[200:3025:25]          # temperature array for CIA table
opacity_path = os.environ['HOME'] + "/Desktop/PhD/OPACITIES/"  # path to opacity binary files
cia_path = os.environ['HOME'] + "/Desktop/PhD/HITRAN/"      # path to CIA files


path = os.getenv("PWD")
planet_path = path + "/planets/" + planet_name + "/"