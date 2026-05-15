#%%
'''
PACKAGE IMPORTS
'''

import numpy as np
import matplotlib.pyplot as plt
import os
import ui as utils
import cv2
import glob
from PIL import Image

#%%
'''
EXPERIMENTAL VALUES
'''

L = 1064e-9 #[m]
m_e = 9.1093837e-31 #[kg]
eps = 8.854187817e-12 #[F/m]
electron = -1.602e-19 #[C] 
c = 3.0e8 #[m/s]
omega = (2 * np.pi * c)/L

def critical_density(m_e, eps, omega, electron):
    return (m_e * eps * omega**2)/(electron**2)

n_c = critical_density(m_e, eps, omega, electron)


#%%
'''
UI
'''

ui = utils.UI()

#%%
'''
FILE IMPORT
'''

names = ["shot"]
(files, images, folder) = utils.select_images(names)
dateshot = folder.split('/')[-3]

print(images["shot"])

#%%
'''
MATH
'''

def getArealElectronDensity(phase_array, wavelength, critical_density):
    return (-phase_array)*wavelength*critical_density / np.pi

arealdensity = getArealElectronDensity(images["shot"],L, n_c)

#%%
'''
PLOTTING for PNG
'''
outputfolder = '2026/out'

shot_name = utils.splitpath(files["shot"])[-1]

fig = plt.figure(figsize=(8, 6))
plt.imshow(abs(arealdensity), cmap='plasma')
plt.colorbar(label='Areal Electron Density [m^-2]')

plt.title("Areal Electron Density [m^-2]")
plt.xlabel("X [\u03bcm]")
plt.ylabel("Y [\u03bcm]")



filepath = os.path.join(outputfolder, shot_name)

os.makedirs(outputfolder, exist_ok=True)

plt.savefig(filepath)

plt.show()

#%%
'''
SAVING TXT FILE
'''

outputfolder = '2026/textfile'

os.makedirs(outputfolder, exist_ok=True)

filepath = os.path.join(outputfolder, "areal_density.txt")

values = arealdensity

values_reshaped = values.reshape(values.shape[0], -1)

np.savetxt(filepath, values_reshaped)

#%%
'''
OVERLAYING PLOTS
'''

#stackexchange
def radial_profile(image, center=None):

    image = np.asarray(image, dtype=np.float32)

    gray_image = image.mean(axis=2)

    y, x = np.indices(gray_image.shape)

    if center is None:
        center = (x//2, y//2)

    x0, y0 = center

    r = np.sqrt((x - x0)**2 + (y - y0)**2)
    r = r.astype(int)

    tbin = np.bincount(r.ravel(), weights=gray_image.ravel())
    nr = np.bincount(r.ravel())

    radialprofile = tbin / nr
    radii = np.arange(len(radialprofile))

    return radii, radialprofile


for filename in glob.glob('2026/out/*.png'):
    img = Image.open(filename)
    
    radii, radialprofile = radial_profile(img)

    base = os.path.basename(filename)

    label = os.path.splitext(base)[0]

    plt.plot(radii, radialprofile, label=label)

    
plt.xlabel("Radius [\u03bcm]")
plt.ylabel("Areal Electron Density [m^-2]")
plt.legend()
plt.grid()
plt.show()

#%%
'''
IMAGE EXPORT
'''

outputfolder = '2026/tifff'

shot_name = utils.splitpath(files["shot"])[-1]

#save_images = ["shot"]

filepath = os.path.join(outputfolder, shot_name)

os.makedirs(outputfolder, exist_ok=True)

plt.savefig(filepath, format="tiff")

#os.makedirs(folder+"2026/out", exist_ok=True)
#utils.save_image_tiff(images, save_images, os.path.join(folder))

#for name in save_images:
#    Image.fromarray(images[name]).save(folder+"2026/out"+dateshot+"_"+name+".png")


# %%
