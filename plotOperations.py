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

def create_fig(rows,cols,figsize,proj):
    # Create matplotlib subplot handle
    #
    fig,ax=plt.subplots(nrows=rows,ncols=cols,figsize=figsize,\
                        subplot_kw={'projection': proj})

    #plt.subplots_adjust(hspace=0.5,wspace=0.15)
    
    return fig,ax

########################################################
def init_fig2(data,nrows,ncols,figsize):
    # Init figure handles

    fig,ax=create_fig(nrows,ncols,figsize,data.geometry.default_cartopy_CRS())

    return fig,ax

########################################################
def plot_multi_member3(fig,ax,data,plottype,masked,scalesMatched,monoColor,dExtra=[],\
                       subZone=0,manualBounds=[]):
    # Plot option for plotting multiple members for a chosen
    # variable/level array.
    #
    # Plotting from AllData
    #
    
    # Unroll over the dimensions indicated by dim
    for i in range(0,data.shape[0]):
        for j in range(0,data.shape[1]):

            # Choose plot options according to plottype
            if plottype == "multiMember":
                if monoColor:
                    # Special treatment for radar case
                    plot_in_fig2(fig,ax[i,j],data[i,j],dataBounds=manualBounds,subZone=subZone,\
                                 inum=j)
                    
                elif scalesMatched:
                    plot_in_fig(fig,ax[i,j],data[i,j],scalesMatched=True,dataBounds=[dExtra[j]])
                        
                else:
                    plot_in_fig(fig,ax[i,j],data[i,j])
                    
            elif plottype == "multiMemberDiff":
                if i==0:
                    if manualBounds:
                        plot_in_fig(fig,ax[i,j],data[i,j],dataBounds=[manualBounds[0]],subZone=subZone)
                    else:
                        plot_in_fig(fig,ax[i,j],data[i,j],subZone=subZone)

                else:
                    if not scalesMatched:
                        dataBounds=[]
                    else:
                        dataBounds=[dExtra[0][j],dExtra[1][j]]
                        if manualBounds:
                            dataBounds=[manualBounds[1],-1*manualBounds[1]]

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
                        
                    plot_in_fig(fig,ax[i,j],data[i,j],colmap="Reds_r",\
                                masked=masked,dataBounds=dataBounds,subZone=subZone)

    
########################################################
def plot_in_fig(fig,ax,data,colmap='plasma',center=False,scalesMatched=False,masked=False,dataBounds=[],subZone=0):
    # Use epygram cartopy function to plot the data
    #
    title="{0}\n Min{1} Max {2}\n Mean {3}".\
        format(data.fid['FA'],format(data.min(),'.3e'),\
        format(data.max(),'.3e'),format(data.mean(),'.3e'))

    if len(dataBounds)==0:
        data.cartoplot(fig=fig,ax=ax,colormap=colmap,center_cmap_on_0=center,title=title)

    else:
        if len(dataBounds)==1:
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
                absMin=min(dataBounds[0],-1*dataBounds[1])
                colorbounds=np.linspace(-1*absMin,absMin,10)

                # Offscale the innermost two values
                colorbounds[4]=colorbounds[4]*0.4
                colorbounds[5]=colorbounds[5]*0.4
                
                extend='both'

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
    #print(data.fid['FA'])
    
