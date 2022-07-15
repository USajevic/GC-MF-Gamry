import matplotlib.pyplot as plt
import os
import seaborn as sns
from tabulate import tabulate
import xlsxwriter




tEIS = {}                       #EIS universal time dictionary
dEIS = {}                       #EIS data disctionary
tCA = {}                        #CA universal time...
dCA = {}
tCV = {}
dCV = {}
tCP = {}
dCP = {}
tMF = {}
dMF = {}
tGC = {}
dGCA = {}
dGCB =  {}

dEIS_UTvsI = {}
dCV_UTvsI = {}
dCV_UTvsU = {}
dCA_UTvsI = {}
dCA_UTvsU = {}
dCP_UTvsI = {}
dCP_UTvsU = {}
    
for file in os.listdir():                           #Reads all data files, puts all data in disctionaries
    if file.endswith('.DTA'):
        with open(file, 'r') as f:
            if file.startswith('EIS'):          #Electrochemical Impedance spectroscopy
                c = f.readlines()
                a = c[4].split('\t')[2].split(':')
                a2 = c[3].split('\t')[2].split('/')
                tEIS['{}'.format(file)] = int(int(a[2]) + int(a[1])*60 + int(a[0])* 3600 +int(int(a2[1]) * 86400))   
                for iii in range(len(c)-1):
                    if c[iii][0:6] == 'ZCURVE':
                        s1 = iii + 3
                b = c[s1:]                                                                          #EIS data starts at line 54
                t = [[] for _ in range(0,11)]
                for i in range(len(b)):
                    a1 = b[i].split('\t')
                    for k in range(1,11):
                        t[k].append(float(a1[k]))                   #0-empty, 1-Pt, 2-Time, 3-Freq, 4-Zreal, 5-Zimag
                dEIS['{}'.format(file)] = t                         #6-Zsig, 7-Zmod, 8-Zphz, 9-Idc, 10-Vdc, 11-IERange
            elif file.startswith('CA'):         #Chronoamperommetry
                c = f.readlines()
                a = c[4].split('\t')[2].split(':')
                a2 = c[3].split('\t')[2].split('/')
                tCA['{}'.format(file)] = int(int(a[2]) + int(a[1])*60 + int(a[0])* 3600 + int(int(a2[1]) * 86400))
                for iii in range(len(c)-1):
                    if c[iii][0:5] == 'CURVE':
                        s1 = iii + 3
                b = c[s1:]                                                          #CA data starts at line 61
                t = [[] for _ in range(0,9)]
                for i in range(len(b)):
                    a1 = b[i].split('\t')                   
                    for k in range(1,9):
                        t[k].append(float(a1[k]))               #0-empty, 1-Pt, 2-Time, 3-Vf, 4-Im, 5-Vu
                dCA['{}'.format(file)] = t                          #6-Sig, 7-Ach, 8-IERange, 9-Over
            elif file.startswith('CV'):         #Cyclic voltammetry
                c = f.readlines()
                a = c[4].split('\t')[2].split(':')
                a2 = c[3].split('\t')[2].split('/')
                tCV['{}'.format(file)] = int(int(a[2]) + int(a[1])*60 + int(a[0])* 3600 + int(int(a2[1]) * 86400))
                for iii in range(len(c)-1):
                    if c[iii][0:6] == 'CURVE1':
                        s1 = iii + 3
                b = c[s1:]                                                               
                t = [[] for _ in range(0,9)]
                for i in range(len(b)-1):                             #0-empty, 1-Pt, 2-Time, 3-Vf, 4-Im, 5-Vu
                    a1 = b[i].split('\t')                           #6-Sig, 7-Ach, 8-IERange, 9-Over
                    for k in range(1,9):
                        if b[i][1] != 'U' and b[i][1] != 'P' and b[i][1] != '#':
                            t[k].append(float(a1[k]))
                        else:
                            t[k].append(0)
                dCV['{}'.format(file)] = t
            elif file.startswith('CP'):         #Chronopotentiommetry
                c = f.readlines()
                a = c[4].split('\t')[2].split(':')
                a2 = c[3].split('\t')[2].split('/')
                tCP['{}'.format(file)] = int(int(a[2]) + int(a[1])*60 + int(a[0])* 3600 + int(int(a2[1]) * 86400))
                for iii in range(len(c)-1):
                    if c[iii][0:5] == 'CURVE':
                        s1 = iii + 3
                b = c[s1:]                                      #CP data starts at line 64
                t = [[] for _ in range(0,9)]
                for i in range(len(b)):
                    a1 = b[i].split('\t')
                    for k in range(1,9):
                        t[k].append(float(a1[k]))               #0-empty, 1-Pt, 2-Time, 3-Vf, 4-Im, 5-Vu
                dCP['{}'.format(file)] = t                          #6-Sig, 7-Ach, 8-IERange, 9-Over
    if file.startswith('plotdata'):             #Mass flow
        with open(file, 'r') as f:
            c = f.readlines()[0:]                                                      #MF data starts instantly
            tMF['{}'.format(file)] = int(int(f.name[21:23]) + int(f.name[19:21]) * 60 + int(f.name[17:19]) * 3600 + int(int(f.name[15:17])) * 86400)            
            t = [[] for _ in range(0,5)]
            for i in range(len(c)-1):
                a1  = c[i].split(';')                               
                for k in range(0,5):                                #0-time, 1-current flow all else- IDK?
                    t[k].append(float(a1[k]))                   
            dMF['{}'.format(file)] = t  
    if file.endswith('.TX0'):                   #Gas chromatography
        with open(file, 'r') as f:
            c = f.readlines()            
            a = c[1].split(',')
            a2 = a[3].split('/')
            tGC['{}'.format(file)] = int(int(a[3][-10:-8])*3600 + int(a[3][-7:-5])*60 + int(a[3][-4:-2]) + int(int(a2[1]) * 86400))
            if str((c[6].split(','))[3][1]) == 'B':
                for i in range(26,40):                                   #GC data starts at 26 and ends in dynamic line
                    if c[i][0:5] == '"",""' and c[i+1][0:5] == '"",""':
                        t = [[] for _ in range(0,8)]
                        for m in range(26,i):
                            a1 = c[m].split(',')
                            for k in [0,1,2,3,4,5,7]:
                                t[k].append(a1[k])         
                        dGCB['{}'.format(file)] = t                                       
            if str((c[6].split(','))[3][1]) == 'A':
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

{Key : [ [], [], [], [] ] }    --> Values in dictionaries are arrays, each one parameter of one experiment

dXX (Data dictionary):

dEIS =
{'EXAMPLE.dta':         [/]  [pt]        [time]      [Frequency]            [Zreal]               [Zimag]                ...     
 'EISafter1point5.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.549097, 3.571528], [-1.12172, -0.978192], [1.0, 1.0], [3.722142, 3.703063], [-17.53955, -15.31691], [0.0020687, 0.0013807], [0.0037947, 0.0024488]], 
 'EISafter1point8.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.510433, 3.663148], [-1.09073, -0.6606696], [1.0, 1.0], [3.67598, 3.722249], [-17.26059, -10.22371], [0.0024697, 0.0017374], [0.0013082, 0.003586]], 
 'EISafter2.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.624848, 3.592735], [-0.7191343, -0.613647], [1.0, 1.0], [3.695494, 3.644764], [-11.22122, -9.69271], [0.0023867, 0.0016823], [0.0004637, -0.0001721]], 
 'EISafter2point2.dta': [[], [0.0, 1.0], [4.0, 5.0], [1000078.0, 794390.6], [3.510492, 3.492043], [-0.6629693, -0.5638231], [1.0, 1.0], [3.572546, 3.537268], [-10.69456, -9.171786], [0.0030767, 0.0023714], [-0.0005934, -0.0001875]], 
 'EISstart.dta': [[], [0.0, 1.0], [3.0, 5.0], [1000078.0, 794390.6], [3.524591, 3.537423], [-1.070966, -0.9247701], [1.0, 1.0], [3.683709, 3.656304], [-16.9017, -14.65065], [0.0005902, 0.0004666], [0.0017475, 0.0012521]]
 }

tXX (Universal time dictionary):

tEIS = 
{'Example.dta'        : EIS start time
 'EISafter1point5.dta': 47019, 
 'EISafter1point8.dta': 49853, 
 'EISafter2.dta': 52682, 
 'EISafter2point2.dta': 56115, 
 'EISstart.dta': 43389
 }

Same is true for all data (XX = EIS,CV,CA,CP,MF,GC)
This means we got all the data ready to be called upon with a simple dEIS.values()[i] function, enabling plotting.
"""
# ---------------------------------------------------------------------------------------------


"Creating Results directories"
os.mkdir('Results')

#----------------------------------------------------------------------------------------------

"Plotting EIS data, creating dictionaries where dict[time] = Current/Flow/Potential"
if dEIS != {}:
    os.mkdir('Results/EIS')
    fullEIS_fig, fullEIS_ax = plt.subplots()
    for i, c in zip(range(len(dEIS)), sns.color_palette()):
        partEIS_fig, partEIS_ax = plt.subplots()
        EISstarttime = list(tEIS.values())[i]                       #Obtain universal time
        print(EISstarttime)
        EIScurrent = list(dEIS.values())[i][9]                      #Idc
        EIStime = list(dEIS.values())[i][2]                         #Time
        
        x = list(dEIS.values())[i][4]                               #Zreal
        y = list(dEIS.values())[i][5]                               #Zimg
    
        for ii in range(len(EIScurrent)):                                   
            EIStime[ii] = EIStime[ii] + EISstarttime                        
            dEIS_UTvsI[EIStime[ii]] = EIScurrent[ii]
            
        name = str(list(dEIS)[i]).replace('.DTA', '')
        name = str(name.replace('point', '.'))
        
        fullEIS_ax.scatter(x,y, color = c, s = 5, label = str(name))    
        partEIS_ax.scatter(x,y, color = c, s = 10)    
        partEIS_ax.invert_yaxis()
        
        partEIS_ax.set_xlabel('Zreal [ohm]')
        partEIS_ax.set_ylabel('-Zimag [ohm]')    
        partEIS_ax.set_title(name)
        partEIS_fig.savefig('Results/EIS/' + str(name) + '.png')
    fullEIS_ax.invert_yaxis()
    fullEIS_ax.legend(fontsize = 'small')
    fullEIS_ax.set_xlabel('Zreal [ohm]')
    fullEIS_ax.set_ylabel('-Zimag [ohm]')
    fullEIS_ax.set_title("All EIS signals")
    fullEIS_fig.savefig('Results/EIS/Combined EIS´s.png')


"Plotting non-iR compensated CV´s, just for comparison, not using the data going forward"
if dCV != {}:
    os.mkdir('Results/CV')
    fullCV_fig, fullCV_ax = plt.subplots()
    for i, c in zip(range(len(dCV)), sns.color_palette()):
        partCV_fig, partCV_ax = plt.subplots()
        y = []
        x = []
        x1 = list(dCV.values())[i][3]                                                   #Vf
        y1 = list(dCV.values())[i][4]                                                   #I
        name = str(list(dCV)[i]).replace('.DTA', '')
        name = str(name.replace('point', '.'))   
        for i in range(len(x1)):
            if x1[i] != 0:
                x.append(x1[i])                      #"Lines in .DTA that indicate a new CV curve got assigned 0 earlier"
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
if dCV != {}:
    os.mkdir('Results/CV_iR')
    fullCViR_fig, fullCViR_ax = plt.subplots()
    for i, c in zip(range(len(dCV)), sns.color_palette()):    
        partCViR_fig, partCViR_ax = plt.subplots()
        CVcurrent = []
        CVpotential = []
        CVtime = []
        x1 = list(dCV.values())[i][3]
        y1 = list(dCV.values())[i][4]
        z1 = list(dCV.values())[i][2]
        name = str(list(dCV)[i]).replace('.DTA', '')
        name = str(name.replace('point', '.'))
           
        R = 0
        CVstarttime = list(tCV.values())[i]
        CVname = list(tCV.keys())[i]
        CVEISname = str(CVname.replace('CV', 'EIS'))
        if CVEISname in list(tEIS.keys()):
            EISstarttimee = tEIS[str(CVEISname)]
            
            
            
        if (CVstarttime - EISstarttimee) < 600 and CVEISname in list(tEIS.keys()):
            R = list(dEIS[CVEISname])[4][dEIS[CVEISname][5].index(max(list(dEIS[CVEISname][5])))]
    
        for i1 in range(len(x1)):
            if x1[i1] != 0:
                CVpotential.append(x1[i1])
                CVcurrent.append(y1[i1])
                CVtime.append(z1[i1])
        for i in range(len(CVpotential)):
            CVpotential[i] = CVpotential[i] - CVcurrent[i] * R      
        for ii in range(len(CVpotential)):
            CVtime[ii] = CVtime[ii] + CVstarttime
            dCV_UTvsI[CVtime[ii]] = CVcurrent[ii]
            dCV_UTvsU[CVtime[ii]] = CVpotential[ii]
        fullCViR_ax.scatter(CVpotential,CVcurrent, color = c, s = 0.01, label = str(name))    
        partCViR_ax.scatter(CVpotential,CVcurrent, color = c, s = 0.1)    
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
if dCA != {}:
    os.mkdir('Results/CA')
    fullCA_fig, fullCA_ax = plt.subplots()
    amin = []
    amax = []
    for i, c in zip(range(len(dCA)), sns.color_palette()):
        partCA_fig, partCA_ax = plt.subplots()    
        CAcurrent = list(dCA.values())[i][4] 
        CAtime = list(dCA.values())[i][2]
        name = str(list(dCA)[i]).replace('.DTA', '')
        name = str(name.replace('_', ' '))    
        fullCA_ax.scatter(CAtime[5:],CAcurrent[5:], color = c, s = 3, label = str(name))    
        partCA_ax.scatter(CAtime[5:],CAcurrent[5:], color = c, s = 2)
        partCA_ax.set_ylim([max(CAcurrent[5:])*0.90,min(CAcurrent[5:]) *1.10]) 
        amin.append(min(CAcurrent[5:]))
        amax.append(max(CAcurrent[5:]))
        partCA_ax.set_xlabel('Time [s]')
        partCA_ax.set_ylabel('Current [A]')    
        partCA_ax.set_title(name)
        partCA_fig.savefig('Results/CA/' + str(name) + '.png')
        
        CAstarttime = list(tCA.values())[i]
        CApotential = list(dCA.values())[i][3]
        CAunivtime = list(dCA.values())[i][2]
        for ii in range(len(CAcurrent)):
            CAunivtime[ii] = CAunivtime[ii] + CAstarttime
            dCA_UTvsI[CAunivtime[ii]] = CAcurrent[ii]
            dCA_UTvsU[CAunivtime[ii]] = CApotential[ii]    
    fullCA_ax.set_ylim((max(amax))*0.90, min(amin)*1.1)
    fullCA_ax.legend(fontsize = 'small')
    fullCA_ax.set_xlabel('Time [s]')
    fullCA_ax.set_ylabel('Current [A]')
    fullCA_ax.set_title("All CA signals")
    fullCA_fig.savefig('Results/CA/Combined CA´s.png')



"Plotting CP data"
if dCP != {}:
    os.mkdir('Results/CP')
    fullCP_fig, fullCP_ax = plt.subplots()
    amin = []
    amax = []
    for i, c in zip(range(len(dCP)), sns.color_palette()):
        partCP_fig, partCP_ax = plt.subplots()    
        CPpotential = list(dCP.values())[i][3] 
        CPtime = list(dCP.values())[i][2]
        name = str(list(dCP)[i]).replace('.DTA', '')
        name = str(name.replace('_', ' '))    
        fullCP_ax.scatter(CPtime[5:],CPpotential[5:], color = c, s = 3, label = str(name))    
        partCP_ax.scatter(CPtime[5:],CPpotential[5:], color = c, s = 2)
        partCP_ax.set_ylim([max(CPpotential[5:])*0.90,min(CPpotential[5:]) *1.10]) 
        amin.append(min(CPpotential[5:]))
        amax.append(max(CPpotential[5:]))
        partCP_ax.set_xlabel('Time [s]')
        partCP_ax.set_ylabel('Potential [V]')    
        partCP_ax.set_title(name)
        partCP_fig.savefig('Results/CP/' + str(name) + '.png')
        
        CPstarttime = list(tCP.values())[i]
        CPcurrent = list(dCP.values())[i][4]
        CPunivtime = list(dCP.values())[i][2]
        for ii in range(len(CPpotential)):
            CPunivtime[ii] = CPunivtime[ii] + CPstarttime
            dCP_UTvsI[CPunivtime[ii]] = CPcurrent[ii]
            dCP_UTvsU[CPunivtime[ii]] = CPpotential[ii]    
    fullCP_ax.set_ylim((max(amax))*0.90, min(amin)*1.1)
    fullCP_ax.legend(fontsize = 'small')
    fullCP_ax.set_xlabel('Time [s]')
    fullCP_ax.set_ylabel('Potential vs Ag/AgCl [V]')
    fullCP_ax.set_title("All CP signals")
    fullCP_fig.savefig('Results/CP/Combined CP´s.png')



  
"Links MF flow to universal time"
if dMF != {}:
    dMF_UTvsF = {}
    for i in range(len(tMF)):
        MFflow = list(dMF.values())[i][1]
    
        MFstarttime = float(list(tMF.values())[i])
        
        MFtime = list(dMF.values())[i][0]
                                        
        for k in range(len(MFtime)):
            MFtime[k] = round((MFtime[k] + MFstarttime), 0)
            dMF_UTvsF[MFtime[k]] = MFflow[k]


"Gas chromatography"
if dGCA != {}:
    os.mkdir('Results/FE')

    F = 96485
    #GF1 = 1.2  # gas flow factor for Ar -------------------- CHANGE  TO 1 IF USING CO2
    GF1 = 1
    
    nETH = 6     # number of electrons
    nMET = 10    # number of electrons
    nCO =  2     # number of electrons
    nHYD = 2     # number of electrons
    
    cETH = 0.000362576                 # Old value: 0.0003701        #calibration factor Ethylene            
    cHYD = 0.007054425                 # Old value: 0.00680013       #calibration factor Hydrogen            
    cMET = 0.000715923                 # Old value: 0.00068207       #calibration factor Methanol            
    cCO  = 0.000707912                 # Old value: 0.00069638       #calibration factor Carbon monoxide     
    
    
    "GC column A"
    
    FEeth = []                 #5.15 - 5.90 ------Ethylene
    FEmet = []                #9.85 - 10.40-----Methane
    FEco = []                 #10.8 - 11.4 ----CO
    Ueth = []
    Umet = []
    Uco = []
    teth = []
    tmet = []
    tco = []
    Ieth = []
    Imet = []
    Ico = []

    for i in dGCA:
        GCAstarttime = float(tGC[i] - 5)   
        if dCA_UTvsI != {}:
            if GCAstarttime in dCA_UTvsI and GCAstarttime in dMF_UTvsF:
                InjectionI = dCA_UTvsI[GCAstarttime]
                InjectionF = dMF_UTvsF[GCAstarttime]
                InjectionU = round(dCA_UTvsU[GCAstarttime], 2)     
                for k in range(len(dGCA[i][1])):                                                             
                    if 5.2 <= float(dGCA[i][1][k]) < 5.90:                      #Ethylene
                        dGCA[i][2][k] = (((float(dGCA[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nETH) / (22.4 * 1000)) * cETH               
                        if (dGCA[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEeth.append(round(float(abs(dGCA[i][2][k]/(InjectionI * 10))), 2))
                            Ueth.append(InjectionU)
                            teth.append(GCAstarttime)
                            Ieth.apend(round(InjectionI, 3))
                    
                    if 9.85 <= float(dGCA[i][1][k]) < 10.40:                     #Methanol
                        dGCA[i][2][k] = (((float(dGCA[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nMET) / (22.4 * 1000)) * cMET
                        if (dGCA[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEmet.append(round(float(abs(dGCA[i][2][k]/(InjectionI * 10))), 2))
                            Umet.append(InjectionU)
                            tmet.append(GCAstarttime)
                            Imet.append(round(InjectionI, 3))
                        
                    if 10.5 <= float(dGCA[i][1][k]) < 11.4:                      #Carbon Monoxide
                        dGCA[i][2][k] = (((float(dGCA[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nCO) / (22.4 * 1000)) * cCO                                              
                        if (dGCA[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEco.append(round(float(abs(dGCA[i][2][k]/(InjectionI * 10))), 2))
                            Uco.append(InjectionU)
                            tco.append(GCAstarttime)
                            Ico.append(round(InjectionI, 3))
                        
        if dCP_UTvsI != {}:
            if GCAstarttime in dCP_UTvsI and GCAstarttime in dMF_UTvsF:
                InjectionI = dCP_UTvsI[GCAstarttime]
                InjectionF = dMF_UTvsF[GCAstarttime]
                InjectionU = round(dCP_UTvsU[GCAstarttime], 2)     
                for k in range(len(dGCA[i][1])):                                                             
                    if 5.2 <= float(dGCA[i][1][k]) < 5.90:                      #Ethylene
                        dGCA[i][2][k] = (((float(dGCA[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nETH) / (22.4 * 1000)) * cETH               
                        if (dGCA[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEeth.append(round(float(abs(dGCA[i][2][k]/(InjectionI * 10))), 2))
                            Ueth.append(InjectionU)
                            teth.append(GCAstarttime)
                            Ieth.apend(round(InjectionI, 3))
                    
                    if 9.85 <= float(dGCA[i][1][k]) < 10.40:                     #Methanol
                        dGCA[i][2][k] = (((float(dGCA[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nMET) / (22.4 * 1000)) * cMET
                        if (dGCA[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEmet.append(round(float(abs(dGCA[i][2][k]/(InjectionI * 10))), 2))
                            Umet.append(InjectionU)
                            tmet.append(GCAstarttime)
                            Imet.append(round(InjectionI, 3))
                        
                    if 10.5 <= float(dGCA[i][1][k]) < 11.4:                      #Carbon Monoxide
                        dGCA[i][2][k] = (((float(dGCA[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nCO) / (22.4 * 1000)) * cCO                                              
                        if (dGCA[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEco.append(round(float(abs(dGCA[i][2][k]/(InjectionI * 10))), 2))
                            Uco.append(InjectionU)
                            tco.append(GCAstarttime)
                            Ico.append(round(InjectionI, 3))
    
  
    
    "GC column B"
    
    FEhyd = []                 #1.30-1.50 ----- Hydrogen
    Uhyd = []                 #3.00 - 3.50---- Carbon dioxide
    thyd = []
    Ihyd = []
    
    
    for i in dGCB:
        GCBstarttime = float(tGC[i] - 10)
        if dCA_UTvsI != {}:
            if GCBstarttime in dCA_UTvsI and GCBstarttime in dMF_UTvsF:
                InjectionI = dCA_UTvsI[GCBstarttime]
                InjectionF = dMF_UTvsF[GCBstarttime]
                InjectionU = round(dCA_UTvsU[GCBstarttime], 2)        
                for k in range(len(dGCB[i][1])):                                                           
                    if 1.30 <= float(dGCB[i][1][k]) < 1.50:                      #Hydrogen
                        dGCB[i][2][k] = (((float(dGCB[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nHYD) / (22.4 * 1000)) * cHYD            
                        if (dGCB[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEhyd.append(round(float(abs(dGCB[i][2][k]/(InjectionI*10))), 2))
                            Uhyd.append(InjectionU)
                            thyd.append(GCBstarttime)
                            Ihyd.append(round(InjectionI, 3))
        if dCP_UTvsI != {}:
            if GCBstarttime in dCP_UTvsI and GCBstarttime in dMF_UTvsF:
                InjectionI = dCP_UTvsI[GCBstarttime]
                InjectionF = dMF_UTvsF[GCBstarttime]
                InjectionU = round(dCP_UTvsU[GCBstarttime], 2)        
                for k in range(len(dGCB[i][1])):                                                           
                    if 1.30 <= float(dGCB[i][1][k]) < 1.50:                      #Hydrogen
                        dGCB[i][2][k] = (((float(dGCB[i][2][k])  * ((InjectionF * GF1) / 60000)) * F * nHYD) / (22.4 * 1000)) * cHYD            
                        if (dGCB[i][2][k]/1000) >= abs(InjectionI * 0.001):
                            FEhyd.append(round(float(abs(dGCB[i][2][k]/(InjectionI*10))), 2))
                            Uhyd.append(InjectionU)
                            thyd.append(GCBstarttime)
                            Ihyd.append(round(InjectionI, 3))
        
    
         
    
    "Coupling of each product´s data to a common array"
    Names = ['Ethylene', 'Methanol', 'Carbon monoxide', 'Hydrogen']
    Potentials = [Ueth, Umet, Uco, Uhyd]
    FEs = [FEeth, FEmet, FEco, FEhyd]
    TIMEs = [teth,tmet,tco,thyd]
    Currents = [Ieth, Imet, Ico, Ihyd]
    FEmax = []
    
    
    
    
    tCOMB = {}
    
    if tCA != {}:
        for i in range(len(tCA)):   
            tCOMB[list(tCA.keys())[i]] = list(tCA.values())[i]
        

    if tCP != {}:
        
        for i in range(len(tCP)):
            tCOMB[list(tCP.keys())[i]] = list(tCP.values())[i]
            

    
    "Creates an array where each data point (FE @ Potential) has a time value --> Namely this point happened 25min into CA"
    for i in range(len(TIMEs)):
        for k in range(len(TIMEs[i])):
            un = []
            a = TIMEs[i][k]
            for s in list(tCOMB.values()):
                c = a-s
                if c <= 0:
                    c = 1000000           
                un.append(c)
            if TIMEs[i] != []:
                TIMEs[i][k] = min(un)
                TIMEs[i][k] = round(float(TIMEs[i][k] / 60), 2)
                
    
                
    Tab_headers = ['Product', 'Potential [V]', 'Current [A]', 'After [min]', 'Partial current [mA]', 'FE [%]']
    Tab_values = []
    
    "Plots the final FE/U graphs, also labels the datapoints for time"
    fullFE_fig, fullFE_ax = plt.subplots()
    for i, c in zip(range(len(Potentials)), sns.color_palette()):
        if FEs[i] != []:
            partFE_fig, partFE_ax = plt.subplots()
            FEmax.append(max(FEs[i]))
            fullFE_ax.scatter(Potentials[i], FEs[i], color = c, s = 5, label = (Names[i]))
            partFE_ax.scatter(Potentials[i], FEs[i], color = c, s = 10)
            partFE_ax.set_ylim([0,float((max(FEs[i]))*1.10)])
            partFE_ax.set_xlabel('Potential vs Ag/AgCl [V]')
            partFE_ax.set_ylabel('Faradaic efficiency [%]')
            partFE_ax.set_title(Names[i])
            for ii in range(len(TIMEs[i])):
                if float(round(float(FEs[i][ii]), 3)) != 0.000:
                    partFE_ax.annotate(str(TIMEs[i][ii]) + ' min', xy = (Potentials[i][ii], FEs[i][ii]),
                                       xytext = (3, 5), textcoords='offset points', size = 9)

                if i == 0:
                    t1 = 'Ethylene'
                elif i == 1:
                    t1 = 'Methanol'
                elif i == 2:
                    t1 = 'CO'
                elif i == 3:                    
                    t1 = 'Hydrogen'
                
                Tab_values.append([ t1, Potentials[i][ii], Currents[i][ii], TIMEs[i][ii], round(abs(Currents[i][ii] * 10 * FEs[i][ii]), 1), FEs[i][ii]])
                partFE_fig.savefig('Results/FE/' + str(Names[i]) + '.png')        
    fullFE_ax.set_ylim([0,max(FEmax)*1.10])
    fullFE_ax.set_xlabel('Potential vs Ag/AgCl [V]')
    fullFE_ax.set_ylabel('Faradaic efficiency [%]')
    fullFE_ax.legend(fontsize = 'small')
    fullFE_ax.set_title('All faradaic efficiencies')
    fullFE_fig.savefig('Results/FE/All FE´s.png')


    
#Display results in a table form in .txt and .xlsx file
if dGCA != {}:  
    
    print(tabulate(Tab_values, headers=Tab_headers))

    with open('Results/Result Table.txt', 'w') as fi:
        fi.write(tabulate(Tab_values, headers=Tab_headers))
    
    workbook = xlsxwriter.Workbook('Results/Results.xlsx')
    worksheet = workbook.add_worksheet('Faradaic efficiences')
    title = workbook.add_format({'bold': True, 'font_size' : 14, 'bg_color' : '#DBDBDB'})
    bold = workbook.add_format({'bold' : True, 'font_size' : 12, 'bg_color' : '#D1FFD9'})
    
    for i in range(len(Tab_headers)):
        worksheet.write(0, i, Tab_headers[i], title)    
    
    for i in range(len(Tab_values)):
        for ii in range(len(Tab_values[i])):
            if ii in [0,5]:
                worksheet.write(i + 2, ii, Tab_values[i][ii], bold)
            else:
                worksheet.write(i + 2, ii, Tab_values[i][ii])
            
    workbook.close()
