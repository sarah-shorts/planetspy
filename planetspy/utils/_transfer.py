from numpy import *
from scipy.optimize import minimize
G = 6.67*10**-11

def delta_v(mass_p, r_parent, r_target):
    return np.sqrt(G*mass_p/r_parent)*(np.sqrt(2*r_target/(r_parent+r_target))-1)
def time_transfer(mass_p, r_parent, r_target):
    return np.pi*np.sqrt((r_parent+r_target)**3/(8*G*mass_p))
def angular_alignment(r_parent, r_target):
    return np.pi*(1-1/np.sqrt(8)*(r_parent/r_target+1)**3/2)
def calc_hohmann_minV():
    return minimize(delta_v, )