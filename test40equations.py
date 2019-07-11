# First Example of usage of the odeint scipy function

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import random as rng

# basic parameters
b = 0.1
L = 1.7*10**-12
C0 = 96*10**-18  
R1 = 6.11*10**6
R2 = 0.9*10**6
k=10**9
neqs = 40

# function that returns dv/dt etc.
# we have 3 second order equations, so 6 first order
# and a variable vector [v1, v2, v3, dv1dt, dv2dt, dv3dt]
def model1(xy,t):
    for i in range(neqs):
        if 1 -2*b*xy[i] == 0:
            raise Exception('V%s causes division by zero (=1/2b) at t = %s' % (i,t))
    res = np.zeros(2*neqs)
    res[neqs]= (1/((k**2)*L*C0*(1 -2*b*xy[0])))*(L*C0 * 2*b*(k*xy[neqs])**2 + xy[1] - 2*xy[0] - R1*C0 *k*(xy[neqs] - 2*b*xy[0]*xy[neqs]) - R2*C0*k*(2*(xy[neqs] - 2*b*xy[0]*xy[neqs])-(xy[neqs+1] - 2*b*xy[1]*xy[neqs+1])))
    for i in range(1,neqs-1):
        res[neqs+i]= (1/((k**2)*L*C0*(1 -2*b*xy[i])))*(L*C0 * 2*b*(k*xy[neqs+i])**2 + xy[i-1] + xy[neqs+i-1] - 2*xy[i] - R1*C0 *k*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i]) - R2*C0*k*(2*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i])-(xy[neqs+i+1] - 2*b*xy[i+1]*xy[neqs+i+1])-(xy[neqs+i-1] - 2*b*xy[i-1]*xy[neqs+i-1])))
    
    res[2*neqs-1]= (1/((k**2)*L*C0*(1 -2*b*xy[neqs-1])))*(L*C0 * 2*b*(k*xy[2*neqs-1])**2 + xy[neqs-2] - 2*xy[neqs-1] - R1*C0 *k*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1]) - R2*C0*k*(2*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])-(xy[2*neqs-2] - 2*b*xy[neqs-2]*xy[2*neqs-2])))
    for i in range(neqs):
        res[i] = xy[i+neqs]
    return res
    
def ufunc(t):
#    if t<5:
#        return 0
#    else:
#        return 2
     return np.sin(t)     
fine = 3

# second method
n=fine*50+1
t = np.linspace(0,fine,n)
x=np.zeros((n,neqs))
x[0][0] = 1

xy=np.zeros(neqs*2)
xy[0] = 1

for i in range(1,n):
    # span for next time step
    tspan = [t[i-1],t[i]]
    # solve for next step
    res = odeint(model1,xy,tspan)
    # store solution for plotting
    x[i] = res[1][:40]
    # next initial condition
    xy = res[1] 

for i in range(neqs):
    color = (rng.randint(0,256), rng.randint(0,256), rng.randint(0,256))
    plt.plot(t,x[:,i],color,linewidth=1,label='v'+str(i))
plt.legend()
plt.show()


