#!/usr/bin/env python
#
# EXAMPLE 3
#
# This example produces plots from two model levels
# of precipitating hydrometeors generated at that level.
# The use of field difference is demonstrated with the
# plottype multiMemberDiff functionality. This example
# will plot the control member fields and differences
# from the control member field of ensemble members 1+2.
#
#########################################################
# What to plot

date = '2023022012'
levels = [25,39]
pars = ['RAIN','GRAUPEL','SNOW']
members = [0,1,2]
t= ['03']

##########################################################
# Experiments
#
exp= ["spp_sp_icenu"]

expName="example3"

# Basename for figures
figName=expName+"_"+date

##########################################################
# Plotting options
#
# plottype: multiExpStd multiMember multiMemberDiff multiMemberStd multiExpDiff

plottype="multiMemberDiff"

# Include control member in the plots
includeRef=True

# Plot monocolor contourfs (setup for only 3 fields currently)
# only activated for "multiMember" and setup for only 3 fields currently
monoColor=False
    
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
parallel=True
poolSize=2

