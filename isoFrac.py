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
