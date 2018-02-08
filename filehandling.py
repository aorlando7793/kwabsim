import os

cwd = os.getcwd()

cavities_folder = os.path.join(cwd,'Cavities')

#Check if Cavities folder exists. If not, make it.
if not os.path.exists(cavities_folder):
    os.makedirs(cavities_folder)

current_cavity = os.path.join(cwd, 'Current Cavity')

#check if Current Cavity folder exists. If not, make it.
if not os.path.exists(current_cavity):
    os.makedirs(current_cavity)

#list all files in directory. There should only ever be one file in this directory, but this is the only way I could figure out 
#how to access it
current_cavity_file = os.listdir(current_cavity)[0]

#Lets user know which file is current cavity. If that file is correct then the user can proceed with the program.  If its incorrect
#then user can enter cavity file they want to use and it will then be fetched from Cavities folder
print('Current Cavity File is:  ', current_cavity_file)
s = input('If this is the file you would like to use press ENTER.  If not, please enter a file name:  ')
if s == '':
    #use whatever file is in current cavity
    filepath = os.path.join(current_cavity, current_cavity_file)
else:
    #create file path for cavity file in Cavites folder that matches user input
    old_filepath = os.path.join(cavities_folder, s)
    #move that file to current cavity
    os.rename(old_filepath, os.path.join(current_cavity, s))
    #then creatte file path for new cavity destination
    filepath = os.path.join(current_cavity, s)
    #create file path for what was in current cavity originally and move it into Cavities folder
    old_cav_path = os.path.join(current_cavity, current_cavity_file) 
    os.rename(old_cav_path, os.path.join(cavities_folder, current_cavity_file))