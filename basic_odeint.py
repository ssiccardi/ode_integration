# First Example of usage of the odeint scipy function

import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

# function that returns dy/dt
def model(y,t,k):
    dydt = -k * y
    return dydt

# initial condition
y0 = 5

# time points
t = np.linspace(0,40)

# solve ODE
k=0.1
y1 = odeint(model,y0,t,args=(k,))
k=0.2
y2 = odeint(model,y0,t,args=(k,))
k=0.5
y3 = odeint(model,y0,t,args=(k,))

# plot results

plt.plot(t,y1,'r-',linewidth=2,label='k=0.1')
plt.plot(t,y2,'b--',linewidth=2,label='k=0.2')
plt.plot(t,y3,'g:',linewidth=2,label='k=0.5')
plt.xlabel('time')
plt.ylabel('y(t)')
plt.legend()
plt.show()

def model1(xy,t):
    dxdt= -0.5 * xy[0] + 0.5* ufunc(t)
    dydt= -0.2 * xy[1] + 0.2 * xy[0]
    return [dxdt, dydt]
    
def ufunc(t):
#    if t<5:
#        return 0
#    else:
#        return 2
     return np.sin(t)     
x0=0
y0=0


# first method

xy = odeint(model1,[x0,y0],t)

plt.plot(t,xy[:,0],'r-',linewidth=2,label='x met1')
plt.plot(t,xy[:,1],'b--',linewidth=2,label='y met1')
plt.legend()
plt.show()

# second method
n=401
t = np.linspace(0,40,n)
x = np.empty_like(t)
y = np.empty_like(t)

z0=[x0,y0]
for i in range(1,n):
    # span for next time step
    tspan = [t[i-1],t[i]]
    # solve for next step
    z = odeint(model1,z0,tspan)
    # store solution for plotting
    x[i] = z[1][0]
    y[i] = z[1][1]
    # next initial condition
    z0 = z[1] 


plt.plot(t,x,'b--',linewidth=2,label='x met2')
plt.plot(t,y,'r-',linewidth=2,label='y met2')
plt.legend()
plt.show()

# with the step function: for t<5 no difference, from t=5 to t=29 big difference, then small 
# with sin(t): there are errors almost always

delta1 = np.zeros(41)
delta2 = np.zeros(41)
t1 = np.linspace(0,41,41)
for i in range(0,41):
    print("delta x "+str(x[0+(i)*10] - xy[i,0]))
    print("delta y "+str(y[0+(i)*10] - xy[i,1]))
    print("t "+str(t[0+(i)*10]))
    delta1[i]=x[i*10]-xy[i,0]
    delta2[i]=y[i*10]-xy[i,1]

print(delta1)
print(t1)
plt.plot(t1,delta1,'b--',linewidth=2,label='delta x')
plt.plot(t1,delta2,'r-',linewidth=2,label='delta y')
plt.legend()
plt.show()

