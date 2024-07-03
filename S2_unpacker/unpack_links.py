import numpy as np
import math
import numpy as np
import xml.etree.ElementTree as ET
from collections import defaultdict
from S2_unpacker.tools import *



def read_pTT_allocation(Edges,Sector):
    if Edges == 'yes':
        tree = ET.parse('config_files/pTT_allocation/28_phi_bins/Allocation.xml')
    if Edges == 'no':
        tree = ET.parse('config_files/pTT_allocation/24_phi_bins/Allocation.xml')

        
    root = tree.getroot()
    data_pTT  = defaultdict(list)

    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id','pTT']):
                    frame  = int(frame_element.get('id'))
                    pTT     = frame_element.get('pTT')
                    n_link = 14 + 14*math.floor(channel/2) + S1_index
                    Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT)
                    data_pTT[(Sector,S1Board,eta,phi,CEECEH )].append((frame,n_link,channel%2))
        S1_index += 1

    
    if Edges == 'yes':
        tree = ET.parse('config_files/pTT_allocation/28_phi_bins/Duplication.xml')
    if Edges == 'no':
        tree = ET.parse('config_files/pTT_allocation/24_phi_bins/Duplication.xml')
        
    root = tree.getroot()

    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id','pTT']):
                    frame  = int(frame_element.get('id'))
                    pTT     = frame_element.get('pTT')
                    if channel//2 == 4:
                        n_link =  S1_index
                    if channel//2 == 5:
                        n_link = 70 + S1_index
                    Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT)
                    data_pTT[(Sector,S1Board,eta,phi,CEECEH )].append((frame,n_link,channel%2))
                    

        S1_index += 1
    return data_pTT


def get_pTTs_from_links(data_links,etaphi_links,args):
    Edges = args.Edges
    if Edges == 'yes': 
        nb_phi = 28
        offset = 3
    else : 
        nb_phi = 24
        offset = 0
        
    Sector = args.Sector
    energiesCEE = [[0 for phi in range(36)]for eta in range(20)]
    for S1Board in range(14):
        for eta in range(20):
            for phi in range(36):
                if etaphi_links[(Sector,S1Board,eta,phi+offset,0)] != []:
                    if data_links[etaphi_links[(Sector,S1Board,eta,phi+offset,0)][0]] != []:
                        energiesCEE[eta][phi] += data_links[etaphi_links[(Sector,S1Board,eta,phi+offset,0)][0]][0]
                        #energies[eta][phi] += 1
    for S1Board in range(14):
        for eta in range(20):
            for phi in range(36):
                if etaphi_links[(Sector+1,S1Board,eta,phi-24+offset,0)] != []:
                    if data_links[etaphi_links[(Sector+1,S1Board,eta,phi-24+offset,0)][0]] != []:
                        energiesCEE[eta][phi] += data_links[etaphi_links[(Sector+1,S1Board,eta,phi-24+offset,0)][0]][0]
                        #energies[eta][phi] += 1
    
    energiesCEH = [[0 for phi in range(36)]for eta in range(20)]
    for S1Board in range(14):
        for eta in range(20):
            for phi in range(36):
                if etaphi_links[(Sector,S1Board,eta,phi+offset,1)] != []:
                    if data_links[etaphi_links[(Sector,S1Board,eta,phi+offset,1)][0]] != []:
                        energiesCEH[eta][phi] += data_links[etaphi_links[(Sector,S1Board,eta,phi+offset,1)][0]][0]
                        #energies[eta][phi] += 1
    for S1Board in range(14):
        for eta in range(20):
            for phi in range(36):
                if etaphi_links[(Sector+1,S1Board,eta,phi-24+offset,1)] != []:
                    if data_links[etaphi_links[(Sector+1,S1Board,eta,phi-24+offset,1)][0]] != []:
                        energiesCEH[eta][phi] += data_links[etaphi_links[(Sector+1,S1Board,eta,phi-24+offset,1)][0]][0]
                        #energies[eta][phi] += 1
    return(energiesCEE,energiesCEH)
