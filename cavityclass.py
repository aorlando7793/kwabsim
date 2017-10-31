import numpy as np
import math
import matplotlib.pyplot as plt


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
    #We'll need this to determine is a string represents a paramter or 
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
# Cavity Class
class Cavity(object):

    def __init__(self, cavity_file, lam):
        self.cavity_file = cavity_file
        self.scavity = self.getStringCav()
        self.cavity = self.getCavity()
        self.lam = lam
        self.rtm = self.get_RTM()
        if self.check_stab():
            self.q0 = self.get_q0()
            print('Cavity is Stable!!!!')
        else:
            print('Cavity is Unstable :(')




    #=========================================
    #Interpretting cavity files

    def getStringCav(self):
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

    


    def getCavity(self):
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
        free_space = [optic for optic in self.cavity if optic[0] == 'D'] 
        q = self.q0
        d = 0
        for optic in self.cavity:
            if optic[0] == 'D':
                d += optic[1]

            if d > z:
                break
            else:
                q = self.prop_q0(q, optics[optic[0]](optic[1]))
                continue
        q += z - d
        return q

    


ds28 = Cavity('datatest.dat', 1064*10**(-7))

print('q at start is:', ds28.q0)

print('q at 20cm is:', ds28.q(20))

q20 = ds28.q(20)

zo = q20.real
zr = q20.imag

waist = np.sqrt((4*ds28.lam/math.pi)*(zr + ((zo)**2)/zr))
print ('waist  at 20cm is', waist)