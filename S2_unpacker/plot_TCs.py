import numpy as np
import math
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import json
from shapely.geometry import Polygon
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from S2_unpacker.unpack_python_links import get_pTTs_from_links
from S2_unpacker.unpack_EMP_file import get_pTTs_from_EMPfile
from mpl_toolkits.axes_grid1 import make_axes_locatable
from data_handle.tools import getuvsector

def getetaphi(phi,roverz):
    phi = phi - np.pi/6 #30 degree shift for Stage 2
    if phi < 0 : phi += 2*np.pi
    eta = -np.log(np.tan(np.arctan(roverz)/2))
    eta = int((eta-1.305)/(np.pi/36)) #1.305 offset
    phi = int(phi/(np.pi/36))%72 
    return(eta,phi)

def get_pTTs_from_TCs(args,event,Sector):
    TCs = event.ds_si
    CEE_TTs = [[0 for phi in range(24)]for eta in range(20)]
    CEH_TTs = [[0 for phi in range(24)]for eta in range(20)]
    for module_idx in range(len(TCs.good_tc_layer)):
        for TC_idx in range(len(TCs.good_tc_layer[module_idx])):
            eta,phi = getetaphi(TCs.good_tc_phi[module_idx][TC_idx],TCs.r_over_z[module_idx][TC_idx])
            sector = phi //24
            if sector == Sector and TCs.good_tc_layer[module_idx][0] < 27 and eta <20:
                CEE_TTs[eta][phi%24] += TCs.good_tc_pt[module_idx][TC_idx]
            if sector == Sector and TCs.good_tc_layer[module_idx][0] >= 27and eta <20:
                CEH_TTs[eta][phi%24] += TCs.good_tc_pt[module_idx][TC_idx]
    return  CEE_TTs, CEH_TTs


def record_plot_TCs(event,args,title):

    if args.whole_endcap == 'no': #choose one sector or the whole endcap 
        #choose the link type
        if args.read_EMP == 'no': 
            CEE_TTs,CEH_TTs= get_pTTs_from_links(args,event,args.Sector)
        if args.read_EMP == 'yes':
            CEE_TTs,CEH_TTs= get_pTTs_from_EMPfile(args,args.Sector)

        #create one plot for the CEE one for the CEH
        createplot_single_sector(args,event,CEE_TTs,title+'CEE')
        createplot_single_sector(args,event,CEH_TTs,title+'CEH')


    if args.whole_endcap == 'yes':
        #choose the link type
        if args.read_EMP == 'no':
            S0_CEE_TTs,S0_CEH_TTs= get_pTTs_from_TCs(args,event,0)
            S1_CEE_TTs,S1_CEH_TTs= get_pTTs_from_TCs(args,event,1)
            S2_CEE_TTs,S2_CEH_TTs= get_pTTs_from_TCs(args,event,2)
            #create one plot for the CEE one for the CEH
            createplot_whole_endcap(args,event, S0_CEE_TTs, S1_CEE_TTs, S2_CEE_TTs,title+'CEE')
            createplot_whole_endcap(args,event, S0_CEH_TTs, S1_CEH_TTs, S2_CEH_TTs,title+'CEH')





def createplot_whole_endcap(args,event,S0_TTs, S1_TTs, S2_TTs,title):

    if args.Edges == 'yes':
        geojson_files = "config_files/Geometry/all_endcap_2028_Bins.json"
    if args.Edges == 'no':
        geojson_files = "config_files/Geometry/all_endcap_2024_Bins.json"
    with open(geojson_files, 'r') as f:
        bins = json.load(f)['Bins']

    fig,ax = plt.subplots(figsize=(11, 10))
    cmap = white_viridis 
    #norm = plt.Normalize(vmin=0, vmax=max(np.log(np.max(np.array([S0_TTs,S1_TTs,S2_TTs]))),np.log(5))) #logarithm scale
    norm = plt.Normalize(vmin=0, vmax=np.max(np.array([S0_TTs,S1_TTs,S2_TTs])))
    colorbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    colorbar.set_array([])

    for bin_index in range(len(bins)):
        eta = bins[bin_index]["S2_coordinates"]['eta_index']
        phi = bins[bin_index]["S2_coordinates"]['phi_index']
        #S1_Sector = bins[bin_index]["S1_Sectors"][0]
        S2_Sector = bins[bin_index]["S2_coordinates"]['Sector']
        bin_geometry = pointtopolygon([bins[bin_index]['verticesX'],bins[bin_index]['verticesY']])
        plt.plot(*bin_geometry.exterior.xy, color='black', linewidth=0.5)

        #plot sectors 
        if S2_Sector == 0 :
            #plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(np.log(S0_TTs[eta][phi]+1)))#logarithm scale
            plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(S0_TTs[eta][phi]))
            #plt.fill(*bin_geometry.exterior.xy, color='red') #if youn want to show the S2_Sector
        if S2_Sector == 1 :
            #plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(np.log(S1_TTs[eta][phi]+1))) #logarithm scale
            plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(S1_TTs[eta][phi]))
            #plt.fill(*bin_geometry.exterior.xy, color='green') #if youn want to show the S2_Sector
        if S2_Sector == 2 :
            #plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(np.log(S2_TTs[eta][phi]+1)))#logarithm scale
            plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(S2_TTs[eta][phi]))
            #plt.fill(*bin_geometry.exterior.xy, color='blue') #if youn want to show the S2_Sector
 
        # if you want to show the phi coordinates
        x,y = np.sum(np.array(bins[bin_index]['verticesX']))/4,np.sum(np.array(bins[bin_index]['verticesY']))/4
        if eta == 0 : 
            x,y = np.sum(np.array(bins[bin_index]['verticesX']))/4,np.sum(np.array(bins[bin_index]['verticesY']))/4
            #plt.annotate(phi,(x,y))


    #little function to find the energy maximum and return the energy sum on neighbour bins
    sect,etamax,phimax = np.unravel_index(np.array([S0_TTs,S1_TTs,S2_TTs]).argmax(), np.array([S0_TTs,S1_TTs,S2_TTs]).shape)
    pt_cluster = ptcluster(np.array([S0_TTs,S1_TTs,S2_TTs])[sect],etamax,phimax)

    if event: #basically it runs if the energies come from python links (so we can search in the rootfile the gen particle)
        x,y = etaphitoXY(event.eta_gen,event.phi_gen,1)
        plt.scatter(x,y,c = 'red', marker = 'x')
        eta_gen = str(round(event.eta_gen))
        phi_gen = str(round(event.phi_gen/np.pi * 180))
        energy_gen  = str(round(event.energy_gen))
        pt_gen  = str(round(event.pT_gen))
        plt.title('Gen particule nb '+str(event.event)+' : '+args.particles+',eta=' + eta_gen+',phi='+phi_gen+',pt_gen=' + pt_gen +',pt_cluster ='+str(round(pt_cluster)))
    else:
        plt.title('pt_cluster ='+str(round(pt_cluster)))

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.04)
    cbar=plt.colorbar(colorbar,cax = cax )
    cbar.set_label('pT (GeV)')


    if event:
        if args.Edges == 'yes': Edges = 'Edges'
        if args.Edges == 'no': Edges = 'No_Edges'
        plt.savefig('Results/plot_TTs/'+args.pTT_version+'/'+Edges+'/'+args.particles+'/'+args.pileup+'/'+title +'_whole_endcap.png')
        print("save " +'Results/plot_TTs/'+args.pTT_version+'/'+Edges+'/'+args.particles+'/'+args.pileup+'/'+title +'_whole_endcap.png')
    else:
        plt.savefig('Results/plot_TTs/from_EMP/'+title+'_whole_endcap.png')

    #plt.show()
    print('TC sum = ' + str(np.sum(np.array([S0_TTs,S1_TTs,S2_TTs]))))


def pointtopolygon(vertices):#convert vertex list to shapely ploygon
    points = []
    for i in range(len(vertices[0])):
        if vertices[0][i]!= 0 or vertices[1][i] != 0:
            points.append((vertices[0][i],vertices[1][i]))
    return(Polygon(points))

    
def etaphitoXY(eta,phi,z): #to plot gen particle 
    x = z * np.tan(2*np.arctan(np.exp(-eta))) * np.cos(phi)
    y = z * np.tan(2*np.arctan(np.exp(-eta))) * np.sin(phi)
    return(x,y)



def ptcluster(energies,etamax,phimax): #to have an idea of the energy of the particle 
    energy = 0
    for i in range(-2,3):
        for j in range(-2,3):
            if (etamax+i)>= 0 and (etamax+i) < len(energies):
                if (phimax+j)>=0 and (phimax+j)< len(energies[etamax+i]):
                    energy += energies[etamax+i][phimax+j]
    return energy

white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    (0,    '#ffffff'),
    (1e-10,'#440053'),
    (0.2,  '#404388'),
    (0.4,  '#2a788e'),
    (0.6,  '#21a784'),
    (0.8,  '#78d151'),
    (1,    '#fde624'),
], N=1000)
