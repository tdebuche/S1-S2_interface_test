import xml.etree.ElementTree as ET
from collections import defaultdict
import math
import numpy as np
import awkward as ak

def get():
    tree = ET.parse('config_files/S1.ChannelAllocation.xml')
    root = tree.getroot()
    
    nb_selected_TCs = defaultdict(list)

    for s1_element in root.findall('.//S1'):
        for channel_element in s1_element.findall('.//Channel'):
            for frame_element in channel_element.findall('.//Frame'):
                if all(attr in frame_element.attrib for attr in ['id', 'column', 'Module']):
                    module = hex(int(frame_element.get('Module'),16))
                    index  = int(frame_element.get('index'))
                    
                    if not nb_selected_TCs[module]:
                        nb_selected_TCs[module].append(0)
                        
                    nb_selected_TCs[module][0] += 1
                    
    return nb_selected_TCs
    
