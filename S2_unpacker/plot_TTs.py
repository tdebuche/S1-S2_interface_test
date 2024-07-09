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



def record_plot(event,args,title):

    if args.whole_endcap == 'no':
        if args.read_EMP == 'no':
            CEE_TTs,CEH_TTs= get_pTTs_from_links(args,event,args.Sector)
        if args.read_EMP == 'yes':
            CEE_TTs,CEH_TTs= get_pTTs_from_EMPfile(args,args.Sector)

        createplot_single_sector(args,event,CEE_TTs,title+'CEE')
        #createplot_single_sector(args,event,CEH_TTs,title+'CEH')


    if args.whole_endcap == 'yes':
        if args.read_EMP == 'no':
            S0_CEE_TTs,S0_CEH_TTs= get_pTTs_from_links(args,event,0)
            S1_CEE_TTs,S1_CEH_TTs= get_pTTs_from_links(args,event,1)
            S2_CEE_TTs,S2_CEH_TTs= get_pTTs_from_links(args,event,2)
        if args.read_EMP == 'yes':
            S0_CEE_TTs,S0_CEH_TTs= get_pTTs_from_EMPfile(args,0)
            S1_CEE_TTs,S1_CEH_TTs= get_pTTs_from_EMPfile(args,2)
            S2_CEE_TTs,S2_CEH_TTs= get_pTTs_from_EMPfile(args,1)

        createplot_whole_endcap(args,event, S0_CEE_TTs, S1_CEE_TTs, S2_CEE_TTs,title+'CEE')
        #createplot_whole_endcap(args,event, S0_CEE_TTs, S1_CEH_TTs, S2_CEH_TTs,title+'CEH')



def createplot_single_sector(args,event,TTs,title):
    if args.Edges == 'yes':
        geojson_files = "config_files/Geometry/all_endcap_2028_Bins.json"
    if args.Edges == 'no':
        geojson_files = "config_files/Geometry/all_endcap_2024_Bins.json"

    with open(geojson_files, 'r') as f:
        bins = json.load(f)['Bins']

    fig,ax = plt.subplots(figsize=(11, 10))
    cmap = white_viridis
    #norm = plt.Normalize(vmin=0, vmax=max(np.log(np.max(np.array(TTs))),np.log(5)))
    norm = plt.Normalize(vmin=0, vmax=np.max(np.array(TTs)))
    colorbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    colorbar.set_array([])

    for bin_index in range(len(bins)):
        eta = bins[bin_index]["S2_coordinates"]['eta_index']
        phi = bins[bin_index]["S2_coordinates"]['phi_index']
        S2_Sector = bins[bin_index]["S2_coordinates"]['Sector']
        bin_geometry = pointtopolygon([bins[bin_index]['verticesX'],bins[bin_index]['verticesY']])
        if S2_Sector == args.Sector :
            plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(TTs[eta][phi]))
            #plt.fill(*bin_geometry.exterior.xy, color='red')
            #plt.annotate(phi,(bins[bin_index]['verticesX'][0],bins[bin_index]['verticesY'][0]))

        plt.plot(*bin_geometry.exterior.xy, color='black', linewidth=0.5)
    etamax,phimax = np.unravel_index(np.array(TTs).argmax(), np.array(TTs).shape)
    energy_cluster = energycluster(TTs,etamax,phimax)
    if event:
        x,y = etaphitoXY(event.eta_gen,event.phi_gen,1)
        plt.scatter(x,y,c = 'red', marker = 'x')
        eta_gen = str(round(event.eta_gen))
        phi_gen = str(round(event.phi_gen/np.pi * 180))
        pt_gen  = str(round(event.pT_gen))
        plt.title('Gen particule : '+args.particles+',eta=' + eta_gen+',phi='+phi_gen+',pt=' + pt_gen +',pt_cluster ='+str(round(energy_cluster)))
        if args.Edges == 'yes': Edges = 'Edges'
        if args.Edges == 'no': Edges = 'No_Edges'
        #plt.savefig('Results/plot_TTs/'+args.pTT_version+'/'+Edges+'/'+args.particles+'/'+args.pileup+'/'+title +'.png')
    else:
        plt.title('pt_cluster ='+str(round(energy_cluster)))
        #plt.savefig('Results/plot_TTs/from_EMP/'+title+'.png')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.04)
    plt.colorbar(colorbar,cax = cax )
    plt.show()



def createplot_whole_endcap(args,event,S0_TTs, S1_TTs, S2_TTs,title):
    if args.Edges == 'yes':
        geojson_files = "config_files/Geometry/all_endcap_2028_Bins.json"
    if args.Edges == 'no':
        geojson_files = "config_files/Geometry/all_endcap_2024_Bins.json"

    with open(geojson_files, 'r') as f:
        bins = json.load(f)['Bins']
    fig,ax = plt.subplots(figsize=(11, 10))
    cmap = white_viridis
    #norm = plt.Normalize(vmin=0, vmax=max(np.log(np.max(np.array([S0_TTs,S1_TTs,S2_TTs]))),np.log(5)))
    norm = plt.Normalize(vmin=0, vmax=np.max(np.array([S0_TTs,S1_TTs,S2_TTs])))
    colorbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    colorbar.set_array([])

    for bin_index in range(len(bins)):
        eta = bins[bin_index]["S2_coordinates"]['eta_index']
        phi = bins[bin_index]["S2_coordinates"]['phi_index']
        S2_Sector = bins[bin_index]["S2_coordinates"]["Sector"]
        bin_geometry = pointtopolygon([bins[bin_index]['verticesX'],bins[bin_index]['verticesY']])
        if S2_Sector == 0 :
            #plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(np.log(S0_TTs[eta][phi]+1)))
            plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(S0_TTs[eta][phi]))
            #plt.fill(*bin_geometry.exterior.xy, color='red')
        if S2_Sector == 1 :
            #plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(np.log(S1_TTs[eta][phi]+1)))
            plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(S1_TTs[eta][phi]))

            #plt.fill(*bin_geometry.exterior.xy, color='green')
        if S2_Sector == 2 :
            #plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(np.log(S2_TTs[eta][phi]+1)))
            plt.fill(*bin_geometry.exterior.xy, color=colorbar.to_rgba(S2_TTs[eta][phi]))

            #plt.fill(*bin_geometry.exterior.xy, color='blue')
     
        plt.plot(*bin_geometry.exterior.xy, color='black', linewidth=0.5)

    sect,etamax,phimax = np.unravel_index(np.array([S0_TTs,S1_TTs,S2_TTs]).argmax(), np.array([S0_TTs,S1_TTs,S2_TTs]).shape)
    energy_cluster = energycluster(np.array([S0_TTs,S1_TTs,S2_TTs])[sect],etamax,phimax)

    if event:
        x,y = etaphitoXY(event.eta_gen,event.phi_gen,1)
        if (event.phi_gen < np.pi) and (event.phi_gen > 0):
            plt.scatter(x,y,c = 'red', marker = 'x')
        eta_gen = str(round(event.eta_gen))
        phi_gen = str(round(event.phi_gen/np.pi * 180))
        pt_gen  = str(round(event.pT_gen))
        plt.title('Gen particule : '+args.particles+',eta=' + eta_gen+',phi='+phi_gen+',pt=' + pt_gen +',pt_cluster ='+str(round(energy_cluster)))
        if args.Edges == 'yes': Edges = 'Edges'
        if args.Edges == 'no': Edges = 'No_Edges'
        #plt.savefig('Results/plot_TTs/'+args.pTT_version+'/'+Edges+'/'+args.particles+'/'+args.pileup+'/'+title +'.png')

    else:
        plt.title('pt_cluster ='+str(round(energy_cluster)))
        #plt.savefig('Results/plot_TTs/from_EMP/wholeendcap'+title+'.png')

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.04)
    plt.colorbar(colorbar,cax = cax )
    plt.show()




def pointtopolygon(vertices):
    points = []
    for i in range(len(vertices[0])):
        if vertices[0][i]!= 0 or vertices[1][i] != 0:
            points.append((vertices[0][i],vertices[1][i]))
    return(Polygon(points))

    
def etaphitoXY(eta,phi,z):
    x = z * np.tan(2*np.arctan(np.exp(-eta))) * np.cos(phi)
    y = z * np.tan(2*np.arctan(np.exp(-eta))) * np.sin(phi)
    return(x,y)



def energycluster(energies,etamax,phimax):
    energy = 0
    for i in range(-1,2):
        for j in range(-1,2):
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

