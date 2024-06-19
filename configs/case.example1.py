#!/usr/bin/env python
#
# EXAMPLE 1
#
# Load data from a single experiment (needs the experiment
# data to be present for ensemble members specified, in
# this setup 1-3). Plot solid water hydrometeor count and
# raw and scaled SPP pattern present for model levels 20
# and 57. Note, plotting for multiple forecast lengths
# requires those FA files to be present.
#
#########################################################
# What to plot

date = '2023022012'
levels = [20,57]
pars = ['SOLID_WATER','SPP_PATTERN1','SPP_PATTERN2']
members = [1,2,3]
t= ['03']

##########################################################
# Experiments
#
exp= ["spp_sp_icenu"]

expName="example1"

# Basename for figures
figName=expName+"_"+date

##########################################################
# Plotting options
#
# plottype: multiExpStd multiMember multiMemberDiff multiMemberStd multiExpDiff

plottype="multiMember"

# Include control member in the plots
includeRef=False

# Plot monocolor contourfs (setup for only 3 fields currently)
# only activated for "multiMember" and setup for only 3 fields currently
monoColor=False
    
# Match colour scales between columns
scalesMatched=False

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
    
# Bring forth small data values
masked=False

# If set, reduce numerical value of fields outside of predefined lat-lon-box
# to zero. This is to set the fields max/min values correctly for the plotting
# of the subsection. predefined fields are set in dataOperations. 
# 'Fin' 'Nor'
hardMaskId=""
    
# There are some negative values for Real+ fields, fix these to 0
fixNegData=False 

# Additional tag to include after name string (figName+lev+addName)
addName="" 

# Use mpool to plot the figures with multiple cpus
parallel=False
poolSize=4

