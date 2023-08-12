import numpy as np

"""
x - variable
Ap -- amplitude
Xp -- peak position
sigp -- peak width
xi -- peak asymmetry
rho1 -- left tail
rho2 -- right tail
"""
def bukin(x, Ap, Xp, sigp, xi, rho1, rho2):
    """
    Returns a Bukin evaluated over all values in x
    """
    r1=0
    r2=np.zeros(len(x))
    r3=0
    r4=0
    r5=0
    hp=0
    x1 = 0
    x2 = 0
    fit_result = np.zeros(len(x))
    consts = 2*np.sqrt(2*np.log(2.))

    hp=sigp*consts
    r3=np.log(2.)
    r4=np.sqrt(np.power(xi,2)+1)
    r1=xi/r4

    if(np.abs(xi) > np.exp(-6.)):
        r5=xi/np.log(r4+xi)
    else:
        r5=1

    x1 = Xp + (hp / 2) * (r1-1)
    x2 = Xp + (hp / 2) * (r1+1)


    # Left Side
    left = np.where(x < x1)
    centre = np.logical_and(np.where(x >= x1,True,False), np.where(x < x2,True,False))
    right = np.where(x >= x2)
    x_l = x[left]
    x_c = x[centre]
    x_r = x[right]

    r2[left]=rho1*np.power((x_l-x1)/(Xp-x1),2)-r3 + 4 * r3 * (x_l-x1)/hp * r5 * r4/np.power((r4-xi),2)
    # Center
    if(np.abs(xi) > np.exp(-6.)):
            #print(len(x_c))
            r2[centre]=np.log(1 + 4 * xi * r4 * (x_c-Xp)/hp)/np.log(1+2*xi*(xi-r4))
            r2[centre]=-r3*(np.power(r2[centre],2))
    else:
            r2[centre]=-4*r3*np.power(((x_c-Xp)/hp),2)

    # Right Side

    r2[right]=rho2*np.power((x_r-x2)/(Xp-x2),2)-r3 - 4 * r3 * (x_r-x2)/hp * r5 * r4/np.power((r4+xi),2)


    # Normalize the result
    fit_result = np.exp(r2)*Ap 

    greater = np.where(np.abs(r2) > 100)
    fit_result[greater] = 0

    return fit_result

