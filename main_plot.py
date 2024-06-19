#!/usr/bin/env python
import epygram
import numpy as np
import matplotlib.pyplot as plt

from os import system, path

import multiprocessing as mp
from functools import partial

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

# Stored config files for specific verification cases. If blanc, define setup below.
#
#ccase='precipphase-diff.2023021712+30.finland'
#ccase='precipphase-diff.2022071512+24.baltic'
ccase='example6'
#ccase=''
if ccase:
    ccase="configs/case."+ccase+".py"

    if not path.exists(ccase):
        print("Config file not found, aborting...")
        exit()
    else:
        print("Using configs from: "+ccase)
        
    system("cp "+ccase+" mycase.py")

    from mycase import *

else:
    #########################################################
    # What to plot
    
    date = '2023022012'
    levels = [57]
    pars = ['SURFINSPLUIE','SURFINSNEIGE','SURFINSGRAUPEL']
    members = [2,3,4]
    t= ['03']

    ##########################################################
    # Experiments
    #
    exp= ["spp_sp_icenu_a120_small"]

    expName="fig_"+exp[0]

    # Basename for figures
    figName=expName+"_"+date

    ##########################################################
    # Plotting options
    #
    
    # plottype: multiExpStd multiMember multiMemberDiff multiMemberStd multiExpDiff
    plottype="multiMember"

    # Include control member in the plots
    includeRef=True

    # Plot monocolor contourfs
    # only activated for "multiMember" and setup for only 3 fields currently
    monoColor=True
    
    # Match colour scales between columns
    scalesMatched=True

    # Force bounds (otherwise calculated from the data max/min)
    # only available currently for the radar case
    manualBounds=[]

    # Option for generating plots from subzones within the main Domain
    # 0: main domain
    # 1: Baltic Sea
    # 2: Southern Norway, Denmark, North Sea
    # 3: Northern Finland + Sweden + Norway
    # 4: Norwegian Sea
    # 5: South Finland + Baltics, tighter zoom 
    # 6: South Norway, tighter zoom
    plotDomains=[0]
    
    # Depracated
    masked=True

    # If set, reduce numerical value of fields outside of predefined lat-lon-box
    # to zero. This is to set the fields max/min values correctly for the plotting
    # of the subsection. predefined fields are set in dataOperations.
    # 'Fin' 'Nor'
    hardMaskId=''

    # There are some negative values for Real+ fields, fix these to 0
    fixNegData=False 

    # Additional tag to include after name string (figName+lev+addName)
    addName=""

    # Use mpool to plot the figures with multiple cpus, only coded for
    # processing multiple levels simultaneously
    parallel=False
    poolSize=4
    

##########################################################
# Setup figures
#
if plottype=="multiMember" or plottype=="multiMemberDiff":
    nrows=len(members)
    ncols=len(pars)
    figsize=(5*ncols,5*nrows)

elif plottype=="multiMemberStd":
    nrows=3
    ncols=len(pars)
    figsize=(5*ncols,5*nrows)

elif plottype=="multiExpDiff" or plottype=="multiExpStd":
    nrows=len(exp)+1
    ncols=len(pars)
    figsize=(5*ncols,5*nrows)
    
else:
    nrows=7
    ncols=len(pars)
    figsize=(5*ncols,5*nrows)


# Try to autoscale everything based on data
#
plt.rc('font',size=0) #+(nrows*ncols)/4)
plt.rc('axes',titlesize=8) #+(nrows*ncols)/4)
plt.rc('ytick',labelsize=6) #+(nrows*ncols)/4)


##########################################################
# Functions
#
def main(level,dpath,exp,date,t,members,pars,plottype,scalesMatched,fixNegData,nrows,ncols,\
         figsize,masked,hardMaskId,plotDomains,manualBounds):

    # Load data
    #
    print("Processing level ",str(level))
    data,dextra=dope.main_data(dpath,exp,date,t,members,level,pars,plottype,scalesMatched,\
                               fixNegData,hardMaskId)
    print("Processing level ",str(level),"DONE")

    # Cycle through domains (0=full domain)
    for izone in plotDomains:
        print("Plotting   level ",str(level),"geozone num",izone)
    
        # Initialize a figure handle
        fig,ax=plop.init_fig2(data[0,0],nrows,ncols,figsize)

        # Call main plotting routine
        plop.plot_multi_member3(fig,ax,data,plottype,masked,scalesMatched,monoColor,\
                                dExtra=dextra,subZone=izone,manualBounds=manualBounds)
        
        # Full domain save
        if izone==0:
            fig.savefig("fig/"+figName+"_+"+t+"h"+"_lev"+str(level)+addName+"_subzone"+str(izone)+".png",\
                        pad_inches=0.5,bbox_inches='tight')
            
        # Sub-domain save, padding messed up due to "cropping"
        else:
            fig.savefig("fig/"+figName+"_+"+t+"h"+"_lev"+str(level)+addName+"_subzone"+str(izone)+".png")

        plt.close(fig)
        print("Plotting   level ",str(level),"geozone num",izone,"DONE")

##############################################################################

# One pdf page is 60Mb, dont understand what's causing this
#with PdfPages(figName+".pdf") as pdf:

# Generate one plot for each level specified
if not parallel:
    for time in t:
        for level in levels:
            main(level,dpath,exp,date,time,members,pars,plottype,scalesMatched,fixNegData,\
                 nrows,ncols,figsize,masked,hardMaskId,plotDomains,manualBounds)

else:
    # Currently only levels parallelized
    for time in t:
        pool=mp.Pool(poolSize)
        print(levels,pool)

        pool.map_async(partial(main,dpath=dpath,exp=exp,date=date,t=time,\
                               members=members,pars=pars,plottype=plottype,\
                               scalesMatched=scalesMatched,fixNegData=fixNegData,\
                               nrows=nrows,ncols=ncols,figsize=figsize,masked=masked,\
                               hardMaskId=hardMaskId,plotDomains=plotDomains,manualBounds=manualBounds),\
                       levels)
        pool.close()
        pool.join()
