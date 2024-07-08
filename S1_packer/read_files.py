
import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak

def read_xml():
    tree = ET.parse('config_files/S1.ChannelAllocation.xml')
    root = tree.getroot()
    reversed_data_si  = defaultdict(list)
    reversed_data_sci = defaultdict(list)

    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id', 'column', 'Motherboard']):
                    frame  = int(frame_element.get('id'))
                    column = int(frame_element.get('column'))
                    MB     = frame_element.get('Motherboard')
                    n_link = 14 + 14*math.floor(channel/3) + S1_index
                    index  = int(frame_element.get('index'))
                    reversed_data_sci[MB].append({'column' : column,
                                                  'frame'  : frame, 
                                                  'channel': channel, 
                                                  'n_link' : n_link,
                                                  'index'  : index})
                if all(attr in frame_element.attrib for attr in ['id', 'column', 'Module']):
                    frame  = int(frame_element.get('id'))
                    column = int(frame_element.get('column'))
                    module = hex(int(frame_element.get('Module'),16))
                    n_link = 14 + 14*math.floor(channel/3) + S1_index
                    index  = int(frame_element.get('index'))
                    reversed_data_si[module].append({'column' : column,
                                                     'frame'  : frame, 
                                                     'channel': channel, 
                                                     'n_link' : n_link,
                                                     'index'  : index})
        S1_index += 1
    return [reversed_data_si, reversed_data_sci]



def MB_geometry():
    tree = ET.parse('config_files/Geometry.xml')
    root = tree.getroot()
    result_dict = {}
    
    for plane in root.findall('.//Plane'):
        plane_id = int(plane.attrib['id'])
        if plane_id < 34: continue
        
        for motherboard in plane.findall('Motherboard'):
            motherboard_id = motherboard.attrib['id']
            
            for module in motherboard.findall('Module')[1:]:
                vertices = module.attrib.get('Vertices')
                if len(vertices.split(";")) > 4: break
                result_dict.setdefault(plane_id, {}).setdefault(int(module.attrib['v']), motherboard_id)
                break

    return result_dict




def read_allocation_pTTs(Edges,Sector,nb_links):
    if Edges == 'yes':
        if nb_links == 4:
            tree = ET.parse('config_files/pTT_allocation/28_phi_bins/Sector'+Sector+'/Allocation.xml')
        if nb_links == 2:
            tree = ET.parse('config_files/pTT_allocation/28_phi_bins/Sector'+Sector+'Duplication.xml')
    if Edges == 'no':
        if nb_links == 4:
            tree = ET.parse('config_files/pTT_allocation/24_phi_bins/Sector'+Sector+'Allocation.xml')
        if nb_links == 2:
            tree = ET.parse('config_files/pTT_allocation/24_phi_bins/Sector'+Sector+'Duplication.xml')
        
    root = tree.getroot()
    reversed_data_pTT  = defaultdict(list)

    S1_index = 0
    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            channel = int(channel_element.get('aux-id'))
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id','pTT']):
                    frame  = int(frame_element.get('id'))
                    pTT     = hex(int(frame_element.get('pTT'),16))
                    n_link =14*math.floor(channel/2) + S1_index
                    reversed_data_pTT[pTT].append({'frame'  : frame, 
                                                  'channel': channel, 
                                                  'n_link' : n_link,})

        S1_index += 1
    return reversed_data_pTT

