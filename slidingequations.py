# Integrate a system of many equation, each representing a physical element,
#   using a window of active elements. That is: we apply an input to the first element
#   and integrate some elements after it. When the 1st element stops changing, we
#   delete it from the set of equations and add another element after the last one, and so on
# LIMITATIONS:
# ONLY constant input function = 1 at first cell is considered
# NO cycling (=closed bundles) are supported

import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode
import matplotlib.pyplot as plt
import random as rng

# basic parameters
b = 0.02
k=10**9
neqs = 64  # windows of equations considered
toteqs = 256 # total number of equations
fine = 5000
durata = 5000  # must be = fine, only constant input
#electrodes = [0,1,2] # to test with an external potential at the first electrodes
electrodes = [0]
newinit = 0  # to restart integration
cycling = 0  # no closed bundles
starteq = 0  # first equation to integrate

# single filament
L = 1.7*10**-12
C0 = 96*10**-18  
R1 = 6.11*10**6
R2 = 0.9*10**6
# high density bundle 450nm width 
#L = 8378*10**-12
#C0 = 76*10**-16  
#R1 = 0.077*10**6
#R2 = R1/7
# low density bundle 50 filaments
#L = 3.83*10**-14
#C0 = 2*10**-18  
#R1 = 0.11*10**6
#R2 = 50*R1/7  # series-addition formula for resistance



print(1/((k**2)*C0*L))
print(k*(R1*C0+2*R2*C0))
print(k*L*C0)
print(1/(k*np.sqrt(L*C0)))

# function that returns dv/dt etc.
# we have neqs second order equations, so 2*neqs first order
# and a variable vector [v1, v2, v3, ..., dv1dt, dv2dt, dv3dt, ...]
def model1(t,xy):
# total number of equations = toteqs
# equations actually integrated = startqs to starteq+neqs-1
# equations 0 to starteq = const = initial value; equations starteq+neqs = const = 0
# this function considers only the neqs to integrate, the calling one slides them
# TODO: how to manage non constant input functions?
    for i in range(neqs):
        if 1 -2*b*xy[i] == 0:
            raise Exception('V%s causes division by zero (=1/2b) at t = %s' % (i+starteq,t))
    res = np.zeros(2*neqs)
    res[neqs]= (1/((k**2)*L*C0*(1 -2*b*xy[0])))*(L*C0 * 2*b*(k*xy[neqs])**2 + ufunc(t,0) + cycling*xy[neqs-1] + xy[1] - 2*xy[0] - R1*C0 *k*(xy[neqs] - 2*b*xy[0]*xy[neqs]) - R2*C0*k*(2*(xy[neqs] - 2*b*xy[0]*xy[neqs])-(xy[neqs+1] - 2*b*xy[1]*xy[neqs+1])-cycling*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])))
    for i in range(1,neqs-1):
        res[neqs+i]= (1/((k**2)*L*C0*(1 -2*b*xy[i])))*(L*C0 * 2*b*(k*xy[neqs+i])**2 + ufunc(t,i) + xy[i-1] + xy[i+1] - 2*xy[i] - R1*C0 *k*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i]) - R2*C0*k*(2*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i])-(xy[neqs+i+1] - 2*b*xy[i+1]*xy[neqs+i+1])-(xy[neqs+i-1] - 2*b*xy[i-1]*xy[neqs+i-1])))
    
    res[2*neqs-1]= (1/((k**2)*L*C0*(1 -2*b*xy[neqs-1])))*(L*C0 * 2*b*(k*xy[2*neqs-1])**2 + ufunc(t,neqs-1) +cycling*xy[0] + xy[neqs-2] - 2*xy[neqs-1] - R1*C0 *k*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1]) - R2*C0*k*(2*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])-(xy[2*neqs-2] - 2*b*xy[neqs-2]*xy[2*neqs-2])-cycling*(xy[neqs] - 2*b*xy[0]*xy[neqs])))
    for i in range(neqs):
        res[i] = xy[i+neqs]

#        res = np.zeros(2*toteqs)
#    res[toteqs+starteq]= (1/((k**2)*L*C0*(1 -2*b*xy[starteq])))*(L*C0 * 2*b*(k*xy[toteqs+starteq])**2 + ufunc(t,0) + cycling*xy[neqs-1] + xy[1] - 2*xy[0] - R1*C0 *k*(xy[toteqs+starteq] - 2*b*xy[starteq]*xy[toteqs+starteq]) - R2*C0*k*(2*(xy[toteqs+starteq] - 2*b*xy[0]*xy[toteqs+starteq])-(xy[toteqs+starteq+1] - 2*b*xy[1+starteq]*xy[toteqs+starteq+1])-cycling*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])))
#    for i in range(1,neqs-1):
#        res[toteqs+starteq+i]= (1/((k**2)*L*C0*(1 -2*b*xy[i+starteq])))*(L*C0 * 2*b*(k*xy[toteqs+starteq+i])**2 + ufunc(t,i) + xy[i+starteq-1] + xy[i+starteq+1] - 2*xy[i+starteq] - R1*C0 *k*(xy[toteqs+starteq+i] - 2*b*xy[i+starteq]*xy[toteqs+starteq+i]) - R2*C0*k*(2*(xy[toteqs+starteq+i] - 2*b*xy[i+starteq]*xy[toteqs+starteq+i])-(xy[toteqs+starteq+i+1] - 2*b*xy[i+starteq+1]*xy[toteqs+starteq+i+1])-(xy[toteqs+starteq+i-1] - 2*b*xy[i+starteq-1]*xy[toteqs+starteq+i-1])))
    
#    res[toteqs+starteq+neqs-1]= (1/((k**2)*L*C0*(1 -2*b*xy[starteq+neqs-1])))*(L*C0 * 2*b*(k*xy[toteqs+starteq+neqs-1])**2 + ufunc(t,starteq+neqs-1) +cycling*xy[0] + xy[starteq+neqs-2] - 2*xy[starteq+neqs-1] - R1*C0 *k*(xy[toteqs+starteq-1] - 2*b*xy[neqs+starteq-1]*xy[toteqs+starteq-1]) - R2*C0*k*(2*(xy[toteqs+starteq-1] - 2*b*xy[neqs+starteq-1]*xy[toteqs+starteq-1])-(xy[toteqs+starteq-2] - 2*b*xy[neqs+starteq-2]*xy[toteqs+starteq-2])-cycling*(xy[neqs] - 2*b*xy[0]*xy[neqs])))
#    for i in range(neqs):
#        res[i+starteq] = xy[i+toteqs+starteq]
#        
#    for i in range(starteq):
#        res[i] = x[i][len(x[i])-1] # const = last value reached
#        res[toteqs+i] = 0
#    # the following instr are usless: it's already all zeros
#    #for i in range(starteq+neqs,toteqs):
#    #    res[i] = 0    # const = 0 not yet reached by the excitation
#    #    res[toteqs+i] = 0 


    return res
    
def ufunc(t,i):
#    i=k+starteq
# at the beginning this is the stimulus
# after this is the value of the discarded element, that is = 1
    if i not in electrodes:
        return 0
    tt = t+newinit
    if tt<=durata:
        return 1
    elif t<durata*2:
        return np.exp(-0.5*(tt-durata)**2)
    else:
        return 0



t1=[0]
x=[[0],[0],[0]]  

for i in range(3,toteqs):
    x.append([0])
xy=np.zeros(neqs*2)

r = ode(model1).set_integrator('lsoda', method='bdf',nsteps=5000)
r.set_initial_value(xy, 0)
dt=0.1
stepi=0
time80 = -1   # when the last element reaches 80% of the input (supposing input == 1)
time05 = -1   # when the first element goes back to zero
maxval = -99999
minval = 99999
timemax = -1   # time of max value
timemin = -1   # time of min value
stopcount = 0
iterations = 0

while r.successful() and r.t < fine:
    t1.append(r.t+dt)
    sol=r.integrate(r.t+dt)
    stepi=stepi+1
    if stepi % 20 == 0:
        print("step %s" % stepi)
    for i in range(starteq):
        x[i].append(x[i][len(x[i])-1])
        
    for i in range(starteq,neqs):
        x[i].append(sol[i])
    for i in range(neqs,toteqs):
        x[i].append(0)
    # check if first cell is constant
    if np.absolute(sol[0] - 1) < 0.05:
        stopcount = stopcount + 1
    else:
        stopcount = 0
    if stopcount > 3:
        if starteq<toteqs-1:
            starteq = starteq + 1
        else:
            iterations = 10 # DON'T go on computing!
            break
        stopcount = 0
    # the following evaluations should be modified!
    if sol[neqs-1] >= 0.0025 and time80 == -1:
        time80 = r.t
    if sol[0] <= 0.05 and time05 == -1:
        time05 = r.t
    if np.absolute(sol[neqs-1]) >= maxval:
        timemax = r.t
        maxval = np.absolute(sol[neqs-1])
    if np.absolute(sol[0]) <= minval:
        timemin = r.t
        minval = np.absolute(sol[0])

# if it does not succeed, I try restarting with initial conditions = the last values
#   computed


print("Time now %s" % r.t)
print("starteq %s" % starteq)

while iterations<5:
    newinit = newinit+r.t
    if newinit>= fine:
        break
    iterations = iterations + 1
    print("Time corresponding to new zero %s" % newinit)
    for i in range(neqs):
        xy[i]= x[i][len(x[i])-1]
        xy[i+neqs]= (x[i][len(x[i])-1]-x[i][len(x[i])-2])/dt
    r.set_initial_value(xy,0)
    remain = fine-newinit
    stopcount = 0
    print("Time remaining to integrate %s" % remain)
    while r.successful() and r.t < remain:
        t1.append(newinit+r.t+dt)
        sol=r.integrate(r.t+dt)
        stepi=stepi+1
        if stepi % 20 == 0:
            print("step %s" % stepi)
        for i in range(starteq):
            x[i].append(x[i][len(x[i])-1])
        for i in range(starteq,neqs):
            x[i].append(sol[i])
        for i in range(neqs,toteqs):
            x[i].append(0)
        # check if first cell is constant
        if np.absolute(sol[0] - 1) < 0.05:
            stopcount = stopcount + 1
        else:
            stopcount = 0
        if stopcount > 3:
            if starteq < toteqs-1:
                starteq = starteq + 1
            else:
                iterations = 10
                break
            stopcount = 0
        # the following evaluations should be modified!
        if sol[neqs-1] >= 0.8 and time80 == -1:
            time80 = r.t
        if sol[0] <= 0.05 and time05 == -1:
            time05 = r.t
        if np.absolute(sol[neqs-1]) >= maxval:
            timemax = r.t
            maxval = np.absolute(sol[neqs-1])
        if np.absolute(sol[0]) <= minval:
            timemin = r.t
            minval = np.absolute(sol[0])

newinit = 0
for i in electrodes:
    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    uu = np.zeros((len(t1)))
    k=0
    for tx in t1:
        uu[k] = ufunc(tx,i)
        k=k+1
    plt.plot(t1,uu,color,linewidth=2,label='v'+str(i))

if electrodes:
    plt.legend()
    plt.show()


for i in range(min(toteqs,10)):
    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


plt.legend()
plt.show()
if toteqs>=20:
    for i in range(10,20):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


plt.legend()
plt.show()
if toteqs>=30:
    for i in range(20,30):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if toteqs>=40:
    for i in range(30,40):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if toteqs>=64:
    for i in range(54,63):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if toteqs>=370:
    for i in range(360,370):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if toteqs>=10:
    for i in range(toteqs-10,toteqs):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if toteqs>=16:
    for i in range(0,toteqs,16):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))

    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
    plt.plot(t1,x[toteqs-1],color,linewidth=2,label='v'+str(toteqs-1))

    plt.legend()
    plt.show()


print("Last element reached max %s at %s" % (maxval,timemax))
print("First element dropped at min %s at %s" % (minval,timemin))
print("Last element reached 0.015 of input at %s" % time80)
print("First element dropped at 0.05 of input at %s" % time05)

