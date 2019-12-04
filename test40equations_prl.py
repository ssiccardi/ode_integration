# First Example of usage of the odeint scipy function

import numpy as np
from scipy.integrate import odeint
from scipy.integrate import ode
import matplotlib.pyplot as plt
import random as rng

# basic parameters
b = 0.02 # tested also b=0.2 
ek = 10
k=10**ek   # k=10**10 # for low density
neqs = 32  # does not succeed with 400 eqs 
fine = 10000
durata = 10000
#electrodes = [0,1,2] # to test with an external potential at the first electrodes
electrodes = [0,15]
v_electrodes = [1,-1,-1,1,-1,-1]
newinit = 0  # to restart integration
cycling = 1  # if =1 the bundle is cloed on itslef

# single filament
#L = 1.7*10**-12
#C0 = 96*10**-18  
#R1 = 6.11*10**6
#R2 = 0.9*10**6
#tit="Filament, total %s elements"
# high density bundle 450nm width (integration converges easily)
#L = 8378*10**-12
#C0 = 76*10**-16  
#R1 = 0.077*10**6
#R2 = R1/7
#tit="H.D. bundle 450nm thick, total %s elements"
# low density bundle 50 filaments
L = 3.83*10**-14
C0 = 2*10**-18  
R1 = 0.11*10**6
R2 = 50*R1/7  # series-addition formula for resistance
tit="L.D. bundle of 50 filaments, total %s elements"



print(1/((k**2)*C0*L))
print(k*(R1*C0+2*R2*C0))
print(k*L*C0)
print(1/(k*np.sqrt(L*C0)))

# function that returns dv/dt etc.
# we have 3 second order equations, so 6 first order
# and a variable vector [v1, v2, v3, dv1dt, dv2dt, dv3dt]
def model1(t,xy):
    for i in range(neqs):
        if 1 -2*b*xy[i] == 0:
            raise Exception('V%s causes division by zero (=1/2b) at t = %s' % (i,t))
    res = np.zeros(2*neqs)
#    res[neqs]= (1/((k**2)*L*C0*(1 -2*b*xy[0])))*(L*C0 * 2*b*(k*xy[neqs])**2 + ufunc(t,0) + cycling*xy[neqs-1] + xy[1] - 2*xy[0] - R1*C0 *k*(xy[neqs] - 2*b*xy[0]*xy[neqs]) - R2*C0*k*(2*(xy[neqs] - 2*b*xy[0]*xy[neqs])-(xy[neqs+1] - 2*b*xy[1]*xy[neqs+1])-cycling*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])))
    res[neqs]= (1/((k**2)*L*C0*(1 -2*b*xy[0])))*(L*C0 * 2*b*(k*xy[neqs])**2 + ufunc(t,0) + cycling*xy[neqs-1] + xy[1] - (1+cycling)*xy[0] - R1*C0 *k*(xy[neqs] - 2*b*xy[0]*xy[neqs]) - R2*C0*k*((1+cycling)*(xy[neqs] - 2*b*xy[0]*xy[neqs])-(xy[neqs+1] - 2*b*xy[1]*xy[neqs+1])-cycling*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])))
    for i in range(1,neqs-1):
        res[neqs+i]= (1/((k**2)*L*C0*(1 -2*b*xy[i])))*(L*C0 * 2*b*(k*xy[neqs+i])**2 + ufunc(t,i) + xy[i-1] + xy[i+1] - 2*xy[i] - R1*C0 *k*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i]) - R2*C0*k*(2*(xy[neqs+i] - 2*b*xy[i]*xy[neqs+i])-(xy[neqs+i+1] - 2*b*xy[i+1]*xy[neqs+i+1])-(xy[neqs+i-1] - 2*b*xy[i-1]*xy[neqs+i-1])))
    
    res[2*neqs-1]= (1/((k**2)*L*C0*(1 -2*b*xy[neqs-1])))*(L*C0 * 2*b*(k*xy[2*neqs-1])**2 + ufunc(t,neqs-1) +cycling*xy[0] + xy[neqs-2] - (1+cycling)*xy[neqs-1] - R1*C0 *k*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1]) - R2*C0*k*((1+cycling)*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])-(xy[2*neqs-2] - 2*b*xy[neqs-2]*xy[2*neqs-2])-cycling*(xy[neqs] - 2*b*xy[0]*xy[neqs])))
#    res[2*neqs-1]= (1/((k**2)*L*C0*(1 -2*b*xy[neqs-1])))*(L*C0 * 2*b*(k*xy[2*neqs-1])**2 + ufunc(t,neqs-1) +cycling*xy[0] + xy[neqs-2] - 2*xy[neqs-1] - R1*C0 *k*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1]) - R2*C0*k*(2*(xy[2*neqs-1] - 2*b*xy[neqs-1]*xy[2*neqs-1])-(xy[2*neqs-2] - 2*b*xy[neqs-2]*xy[2*neqs-2])-cycling*(xy[neqs] - 2*b*xy[0]*xy[neqs])))
    for i in range(neqs):
        res[i] = xy[i+neqs]
    return res
    
def ufunc(t,i):
    if i not in electrodes:
        return 0
    k=electrodes.index(i)
    val_func = v_electrodes[k]
    tt = t+newinit
    tt0 = durata/10
    if tt<=durata:
#        return np.cos(np.pi*t)
        if i==1:
            xx=1.0
        else:
            xx=0.5
        #return 0.00006*xx*np.sin((t+newinit)/1000)  # to compare to the Mathematica old progr
#        return np.cos((1/(k*np.sqrt(L*C0)*0.7))*tt)  # RLC resonance?
#        if i==0:
#            return np.cos(2*np.pi*tt/(durata/2))
#        else:
#            return -np.cos(2*np.pi*tt/(durata/2))
        tmp=(tt-tt0)/tt0
#        return (1/2 - ((np.exp(tmp)-np.exp(-tmp))/(2*(np.exp(tmp)+np.exp(-tmp)))))
#        if i==0:
#            return (((np.exp(tmp)-np.exp(-tmp))/((np.exp(tmp)+np.exp(-tmp)))))
#        else:
#            return -(((np.exp(tmp)-np.exp(-tmp))/((np.exp(tmp)+np.exp(-tmp)))))
#        if i==0:  
#            return 1
#        else:
#            return -1
        return val_func
    elif tt<durata*2:
#        return np.cos((1/(k*np.sqrt(L*C0)*0.7))*tt)*np.exp(-0.5*(t-durata)**2) # RLC resonance?
#        return np.cos(2*np.pi*tt/(durata/2))*np.exp(-0.5*(tt-durata)**2)
#        return np.exp(-0.01*(tt-durata))
        return np.exp(-0.5*(tt-durata)**2)*val_func
#        return 0.0
#        return 1-tt/(durata*2)
    else:
        return 0



#n=fine*50+1
t1=[0]
x=[[0],[0],[0]]  
#x=[[1],[1],[1]]  # to compare to the old mathematica program with in. cond 1
for i in range(3,neqs):
    x.append([0])
#for i in range(20,40):
#    x[i][0]=1
#print(x)
# to compare old programs with the "initial bump"
#x[0][0] = 0.05*0.01
#x[1][0] = 0.05*0.025
#x[2][0] = 0.05*0.075
#x[3][0] = 0.05*0.15
#x[4][0] = 0.05*0.275
#x[5][0] = 0.05*0.4
#x[6][0] = 0.05*0.4
#x[7][0] = 0.05*0.275
#x[8][0] = 0.05*0.15
#x[9][0] = 0.05*0.075
#x[10][0] = 0.05*0.025
#x[10][0] = 0.05*0.01
xy=np.zeros(neqs*2)
# set all = 0 to test comparison to old progr with sin(x) added
#xy[0] = 1
#xy[1] = 1
#xy[2] = 1
#xy[0+neqs] = -1
#xy[1+neqs] = -1
#xy[2+neqs] = -1
# to compare old programs with the "initial bump"
#xy[0] = 0.5*0.01
#xy[1] = 0.5*0.025
#xy[2] = 0.5*0.075
#xy[3] = 0.5*0.15
#xy[4] = 0.5*0.275
#xy[5] = 0.5*0.4
#xy[6] = 0.5*0.4
#xy[7] = 0.5*0.275
#xy[8] = 0.5*0.15
#xy[9] = 0.5*0.075
#xy[10] = 0.5*0.025
#xy[11] = 0.5*0.01
#xy[0+neqs] = -0.5*0.01
#xy[1+neqs] = -0.5*0.015
#xy[2+neqs] = -0.5*0.05
#xy[3+neqs] = -0.5*0.075
#xy[4+neqs] = -0.5*0.125
#xy[5+neqs] = -0.5*0.125
#xy[6+neqs] = 0
#xy[7+neqs] = 0.5*0.125
#xy[8+neqs] = 0.5*0.125
#xy[9+neqs] = 0.5*0.075
#xy[10+neqs] = 0.5*0.05
#xy[11+neqs] = 0.5*0.015
#xy[12+neqs] = 0.5*0.01

#for i in range(20,40):
#    xy[i]=1
#xy[2] = 1

r = ode(model1).set_integrator('lsoda', method='bdf',nsteps=5000)
#r = ode(model1).set_integrator('vode', method='bdf',nsteps=5000)
r.set_initial_value(xy, 0)
dt=0.1 #  dt=0.001  # for low density bundles, as numerical integration is mode difficult, dt=0.1 in normal cases
stepi=0
time80 = -1   # when the last element reaches 80% of the input (supposing input == 1)
time05 = -1   # when the first element goes back to zero
maxval = -99999
maxval1 = -99999
maxval2 = -99999
minval = 99999
timemax = -1   # time of max value
timemin = -1   # time of min value
checksum = [0]  # to check sum of V-bV^2
while r.successful() and r.t < fine:
#    if r.t+dt>=durata:  # forced restard for low density bundles when the input goes to zero
#        print("exit at %s" % r.t)
#        break
    t1.append(r.t+dt)
    sol=r.integrate(r.t+dt)
    stepi=stepi+1
    if stepi % 20 == 0:
        print("step %s" % stepi)
    tmpchk = 0
    for i in range(neqs):
#        print(x[i])
#        print(sol[i])
        x[i].append(sol[i])
        tmpchk = tmpchk + sol[i] - b*(sol[i])**2
#        print(sol[i])
#        print(tmpchk)
    checksum.append(tmpchk)
    if sol[neqs-1] >= 0.0025 and time80 == -1:
        time80 = r.t
    if sol[0] <= 0.05 and time05 == -1:
        time05 = r.t
    if np.absolute(sol[neqs-1]) >= maxval:
        timemax = r.t
        maxval = np.absolute(sol[neqs-1])
    if np.absolute(sol[0]) >= maxval1:
        maxval1 = np.absolute(sol[0])
    if np.absolute(sol[1]) >= maxval2:
        maxval2 = np.absolute(sol[1])
    if np.absolute(sol[0]) <= minval:
        timemin = r.t
        minval = np.absolute(sol[0])
    if stepi>fine-25:  # forcing restart is a good idea in some cases
        print("exit at %s" % r.t)
        break

# if it does not succeed, I try restarting with initial conditions = the last values
#   computed

iterations = 0

print("Time now %s" % r.t)


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
    print("Time remaining to integrate %s" % remain)
    while r.successful() and r.t < remain:
        t1.append(newinit+r.t+dt)
        sol=r.integrate(r.t+dt)
        stepi=stepi+1
        if stepi % 20 == 0:
            print("step %s" % stepi)
        tmpchk=0
        for i in range(neqs):
#        print(x[i])
#        print(sol[i])
            x[i].append(sol[i])
            tmpchk = tmpchk + sol[i] - b*sol[i]**2
        checksum.append(tmpchk)
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
#        if r.t>remain-25:  # sometimes the last steps are tricky...
#            print("forced exit")
#            iterations = 10
#            break

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

plt.plot(t1,checksum,color,linewidth=2,label='checksum')
plt.legend()
plt.show()


for i in range(min(neqs,10)):
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
if neqs>=20:
    for i in range(10,20):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


plt.legend()
plt.show()
if neqs>=30:
    for i in range(20,30):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if neqs>=40:
    for i in range(30,40):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if neqs>=64:
    for i in range(54,63):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if neqs>=370:
    for i in range(360,370):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if neqs>=10:
    for i in range(neqs-10,neqs):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))


    plt.legend()
    plt.show()

if neqs>=16:
    plt.ylabel("Voltage (arb.units)")
#    plt.xlabel("Time (sec^-"+str(ek)+")")
    plt.xlabel("Time (ns)")  # per figura finale
    plt.title(tit % neqs)
    plt.tight_layout()
    linestyles=['-',':','-.']  # solo per 3 linee
    k = 0
    for i in range(0,neqs,12):
        color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
#        plt.plot(t1,x[i],color,linewidth=2,label='v'+str(i))
        plt.plot(t1,x[i],"#000000",linestyle=linestyles[k],linewidth=2,label='v'+str(i))
        k=k+1

    color = '#'+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))+'{:02x}'.format(rng.randint(0,255))
#    plt.plot(t1,x[neqs-1],color,linewidth=2,label='v'+str(neqs-1))
    plt.plot(t1,x[neqs-1],"#000000",linestyle='--',linewidth=2,label='v'+str(neqs-1))

    plt.legend(loc='upper right', bbox_to_anchor=(0.9, 0.8))
    plt.show()

print("Last element reached max %s at %s" % (maxval,timemax))
print("First element dropped at min %s at %s" % (minval,timemin))
print("Last element reached 0.015 of input at %s" % time80)
print("First element dropped at 0.05 of input at %s" % time05)

print("First element max is %s" % maxval1)
print("Second element max is %s" % maxval2)