# First Example of usage of the odeint scipy function

import numpy as np
from scipy.integrate import odeint
from scipy.integrate import solve_ivp
from scipy.integrate import ode
import matplotlib.pyplot as plt


# basic parameters
b = 0.1
L = 1.7*10**-12
C0 = 96*10**-18  
R1 = 6.11*10**6
R2 = 0.9*10**6
k=10**9

print(1/((k**2)*C0*L))
print(k*(R1*C0+2*R2*C0))
print(k*L*C0)

# function that returns dv/dt etc.
# we have 3 second order equations, so 6 first order
# and a variable vector [v1, v2, v3, dv1dt, dv2dt, dv3dt]
def model1(xy,t):
    if 1 -2*b*xy[0] == 0:
        raise Exception('V1 causes division by zero (=1/2b) at t = %s' % t)
    if 1 -2*b*xy[1] == 0:
        raise Exception('V2 causes division by zero (=1/2b) at t = %s' % t)
    if 1 -2*b*xy[2] == 0:
        raise Exception('V3 causes division by zero (=1/2b) at t = %s' % t)
    dv1dt= (1/((k**2)*L*C0*(1 -2*b*xy[0])))*(L*C0 * 2*b*(k*xy[3])**2 + xy[1] - 2*xy[0]         - R1*C0 *k*(xy[3] - 2*b*xy[0]*xy[3]) - R2*C0*k*(2*(xy[3] - 2*b*xy[0]*xy[3])-(xy[4] - 2*b*xy[1]*xy[4])))
    dv2dt= (1/((k**2)*L*C0*(1 -2*b*xy[1])))*(L*C0 * 2*b*(k*xy[4])**2 + xy[0] + xy[2] - 2*xy[1] - R1*C0 *k*(xy[4] - 2*b*xy[1]*xy[4]) - R2*C0*k*(2*(xy[4] - 2*b*xy[1]*xy[4])-(xy[5] - 2*b*xy[2]*xy[5])-(xy[3] - 2*b*xy[0]*xy[3])))
    dv3dt= (1/((k**2)*L*C0*(1 -2*b*xy[2])))*(L*C0 * 2*b*(k*xy[5])**2 + xy[1] - 2*xy[2]         - R1*C0 *k*(xy[5] - 2*b*xy[2]*xy[5]) - R2*C0*k*(2*(xy[5] - 2*b*xy[2]*xy[5])-(xy[4] - 2*b*xy[1]*xy[4])))
    return [xy[3],xy[4],xy[5], dv1dt, dv2dt, dv3dt]
    

x0=1
y0=0
z0=0
dx0=0
dy0=0
dz0=0
fine = 3

# second method
n=fine*50+1
t = np.linspace(0,fine,n)
x = np.empty_like(t)
y = np.empty_like(t)
z = np.empty_like(t)
x[0]=x0
y[0]=y0
z[0]=z0

xy=[x0,y0,z0,dx0,dy0,dz0]
#####################à
#for i in range(1,n):
#    # span for next time step
#    tspan = [t[i-1],t[i]]
#    # solve for next step
#    res = odeint(model1,xy,tspan)
#    # store solution for plotting
#    x[i] = res[1][0]
#    y[i] = res[1][1]
#    z[i] = res[1][2]
#    # next initial condition
#    xy = res[1] 


#plt.plot(t,x,'b-',linewidth=2,label='v1')
#plt.plot(t,y,'r-',linewidth=2,label='v2')
#plt.plot(t,z,'g-',linewidth=2,label='v2')
#plt.legend()
#plt.show()

# third method - does not end!

def model2(t,xy):
    if 1 -2*b*xy[0] == 0:
        raise Exception('V1 causes division by zero (=1/2b) at t = %s' % t)
    if 1 -2*b*xy[1] == 0:
        raise Exception('V2 causes division by zero (=1/2b) at t = %s' % t)
    if 1 -2*b*xy[2] == 0:
        raise Exception('V3 causes division by zero (=1/2b) at t = %s' % t)
    dv1dt= (1/((k**2)*L*C0*(1 -2*b*xy[0])))*(L*C0 * 2*b*(k*xy[3])**2 + xy[1] - 2*xy[0] - R1*C0 *k*(xy[3] - 2*b*xy[0]*xy[3]) - R2*C0*k*(2*(xy[3] - 2*b*xy[0]*xy[3])-(xy[4] - 2*b*xy[1]*xy[4])))
    dv2dt= (1/((k**2)*L*C0*(1 -2*b*xy[1])))*(L*C0 * 2*b*(k*xy[4])**2 + xy[0] + xy[2] - 2*xy[1] - R1*C0 *k*(xy[4] - 2*b*xy[1]*xy[4]) - R2*C0*k*(2*(xy[4] - 2*b*xy[1]*xy[4])-(xy[5] - 2*b*xy[2]*xy[5])-(xy[3] - 2*b*xy[0]*xy[3])))
    dv3dt= (1/((k**2)*L*C0*(1 -2*b*xy[2])))*(L*C0 * 2*b*(k*xy[5])**2 + xy[1] - 2*xy[2] - R1*C0 *k*(xy[5] - 2*b*xy[2]*xy[5]) - R2*C0*k*(2*(xy[5] - 2*b*xy[2]*xy[5])-(xy[4] - 2*b*xy[1]*xy[4])))
    return [xy[3],xy[4],xy[5], dv1dt, dv2dt, dv3dt]

#res = solve_ivp(fun=model2,t_span=[0,3],y0=[1,0,0,0,0,0],method='LSODA')
#print(res.t)
#print(res.y)
r = ode(model2).set_integrator('lsoda', method='bdf',nsteps=5000)
r.set_initial_value(xy, 0)

dt=0.1
t1=[0]
x1=[1]
y1=[0]
z1=[0]
while r.successful() and r.t < fine:
    t1.append(r.t+dt)
    sol=r.integrate(r.t+dt)
    x1.append(sol[0])
    y1.append(sol[1])
    z1.append(sol[2])
    print(r.t+dt, sol)
    
plt.plot(t1,x1,'b-',linewidth=2,label='v1')
plt.plot(t1,y1,'r-',linewidth=2,label='v2')
plt.plot(t1,z1,'g-',linewidth=2,label='v2')
plt.legend()
plt.show()

