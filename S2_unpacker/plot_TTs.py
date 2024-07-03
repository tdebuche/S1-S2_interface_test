import numpy as np
import math
import os
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from S2_unpacker.unpack_links import get_pTTs_from_links
from S2_unpacker.unpack_links import read_pTT_allocation
from S2_unpacker.read_EMP_file import read_allocation
from S2_unpacker.read_EMP_file import get_pTTs_from_EMPfile




def record_plot(event,args,title):
    data_links = event.pTT_packer
    reversed_pTT_allocation = read_pTT_allocation(args.Edges,args.Sector)
    energiesCEE,energiesCEH = get_pTTs_from_links(args,data_links,reversed_pTT_allocation)
    BinXY = create_bins(args)
    createplot(args,event,energiesCEE,BinXY,title+'CEE')
    createplot(args,event,energiesCEH,BinXY,title+'CEH')





def plot_EMPfile(args,EMPfile):
    pTT_allocation,TC_allocation = read_allocation(args.Edges,args.Sector)
    energiesCEE,energiesCEH = get_pTTs_from_EMPfile(args,EMPfile,pTT_allocation,TC_allocation)
    BinXY = create_bins(args)
    createplot(args,None,energiesCEE,BinXY,None)
    createplot(args,None,energiesCEH,BinXY,None)



def createplot(args,event,energies,BinXY,title):
    plt.figure(figsize = (20,8))
    X =[]
    Y = []
    pointXY = [[],[]]
    weights = []
    weightmax = 0
    etamax = 0
    phimax = 0
    for eta in range(len(BinXY)):
        for phi in range(len(BinXY[0])):
            X.append(BinXY[eta][phi][0][0])
            Y.append(BinXY[eta][phi][1][0])
            if energies[eta][phi] != 100000:
                weights.append(np.log(energies[eta][phi]+1))
                if  np.log(energies[eta][phi]+1) > weightmax:
                    weightmax = np.log(energies[eta][phi]+1)
                    etamax = eta
                    phimax = phi
            else : 
                weights.append(0)
            pointXY[0].append(np.sum(np.array(BinXY[eta][phi][0][0:4]))/4)
            pointXY[1].append(np.sum(np.array(BinXY[eta][phi][1][0:4]))/4)
    if weightmax == 0: weightmax = 1
    sc = plt.scatter(pointXY[0],pointXY[1],c=weights/max(weightmax,5), vmin=0)
    plt.colorbar(sc)
    res = 0 
    #colors = cm.get_cmap("viridis", 8)
    colors = white_viridis
    for eta in range(len(BinXY)):
        for phi in range(len(BinXY[0])):
            plt.plot(BinXY[eta][phi][0],BinXY[eta][phi][1],color = 'black')
            plt.fill(BinXY[eta][phi][0],BinXY[eta][phi][1],c = colors(weights[res]/max(weightmax,5)))
            res +=1
            #if energies[eta][phi] != 100000:
                #plt.annotate(str(round(energies[eta][phi],2)),(np.sum(np.array(BinXY[eta][phi][0][0:4]))/4,np.sum(np.array(BinXY[eta][phi][1][0:4]))/4))
    if event:
        x,y = etaphitoXY(event.eta_gen,event.phi_gen,1)
        if (event.phi_gen < np.pi) and (event.phi_gen > 0):
            plt.scatter(x,y,c = 'red', marker = 'x')
        eta_gen = str(round(event.eta_gen))
        phi_gen = str(round(event.phi_gen/np.pi * 180))
        pt_gen  = str(round(event.pT_gen))
        plt.title('Gen particule : '+args.particles+',eta=' + eta_gen+',phi='+phi_gen+',pt=' + pt_gen +',pt_cluster ='+str(round(energy_cluster)))
    energy_cluster = energycluster(energies,etamax,phimax)
    if args.Edges == 'yes': Edges = 'Edges'
    if args.Edges == 'no': Edges = 'No_Edges'
    if args.read_EMP == "no":
        plt.savefig('Results/plot_pTTs/'+args.pTT_version+'/'+Edges+'/'+args.particles+'/'+args.pileup+'/'+title +'.png')
    if args.read_EMP == "yes":
        plt.show()


def create_bins(args):
    Edges = args.Edges
    if Edges == 'yes': 
        nb_phi = 28 + 9
        phimin =-15 * np.pi/180
    else : 
        nb_phi = 24 + 6
        phimin =  0 * np.pi/180
    nb_phi = 36
    phimin =  0 * np.pi/180
    etamin = 1.305
    L = [[[]for phi in range(nb_phi)]for eta in range(20)]
    BinsXY =[[[]for phi in range(nb_phi)]for eta in range(20)] 
    for eta in range(20):
        for phi in range(nb_phi):
            vertices = np.array([[eta * np.pi/36 + etamin,(eta+1) * np.pi/36 + etamin,
                    (eta+1) * np.pi/36 + etamin,eta * np.pi/36 + etamin],
                   [phi * np.pi/36  + phimin,phi * np.pi/36 + phimin,
                    (phi+1) * np.pi/36 + phimin,(phi+1) * np.pi/36 + phimin]])
            verticesXY = etaphitoXY(vertices[0],vertices[1],1)
            BinsXY[eta][phi].append(verticesXY[0].tolist()+[verticesXY[0][0]])
            BinsXY[eta][phi].append(verticesXY[1].tolist()+[verticesXY[1][0]])
    return BinsXY
            

    
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

