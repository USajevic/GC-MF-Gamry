import matplotlib.pyplot as plt
import os
import seaborn as sns




tEIS = {}                       #EIS universal time dictionary
dEIS = {}                       #EIS data disctionary
tCA = {}                        #CA universal time...
dCA = {}
tCV = {}
dCV = {}
tMF = {}
dMF = {}
tGC = {}
dGCA = {}
dGCB =  {}









for file in os.listdir():                           #Reads all data files, puts all data in disctionaries
    if file.endswith('.dta'):
        with open(file, 'r') as f:
            if file.startswith('EIS'):
                c = f.readlines()
                a = c[4].split('\t')[2].split(':')
                tEIS['{}'.format(file)] = int(int(a[2]) + int(a[1])*60 + int(a[0])* 3600)     
                b = c[54:]                                                            #EIS data starts at line 54
                t = [[] for _ in range(0,11)]
                for i in range(len(b)):
                    a1 = b[i].split('\t')
                    for k in range(1,11):
                        t[k].append(float(a1[k]))                   #0-empty, 1-Pt, 2-Time, 3-Freq, 4-Zreal, 5-Zimag
                dEIS['{}'.format(file)] = t                         #6-Zsig, 7-Zmod, 8-Zphz, 9-Idc, 10-Vdc, 11-IERange
            elif file.startswith('CA'):
                c = f.readlines()
                a = c[4].split('\t')[2].split(':')
                tCA['{}'.format(file)] = int(int(a[2]) + int(a[1])*60 + int(a[0])* 3600)
                b = c[61:]                                                            #CA data starts at line 61
                t = [[] for _ in range(0,9)]
                for i in range(len(b)):
                    a1 = b[i].split('\t')
                    a1[2] = float(a1[2])
                    if a1[2].is_integer() == True:                  #Makes sure it only takes 1 measurement per second
                        for k in range(1,9):
                            t[k].append(float(a1[k]))                   #0-empty, 1-Pt, 2-Time, 3-Vf, 4-Im, 5-Vu
                dCA['{}'.format(file)] = t                          #6-Sig, 7-Ach, 8-IERange, 9-Over
            elif file.startswith('CV'):         #CV
                c = f.readlines()
                a = c[4].split('\t')[2].split(':')
                tCV['{}'.format(file)] = int(int(a[2]) + int(a[1])*60 + int(a[0])* 3600)               
                b = c[60:]                                                            #CV data starts at line 60
                t = [[] for _ in range(0,9)]
                for i in range(len(b)):                             #0-empty, 1-Pt, 2-Time, 3-Vf, 4-Im, 5-Vu
                    a1 = b[i].split('\t')                           #6-Sig, 7-Ach, 8-IERange, 9-Over
                    for k in range(1,9):
                        if b[i][1] != 'U' and b[i][1] != 'P' and b[i][1] != '#':
                            t[k].append(float(a1[k]))
                        else:
                            t[k].append(0)
                dCV['{}'.format(file)] = t
    if file.startswith('plotdata'):             #MF 
        with open(file, 'r') as f:
            c = f.readlines()[0:]                                                      #MF data starts instantly
            tMF['{}'.format(file)] = int(int(f.name[21:23]) + int(f.name[19:21]) * 60 + int(f.name[17:19]) * 3600)            
            t = [[] for _ in range(0,5)]
            for i in range(len(c)):
                a1  = c[i].split(';')                               
                for k in range(0,5):                                #0-time, 1-current flow all else- IDK?
                    t[k].append(float(a1[k]))                   
            dMF['{}'.format(file)] = t 
 
    if file.endswith('.TX0'):
        with open(file, 'r') as f:
            c = f.readlines()            
            a = c[1].split(',')
            tGC['{}'.format(file)] = int(int(a[3][11:13])*3600 + int(a[3][14:16])*60 + int(a[3][17:19]))
            if f.name[33] == 'B':    
                for i in range(26,40):                                   #GC data starts at 26 and ends in dynamic line
                    if c[i][0:5] == '"",""' and c[i+1][0:5] == '"",""':
                        t = [[] for _ in range(0,8)]
                        for m in range(26,i):
                            a1 = c[m].split(',')
                            for k in [0,1,2,3,4,5,7]:
                                t[k].append(a1[k])         
                        dGCB['{}'.format(file)] = t                                       
            if f.name[33] == 'A':
                for i in range(26,35):
                    if c[i][0:5] == '"",""' and c[i + 1][0:5] == '"",""':
                        t = [[] for _ in range(0,8)]
                        for m in range(26,i):
                            a1 = c[m].split(',')
                            for k in range(0,8):
                                t[k].append(a1[k])                  
                        dGCA['{}'.format(file)] = t  
 
                
 
    
 
"""                                                 #Comment regarding data dictionary shapes

All the data is now stored in dictionaries that consist of these shapes:

{Key : [[],[],[],[]]}    --> Values in dictionaries are arrays, each one parameter of one experiment

dXX (Data dictionary):

dEIS =
{'EISafter1point5.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.549097, 3.571528], [-1.12172, -0.978192], [1.0, 1.0], [3.722142, 3.703063], [-17.53955, -15.31691], [0.0020687, 0.0013807], [0.0037947, 0.0024488]], 
 'EISafter1point8.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.510433, 3.663148], [-1.09073, -0.6606696], [1.0, 1.0], [3.67598, 3.722249], [-17.26059, -10.22371], [0.0024697, 0.0017374], [0.0013082, 0.003586]], 
 'EISafter2.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.624848, 3.592735], [-0.7191343, -0.613647], [1.0, 1.0], [3.695494, 3.644764], [-11.22122, -9.69271], [0.0023867, 0.0016823], [0.0004637, -0.0001721]], 
 'EISafter2point2.dta': [[], [0.0, 1.0], [4.0, 5.0], [1000078.0, 794390.6], [3.510492, 3.492043], [-0.6629693, -0.5638231], [1.0, 1.0], [3.572546, 3.537268], [-10.69456, -9.171786], [0.0030767, 0.0023714], [-0.0005934, -0.0001875]], 
 'EISstart.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.524591, 3.537423], [-1.070966, -0.9247701], [1.0, 1.0], [3.683709, 3.656304], [-16.9017, -14.65065], [0.0005902, 0.0004666], [0.0017475, 0.0012521]]
 }

tXX (Universal time dictionary):

tEIS = 
{'EISafter1point5.dta': 47019, 
 'EISafter1point8.dta': 49853, 
 'EISafter2.dta': 52682, 
 'EISafter2point2.dta': 56115, 
 'EISstart.dta': 43389
 }

This means we got all the data ready to be called upon with a simple dEIS.values()[i] function, enabling plotting.
"""




# ---------------------------------------------------------------------------------------------
"Creating Results directories"
os.mkdir('Results')
os.mkdir('Results/EIS')
os.mkdir('Results/CV')
os.mkdir('Results/CV_iR')
os.mkdir('Results/CA')

"Plotting EIS data"
fullEIS_fig, fullEIS_ax = plt.subplots()
dEIS_UTvsI = {}
for i, c in zip(range(len(dEIS)), sns.color_palette()):
    partEIS_fig, partEIS_ax = plt.subplots()
    EISstarttime = list(tEIS.values())[i]                       #Obtain universal time
    x = list(dEIS.values())[i][4]                               #Zreal
    y = list(dEIS.values())[i][5]                               #Zimg
    EIScurrent = list(dEIS.values())[i][9]                      #Idc
    EIStime = list(dEIS.values())[i][2]                         #Time
    for ii in range(len(EIScurrent)):                                   #Creates a dictionary that takes a form:
        EIStime[ii] = EIStime[ii] + EISstarttime                        # dict = {key = universal time : value = Idc}
        dEIS_UTvsI[EIStime[ii]] = EIScurrent[ii]        
    name = str(list(dEIS)[i]).replace('.dta', '')
    name = str(name.replace('point', '.'))
    fullEIS_ax.scatter(x,y, color = c, s = 5, label = str(name))    
    partEIS_ax.scatter(x,y, color = c, s = 10)    
    partEIS_ax.invert_yaxis()
    fullEIS_ax.invert_yaxis()
    partEIS_ax.set_xlabel('Zreal [ohm]')
    partEIS_ax.set_ylabel('-Zimag [ohm]')    
    partEIS_ax.set_title(name)
    partEIS_fig.savefig('Results/EIS/' + str(name) + '.png')
fullEIS_ax.legend(fontsize = 'small')
fullEIS_ax.set_xlabel('Zreal [ohm]')
fullEIS_ax.set_ylabel('-Zimag [ohm]')
fullEIS_ax.set_title("All EIS signals")
fullEIS_fig.savefig('Results/EIS/Combined EIS´s.png')


"Plotting non-iR compensated CV´s"
fullCV_fig, fullCV_ax = plt.subplots()
for i, c in zip(range(len(dCV)), sns.color_palette()):
    partCV_fig, partCV_ax = plt.subplots()
    y = []
    x = []
    x1 = list(dCV.values())[i][3]
    y1 = list(dCV.values())[i][4]
    name = str(list(dCV)[i]).replace('.dta', '')
    name = str(name.replace('point', '.'))   
    for i in range(len(x1)):
        if x1[i] != 0:
            x.append(x1[i])
            y.append(y1[i])
    fullCV_ax.scatter(x,y, color = c, s = 0.01, label = str(name))    
    partCV_ax.scatter(x,y, color = c, s = 0.1)    
    partCV_ax.set_xlabel('U vs. Ag/AgCl [V]')
    partCV_ax.set_ylabel('I [A]')    
    partCV_ax.set_title(name)
    partCV_fig.savefig('Results/CV/' + str(name) + '.png')
fullCV_ax.legend(fontsize = 'small', markerscale = 20)
fullCV_ax.set_xlabel('U vs. Ag/AgCl [V]')
fullCV_ax.set_ylabel('I [A]')
fullCV_ax.set_title("All CV´s")
fullCV_fig.savefig('Results/CV/Combined CV´s.png')




"Plotting iR compensated CV´s"
fullCViR_fig, fullCViR_ax = plt.subplots()
dCV_UTvsI = {}
dCV_UTvsU = {}
for i, c in zip(range(len(dCV)), sns.color_palette()):
    partCViR_fig, partCViR_ax = plt.subplots()
    y = []
    x = []
    x1 = list(dCV.values())[i][3]
    y1 = list(dCV.values())[i][4]
    name = str(list(dCV)[i]).replace('.dta', '')
    name = str(name.replace('point', '.'))
    R = 0
    a1 = list(tEIS.values())[i]
    if list(tCV.values())[i] - a1 <= 600: #If EIS was done atleast 10min before CV, compensate for resistance, else not
        R = list(dEIS.values())[i][4][list(dEIS.values())[i][5].index(max(list(dEIS.values())[i][5]))]                       
    for i in range(len(x1)):
        if x1[i] != 0:
            x.append(x1[i])
            y.append(y1[i])
    for i in range(len(x)):
        x[i] = x[i] - y[i] * R        
    fullCViR_ax.scatter(x,y, color = c, s = 0.01, label = str(name))    
    partCViR_ax.scatter(x,y, color = c, s = 0.1)    
    partCViR_ax.set_xlabel('U vs. Ag/AgCl [V]')
    partCViR_ax.set_ylabel('I [A]')    
    partCViR_ax.set_title(name)
    partCViR_fig.savefig('Results/CV_iR/' + str(name) + '.png')
fullCViR_ax.legend(fontsize = 'small', markerscale = 20)
fullCViR_ax.set_xlabel('U vs. Ag/AgCl [V]')
fullCViR_ax.set_ylabel('I [A]')
fullCViR_ax.set_title("All CV´s")
fullCViR_fig.savefig('Results/CV_iR/Combined CV´s.png')




"Plotting CA data"
fullCA_fig, fullCA_ax = plt.subplots()
amin = []
amax = []
for i, c in zip(range(len(dCA)), sns.color_palette()):
    partCA_fig, partCA_ax = plt.subplots()
    x = list(dCA.values())[i][2]
    y = list(dCA.values())[i][4]
    name = str(list(dCA)[i]).replace('.dta', '')
    name = str(name.replace('point', '.'))
    fullCA_ax.scatter(x[5:],y[5:], color = c, s = 3, label = str(name))    
    partCA_ax.scatter(x[5:],y[5:], color = c, s = 2)
    partCA_ax.set_ylim([max(y[5:])*0.90,min(y[5:]) *1.10]) 
    amin.append(min(y[5:]))
    amax.append(max(y[5:]))
    partCA_ax.set_xlabel('Time [s]')
    partCA_ax.set_ylabel('Current [A]')    
    partCA_ax.set_title(name)
    partCA_fig.savefig('Results/CA/' + str(name) + '.png')
fullCA_ax.set_ylim((max(amax))*0.90, min(amin)*1.1)
fullCA_ax.legend(fontsize = 'small')
fullCA_ax.set_xlabel('Time [s]')
fullCA_ax.set_ylabel('Current [A]')
fullCA_ax.set_title("All CA signals")
fullCA_fig.savefig('Results/CA/Combined CA´s.png')

#----------------------------------------------------------------------------------------
"""          
"Links MF flow to universal time"
UnivMF = {}
for i in range(len(tMF)):
    MFflow = list(dMF.values())[i][1]
    
    MFstarttime = float(list(tMF.values())[i])
    
    MFtime = list(dMF.values())[i][0]                               
    for k in range(len(MFtime)):
        MFtime[k] = round((MFtime[k] + MFstarttime), 0)
    
for i in range(len(MFtime)):
    UnivMF[MFtime[i]] = MFflow[i]                   
    
print(dCA)    
    
UnivCA = {}
for i in range(len(tCA)):
    print(i)
    CAcurrent = list(dCA.values())[i][4]
    print(CAcurrent)
    
    CAstarttime = float(list(tCA.values())[i])
    
    CAtime = list(dCA.values())[i][2]
    for k in range(len(CAtime)):
        CAtime[k] = round((CAtime[k] + CAstarttime),0)
        
    print(CAtime)
"""
"""
F = 96485
GF1 = 1.2  # gas flow factor for Ar -------------------- CHANGE  TO 1 IF USING CO2

nETH = 6     # number of electrons
nMET = 10    # number of electrons
nCO =  2     # number of electrons
nHYD = 2     # number of electrons

cETH = 0.0003701        #calibration factor Ethylene
cHYD = 0.00680013       #calibration factor Hydrogen
cMET = 0.00068207       #calibration factor Methanol
cCO  = 0.00069638       #calibration factor Carbon monoxide


"GCA"
a1 = []                 #4.75-5
a2 = []                 #5.15 - 5.90
a3 = []                 #9.85 - 10.40
a4 = []                 #10.8 - 11.4
a5 = []
"""
