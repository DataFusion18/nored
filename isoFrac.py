#This script will integrate several differential equations
#that will describe the change in isotopic value of the alpha and beta nitrogen of N2O
#produced from anaerobic nitrate reduction
#
#                                                       ---> isotopic value of alpha N
#             knired        knored        
#       NO2 --------> NO -----------> N2O 
#                   ^   
#              kin  | |  kout                   
#                     v                               ---> isotopic value of beta N
#                  NOenv  
#                   
#
#
#The nitrate concentration and rate constant ko are not inlcuded in the simulation because
#this particular step occurs so rapidly that all nitrate is converted to nitrite in a few seconds
#All rates are in units of 1/min 
#Concentrations are in units of nmols/L or nM
#
#All species are described in the state vector X:
#       X = [NO2,NO,NOenv,N2O]            the concentration of each species nM
#
#       Y = [iNO2,iNO,iNOenv,iN2O]        the isotopic value of N in N species
#
#All rates are described in the rate vector R:
#       R = [knired,kin,kout,knored]
#
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
add_time = [-0.001,320,640]# in min

NO20 = 1200 #intial concentration (nM) of NO2 after rapid total conversion of NO3 by NAR
X0 = np.array([0,0,0]) #array of starting conditions
R = np.array([45,10,5,0]) # array of rates for each step
t = np.linspace(tmin, tmax, num=641) # vector of minutes

#functions

def NO2_of_t (t):
  isum = 0
  for dt, conc in zip(add_time,add_conc):
    isum += step(t-dt)*conc*np.exp(-R[0]*(t-dt))
  return isum
  
def step(x):
  return 1*(x>0)
  
def NOcell_of_t (X,t):
  dNOcell_dt = R[0]*NO2_of_t(t)+X[1]*R[1]-X[1]*R[2]
  return dNOcell_dt
  
def NOenv_of_t (X,t):
  dNOenv_dt = X[1]*R[2]-X[0]*R[1]

def N2O_of_t (X,t):
  dN2O_dt = R[3]*X[1]
  return dN2O_dt
  
def dX_dt (X,t):
  return np.array([NOcell_of_t (X,t), NOenv_of_t (X,t), N2O_of_t (X,t)])

X, infodict = integrate.odeint(dX_dt,X0,t,full_output=True);
print(infodict['message'])
print(X)

plt.figure(1)
plt.plot(t,NO2_of_t(t))
plt.xlabel("Time")
plt.ylabel("NO2 concentration")
p.savefig('NO2.png', bbox_inches='tight')


plt.clf()
plt.plot(t,X.T[0],'r')
plt.xlabel("Time (min)")
plt.ylabel("NOcell")
p.savefig('NOcell.png', bbox_inches='tight')

plt.clf()
plt.plot(t,X.T[1],'b')
plt.xlabel("Time (min)")
plt.ylabel("NOenv")
p.savefig('NOenv.png', bbox_inches='tight')

plt.clf()
plt.plot(t,X.T[2],'g')
plt.plot(t,X.T[1],'r')
plt.plot(t,X.T[0],'b')
plt.xlabel("Time (min)")
plt.ylabel("Concentration")
p.savefig('All.png', bbox_inches='tight')
