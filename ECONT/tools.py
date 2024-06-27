import json
from collections import defaultdict
# create list with HD or LD module item
def create_list_HDorLD(args):
  with open('config_files/Geometry/'+args.pTT_version+'/Modules.json','r') as file:
    Modules = json.load(file)

  HDorLD = defaultdict(list)
  for layer in range(len(Modules)):
    for module_idx in range(len(Modules[layer])):
      module = Modules[layer][module_idx]
      if module["TCcount"] == 12:
        HDorLD[(layer+1,module["u"],module["v"])].append("HD")
      else :
        HDorLD[(layer+1,module["u"],module["v"])].append("LD")
  return HDorLD

# STC index from CELL coordinates
def get_STC_index(HDorLD,cell_u,cell_v):
  #LD
  if HDorLD == 'LD':
    if (cell_u <= cell_v) and (cell_u < 8):
      return 0
    if (cell_v > 7) and (cell_u >= 8):
      return 1
    if (cell_u > cell_v) and (cell_v <= 7):
      return 2
  #HD
  if HDorLD == 'HD':
    if (cell_v-cell_u >= 6) and (cell_u <= 5):
      return 0
    if (cell_v-cell_u >= 6) and (cell_u <= 11) and (cell_u > 5):
      return 1
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 6) and  (cell_u <= 11) and (cell_u > 5):
      return 2
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 6) and  (cell_u <= 5):
      return 3
    if (cell_v > 17) and  (cell_u > 17):
      return 4
    if (cell_v > 11) and (cell_v <= 17) and (cell_u > 17):
      return 5
    if (cell_v > 11) and (cell_v <= 17) and (cell_u > 11) and (cell_u <= 17):
      return 6
    if  (cell_v > 17) and (cell_u > 11) and (cell_u <= 17):
      return 7
    if (cell_v-cell_u < -6) and (cell_v <= 5):
      return 8
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -6) and (cell_v <= 5):
      return 9
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -6) and (cell_v <= 11) and (cell_v > 5):
      return 10
    if (cell_v-cell_u < -6) and (cell_v <= 11) and (cell_v > 5):
      return 11

# STC index from TRIGGER CELL coordinates
def get_STC_index_from_TC(HDorLD,cell_u,cell_v):
  #LD
  if HDorLD == 'LD':
    if (cell_u <= cell_v) and (cell_u <= 3):
      return 0
    if (cell_v >= 4) and (cell_u >= 4):
      return 1
    if (cell_u > cell_v) and (cell_v <= 3):
      return 2
  if HDorLD == 'HD':
    if (cell_v-cell_u >= 2) and (cell_u <= 1):
      return 0
    if (cell_v-cell_u >= 2) and (cell_u <= 3) and (cell_u > 1):
      return 1
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 2) and  (cell_u <= 3) and (cell_u > 1):
      return 2
    if (cell_v-cell_u >= 0) and (cell_v-cell_u < 2) and  (cell_u <= 1):
      return 3
    if (cell_v > 5) and  (cell_u > 5):
      return 4
    if (cell_v > 3) and (cell_v <= 5) and (cell_u > 5):
      return 5
    if (cell_v > 3) and (cell_v <= 5) and (cell_u > 3) and (cell_u <= 5):
      return 6
    if  (cell_v > 5) and (cell_u > 3) and (cell_u <= 5):
      return 7
    if (cell_v-cell_u <= -3) and (cell_v <= 1):
      return 8
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -2) and (cell_v <= 1):
      return 9
    if (cell_v-cell_u < 0) and (cell_v-cell_u >= -2) and (cell_v <= 3) and (cell_v > 1):
      return 10
    if (cell_v-cell_u < -2) and (cell_v <= 3) and (cell_v > 1):
      return 11
  print((HDorLD,cell_u,cell_v))

def Sector0(layer,u,v):
        if (layer <34) and (layer != 30) and (layer != 32) and (layer != 28):
            if (v-u > 0) and (v >= 0):
                return(True)
        if (layer >= 34) and (layer%2 == 0):
            if (v-u > 0) and (v > 0):
                return(True)
        if (layer >= 34) and (layer%2 == 1):
            if (v-u >= 0) and (v >= 0):
                return(True)
        if (layer == 28) or (layer == 30) or (layer == 32):
            if (u - 2*v <0) and (u+v >= 0):
                return(True)
        return False

def getuvsector(layer,u,v):
        if u == -999:
            return (u,v,0)
        if Sector0(layer,u,v):
            if (layer != 28) and (layer != 30) and (layer != 32): 
                return(v-u,v,0)
            else :
                if u >= 0:
                    return (v,u,0)
                else :
                    return(-u,v-u,0)
        else:
            if  (layer <34):
                u,v = -v,u-v
            if (layer >= 34) and (layer%2 == 0):
                u,v = -v+1,u-v+1
            if (layer >= 34) and (layer%2 == 1):
                u,v = -v-1,u-v-1
            if Sector0(layer,u,v):
                if (layer != 28) and (layer != 30) and (layer != 32): 
                    return(v-u,v,1)
                else:
                    if u >= 0:
                        return (v,u,1)
                    else :
                        return(-u,v-u,1)
                    
            else : 
                if  (layer <34):
                    u,v = -v,u-v
                if (layer >= 34) and (layer%2 == 0):
                    u,v = -v+1,u-v+1
                if (layer >= 34) and (layer%2 == 1):
                    u,v = -v-1,u-v-1
                if Sector0(layer,u,v):
                    if (layer != 28) and (layer != 30) and (layer != 32): 
                        return(v-u,v,2)
                    else :
                        if u >= 0:
                            return (v,u,2)
