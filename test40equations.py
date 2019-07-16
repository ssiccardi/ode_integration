# First Example of usage of the odeint scipy function

import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode
import matplotlib.pyplot as plt
import random as rng

# basic parameters
b = 0.1
L = 1.7*10**-12
C0 = 96*10**-18  
R1 = 6.11*10**6
R2 = 0.9*10**6
k=10**9
neqs = 80  # does not succeed with 400 eqs 
fine = 1000
durata = 10
electrodes = [0]

print(1/((k**2)*C0*L))
print(k*(R1*C0+2*R2*C0))
print(k*L*C0)


# function that returns dv/dt etc.
# we have 3 second order equations, so 6 first order
# and a variable vector [v1, v2, v3, dv1dt, dv2dt, dv3dt]
def model1(t,xy):
    for i in range(neqs):
        if 1 -2*b*xy[i] == 0:
            raise Exception('V%s causes division by zero (=1/2b) at t = %s' % (i,t))
    res = np.zeros(2*neqs)
    res[neqs]= (1/((k**2)*L*C0*(1 -2*b*xy[0])))*(L*C0 * 2*b*(k*xy[neqs])**2 + ufunc(t,0) + xy[1] - 2*xy[0] - R1*C0 *k*(xy[neqs] - 2*b*xy[0]*xy[neqs]) - R2*C0*k*(2*(xy[neqs] - 2*b*xy[0]*xy[neqs])-(xy[neqs+1] - 2*b*xy[1]*xy[neqs+1])))
    for i in range(1,neqs-1):
        res[neqs+i]= (1/((k**2)*L*C0*(1 -2*b*xy[i])))*(L*C0 * 2*b*(k*xy[neqs+i])**2 + ufunc(t,i) + xy[i-1] + xy[i+1] - 2*xy[i] - R1*C0 *k*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i]) - R2*C0*k*(2*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i])-(xy[neqs+i+1] - 2*b*xy[i+1]*xy[neqs+i+1])-(xy[neqs+i-1] - 2*b*xy[i-1]*xy[neqs+i-1])))
    
    res[2*neqs-1]= (1/((k**2)*L*C0*(1 -2*b*xy[neqs-1])))*(L*C0 * 2*b*(k*xy[2*neqs-1])**2 + ufunc(t,neqs-1) + xy[neqs-2] - 2*xy[neqs-1] - R1*C0 *k*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1]) - R2*C0*k*(2*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])-(xy[2*neqs-2] - 2*b*xy[neqs-2]*xy[2*neqs-2])))
    for i in range(neqs):
        res[i] = xy[i+neqs]
    return res
    
def ufunc(t,i):
    if i not in electrodes:
        return 0
    if t<durata:
        return np.cos(np.pi*t)
    elif t<durata*2:
        return np.cos(np.pi*t)*np.exp(-0.5*(t-durata)**2)
    else:
        return 0



#n=fine*50+1
t1=[0]
x=[[0],[0],[0]]
for i in range(3,neqs):
    x.append([0])

#print(x)

xy=np.zeros(neqs*2)
#xy[0] = 1
#xy[1] = 1
#xy[2] = 1

r = ode(model1).set_integrator('lsoda', method='bdf',nsteps=5000)
r.set_initial_value(xy, 0)
dt=0.1
stepi=0
while r.successful() and r.t < fine:
    t1.append(r.t+dt)
    sol=r.integrate(r.t+dt)
    stepi=stepi+1
    if stepi % 20 == 0:
        print("step %s" % stepi)
    for i in range(neqs):
#        print(x[i])
#        print(sol[i])
        x[i].append(sol[i])

for i in range(10):
    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))

#plt.plot(t1,x[0],'b-',linewidth=2,label='v1')
#plt.plot(t1,x[1],'r-',linewidth=2,label='v2')
#plt.plot(t1,x[2],'g-',linewidth=2,label='v2')
#plt.plot(t1,x[3],'b--',linewidth=2,label='v2')
#plt.plot(t1,x[4],'r--',linewidth=2,label='v2')
#plt.plot(t1,x[5],'g--',linewidth=2,label='v2')

plt.legend()
plt.show()

for i in range(10,20):
    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


plt.legend()
plt.show()

for i in range(20,30):
    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


plt.legend()
plt.show()

for i in range(30,40):
    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


plt.legend()
plt.show()

for i in range(neqs-10,neqs):
    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


plt.legend()
plt.show()

