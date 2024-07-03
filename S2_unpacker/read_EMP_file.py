import numpy as np
import math
import numpy as np
import xml.etree.ElementTree as ET
from collections import defaultdict
from S2_unpacker.tools import *


def read_allocation(Edges,Sector):
    if Edges == 'yes':
        tree = ET.parse('config_files/pTT_allocation/28_phi_bins/Allocation.xml')
    if Edges == 'no':
        tree = ET.parse('config_files/pTT_allocation/24_phi_bins/Allocation.xml')

        
    root = tree.getroot()
    pTT_allocation  = defaultdict(list)

    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id','pTT']):
                    frame  = int(frame_element.get('id'))
                    pTT     = frame_element.get('pTT')
                    if pTT :
                        n_link = 14 + 14*math.floor(channel/2) + S1_index
                        Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT)
                        pTT_allocation[(frame,n_link,channel%2)].append((Sector,S1Board,eta,phi,CEECEH))
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
                    if pTT :
                        if channel//2 == 4:
                            n_link =  S1_index
                        if channel//2 == 5:
                            n_link = 70 + S1_index
                        Sector,S1Board,eta,phi,CEECEH = get_pTT_numbers(pTT)
                        pTT_allocation[(frame,n_link,channel%2)].append((Sector,S1Board,eta,phi,CEECEH))
                    

        S1_index += 1


    
    tree = ET.parse('config_files/S1.ChannelAllocation.xml')
    root = tree.getroot()
    data_TC = defaultdict(list)
    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id', 'column', 'Module']):
                    frame  = int(frame_element.get('id'))
                    module = hex(int(frame_element.get('Module'),16))
                    n_link = 14 + 14*math.floor(channel/3) + S1_index
                    index  = int(frame_element.get('index'))
                    data_TC[(frame,n_link,channel%2)].append((module,index))
        S1_index += 1
    return pTT_allocation,data_TC


def get_pTTs_from_EMPfile(args,EMPfile,pTT_allocation,TC_allocation):
    Edges = args.Edges
    if Edges == 'yes': 
        nb_phi = 28
        offset = 3
    else : 
        nb_phi = 24
        offset = 0
    energiesCEE = [[0 for phi in range(36)]for eta in range(20)]
    energiesCEH = [[0 for phi in range(36)]for eta in range(20)]
    EMP_file = open(EMPfile, 'r')
    lines = EMP_file.readlines()
    EMP_file.close()
    EMP_data = []
    for line in lines:
        EMP_data.append(line.split())
    for frame_idx in range(1,len(EMP_data)):
        frame_element = EMP_data[frame_idx]
        frame_index =  int(frame_element[1])
        if frame_element[0] != 'Frame':
            print('not a frame element')
        if (len(frame_element)//2 - 1) != 84:
            print( 'not the true link number')
        for n_link in range(len(frame_element)//2-1):
            header = frame_element[2 + n_link *2]
            if (header != "1101" and frame_index == 0) or (header != "0001" and frame_index != 0 and frame_index != 107) or (header != "0011" and frame_index == 107):
                print('wrong header')
            word = frame_element[2 + n_link *2 + 1]
            for pTT_number in range(2):
                pTT_energy = get_pTT_energy(word,pTT_number)
                if pTT_energy < 0 :pTT_energy = 0
                if pTT_allocation[(frame_index,n_link,pTT_number)]:
                    Sector,S1Board,eta,phi,CEECEH = pTT_allocation[(frame_index,n_link,pTT_number)][0]
                    if CEECEH == 0: energiesCEE[eta][phi-offset + Sector*24] += pTT_energy
                    if CEECEH == 1: energiesCEH[eta][phi-offset + Sector*24] += pTT_energy
    print(energiesCEE,energiesCEH)
    return(energiesCEE,energiesCEH)
