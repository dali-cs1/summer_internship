#%%
import sys
def extract_size_from_config(content):
    
    size_match = re.search(r'Size=(\d+)\s+(\d+)', content)
    if size_match:
        columns = int(size_match.group(1))
        rows = int(size_match.group(2))
        print(f"Extracted Size: Columns={columns}, Rows={rows}")
        return columns, rows
    else:
        raise ValueError("Size not found in the configuration file")
#%%
import matplotlib.pyplot as plt
import numpy as np
import os
from PIL import Image
import json
import shutil
import rasterio
import re
np.seterr(divide='ignore', invalid='ignore')

index_angle = [1, 8, 9, 10, 11, 12, 13, 25, 26, 27, 28, 29]  #

pathsim = "C:/DART/user_data/simulations/Simulation_monastir5_2parc/sequence"  # l'emplacement des sequences
pathsavesim = f"C:/Users/moham/OneDrive/Bureau/summer_internship/data/grp2/{sys.argv[1]}"
lst = os.listdir(pathsim)

nbreseq = len(lst)

props_dict = dict()

for dir in lst:
    savedirectory = pathsavesim + dir
    if os.path.exists(savedirectory):
        shutil.rmtree(savedirectory)
    os.makedirs(savedirectory)

    g = open(pathsim + '/' + dir + '/output/dart.sequenceur.properties', 'r')
    contenu = g.read()
    caractere = "\n"
    x2 = contenu.split(caractere)
    
    for k in range(1, len(x2) - 1, 10):
        for i in range(0,10,2):
            prop = (x2[k+i].split(":")[1]).split(".")[-1]
            prop_value = float(x2[k +i + 1].split(":")[1])
            props_dict[prop + str((k // 10))] = prop_value

    with open(savedirectory + "/props.json", "w") as outfile:
        json.dump(props_dict, outfile)
    
    bands = ["BAND0","BAND1","BAND2","BAND3","BAND4","BAND5","BAND6","BAND7","BAND8","BAND9"]
    bands_arr = []
    
    for band in bands:
        band_folder = pathsim + '/' + dir + '/output/' + band + '/BRF/ITERX/IMAGES_DART'
        ima_prefixed = [filename for filename in os.listdir(band_folder) if filename.startswith("ima")]
        header_name = [filename for filename in ima_prefixed if filename.endswith("mpr")][0]

        with open(os.path.join(band_folder, header_name), "rb") as header_file:
            header_content = header_file.read().decode()  # Read and decode the content
            rows,columns = extract_size_from_config(header_content)
        
        header_file = open(os.path.join(band_folder, header_name), "rb")
        header_data = header_file.read()
        
        img_name = [filename for filename in ima_prefixed if filename.endswith("mp#")][0]
        img_data = np.fromfile(os.path.join(band_folder, img_name), dtype=np.double)
        print(band,' ',min(img_data),' ',max(img_data))
        img_data = np.reshape(img_data, (rows, columns))
        #plt.figure()
        #plt.imshow(img_data, cmap='gray')
        #plt.title(band)
        #plt.show()
        
        img_data_16bit = (10000 * img_data).astype(np.uint16)
        bands_arr.append(img_data_16bit)
    
    img_data_16bit_all_bands = np.array(bands_arr)
    imagename = savedirectory + "/" + dir + ".tif"
    
    with rasterio.open(imagename, 'w', driver='GTiff', height=img_data_16bit.shape[0], width=img_data_16bit.shape[1],
                       count=len(bands_arr), dtype=str(img_data_16bit.dtype)) as dst:
        for i in range(len(bands_arr)):
            dst.write(bands_arr[i], i + 1)

    
    src = rasterio.open(imagename)
    array=src.read()
    print(dir)
    '''
    for band in array:
        plt.figure()
        plt.imshow(band, cmap='gray')
        #plt.title(band)
        plt.show()
    '''
    print(np.max(array - img_data_16bit_all_bands))

#%%
g.close()
header_file.close()
src.close()