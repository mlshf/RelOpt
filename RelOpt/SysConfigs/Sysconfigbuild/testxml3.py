import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, Comment
from xml.dom import minidom
import os
import random

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")

def xmlbuild(sysclasst, sysclassc, sysmodnum, systimes, syshwnum, sysswnum, sysmoo):
    system = Element("system", limitcost="")
    modules = []
    smax = 0
    smin = 0    
    for i in range(sysmodnum):
        module = SubElement(system, "module", limittime=str(systimes[i]), num=str(i), qall="0.99", qd="0.99", qrv="0.99", trecov="3", ttest="2", tvote="1")
        for j in range(len(sysmoo[i])):
            SubElement(module, "tool", name=sysmoo[i][j])
            
        swcost = []
        for j in range(sysswnum[i]):
            swcost1 = random.randint(5, 35)
            swcost.append(swcost1)
            SubElement(module, "sw", cost=str(swcost1), num=str(j), rel=str(random.uniform(0.85, 0.99)))
        hwcost = []
        for j in range(syshwnum[i]):
            hwcost1 = random.randint(5, 35)
            hwcost.append(hwcost1)
            SubElement(module, "hw", cost=str(hwcost1), num=str(j), rel=str(random.uniform(0.85, 0.99)))
        swcost.sort()
        hwcost.sort()
        smin = smin + swcost[0] + hwcost[0]
        swcost.reverse()
        hwcost.reverse()
        if ("nvp11" in sysmoo[i]):
            smax = smax + swcost[0] + hwcost[0] + swcost[1] + hwcost[1] + swcost[2] + hwcost[2]
        elif ("nvp01" in sysmoo[i] and "rb11" not in sysmoo[i]):
            smax = smax + swcost[0] + swcost[1] + swcost[2] + hwcost[0]
        elif ("nvp01" not in sysmoo[i] and "rb11" in sysmoo[i]):
            smax = smax + swcost[0] + swcost[1] + hwcost[0] + hwcost[1]
        elif ("nvp01" in sysmoo[i] and "rb11" in sysmoo[i]):
            smax1 = swcost[0] + swcost[1] + swcost[2] + hwcost[0]
            smax2 = swcost[0] + swcost[1] + hwcost[0] + hwcost[1]
            smax = smax + max(smax1, smax2)
        else:
            smax = smax + swcost[0] + hwcost[0]
            
        if (sysclasst == 1):
            tworkl = 100
            tworkr = 150
        elif (sysclasst == 2):
            tworkl = 10
            tworkr = 30
        elif (sysclasst == 3):
            tworkl = 1
            tworkr = 30
        elif (sysclasst == 4):
            tworkl = 1
            tworkr = 10
        else:
            tworkl = 1
            tworkr = 5
        for j1 in range(sysswnum[i]):
            for j2 in range(syshwnum[i]):
                SubElement(module, "time", hwnum=str(j2), swnum=str(j1), t=str(random.randint(tworkl, tworkr)))
        modules.append(module)
        
    if (sysclasst == 1):
        ttransferl = 1
        ttransferr = 5
    elif (sysclasst == 2):
        ttransferl = 1
        ttransferr = 10
    elif (sysclasst == 3):
        ttransferl = 1
        ttransferr = 30
    elif (sysclasst == 4):
        ttransferl = 10
        ttransferr = 30
    else:
        ttransferl = 100
        ttransferr = 150
    for i in range(sysmodnum-1):
        for j in range(i, sysmodnum-1):
            p = random.randint(0, 1)
            if (p == 1):
                SubElement(system, "link", dst=str(j+1), src=str(i), vol=str(random.randint(ttransferl, ttransferr)))
        
    if (sysclassc == 1):
        constraitp = 0
    elif (sysclassc == 2):
        constraitp = 0.2
    elif (sysclassc == 3):
        constraitp = 0.4
    elif (sysclassc == 4):
        constraitp = 0.6
    else:
        constraitp = 0.8
    syscost = int(smax -(smax - smin)*constraitp)
    system.set("limitcost", str(syscost))
    
    return system  

def manualbuild():

    confisright = False 

    while (not confisright): 
        print "Enter time class of system (from 1 to 5):" 
        while True:
            try:
                sysclasst = int(raw_input())
                while (sysclasst < 1 or sysclasst > 5):
                    print "Enter time class of system (from 1 to 5) again:"
                    sysclasst = int(raw_input())
                break
            except ValueError:
                print "Enter time class of system (from 1 to 5) again:"
            
        print "Enter constrait class of system (from 1 to 5):" 
        while True:
            try:
                sysclassc = int(raw_input())
                while (sysclassc < 1 or sysclassc > 5):
                    print "Enter constrait class of system (from 1 to 5) again:"
                    sysclassc = int(raw_input())
                break
            except ValueError:
                print "Enter constrait class of system (from 1 to 5) again:"
    
        print "Enter number of modules:"
        while True:
            try:
                sysmodnum = int(raw_input())  
                while (sysmodnum < 1):
                    print "Enter number of modules again:"
                    sysmodnum = int(raw_input())  
                break
            except ValueError:
                print "Enter number of modules again:"
            
        print "Enter limittimes for each of modules:" 
        systimes = []
        for i in range(sysmodnum):
            print "Time for "+str(i)+" module:"
            while True:
                try:
                    systime = int(raw_input())
                    while (systime < 1):
                        print "Enter time for "+str(i)+" module again:"
                        systime = int(raw_input())
                    systimes.append(systime)
                    break
                except ValueError:
                    print "Enter time for "+str(i)+" module again:"

        print "Enter number of hw components for each of modules:"
        syshwnum = []
        for i in range(sysmodnum):
            print "Number of hw components for "+str(i)+" module:"
            while True:
                try:
                    syshw = int(raw_input())
                    while (syshw < 3):
                        print "Enter number of hw components for "+str(i)+" module again:"
                        syshw = int(raw_input())
                    syshwnum.append(syshw)
                    break
                except ValueError:
                    print "Enter number of hw components for "+str(i)+" module again:"
    
        print "Enter number of sw components for each of modules:"
        sysswnum = []
        for i in range(sysmodnum):
            print "Number of sw components for "+str(i)+" module:"
            while True:
                try:
                    syssw = int(raw_input())
                    while (syssw < 3):
                        print "Enter number of sw components for "+str(i)+" module again:"
                        syssw = int(raw_input())
                    sysswnum.append(syssw)
                    break
                except ValueError:
                    print "Enter number of sw components for "+str(i)+" module again:"
            
        print "Enter available MOO for each of modules:"
        sysmoo = []
        for i in range(sysmodnum):
            print "Enter available MOO for "+str(i)+" module:"
            sysmoo1 = ["none"]
            moo = "enter"
            mooc = 0
            #moonum = int(input())
            #while (moonum < 1 and moonum > 3)
            while (moo != "exit" and mooc < 3):
                print "Enter MOO or exit:"
                moo = raw_input()
                while (moo != "nvp01" and moo != "nvp11" and moo != "rb11" and moo != "exit" or moo in sysmoo1):
                    print "Enter MOO again:"
                    moo = raw_input()
                if (moo != "exit"):
                    sysmoo1.append(moo)
                    mooc = mooc + 1
            sysmoo.append(sysmoo1)
    
        print "##########################################################" 
        print "Check system configuration. Is it right <yes/no>?"
        print "System time class is "+str(sysclasst)
        print "System constrait class is "+str(sysclassc)
        print "Number of modules is "+str(sysmodnum)
        print "System limittimes are:"
        for i in range(sysmodnum):
            print "Time for "+str(i)+" module is "+str(systimes[i])
        print "Numbers of hw components are:"
        for i in range(sysmodnum):
            print "Number of hw components for "+str(i)+" module is "+str(syshwnum[i])
        print "Numbers of sw components are:"
        for i in range(sysmodnum):
            print "Number of sw components for "+str(i)+" module is "+str(sysswnum[i])
        print "Available MOO are:"
        for i in range(sysmodnum):
            print "Available MOO for "+str(i)+" module are:"
            for j in range(len(sysmoo[i])):
                print sysmoo[i][j]
        print "##########################################################"        
    
        checkconf = raw_input()  
        while (checkconf != "yes" and checkconf != "no"):
            print "Enter answer again:" 
            checkconf = raw_input() 
        if checkconf == "yes":
            confisright = True   

    return (sysclasst, sysclassc, sysmodnum, systimes, syshwnum, sysswnum, sysmoo)            

def autobuild():
    pass
    
###################################################################

choosemode = raw_input("Choose mode to build xml file <manual/auto>:")
while (choosemode != "manual" and choosemode != "auto"):
    choosemode = raw_input("Choose mode to build xml file <manual/random> again:")
    
if choosemode == "manual":
    sysclasst, sysclassc, sysmodnum, systimes, syshwnum, sysswnum, sysmoo = manualbuild()  
else:
    autobuild()    

###################################################################
    
systemconf = xmlbuild(sysclasst, sysclassc, sysmodnum, systimes, syshwnum, sysswnum, sysmoo)

nm = os.path.join("", "testxml3.xml")
f = open(nm, "w")
f.write(prettify(systemconf))

raw_input()
