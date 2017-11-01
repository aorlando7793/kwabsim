import numpy as np
import math
import matplotlib.pyplot as plt

#======================================================
#Define preliminary functions that are not contained in the Cavity class.

def is_number(s):
	try:
		float(s)
		return True
	except ValueError:
		return False
	#We'll need this to determine if a string represents a paramter or 
	# not

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

#===================================================

optics = {
	'D':m_freeSpace,
	'L':m_lens,
	'M':m_mirror,
	'Cx':m_lens,
	'Cy':m_lens
}

#======================================================
#Cavity Class:

class Cavity(object):

	def __init__(self, cavity_file, lam):
		self.cavity_file = cavity_file
		self.scavity = self.get_string_cav()
		self.cavity = self.get_cavity()
		self.lam = lam
		self.rtm = self.get_RTM()
		if self.check_stab():
			self.q0 = self.get_q0()
			print('Cavity is Stable!!!!')
		else:
			print('Cavity is Unstable :(')




	#=========================================
	#Interpretting cavity files:

	def get_string_cav(self):
		cfile = open(self.cavity_file,'r+')
		scavity = cfile.readline()

		if(scavity[-1:]=='\n'):
			scavity = scavity[:-1]
			#Removes line break in case there is one
		while(scavity[-1]==' '):
			scavity = scavity[:-1]
			#Removes spaces at the end. Having one can cause us to 
			#never add the last optic/paramter pair

		return scavity
	# get the first line of a file. Presumabley we're not idiots and 
	# load the file with the cavity inside

	def get_cavity(self):
		scavity = self.scavity
		cavity = []
		subcav = []
		# initialize cavity. add components with .append()

		skip = 0
		end = False #Indicates if we've reached the end
		
		for i in np.array(range(0,len(scavity))):
			#scanning individual characters

			if(scavity[i] == ' '):
				continue
				#ignore spaces

			if(skip > 0):
				#we wish to skip over elements already accounted for
				skip = skip -1 
				continue

			length = 0 #this will be how many characters it take to
			#reach a space
			while(scavity[i+length] != ' '):
				#Increase length until i+length gets a space
				#We must also check to see if we're at the end of the
				#line
				length = length + 1 
				if(i+length == len(scavity)):
					end = True
					break
					
			#Now scavity[i:i+length] is a block of strings between 2 ' '
			if(is_number(scavity[i:i+length])):
				subcav.append(float(scavity[i:i+length]))
				#submit a block of numbers to subcavity.

				if(end==True):
					cavity.append(subcav)
					#If we're at the last parameter, this will trigger
					#the last dump

			else:
				#This block contains letter(s)
				#We need to dump everything subcav has to cavity before 
				#appending subcav and then reset it

				cavity.append(subcav)
				subcav = []
				subcav.append(scavity[i:i+length])
				
			skip = length - 1 
			# set skip to 
			# continue over the rest of the characters
			# Example: We don't want 1.03 to give [1.03,.03,03,3]
			# skip = 3 will assure we read only the first 
			
		return cavity[1:]
	#==================================================================
	# Class Methods:

	def get_RTM(self):
		cavity = self.unfold_Cav()
		rtm = np.array([[1,0],[0,1]])
		for optic in list(reversed(cavity)):
			m = optics[optic[0]](optic[1])
			rtm = np.dot(rtm,m)
		return rtm

	def unfold_Cav(self):
		return self.cavity[0:-1]+list(reversed(self.cavity))[0:-1]

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
		#free_space = [optic for optic in self.cavity if optic[0] == 'D'] 
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

	def plot_waist(self, cavity, n_points):
		ds = [optic[1] for optic in self.cavity if optic[0] == 'D']
		L = sum(ds)
		Z = np.linspace(0,L,num=n_points)
		W = [ds28.waist(z) for z in Z]
		plt.plot(Z,W)
		return plt.show()

	def insert_optic(self, optic, par, pos):
		#Inserts ['optic',par] as the pos'th position in [cavity]
		cav1 = self.cavity[:pos]
		cav2 = self.cavity[pos:]
		return cav1 + [[optic,par]]+ cav2

	#def multiply_optic(pos,start,stop,step,cavity):
		# Add ['X',start,stop,step] after the pos'th optic in [cavity]
		#return cavity[:pos+1] + [['X',start,stop,step]] + cavity[pos+1:]

	def remove_optic(self, pos):
		#Removes pos'th optic
		return self.cavity[:pos]+self.cavity[pos+1:]

	def get_x_cav(self):
		x_cav = self.cavity
		i = 0
		off = 0
		while(i<len(self.cavity)):
			if self.cavity[i][0] == 'Cy':
				x_cav = self.remove_optic(i+off)
				off += -1
			elif self.cavity[i][0] == 'B':
				x_cav = self.remove_optic(i+off)
				off += -1
			i += 1
		self.x_cav = x_cav
		return

	def get_y_cav(self):
		y_cav = self.cavity
		i = 0
		off = 0
		while(i<len(self.cavity)):
			if self.cavity[i][0] == 'Cx':
				y_cav = self.remove_optic(i+off)
				off += -1
			i += 1
		self.y_cav = y_cav
		return

	def plot_waist_XY(self, n_points):
		self.get_x_cav()
		self.get_y_cav()
		if self.x_cav == self.y_cav:




	


ds28 = Cavity('datatest.dat', 1064*10**(-7))

print('q at start is:', ds28.q0)

print('q at 50cm is:', ds28.q(50))

print ('waist  at 50cm is', ds28.waist(50))



