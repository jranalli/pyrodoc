#!/usr/bin/python
#
#   Isobar plot generator

import matplotlib as mpl
# It is vital to set the matplotlib interface to one without a display
# BEFORE loading pyplot!  This makes things work behind Apache.
mpl.use('Agg')
import matplotlib.pyplot as plt
import pmcgi
import pyromat as pm
import numpy as np
import sys


print("Content-type: image/png")
print("")


species, p1, p2, up, uT, uE, uM, uV = pmcgi.argparse([
        ('id'), 
        ('p1',float), 
        ('p2',float),
        ('up'),
        ('uT'),
        ('uE'),
        ('uM'),
        ('uV') ])


this = pm.get(species)

# Calculate the states
F = pm.get(species)

# The condenser exit will be on the dome
T1 = F.Ts(p1)           # Saturation temperature
d1,_ = F.ds(T=T1)       # Saturation density (faster by temperature)
s1,_ = F.ss(T=T1)       # Saturation entropy
h1,_ = F.hs(T=T1)       # Saturation enthalpy

# The feed pump exit will be isentropic
s2 = s1
T2 = F.T_s(s=s2, p=p2)
h2 = F.h(T2,p2)
d2 = F.d(T2,p2)

# The boiler exit will be on the dome and isobaric
p3 = p2
T3 = F.Ts(p=p3)
_,s3 = F.ss(T=T3)       # Saturation entropy
_,h3 = F.hs(T=T3)       # Saturaiton enthalpy
_,d3 = F.ds(T=T3)       # Saturation density

# The piston exit wll be isentropic and at the condenser pressure
p4 = p1
s4 = s3
T4,x4 = F.T_s(s=s3, p=p4, quality=True)
h4 = F.h(T=T4,x=x4)
d4 = F.d(T=T4,x=x4)

# Build the T-s plot

f = plt.figure()
ax = f.add_subplot(111)

# 1-2
p = np.linspace(p1,p2,20)
T = F.T_s(s=s1, p=p)
s = s1 * np.ones_like(p,dtype=float)
ax.plot(s,T,lw=2,color='r')

# 2-3
s = np.linspace(s2,s3,50)
T = F.T_s(s=s, p=p2)
ax.plot(s,T,lw=2,color='r')

# 3-4
p = np.linspace(p3,p4,20)
T = F.T_s(s=s3,p=p)
s = s3 * np.ones_like(p,dtype=float)
ax.plot(s,T,lw=2,color='r')

# 4-1
s = np.linspace(s4,s1,50)
T = F.T_s(s,p=p1)
ax.plot(s,T,lw=2,color='r')

# Dress up the plot
ax.set_xlabel('Entropy (' + uE + '/' + uM + uT + ')')
ax.set_ylabel('Temperature (' + uT + ')')
ax.grid('on')

# Instead of saving to a file, write directly to stdout!
f.savefig(sys.stdout, format='png')