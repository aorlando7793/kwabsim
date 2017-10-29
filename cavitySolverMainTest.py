import cavitySolverMain as csm


LAM = 1064*10**(-7)
M2 = 1
n=1

cfile = 'datatest.dat'

cavity = csm.getCavity(csm.getStringCav(cfile))

print(csm.check_stab(csm.get_RTM(cavity)))

actions = csm.check_actions(cavity)
#print(actions)

if ((actions[0] + actions[1]) > 0):
    cavities = csm.split_cavity(cavity)
    csm.plot_xy(cavities,LAM,100)
    
else:
    print('woops')

