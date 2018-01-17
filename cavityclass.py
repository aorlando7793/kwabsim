import numpy as np
import math
import matplotlib.pyplot as plt

#======================================================
#Define preliminary functions that are not contained in the Cavity class.

#Ray Trace Matricies
#================================================

#Free Space
def m_freeSpace(dist):
    #|1 d|
    #|0 1|
    return np.array([[1,dist],[0,1]])

#Lens
def m_lens(f):
    #|1    0|
    #|-1/f 1|
    if(f==0):
        return np.array([[1,0],[0,1]])
    return np.array([[1,0],[-1/f,1]])

#Mirror
def m_mirror(roc):
    #|1     0|
    #|-2/f  1|
    return m_lens(roc/2)

#Brewster Surface
def m_brewster(n):
    #|1    0|
    #|0    k|
    theta_I = np.arctan(1/n)
    theta_R = np.arcsin((1/n)*np.sin(theta_I))
    k = np.cos(theta_I)/np.cos(theta_R)
    return np.array([[1, 0],[0, k]])

def m_brewster_inv(n):
    theta_I = np.arctan(1/n)
    theta_R = np.arcsin((1/n)*np.sin(theta_I))
    k = np.cos(theta_I)/np.cos(theta_R)
    return np.array([[1, 0],[0, 1/k]])
#===================================================
#Dictionary of optics that corrrespond to their respective ray trace matrices

optics = {
    'D':m_freeSpace,
    'L':m_lens,
    'M':m_mirror,
    'Cx':m_lens,
    'Cy':m_lens,
    'B':m_brewster,
    'B_inv':m_brewster_inv
}

#======================================================
#Cavity Class:

class Cavity(object):

    def __init__(self, cavity_input, lam):
        if isinstance(cavity_input, list):
            self.cavity = cavity_input
        else:
            self.cavity_file = open(cavity_input, 'r+')
            #self.scavity = self.get_string_cav()
            self.cavity = self.get_cavity()
            #print(self.cavity)
        self.lam = lam
        self.rtm = self.get_RTM()
        if self.check_stab():
            self.is_stable = True
            self.q0 = self.get_q0()
            self.L = self.L()
            #print('Cavity is Stable!!!!')
        else:
            self.is_stable = False
            print('Cavity is Unstable :(')

    #=========================================
    #Interpretting cavity files:

    def get_cavity(self):
        cavity = []
        for line in self.cavity_file:
            part = []
            for s in line.split():
                try:
                    part.append(float(s))
                except ValueError:
                    part.append(s)
            cavity.append(part)
        return cavity

    #==================================================================
    # Class Methods:

    def unfold_Cav(self):
        return self.cavity[0:]+list(reversed(self.cavity))[1:-1]

    def get_RTM(self):
        cavity = self.unfold_Cav()
        rtm = np.array([[1,0],[0,1]])
        second_pass = False
        for optic in cavity:
            if optic[0] == 'B' and not second_pass:
                second_pass = True
                m = optics[optic[0]](optic[1])
            elif optic[0] == 'B' and second_pass:
                m = optics['B_inv'](optic[1])
            else:
                m = optics[optic[0]](optic[1])
            rtm = np.dot(m,rtm)
        return rtm


    def check_stab(self):
        x = (self.rtm[0][0]+self.rtm[1][1]+2)/4.0
        if((x>0) & (x<1)):
            return True
        return False

    def get_q0(self):
        rtm = self.rtm
        a,b,c,d =[rtm[0][0],rtm[0][1],rtm[1][0],rtm[1][1]]
        rover1 = (d-a)/(2*b)
        w2 = ((self.lam/math.pi)*abs(b)/(math.sqrt(1 - ((a+d)/2)**2)))
        #print(w2*math.pi/(1064*10**(-7)))
        q0 = 1/(rover1 - (self.lam/(math.pi*w2))*1j)
        q0 = q0.real + q0.imag*1j
        return q0

    def prop_q0(self,q0,rtm):
        a,b,c,d =[rtm[0][0],rtm[0][1],rtm[1][0],rtm[1][1]]
        q = (q0*a + b)/(q0*c + d)
        return q

    def q(self, z): 
        q = self.q0
        d = 0 #running cumulative distance of free space elements
        for optic in self.cavity:
            if optic[0] == 'D' and ((z - d) > optic[1]):
                q = self.prop_q0(q, optics[optic[0]](optic[1]))
                d += optic[1]
            elif optic[0] != 'D':
                q = self.prop_q0(q, optics[optic[0]](optic[1]))
            else:
                break
        q += z - d
        return q

    def waist(self, z):
        z0 = self.q(z).real
        zR = self.q(z).imag
        waist = np.sqrt((4*self.lam/math.pi)*(zR + ((z0)**2)/zR))
        return waist

    def plot_waist(self, n_points):
        Z = np.linspace(0,self.L,num=n_points)
        W = [self.waist(z) for z in Z]
        return Z, W

    def insert_optic(self, optic, par, pos):
        #Inserts ['optic',par] as the pos'th position in [cavity]
        cav1 = self.cavity[:pos-1]
        cav2 = self.cavity[pos-1:]
        new_cavity = cav1 + [[optic,par]]+ cav2        
        return Cavity(new_cavity,self.lam)

    def remove_optic(self, pos):
        #Removes pos'th optic
        new_cavity = self.cavity[:pos-1]+self.cavity[pos:]
        return Cavity(new_cavity, self.lam)

    def get_xcav(self):
        xcav = self
        i = 0
        off = 1
        while(i<len(self.cavity)):
            if self.cavity[i][0] == 'Cy':
                xcav = xcav.remove_optic(i+off)
                off += -1
            i += 1
        return Cavity(xcav.cavity, self.lam)

    def get_ycav(self):
        ycav = self
        i = 0
        off = 1
        while(i<len(self.cavity)):
            if self.cavity[i][0] == 'Cx':
                ycav = ycav.remove_optic(i+off)
                off += -1
            elif self.cavity[i][0] == 'B':
                ycav = ycav.remove_optic(i+off)
                off += -1
            i += 1
        return Cavity(ycav.cavity, self.lam)

    def L(self):
        space = [optic[1] for optic in self.cavity if optic[0] == 'D']
        return sum(space)

    def div(self, z):
    	h = .01
    	if z < h:
    		d = (self.waist(z+h) - self.waist(z))/h
    	elif z > (self.L - h):
    		d = (self.waist(z) - self.waist(z-h))/h
    	else:
    		d = (self.waist(z+h) - self.waist(z-h))/(2*h)
    	return d


if __name__ == "__main__":
	M_2 = 1
	LAM = 1064*10**(-7) * M_2

	cav_parts = [['M',100],['D',21],['M',-70],['D',3.5],['L',17],['D', 3.5],['M', -100],['D',19],['B',1.5],['D',5],['M',0]]
	laser = Cavity(cav_parts, LAM)
	
	#test spot size plot
	Z, W = laser.plot_waist(200)
	plt.plot(Z,W)
	plt.show()

	#test divergence plot
	D = [laser.div(z) for z in Z]
	plt.plot(Z,D)
	plt.show()
