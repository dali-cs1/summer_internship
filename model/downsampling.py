import matplotlib.pyplot as plt
import numpy as np
import os
import rasterio
import cv2


def bicubic_interpolation(img, scale_factor=0.33):
    # Convertir l'image en float32 pour OpenCV
    img_float = img.astype(np.float32)
    # Calculer et afficher la moyenne et l'écart-type de l'image originale
    #original_mean = np.mean(img)
    #original_std = np.std(img)
    #print(f"Original Image Stats - Mean: {original_mean:.2f}, Std: {original_std:.2f}")
    # Afficher l'image originale
    #fig, axes = plt.subplots(1, 4, figsize=(12, 4))
    #axes[0].imshow(img, cmap='gray')
    #axes[0].set_title("Original Image")
    #axes[0].axis('off')

    # Calculer la nouvelle taille de l'image après interpolation
    new_height = int(img.shape[0] * scale_factor)
    new_width = int(img.shape[1] * scale_factor)
    # Appliquer l'interpolation bicubique
    interpolated_img = cv2.resize(img_float, (new_width, new_height), interpolation=cv2.INTER_CUBIC)
    # Calculer et afficher la moyenne et l'écart-type de l'image originale
    #processed_mean = np.mean(interpolated_img)
    #processed_std = np.std(interpolated_img)
    #print(f"Interpolated Image Stats - Mean: {processed_mean:.2f}, Std: {processed_std:.2f}")
    # Afficher l'image interpolée avant la conversion
    #axes[1].imshow(interpolated_img, cmap='gray')
    #axes[1].set_title("Interpolated Image (Before Conversion)")
    #axes[1].axis('off')

    # Appliquer le traitement avant la conversion en uint16
    interpolated_img1 = np.maximum(interpolated_img, 0)
    interpolated_img1 = np.minimum(interpolated_img, 2 ** 16 - 1)
    interpolated_img1 = interpolated_img.astype(np.int16)
    # Calculer et afficher la moyenne et l'écart-type de l'image interpolée en uint16
    #processed_mean_f = np.mean(interpolated_img1)
    #processed_std_f = np.std(interpolated_img1)
    #print(f"Interpolated Image (int16) Stats - Mean: {processed_mean_f:.2f}, Std: {processed_std_f:.2f}")
    # Afficher l'image interpolée après la conversion en uint16
    #axes[2].imshow(interpolated_img1, cmap='gray')
    #axes[2].set_title("Interpolated Image (int16)")
    #axes[2].axis('off')

    # Convertir l'image interpolée en uint16 (format TIFF)
    interpolated_img_uint16 = interpolated_img.astype(np.uint16)
    # Calculer et afficher la moyenne et l'écart-type de l'image interpolée en uint16
    processed_mean_uint16 = np.mean(interpolated_img_uint16)
    processed_std_uint16 = np.std(interpolated_img_uint16)
    #print(f"Interpolated Image (uint16) Stats - Mean: {processed_mean_uint16:.2f}, Std: {processed_std_uint16:.2f}")
    # Afficher l'image interpolée en uint16
    #axes[3].imshow(interpolated_img, cmap='gray')
    #axes[3].set_title("Interpolated Image (uint16)")
    #axes[3].axis('off')

    #plt.tight_layout()
    #plt.show()

    return interpolated_img


def process_tif_files(pathsavesim):
    with rasterio.open(pathsavesim) as src:
        bands_arr = src.read()
        profile = src.profile

        # Récupérer le nom de fichier sans extension et le chemin du dossier parent
        filename = os.path.splitext(os.path.basename(pathsavesim))[0]
        parent_folder = os.path.dirname(pathsavesim)

        processed_bands = []
        for i, band in enumerate(bands_arr):
            # Appliquer l'interpolation bicubique
            processed_band = bicubic_interpolation(band)
            processed_bands.append(processed_band)

            # Sauvegarder le fichier TIFF interpolé dans dataset_interpolated avec le même nom
            savedirectory = os.path.join(parent_folder, "dataset_interpolated")
            os.makedirs(savedirectory, exist_ok=True)
            new_tif_file = os.path.join(savedirectory, f"{filename}_processed_{i + 1}.tif")

            with rasterio.open(new_tif_file, 'w', **profile) as dst:
                dst.write(processed_band, 1)

            # Copier le fichier props correspondant dans dataset_interpolated
            props_file = f"{filename}_{i + 1}.json"
            src_props_path = os.path.join(parent_folder, props_file)
            dst_props_path = os.path.join(savedirectory, props_file)

            # Afficher les images (optionnel)
            # plt.figure(figsize=(12, 6))
            # plt.subplot(1, 2, 1)
            # plt.imshow(band, cmap='gray')
            # plt.title(f"Original Band {i+1}")

            # plt.subplot(1, 2, 2)
            # plt.imshow(processed_band, cmap='gray')
            # plt.title(f"Processed Band {i+1}")

            # plt.show()

        print(f"Processed and saved files in {savedirectory}")


# Exemple d'utilisation avec un chemin vers un fichier TIFF spécifique
#pathsavesim = "D:/dataset/cab1_2026_field0-_1/cab1_2026_field0-_1.tif"
#process_tif_files(pathsavesim)