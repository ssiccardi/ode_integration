===============================

Integration of ODE in a network

===============================

We have a network composed of chains of elements.
Each element's status is the solution of an ordinary differential equation.
We want to solve the system of equations, taking into account elements that are excited and disregarding all the others.

This makes sense because the network is in general at rest and occasionally some solitons arise and travel along some edges of the network.

We study how the ode, odeint functions of scipy can be used to solve this problems.
We start with very basic examples of odeint usage.

