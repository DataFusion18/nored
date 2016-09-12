#This script will integrate several differential equations
#that will describe the change in isotopic value of the alpha and beta nitrogen of N2O
#produced from anaerobic nitrate reduction
#
#                                                         ---> fractionation of alpha N
#             ko            k1            k2            -
#       NO3 -------> NO2 --------> NO -----------> N2O -
#                                           |            -
#                                           |              ---> fractionation of beta 
#
#
#The nitrate concentration and rate constant ko are not inlcuded in the simulation because
#this particular step occurs so rapidly that all nitrate is converted to nitrite in a few seconds
#All rates are in units of 1/min 
#Concentrations are in units of nmols/L or nM
#
#All species are described in the state vector X:
#       X = [NO2,NO,N2O]
#
#All rates are describe in the rate vector R:
#       R = [k1,k2
#
#Where [E]=(1-f)Etot and [EI]=f*Etot
# and Etot is the concentration of the target protein
#
#
#This has been adapted from run_pk.py from Alex Dickson at Michigan State University 2016 under repository pk
#
#

import numpy as np
import pylab as p
import matplotlib.pyplot as plt
from scipy import integrate

#set time parameters
tmin = 0.0 #first time point
tmax = 320.0 #last time point

#set dose profile
add_conc = [1200,1200,1200]# increase NO2 in nM
add_time = [1,300,600]# in min

NO20 = 1200 #intial concentration (nM) of NO2 after rapid total conversion of NO3 by NAR
X0 = np.array([1200,0,0]) #array of starting conditions
R = np.array([45,10,0]) # array of rates for each step
t = np.linspace(tmin, tmax, num=321) # vector of minutes

#functions

def NO2_of_t (X,t):
  #max(0,X)
  dNO2_dt = -R[0]
  return dNO2_dt
  
def NO_of_t (X,t):
  dNO_dt = R[0]-R[1]
  return dNO_dt

def N2O_of_t (X,t):
  dN2O_dt = R[1]
  return dN2O_dt
  
def dX_dt (X,t):
  return np.array([NO2_of_t (X,t), NO_of_t (X,t), N2O_of_t (X,t)])

X, infodict = integrate.odeint(dX_dt,X0,t,ml>=0,full_output=True);
print(infodict['message'])
print(X)

plt.figure(1)
plt.plot(t,X.T[0])
plt.xlabel("Time")
plt.ylabel("NO2 concentration")
p.savefig('NO2.png', bbox_inches='tight')


plt.clf()
plt.plot(t,X.T[1],'r')
plt.xlabel("Time (min)")
plt.ylabel("NO")
p.savefig('NO.png', bbox_inches='tight')

plt.clf()
plt.plot(t,X.T[2],'b')
plt.xlabel("Time (min)")
plt.ylabel("N2O")
p.savefig('N2O.png', bbox_inches='tight')

plt.clf()
plt.plot(t,X.T[2],'g')
plt.plot(t,X.T[1],'r')
plt.plot(t,X.T[0],'b')
plt.xlabel("Time (min)")
plt.ylabel("Concentration")
p.savefig('All.png', bbox_inches='tight')
