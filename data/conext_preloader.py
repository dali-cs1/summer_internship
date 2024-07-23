import os
from contextializer import land_patch
import json as js
import rasterio
import numpy as np
import torch
import matplotlib.pyplot as plt
positions=[(71,45),(86,58),(55.5,61.5),(75.5,152),(85.5,43),(47,159),(60,140),(90,149),(47,174),(84.5,27),(69.5,170),(96.5,170),(71.5,58.5),(90.5,163.5),(73.0,91.5),(75,136.5),(44.5,128.5),(100,40),(88.5,86.5),(75,122),(57,78.5),(90,134),(100,102),(41.5,66.5),(98.5,24.5),(45,143.5),(73.5,106.5),(61.5,28.5),(99.5,33),(84.5,17.5),(76,166.5),(43.5,112.5),(45,135.5),(39.5,176),(89.5,14.5),(101.5,54.5),(42.5,81.5),(30,147.5),(76.5,21),(41.5,51.5),(101.5,70.5),(46,45),(43,99),(27,69.5),(43.5,90.5),(62,170),(90,117),(27,85),(100,86),(60,125),(32.5,62.5),(57,94.5),(59.5,109.5),(27.5,85),(29,116.5),(56.5,34.5),(28,101),(61,155),(87,73.5),(30,131.5)]

for i in os.listdir('C:/Users/moham/OneDrive/Bureau/summer_internship/data/grp2'):
    if len(os.listdir(os.path.join("C:/Users/moham/OneDrive/Bureau/summer_internship/data/grp2",i)))<3:
        cab, cw, scale = [], [], []
        props_path=os.path.join("C:/Users/moham/OneDrive/Bureau/summer_internship/data/grp2",i,"props.json")
        f = open(props_path, 'r')
        props = js.load(f)
        for j in range(60):
            cab.append(props[f"Cab{j}"])
            cw.append(props[f"Cw{j}"])
            scale.append(props[f"xscale{j}"])
        cab_patch, cw_patch = land_patch(positions, scale, cab, cw, np.zeros((128, 224)))
        patch = (np.zeros((2, 128, 224)).astype(np.float32))
        patch[0] = cab_patch
        patch[1] = cw_patch
        patch = torch.tensor(patch)
        torch.save(patch, os.path.join("C:/Users/moham/OneDrive/Bureau/summer_internship/data/grp2",i,'context.pt'))
        print(i)
