#!/usr/bin/env python
import epygram
import numpy as np
import copy

from os import system, path

import toml

#import warnings
#warnings.filterwarnings("ignore",category=np.VisibleDeprecationWarning)

#epygram.init_env()

########################################################
# Functions
#
def init(ccase,tomlCase):
    # Initialize setup

    if ccase:
        # Copy config file for specified case
        #
        ccase="configs/case."+ccase+".py"

        if not path.exists(ccase):
            print("Config file not found, aborting...")
            exit()
        else:
            print("Using configs from: "+ccase)
        
        system("cp "+ccase+" mycase.py")
        cnf=None

    else:
        # Read in toml config
        #
        with open('configs/base.'+tomlCase+'.toml',mode='r') as fp:
            cnf = toml.load(fp)

    return cnf

########################################################
def constructCasesNew(cnf):
    # Link toml fields to local variables
    #
    # !NOTE!
    # Later link these directly to mainOper()

    listCases=[]
            
    for iCase in cnf['opts']['Case'].items():

        date=iCase[1]['date']
        time=iCase[1]['t']
        plotDomains=iCase[1]['plotDomains']

        for iField in iCase[1]['fieldDef']:
            ifld=cnf['opts']['Fields'][iField]

            print(ifld)
                
            for itype in cnf['opts']['Type']:
            
                listCases.append({
                    'Date': date,
                    'Time': time,
                    'Case': iCase[0],
                    'Type': itype,
                    'Flds': iField,
                    'plotDomains': plotDomains})

    return listCases

########################################################
def tomlToFuncNew(iSelection,cnf):
    # Link toml fields to local variables
    #
    # !NOTE!
    # Later link these directly to mainOper()

    # MAIN
    cMain=cnf['opts']['Main']

    dpath=cMain['dpath']
    exp=cMain['exp']
    members=cMain['members']

    # CASE
    cCase=iSelection['Case']
    date=iSelection['Date']
    t=[iSelection['Time'].zfill(2)]
    plotDomains=iSelection['plotDomains']    
    
    # TYPE
    cType=cnf['opts']['Type'][iSelection['Type']]

    plottype=cType['plottype']
    expName=cType['expName']
    scalesMatched=cType['scalesMatched']
    manualBounds=cType['manualBounds']
    masked=cType['masked']
    try:
        spgPattern=cType['spgPattern']
    except:
        spgPattern=False

    # FIELDS
    if iSelection['Flds']:
        cFlds=cnf['opts']['Fields'][iSelection['Flds']]
    else:
        iFlds=cCase['fieldDef'][0]
        cFlds=cnf['opts']['Fields'][iFlds]

    levels=cFlds['levels']
    pars=cFlds['pars']    

    # ADD
    cAdd=cnf['opts']['Add']

    figName=cAdd['figName']
    fixNegData=cAdd['fixNegData']
    hardMaskId=cAdd['hardMaskId']


    return levels,dpath,exp,date,t,members,pars,plottype,scalesMatched,\
        fixNegData,masked,hardMaskId,plotDomains,manualBounds,\
        figName,expName,spgPattern

########################################################
def constructCases(cSelection,cnf):
    # Link toml fields to local variables
    #
    # !NOTE!
    # Later link these directly to mainOper()

    listCases=[]

    icounter=0
    # Construct all cnf files requested
    for icase in cSelection:
        
        #for iterItem in cnf['opts']['Case'][cSelection[icase]['Case']].items():
        #    print(iterItem)
        #    print("\n")
            
        for iterItem in cnf['opts']['Case'][cSelection[icase]['Case']].items():

            if iterItem[0]=='date':
                date=iterItem[1]
                continue

            else:

                time=iterItem[1]['t']
                fieldDef=iterItem[1]['fieldDef']
                plotDomains=iterItem[1]['plotDomains']
                
                #listCases.update({icounter:{
                #    'Time': iterItem[1]['t'],
                #    'fieldDef': iterItem[1]['fieldDef'],
                #    'plotDomains': iterItem[1]['plotDomains']}})


                #icounter+=1

            for itype in cSelection[icase]['Type']:
                try:
                    flds=cSelection[icase]['Flds']
                except:
                    flds=fieldDef
                    
                for ifld in flds:
                    #listCases[icounter]={
                    listCases.append({
                        'Date': date,
                        'Time': time,
                        'Case': cSelection[icase]['Case'],
                        'Type': itype,
                        'Flds': ifld,
                        'plotDomains': plotDomains})
                    icounter+=1
                


    return listCases

########################################################
def tomlToFunc(iSelection,cnf):
    # Link toml fields to local variables
    #
    # !NOTE!
    # Later link these directly to mainOper()

    # MAIN
    cMain=cnf['opts']['Main']

    dpath=cMain['dpath']
    exp=cMain['exp']
    members=cMain['members']

    # CASE
    cCase=cnf['opts']['Case'][iSelection['Case']]
    
    date=cCase['date']
    tCase=cCase[iSelection['Time']]
    t=[iSelection['Time'].zfill(2)]
    plotDomains=tCase['plotDomains']
    
    # TYPE
    cType=cnf['opts']['Type'][iSelection['Type']]

    plottype=cType['plottype']
    expName=cType['expName']
    scalesMatched=cType['scalesMatched']
    manualBounds=cType['manualBounds']
    masked=cType['masked']


    # FIELDS
    if iSelection['Flds']:
        cFlds=cnf['opts']['Fields'][iSelection['Flds']]
    else:
        iFlds=cCase['fieldDef'][0]
        cFlds=cnf['opts']['Fields'][iFlds]

    levels=cFlds['levels']
    pars=cFlds['pars']    

    # ADD
    cAdd=cnf['opts']['Add']

    figName=cAdd['figName']
    fixNegData=cAdd['fixNegData']
    hardMaskId=cAdd['hardMaskId']


    return levels,dpath,exp,date,t,members,pars,plottype,scalesMatched,\
        fixNegData,masked,hardMaskId,plotDomains,manualBounds,\
        figName,expName


########################################################
def file_name(path,exp,date,time,memb):
    # Construct the file path
    #
    fname=path+"/"+exp+"_"+date+"_00"+time+"_00"+memb

    return fname

########################################################
def load_data(fname,level,par):
    # Load data with epygram and read the desired field in
    #
    if level > 9:
        parname="S0"+str(level)+par
    elif level > 0:
        parname="S00"+str(level)+par
    else:
        parname=par
        # Overwrite for SPP pattern (stored differently),
        # and for surface fields
        if par=="SPP_PATTERN1":
            parname="S001SPP_PATTERN"
        elif par=="SPP_PATTERN2":
            parname="S002SPP_PATTERN"
        elif par=="SPP_PATTERN3":
            parname="S003SPP_PATTERN"
        elif par=="SPP_PATTERN4":
            parname="S004SPP_PATTERN"
        elif par=="SPP_PATTERN5":
            parname="S005SPP_PATTERN"
        elif par=="SPP_PATTERN6":
            parname="S006SPP_PATTERN"
        elif par=="SPP_PATTERN7":
            parname="S007SPP_PATTERN"
        elif par=="SPP_PATTERN8":
            parname="S008SPP_PATTERN"
        elif par=='SURFINSPLUIE' or par=='SURFINSNEIGE' or par=='SURFINSGRAUPEL':
            parname=par
        elif par=='SURFNEBUL.TOTALE':
            parname=par
    
    r=epygram.formats.resource(fname,'r')

    data=r.readfield(parname)
    
    return data

########################################################
def loadAllData(path,exp,date,t,members,level,pars,fixNegData,hardMaskId):
    # Load all model data in to memory

    # Init an np array to contain all the data
    #data=np.empty((len(exp),len(members),len(pars),len(level)),dtype=object)
    data=np.empty((len(exp),len(members),len(pars)),dtype=object)

    iexp=0
    for expi in exp:
        imemb=0
        for memb in members:
            # Construct filename for exp and member
            if memb==0:
                try:
                    path.isname(file_name(path,"control",date,t,str(memb)))
                except:
                    fname=file_name(path,expi,date,t,str(memb))
                else:
                    fname=file_name(path,"control",date,t,str(memb))

            else:
                fname=file_name(path,expi,date,t,str(memb))

            ipar=0
            for par in pars:
                #ilev=0
                #for lev in levels:

                d=load_data(fname,level,par)
                
                # There are negative data values in someplaces for some reason
                # fix this
                if fixNegData:
                    d.data[d.data<0]=0.
                    #print(d.data<0)

                if hardMaskId:
                    if hardMaskId=="Fin":
                        # Finnish South + Baltic
                        d.data[0:961,740:751]=0.
                        d.data[0:961,0:400]=0.
                        d.data[0:190,:]=0.
                        d.data[610:961,:]=0.
                    elif hardMaskId=="Nor":
                        # Norwegian South + North Sea
                        d.data[0:961,500:751]=0.
                        d.data[700:961,:]=0.
                    elif hardMaskId=="Gavle":
                        d.data[0:961,740:751]=0.
                        d.data[0:961,0:400]=0.
                        d.data[0:290,:]=0.
                        d.data[610:961,:]=0.
                        
                
                # Load data in per variable and level
                #data[iexp,imemb,ipar,ilev]=d
                data[iexp,imemb,ipar]=d
                    
                #    ilev+=1
                ipar+=1
            imemb+=1
        iexp+=1
        
    return data

########################################################
def mainData(path,exp,date,t,members,level,pars,plottype,scalesMatched,\
             fixNegData,areaMask,printLog):


    # LOG
    if printLog:
        print("Processing fc+",t,"on level",str(level),"       ",\
              "    ",date,exp)
    
    # Load in all data
    data=loadAllData(path,exp,date,t,members,level,pars,fixNegData,areaMask)

    # Clean out not used dimensions frm the data matrix
    if plottype!="multiExpDiff" and plottype!="multiExpStd" and \
       plottype!="multiExpDiffStd":
        data=reduceData(data,dim=(1,2))

    dextra=[]

    if plottype=="multiMember":
        if scalesMatched:
            dextra=getMax(data,dim=0)

    elif plottype=="multiMemberDiff":
        data=dhDiff(data,False)

        if scalesMatched:
            dextra=getStats(data)[1:3]
            
    elif plottype=="multiMemberDiff2":
        data=dhDiff2(data,False)

        if scalesMatched:
            dextra=getStats(data)[1:3]
            
    elif plottype=="multiMemberStd" or plottype=="multiMemberStdMasked":
        data=dhStd(data,False)
    
    elif plottype=="multiExpDiffStd":
        data=expDiffStd(data)

        if scalesMatched:
            dextra=[]
            dextra.append(getStats(data[1:-1:2,:],excludeCtrl=0)[1:3])
            dextra.append(getStats(data[2:-1:2,:],excludeCtrl=0)[1:3])

    elif plottype=="multiExpDiff":
        data=expDiff(data)

        if scalesMatched:
            dextra=getStats(data[1:-1:1,:],excludeCtrl=0)[1:3]

    elif plottype=="multiExpStd":
        data=expStd(data)

        if scalesMatched:
            dextra=getStats(data)[1:3]

    # LOG
    if printLog:
        print("Processing fc+",t,"on level",str(level),"       ",\
              "DONE",date,exp)
            
    return data,dextra

########################################################
class MinValue:
    def __init__(self):
        self.min_value=float("inf")

    def __call__(self,new_value):
        if new_value < self.min_value:
            self.min_value=new_value
            
        return self.min_value

########################################################
def reduceData(data,dim=(0,1)):
    # Clean out 1-size dimensions

    # Get dim of data
    allDim=data.shape

    # Reduce data matrix to dim-shape
    data=np.reshape(data,(allDim[dim[0]],allDim[dim[1]]))

    return data

########################################################
def getMax(data,dim=0):
    # Create a min value vector keeping track of each variable/level
    # smallest max values

    dataMin=[]

    # Depending on the choice, unroll data structure differently
    if dim==0:
        for j in range(0,data.shape[1]):

            # Initialize
            n=MinValue()
            
            for i in range(0,data.shape[0]):
                dd=n(data[i,j].max())
                
            dataMin.append(dd)

    else:
        for i in range(0,data.shape[1]):

            # Initialize
            n=MinValue()
            
            for j in range(0,data.shape[0]):
                dd=n(data[i,j].max())
                
            dataMin.append(dd)
    
    return dataMin

########################################################
def getStats(data,excludeCtrl=1):
    # Get max, min and mean from the data to be displayed later on
    dataStats=np.empty((data.shape[0],data.shape[1],3),dtype=object)

    sMax=[]
    lMin=[]
   
    for j in range(0,data.shape[1]):

        smallestMax=np.inf
        largestMin=-np.inf
        #n=MinValue()
        
        for i in range(excludeCtrl,data.shape[0]):
            dataStats[i,j,0]=data[i,j].max()
            dataStats[i,j,1]=data[i,j].min()
            dataStats[i,j,2]=data[i,j].mean()
            
            smallestMax=min(smallestMax,dataStats[i,j,0])
            largestMin=max(largestMin,dataStats[i,j,1])

        sMax.append(smallestMax)
        lMin.append(largestMin)
        
    return dataStats,sMax,lMin

########################################################
def stdvFromData(data):

    mean=[]
    sdev=[]
    
    for i in range(0,data.shape[1]):
        # Mean
        dd=copy.deepcopy(data[0,i])
        dd.data-=data[0,i].data
        for j in range(1,data.shape[0]):
            dd.data += data[j,i].data

        dd.data=dd.data/float(j)
        mean.append(dd)
        
        # SDEV
        sdd=copy.deepcopy(data[0,i])
        sdd.data-=data[0,i].data
        for j in range(1,data.shape[0]):
            sdd.data += (data[j,i].data - dd.data)**2

        sdd.data=sdd.data/float(j)
        sdd.data=sdd.data**(0.5)
        sdev.append(sdd)
        
    return mean,sdev

########################################################
def expDiffStd(data):
    # Calc mean and sdev for each experiment

    ddd=np.empty((1+data.shape[0]*2,data.shape[2]),dtype='object')
    iddd=0
    # Cycle over exps and create a single data structure containing
    # all the data
    for i in range(0,data.shape[0]):
        dd=data[i,:,:]
        dd=dhStd(dd,False)

        if i==0:
            ctrl=0
        else:
            ctrl=1

        for j in range(ctrl,3):
            ddd[iddd,:]=dd[j,:]

            iddd+=1
            
    return(ddd)

########################################################
def expDiff(data):
    # Calc mean for each experiment

    ddd=np.empty((1+data.shape[0],data.shape[2]),dtype='object')
    iddd=0
    # Cycle over exps and create a single data structure containing
    # all the data
    for i in range(0,data.shape[0]):
        dd=data[i,:,:]
        dd=dhStd(dd,False)

        if i==0:
            ctrl=0
        else:
            ctrl=1

        for j in range(ctrl,2):
            ddd[iddd,:]=dd[j,:]

            iddd+=1
            
    return(ddd)

########################################################
def expStd(data):
    # Calc mean for each experiment
    ddd=np.empty((1+data.shape[0],data.shape[2]),dtype='object')
    iddd=0
    # Cycle over exps
    for i in range(0,data.shape[0]):
        dd=data[i,:,:]
        dd=dhStd(dd,False)

        if i==0:
            exps=[0,2]
        else:
            exps=[2]

        for j in exps:
            ddd[iddd,:]=dd[j,:]

            iddd+=1
            
    return(ddd)

########################################################
def dhStd(data,masked):
    # Data Handling for Std decision tree
    mean,sdev=stdvFromData(data)

    dd=np.empty((3,data.shape[1]),dtype='object')
    for i in range(0,data.shape[1]):
        dd[0,i]=data[0,i]
        dd[1,i]=mean[i]-data[0,i]
        dd[2,i]=sdev[i]

    if masked:
        ddMasked=onesMask(dd)
        plottype=plottype+"Masked"
        data=ddMasked
    else:
        data=dd

    return data

########################################################
def dhDiff(data,masked):
    # Data Handling for Diff decision tree

    for i in range(1,data.shape[0]): #1,6
        for j in range(0,data.shape[1]):
            data[i,j]=data[i,j]-data[0,j]

            if masked:
                data[i,j]=levelsMaskDiff(data[i,j])


    return data

########################################################
def dhDiff2(data,masked):
    # Data Handling for Diff decision tree when SPP patterns
    # are requested
    # Data format:
    #  1st column - field (DO DIFF)
    #  2nd column - raw pert pattern (KEEP)
    #  3rd column - scaled pert pattern (MODIFY)
    
    for i in range(1,data.shape[0]): #1,6
        data[i,0]=data[i,0]-data[0,0]
        #data[2,j]=data[2,j]
        #data[3,j]=data[3,j]*data[0,j]-data[0,j]

        dd=copy.deepcopy(data[i,0])
        dd.data-=data[i,0].data
        dd.data += data[i,2].data*data[0,0].data-data[0,0].data

        data[i,2]=dd
        
        dd=copy.deepcopy(data[i,0])
        dd.data-=data[i,0].data
        dd.data += data[i,3].data*data[i,0].data-data[0,0].data

        data[i,3]=dd
        
        if masked:
            data[1,j]=levelsMaskDiff(data[1,j])
            data[2,j]=levelsMaskDiff(data[2,j])
            data[3,j]=levelsMaskDiff(data[3,j])


    return data


def setPredefinedBounds(date,t,pars,plottype):
    # Predefined list for output field bounds
    #
    # [value for raw field upper limit, value for field diff]
    #
    # In case two values are defined for the raw field,
    # the 1st element is used as the lower limit for colorscale
    #

    tempBounds=[]
    
    for par in pars:
        table=[]

        if par=='SURFACCPLUIE':
            base=[10.,1] # kg/m3

            table=dict([('2022071512'+'06',[20,5]),
                        ('2022071512'+'12',[32,8]),
                        ('2022071512'+'24',[40,10]),
                        ('2022071712'+'06',[20,5]),
                        ('2022071712'+'12',[32,8]),
                        ('2022071712'+'24',[40,10])
            ])
            
        elif par=='SURFNEBUL.TOTALE':

            base=[1.,1.] # 0-1
            
        elif par=='CLSTEMPERATURE':
    
            base=[[263.,283.],1] # K

            table=dict([('2022071512'+'06',[[278,303],2]),
                        ('2022071512'+'12',[[278,303],4]),
                        ('2022071512'+'24',[[278,303],6]),
                        ('2022071712'+'06',[[278,303],2]),
                        ('2022071712'+'12',[[278,303],4]),
                        ('2022071712'+'24',[[278,303],6])
            ])

        # Overwrite base if table value is found for date+t
        if table:
            try:
                base=table[date+t]
            except:
                None

        tempBounds.append(base)

    # Rearrange the list into a format that plot
    # understands (could be revisited)
    control=[]
    diff=[]
    for item in tempBounds:
        control.append(item[0])
        diff.append(item[1])

    if plottype=='multiMemberDiff':
        manualBounds=[control,diff]

    elif plottype=='multiMember':
        manualBounds=[control]
    
    return manualBounds


########################################3
# OBSOLETE????
#########################

def onesMask(data):

    for i in range(0,data.shape[0]):
        for j in range(0,data.shape[1]):
            data[i,j].data[data[i,j].data>0.]=1.
            data[i,j].data[data[i,j].data<0.]=-1.
            
    return data


def levelsMaskDiff2(data):

    for i in range(0,data.shape[0]):
        for j in range(0,data.shape[1]):
            dmax=data[i,j].max
            dmin=data[i,j].min
            # Center around zero
            dabs=max(dmax,-1*dmin)

            print(dmax,dmin,dabs)
            
            data[i,j].data[data[i,j].data > dabs*0.01] =.01
            data[i,j].data[data[i,j].data > dabs*0.1] =.1
            data[i,j].data[data[i,j].data > dabs*0.5] =.5
            data[i,j].data[data[i,j].data > dabs*0.9] =.9

            data[i,j].data[data[i,j].data < dabs*-0.01] =-.01
            data[i,j].data[data[i,j].data < dabs*-0.1] =-.1
            data[i,j].data[data[i,j].data < dabs*-0.5] =-.5
            data[i,j].data[data[i,j].data < dabs*-0.9] =-.9

            
    return data




def levelsMaskDiff(data):

    dmax=data.max()
    dmin=data.min()
    # Center around zero
    dabs=max([dmax,-1*dmin])

    print(dmax,dmin,dabs)
            
    data.data[data.data > dabs*0.01] =.01
    data.data[data.data > dabs*0.1] =.1
    data.data[data.data > dabs*0.5] =.5
    data.data[data.data > dabs*0.9] =.9

    data.data[data.data < dabs*-0.01] =-.01
    data.data[data.data < dabs*-0.1] =-.1
    data.data[data.data < dabs*-0.5] =-.5
    data.data[data.data < dabs*-0.9] =-.9

            
    return data

