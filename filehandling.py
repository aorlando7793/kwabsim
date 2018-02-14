import os
import pickle

#Get the current working directory.
cwd = os.getcwd()
#Get 'Cavities' folder.
cavities = os.path.join(cwd,'Cavities')

if __name__ == "__main__":
	#Check if Cavities folder exists. If not, make it.
	if not os.path.exists(cavities_folder):
		os.makedirs(cavities_folder)


filename = input('If this is the file you would like to use press ENTER.  If not, please enter a file name:	 ')
if filename == '':
	#Use whatever file is in current cavity.
	pass
else:
	#Create path to file name in 'Cavities' folder.
	filepath = os.path.join(cavities, filename)
	#Save path name to 'filepath.pkl'
	with open('filepath.pkl', 'wb') as f:
		pickle.dump(filepath, f)