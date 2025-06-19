#!/usr/bin/env python
import epygram
import numpy as np
import matplotlib.pyplot as plt

import multiprocessing as mp
from functools import partial

import istarmap
import itertools
import tqdm
#from matplotlib.backends.backend_pdf import PdfPages

import warnings
warnings.filterwarnings("ignore",category=np.VisibleDeprecationWarning)

import dataOperations as dope
import plotOperations as plop

epygram.init_env()

##########################################################
# Paths and variables to be plotted
#
dpath="/ec/res4/scratch/fi3/investigation/icenu"

# Stored config files for specific verification cases. If blank,
# load from toml base template.
#
#ccase='example1'

ccase=""

tomlCase="deode.NorwaySouth1"

# EXAMPLES
#cSelection={
#    0:{
#        "Case": '2022071512',
#        "Type": ['2','3']},
#    1:{
#        "Case": '2022071712',
#        "Type": ['2','3']}
#}
#
#cSelection={
#    0:{
#        "Case": '2022071512',
#        "Type": ['1','2'],
#        "Flds": ['0','1']}
#    }

##########################################################
# Functions
#
def mainOper(level,dpath,exp,date,t,members,pars,plottype,scalesMatched,\
             fixNegData,masked,hardMaskId,plotDomains,manualBounds,\
             figName,expName,spgPattern,printLog=True):

    # Enter main data processing routines
    data,dextra=dope.mainData(dpath,exp,date,t,members,level,pars,plottype,\
                               scalesMatched,fixNegData,hardMaskId,printLog)

    # Cycle through domains (0=full domain)
    for izone in plotDomains:
        
        # Setup figure dimensions
        nrows,ncols,figsize=plop.setupFig(plottype,members,pars,exp)
        
        # Initialize a figure handle
        fig,ax=plop.initFig(data[0,0],nrows,ncols,figsize)

        # Call main plotting routine
        plop.plotMain(fig,ax,data,plottype,masked,scalesMatched,monoColor=False,\
                      dExtra=dextra,subZone=izone,manualBounds=manualBounds,\
                      spgPattern=spgPattern,t=t,level=level,date=date,exp=exp,\
                      printLog=printLog)

        # Save the figure
        plop.saveFig(fig,figName,expName,date,t,level,exp,izone)
        


        
##############################################################################
# MAIN
#
def mainOld():

    # If manualBounds are asked from table, use this
    # logical to do it again for different fc lengths
    # (the same manualBounds otherwise used for all fc len)
    #
    reset=False
    
    for time in t:
        for level in levels:
            # If requsted, get boundary values from table
            #
            global manualBounds
            if manualBounds=="getFromTable" or reset:
                manualBounds=dope.setPredefinedBounds(date,time,pars,plottype)
                reset=True

            # Call main operation execution
            #
            mainOper(level,dpath,exp,date,time,members,pars,plottype,\
                     scalesMatched,fixNegData,masked,hardMaskId,\
                     plotDomains,manualBounds,figName,expName)

def main(lCase,cnf):
    
    levels,dpath,exp,date,t,members,pars,plottype,scalesMatched,\
    fixNegData,masked,hardMaskId,plotDomains,manualBounds,\
    figName,expName,spgPattern=dope.tomlToFuncNew(lCase,cnf)

    # If manualBounds are asked from table, use this
    # logical to do it again for different fc lengths
    # (the same manualBounds otherwise used for all fc len)
    #
    reset=False
    
    for time in t:
        for level in levels:
            # If requsted, get boundary values from table
            #
            if manualBounds=="getFromTable" or reset:
                manualBounds=dope.setPredefinedBounds(date,time,pars,plottype)
                reset=True

            # Call main operation execution
            #
            mainOper(level,dpath,exp,date,time,members,pars,plottype,\
                     scalesMatched,fixNegData,masked,hardMaskId,\
                     plotDomains,manualBounds,figName,expName,\
                     spgPattern,printLog=False)      

    
##########################################################
# Call initialization
#
if ccase:
    cnf = dope.init(ccase)
    from mycase import *

    mainOld()

    
if not ccase:
    cnf = dope.init("",tomlCase=tomlCase)
    
    #listCases=dope.constructCases(cSelection,cnf)
    listCases=dope.constructCasesNew(cnf)
    
    print()
    for item in listCases:
        print(item)
    print()

    try:
        parallel=cnf['run']['Main']['parallel']
    except:
        parallel=False

    if not parallel:
        for iCase in listCases:

            main(iCase,cnf)

    else:
        try:
            pool=mp.Pool(processes=cnf['run']['parallelProcesses'])
        except:
            pool=mp.Pool(processes=2)

        #pool.starmap_async(main,zip(listCases,itertools.repeat(cnf)))
        
        for _ in tqdm.tqdm(pool.istarmap(main,zip(listCases,itertools.repeat(cnf))),total=len(listCases)):
            pass

        pool.close()
        pool.join()
    
    quit()

#######################################
# OLD VERSION
#######################################

# Generate one plot for each level and forecast length specified
if not parallel:

    # If manualBounds are asked from table, use this
    # logical to do it again for different fc lengths
    # (the same manualBounds otherwise used for all fc len)
    #
    reset=False
    
    for time in t:
        for level in levels:
            # If requsted, get boundary values from table
            if manualBounds=="getFromTable" or reset:
                manualBounds=dope.setPredefinedBounds(date,time,pars,plottype)
                reset=True

            mainOper(level,dpath,exp,date,time,members,pars,plottype,\
                     scalesMatched,fixNegData,masked,hardMaskId,\
                     plotDomains,manualBounds,figName,expName)

else:
    # Currently only levels parallelized
    for time in t:
        pool=mp.Pool(poolSize)
        print(levels,pool)

        pool.map_async(partial(mainOper,dpath=dpath,exp=exp,date=date,t=time,\
                               members=members,pars=pars,plottype=plottype,\
                               scalesMatched=scalesMatched,fixNegData=fixNegData,\
                               masked=masked,\
                               hardMaskId=hardMaskId,plotDomains=plotDomains,\
                               manualBounds=manualBounds,\
                               figName=figName,expName=expName),\
                       levels)
        pool.close()
        pool.join()



