import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
from data_handle.tools import compress_value, printProgressBar, getuvsector,get_module_id,etaphitoXY
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import awkward as ak
from collections import defaultdict
import mpl_toolkits.mplot3d.art3d as art3d
from shapely.geometry import Polygon
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
teta = np.pi/6
Modules_to_plot = [(1,'silicon',5,5),(3,'silicon',5,5),(5,'silicon',5,5),(7,'silicon',5,5),(9,'silicon',5,5)]
        
        
def plot_modules(args,event):
    eta_gen, phi_gen = event.eta_gen,event.phi_gen
    x_gen,y_gen = etaphitoXY(eta_gen,phi_gen,3407) #Layer 13
    TCs = event.ds_si
    with open('config_files/Geometry/'+args.pTT_version+'/Modules.json','r') as file:
        Modules = json.load(file)
    if eta_gen < 0 or  phi_gen < 0 or phi_gen > 2*np.pi/3 : 
        print('event not good')
        return()
    # Create a new figure
    fig = plt.figure(figsize=(15,10))

    # Add a 3D subplot
    ax = plt.figure().add_subplot(projection='3d')
    #plt.xlabel('x (mm)')
    #plt.zlabel('y (mm)')
    #cmap = white_viridis
    cmap = cm.get_cmap("viridis", 256)
    norm = plt.Normalize(vmin=0, vmax=np.max(np.array(ak.flatten(TCs.good_tc_pt))))
    colorbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    colorbar.set_array([])

    
    for layer in range(27):
        if layer%2 == 0 or layer > 26 or layer < 5: continue    
        for module_idx in range(len(Modules[layer-1])):
            Module = Modules[layer-1][module_idx]
            Xvertices = np.array(Module ['verticesX'] + [Module ['verticesX'][0]]) 
            Yvertices = Module ['verticesY'] + [Module ['verticesY'][0]]
            if np.sqrt((np.sum(np.array(Xvertices[:-1]))/len(Xvertices[:-1])-x_gen)**2+(np.sum(np.array(Yvertices[:-1]))/len(Xvertices[:-1])-y_gen)**2) >200: continue
            z = [layer * 100 for i in range(len(Xvertices))]
            ax.plot(Xvertices,z,Yvertices,color = 'black',linewidth= 0.5)

    x_to_plot = []
    layer_to_plot = []
    y_to_plot = []
    pt_to_plot = []

    for idx in range(len(TCs.good_tc_layer)):
        for tc_idx in range(len(TCs.good_tc_layer[idx])):
            Layer = TCs.good_tc_layer[idx][tc_idx]
            pt =  TCs.good_tc_pt[idx][tc_idx]
            x,y = TCs.good_tc_x[idx][tc_idx],TCs.good_tc_y[idx][tc_idx]
            if Layer %2 == 0 or Layer > 26  or Layer < 5 : continue
            #ax.scatter(x*10,Layer * 100,y*10, color=colorbar.to_rgba(pt),s = 15)
            x_to_plot.append(x*10)
            layer_to_plot.append(Layer*100)
            y_to_plot.append(y*10)
            pt_to_plot.append(pt)

    x_to_plot = np.array(x_to_plot)
    y_to_plot = np.array(y_to_plot)
    layer_to_plot = np.array(layer_to_plot)
    pt_to_plot = np.array(pt_to_plot)


    x_to_plot = x_to_plot[ak.argsort(pt_to_plot)]
    y_to_plot = y_to_plot[ak.argsort(pt_to_plot)]
    layer_to_plot = layer_to_plot[ak.argsort(pt_to_plot)]
    pt_to_plot = ak.sort(pt_to_plot)


    ax.scatter(x_to_plot,layer_to_plot,y_to_plot,color=colorbar.to_rgba(pt_to_plot),s = 1, alpha=1.0)
    fig.colorbar(colorbar, ax = ax)    
    ax.set_facecolor("white")

    ax.set_xlim(0,1300)
    ax.set_ylim(600,2400)
    
    ax.set_zlim(0,1300)
    elevation_angle = 15
    azimuthal_angle = 345
    ax.view_init(elevation_angle, azimuthal_angle)
    #divider = make_axes_locatable(ax)
    #cax = divider.append_axes("right", size="5%", pad=0.04)
    #plt.colorbar(colorbar,cax = cax)
    ax.grid(False)
    plt.savefig("test_3D_TCs")
    print("save test_3D_TCs.png")


def plot_pTTs(args,event):

    eta_gen, phi_gen = event.eta_gen,event.phi_gen
    x_gen,y_gen = etaphitoXY(eta_gen,phi_gen,3407) #Layer 13
    if eta_gen < 0 or  phi_gen < 0 or phi_gen > 2*np.pi/3 : 
        print('event not good')
        return()

    pTT_data = event.ds_pTTs['CEE']['Sector0']
    pTTs = defaultdict(list)
    pt_scale = []
    Layers = [3,1,'no',9,7,13,17,25,23,15,19,21,5,11]
    for pTT_idx in range(len(pTT_data)):
        pTT = pTT_data[pTT_idx]['pTT_id']
        S1_Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT)
        layer =  Layers[S1Board]
        if CEECEH == 1 : continue
        pTTs[(layer,eta,phi)].append(pTT_data[pTT_idx]['energy'])
        pt_scale.append(pTT_data[pTT_idx]['energy'])
    with open('config_files/Geometry/'+args.pTT_version+'/Modules.json','r') as file:
        Modules = json.load(file)
    with open('config_files/Geometry/2028_Bins.json','r') as file:
        Bins = json.load(file)['Bins']

    # Create a new figure
    fig = plt.figure(figsize=(15,10))

    # Add a 3D subplot
    ax = plt.figure().add_subplot(projection='3d')
    #plt.xlabel('x (mm)')
    #plt.zlabel('y (mm)')
    #cmap = white_viridis
    cmap = cm.get_cmap("viridis", 256)
    cmap =white_viridis
    norm = plt.Normalize(vmin=0, vmax=np.max(np.array((pt_scale))))
    colorbar = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    colorbar.set_array([])

    
    for layer in range(27):
        if layer%2 == 0 or layer > 26 or layer < 5: continue    
        for module_idx in range(len(Modules[layer-1])):
            Module = Modules[layer-1][module_idx]
            Xvertices = np.array(Module ['verticesX'] + [Module ['verticesX'][0]]) 
            Yvertices = Module ['verticesY'] + [Module ['verticesY'][0]]
            if np.sqrt((np.sum(np.array(Xvertices[:-1]))/len(Xvertices[:-1])-x_gen)**2+(np.sum(np.array(Yvertices[:-1]))/len(Xvertices[:-1])-y_gen)**2) >200: continue
            z = [layer * 100 for i in range(len(Xvertices))]
            ax.plot(Xvertices,z,Yvertices,color = 'black',linewidth= 0.4,alpha = 1)

    for layer in range(27):
        if layer%2 == 0 or layer > 26 or layer < 5: continue    
        for bin_idx in range(len(Bins[layer-1])):
            Bin = Bins[layer-1][bin_idx]
            Xvertices = np.array(Bin['verticesX'] + [Bin['verticesX'][0]]) 
            Yvertices = Bin['verticesY'] + [Bin['verticesY'][0]]
            eta,phi =  Bin['eta_index'],Bin['phi_index']
            pt = pTTs[(layer,eta,phi)][0]
            if np.sqrt((np.sum(np.array(Xvertices[:-1]))/len(Xvertices[:-1])-x_gen)**2+(np.sum(np.array(Yvertices[:-1]))/len(Xvertices[:-1])-y_gen)**2) >200: continue
            z = layer * 100
            ax.add_collection3d(Poly3DCollection([np.array([[Xvertices[i],z,Yvertices[i]] for i in range(len(Xvertices))])], facecolor=colorbar.to_rgba(pt),alpha = 0.8,edgecolor = 'black',linewidth = 0.4))
            ax.plot(Xvertices,[layer * 100 for i in range(len(Xvertices))],Yvertices,color = 'black',linewidth= 0.4,alpha = 1)
        
            #ax.add_patch(Poly3DCollection([np.array([[Xvertices[i],Yvertices[i],z] for i in range(len(Xvertices))])],facecolor='red'))
            #art3d.pathpatch_2d_to_3d(plt.Polygon([np.array([[Xvertices[i],Yvertices[i],z] for i in range(len(Xvertices))])],facecolor='red'), z=z, zdir="x") #colorbar.to_rgba(pt)
            #art3d.pathpatch_2d_to_3d(Xvertices,Yvertices, z =z, zdir="x")



    fig.colorbar(colorbar, ax = ax)    
    ax.set_facecolor("white")

    ax.set_xlim(0,1300)
    ax.set_ylim(600,2400)
    
    ax.set_zlim(0,1300)
    elevation_angle = 15
    azimuthal_angle = 345
    ax.view_init(elevation_angle, azimuthal_angle)
    #divider = make_axes_locatable(ax)
    #cax = divider.append_axes("right", size="5%", pad=0.04)
    #plt.colorbar(colorbar,cax = cax)
    ax.grid(False)

    plt.savefig("test_3D_ptt")
    print("save test_3D_ptt.png")



def get_pTT_numbers(pTT): #get pTT information from the pTT id
    S1Board = int(pTT,16) >> 16 & 0x3F
    phi = int(pTT,16) & 0x1F
    eta = int(pTT,16)>> 5 & 0x1F
    CEECEH = int(pTT,16)>>10 & 0x1
    S1_Sector = int(pTT,16) >> 29 & 0x3
    return(S1_Sector,S1Board,eta,phi,CEECEH)





white_viridis = LinearSegmentedColormap.from_list('white_viridis', [
    (0,    '#ffffff'),
    (1e-10,'#440053'),
    (0.2,  '#404388'),
    (0.4,  '#2a788e'),
    (0.6,  '#21a784'),
    (0.8,  '#78d151'),
    (1,    '#fde624'),
], N=1000)

