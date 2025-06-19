#!/usr/bin/env python
import epygram
import numpy as np
#import copy
import matplotlib.pyplot as plt
import matplotlib.colors as colors

#import warnings
#warnings.filterwarnings("ignore",category=np.VisibleDeprecationWarning)

#epygram.init_env()

##########################################################
# Functions
#
def setupFig(plottype,members,pars,exp):
    
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

    return nrows,ncols,figsize

########################################################
def createFig(rows,cols,figsize,proj):
    # Create matplotlib subplot handle
    #
    fig,ax=plt.subplots(nrows=rows,ncols=cols,figsize=figsize,\
                        subplot_kw={'projection': proj})

    #plt.subplots_adjust(hspace=0.5,wspace=0.15)
    
    return fig,ax

########################################################
def initFig(data,nrows,ncols,figsize):
    # Init figure handles

    fig,ax=createFig(nrows,ncols,figsize,data.geometry.default_cartopy_CRS())

    return fig,ax


########################################################
def saveFig(fig,figName,expName,date,t,level,exp,izone):
    # Save figure

    # Create figure name if not given
    if not figName:
        figName=expName+"_"+date+"_+"+t+"h"+"_lev"+str(level)+"_"\
            +exp[0]+"_domain"+str(izone)+".png"

    # Full domain save
    if izone==0:
        fig.savefig("fig/"+figName,\
                    pad_inches=0.5,bbox_inches='tight')
        
    # Sub-domain save, padding messed up due to "cropping"
    else:
        fig.savefig("fig/"+figName)

    plt.close(fig)

########################################################
def plotMain(fig,ax,data,plottype,masked,scalesMatched,monoColor,\
             dExtra=[],subZone=0,manualBounds=[],spgPattern=False,\
             t='N',level='NaN',date='NaN',exp='NaN',printLog=True):
    # Plot option for plotting multiple members for a chosen
    # variable/level array.
    #
    # Plotting from AllData
    #
    
    # LOG
    if printLog:
        print("Plotting   fc+",t, "on level" ,str(level),"izone",subZone,\
              "    ",date,exp)

    # Unroll over the dimensions indicated by dim
    for i in range(0,data.shape[0]):
        for j in range(0,data.shape[1]):

            # Choose plot options according to plottype
            if plottype == "multiMember":
                if monoColor:
                    # Special treatment for radar case
                    plot_in_fig2(fig,ax[i,j],data[i,j],dataBounds=[manualBounds[j]],subZone=subZone,\
                                 inum=j)
                    #plot_in_fig2(fig,ax[i],data[i,j],dataBounds=manualBounds,subZone=subZone,\
                    #             inum=j)
                    
                else:
                    colmap='plasma'
                    if not scalesMatched:
                        dataBounds=[]
                    else:
                        dataBounds=[dExtra[j]]

                        if spgPattern:
                            dataBounds=manualBounds[j]
                            colmap='RdBu_r'
                            
                        elif manualBounds:
                            dataBounds=[manualBounds[0][j]]
                                        
                    #plot_in_fig(fig,ax[i,j],data[i,j],scalesMatched=True,dataBounds=[0,dExtra[j]])
                    #plot_in_fig(fig,ax[i],data[i,j],scalesMatched=True,dataBounds=manualBounds)
                    plot_in_fig(fig,ax[i,j],data[i,j],colmap=colmap,scalesMatched=scalesMatched,\
                                masked=masked,\
                                dataBounds=dataBounds,subZone=subZone,spgPattern=spgPattern)
                        
                #else:
                #    plot_in_fig(fig,ax[i,j],data[i,j])
                    
            elif plottype == "multiMemberDiff":
                if i==0:
                    if manualBounds:
                        plot_in_fig(fig,ax[i,j],data[i,j],dataBounds=[manualBounds[0][j]],subZone=subZone)
                    else:
                        plot_in_fig(fig,ax[i,j],data[i,j],subZone=subZone)

                else:
                    if not scalesMatched:
                        dataBounds=[]
                    else:
                        dataBounds=[dExtra[0][j],dExtra[1][j]]
                        if manualBounds:
                            dataBounds=[manualBounds[1][j],-1*manualBounds[1][j]]

                    plot_in_fig(fig,ax[i,j],data[i,j],colmap='RdBu_r',center=True,\
                                scalesMatched=scalesMatched,masked=masked,dataBounds=dataBounds,\
                                subZone=subZone)

            elif plottype == "multiMemberDiff2":
                if i==0:
                    plot_in_fig(fig,ax[i,j],data[i,0],dataBounds=[3*10**-5])

                else:
                    if not scalesMatched:
                        dataBounds=[]
                    else:
                        dataBounds=[dExtra[0][j],dExtra[1][j]]           

                    plot_in_fig(fig,ax[i,j],data[i,j],colmap='RdBu_r',center=True,\
                                scalesMatched=scalesMatched,masked=masked,dataBounds=dataBounds)

                        
            elif plottype == "multiMemberStd":
                if i==0:
                    plot_in_fig(fig,ax[i,j],data[i,j])
                elif i==1:
                    # Mean diff from ctrl
                    dDiff=data[i,j]-data[0,j]
                    if masked:
                        dataBounds=[dDiff.max(),dDiff.min()]
                    else:
                        dataBounds=[]
                        
                    plot_in_fig(fig,ax[i,j],dDiff,colmap="RdBu_r",center=True,\
                                masked=masked,dataBounds=dataBounds)
                else:
                    if masked:
                        dataBounds=[data[i,j].max()]
                    else:
                        dataBounds=[]

                    print(dataBounds)
                        
                    plot_in_fig(fig,ax[i,j],data[i,j],colmap="Reds",center=True,\
                                masked=masked,dataBounds=dataBounds)
            
            elif plottype == "multiMemberStdMasked":
                if i==1:
                    plot_in_fig(fig,ax[i,j],data[i,j],colmap="RdBu",center=True)
                else:
                    plot_in_fig(fig,ax[i,j],data[i,j],colmap="Greens")


            elif plottype == "multiExpDiff":
                if i==0:
                    plot_in_fig(fig,ax[i,j],data[i,j],subZone=subZone)
                else:
                    if not scalesMatched:
                        dataBounds=[]
                    else:
                        dataBounds=[dExtra[0][j],dExtra[1][j]]
                        
                    plot_in_fig(fig,ax[i,j],data[i,j],colmap="RdBu_r",center=True,\
                                masked=masked,dataBounds=dataBounds,subZone=subZone)

            elif plottype == "multiExpStd":
                if i==0:
                    plot_in_fig(fig,ax[i,j],data[i,j],subZone=subZone)
                else:
                    if not scalesMatched:
                        dataBounds=[]
                    else:
                        dataBounds=[dExtra[0][j]]
                        
                    plot_in_fig(fig,ax[i,j],data[i,j],colmap="Reds",\
                                masked=masked,dataBounds=dataBounds,subZone=subZone)

    # LOG
    if printLog:
        print("Plotting   fc+",t, "on level",str(level),"izone",subZone,\
              "DONE",date,exp)
    
########################################################
def plot_in_fig(fig,ax,data,colmap='plasma',center=False,scalesMatched=False,masked=False,\
                dataBounds=[],subZone=0,spgPattern=False):
    # Use epygram cartopy function to plot the data
    #
    title="{0}\n Min{1} Max {2}\n Mean {3}".\
        format(data.fid['FA'],format(data.min(),'.3e'),\
        format(data.max(),'.3e'),format(data.mean(),'.3e'))
    
    if len(dataBounds)==0:
        data.cartoplot(fig=fig,ax=ax,colormap=colmap,center_cmap_on_0=center,title=title)

    else:
        if len(dataBounds)==1:
            # Try if the element contains two values. Used for fields that are
            # displaced w.r.t. to zero (e.g. temp in [K])
            try:
                minmax=(dataBounds[0][0],dataBounds[0][1])
            except:
                minmax=(0.,dataBounds[0])
        else:
            minmax=(dataBounds[1],dataBounds[0])

        if not masked:
            data.cartoplot(fig=fig,ax=ax,colormap=colmap,center_cmap_on_0=center,\
                           plot_method='contourf',\
                           contourf_kw={'extend':'both'},\
                           minmax=minmax,
                           title=title)

        else:
            if len(dataBounds)==1:
                # Modify the colormap to start from darker colors
                cmap=plt.cm.RdPu(np.linspace(0,1,20))
                cmap=colors.ListedColormap(cmap[14:,:-1])

                # Create a white color to start of the colmap
                my_cmap=cmap(np.arange(cmap.N))
                my_cmap[:,-1]=np.linspace(0,1,cmap.N)

                my_cmap=colors.ListedColormap(my_cmap)
                
                colmap=my_cmap

                colorbounds=np.linspace(0,dataBounds[0],7)

                # Offscale smallest value
                colorbounds[1]=colorbounds[1]*0.1
                #colorbounds[2]=colorbounds[2]*0.5

                extend='max'
            else:
                if spgPattern:
                    
                    #norm=colors.DivergingNorm(vmin=dataBounds[0],vcenter=dataBounds[1],vmax=dataBounds[2])
                    norm=colors.TwoSlopeNorm(vmin=dataBounds[0],vcenter=dataBounds[1],vmax=dataBounds[2])
                    colorbounds=np.linspace(dataBounds[0],dataBounds[2],15)
                    if dataBounds[0] < 0.0:
                        extend='both'
                    else:
                        extend='max'
                        
                else:
                    absMin=min(dataBounds[0],-1*dataBounds[1])
                    colorbounds=np.linspace(-1*absMin,absMin,10)

                    # Offscale the innermost two values
                    colorbounds[4]=colorbounds[4]*0.4
                    colorbounds[5]=colorbounds[5]*0.4
                
                    extend='both'

            # Run spgPattern with additional norm arg
            if spgPattern:
                data.cartoplot(fig=fig,ax=ax,center_cmap_on_0=center,\
                               plot_method='contourf',\
                               contourf_kw={'extend':extend,'cmap':colmap, 'norm':norm},\
                               colorbounds=colorbounds,
                               title=title)
            else:
                data.cartoplot(fig=fig,ax=ax,center_cmap_on_0=center,\
                               plot_method='contourf',\
                               contourf_kw={'extend':extend,'cmap':colmap},\
                               colorbounds=colorbounds,
                               title=title)

    if subZone==1:
        ax.set_extent([14, 27, 54, 63])
    elif subZone==2:
        ax.set_extent([1, 14, 54, 63])
    elif subZone==3:
        ax.set_extent([14, 33, 63, 74])
    elif subZone==4:
        ax.set_extent([-4, 15, 63, 74])
    elif subZone==5:
        ax.set_extent([17, 30, 57, 66])
    elif subZone==6:
        ax.set_extent([1, 14, 56, 66])
    elif subZone==7:
        ax.set_extent([16, 18, 59, 63])
    #print(data.fid['FA'])

########################################################
def plot_in_fig2(fig,ax,data,colmap='plasma',center=False,scalesMatched=False,masked=False,dataBounds=[],subZone=0,inum=0):
    # Special case for radar phase
    
    # Use epygram cartopy function to plot the data
    #
    title="{0}\n Min{1} Max {2}\n Mean {3}".\
        format(data.fid['FA'],format(data.min(),'.3e'),\
        format(data.max(),'.3e'),format(data.mean(),'.3e'))

    colorbounds=np.linspace(0,dataBounds[0],6)

    # Generate monocolor colourpmaps
    if inum==0:
        colmap="Blues"
        cmap=plt.cm.Blues(np.linspace(0,1,18))
    elif inum==1:
        colmap="Greens"
        cmap=plt.cm.Greens(np.linspace(0,1,18))
    elif inum==2:
        colmap="Reds"
        cmap=plt.cm.Reds(np.linspace(0,1,18))
        
    # Modify the colormap to start from darker colors
    cmap=colors.ListedColormap(cmap[13:,:-1])

    # Create a white color to start of the colmap
    my_cmap=cmap(np.arange(cmap.N))
    my_cmap[:,-1]=np.linspace(0,1,cmap.N)
        
    my_cmap=colors.ListedColormap(my_cmap)
        
    colmap=my_cmap

    #data.cartoplot(fig=fig,ax=ax,colormap=colmap,center_cmap_on_0=center,\
    #               plot_method='contourf',\
    #               contourf_kw={'extend':'both'},\
    #               colorbounds=colorbounds,\
    #               minmax=minmax,
    #               title=title)
    data.cartoplot(fig=fig,ax=ax,center_cmap_on_0=center,\
                   plot_method='contourf',\
                   contourf_kw={'extend':'max','cmap':colmap},\
                   colorbounds=colorbounds,\
                   title=title)

    if subZone==1:
        ax.set_extent([14, 27, 54, 63])
    elif subZone==2:
        ax.set_extent([1, 14, 54, 63])
    elif subZone==3:
        ax.set_extent([14, 33, 63, 74])
    elif subZone==4:
        ax.set_extent([-4, 15, 63, 74])
    elif subZone==5:
        ax.set_extent([17, 30, 57, 66])
    elif subZone==6:
        ax.set_extent([1, 14, 56, 66])
    elif subZone==7:
        ax.set_extent([16, 18, 59, 63])
    #print(data.fid['FA'])
    
