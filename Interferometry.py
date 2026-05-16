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
(files, images, folder) = utils.select_txt(names)
dateshot = folder.split('/')[-3]

print(images["shot"])

#%%
'''
MATH
'''
#just the math to get the areal electron density
def getArealElectronDensity(phase_array, wavelength, critical_density):
    return (-phase_array)*wavelength*critical_density / np.pi

arealdensity = getArealElectronDensity(images["shot"],L, n_c)

print(arealdensity)

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



filepath = os.path.join(outputfolder, shot_name + ".png")

os.makedirs(outputfolder, exist_ok=True)

plt.savefig(filepath)

plt.show()

#%%
'''
SAVING TXT FILE
'''
# giving an output folder for the new images or txt files. 
# this also remembers the original name of the imported files
# then saves it onto the new folder with the same name. 


outputfolder = '2026/textfile'

shot_name = utils.splitpath(files["shot"])[-1]

filepath = os.path.join(outputfolder, shot_name)

os.makedirs(outputfolder, exist_ok=True)

np.savetxt(filepath, arealdensity)


#%%
'''
OVERLAYING PLOTS
'''
#done to take off the offset value above plot
fig, ax = plt.subplots()

outputfolder = '2026/radialprofile'

#stackexchange
def radial_profile(image, center=None):

    image = np.asarray(image, dtype=np.float32)

    #gray_image = image.mean(axis=2)

    y, x = np.indices(image.shape)

    if center is None:
        center = (image.shape[1] // 2,
                  image.shape[0] // 2)

    x0, y0 = center

    r = np.sqrt((x - x0)**2 + (y - y0)**2)
    r = r.astype(int)

    tbin = np.bincount(r.ravel(), weights=image.ravel())
    nr = np.bincount(r.ravel())

    radialprofile = tbin / nr
    radii = np.arange(len(radialprofile))

    return radii, radialprofile


for filename in glob.glob('2026/textfile/*.txt'):
    #loads in the txt file
    img = np.loadtxt(filename)
    
    #choosing the most dense of all the txt files as the center
    #done because all images are cropped differently in tnt
    y0, x0 = np.unravel_index(np.argmax(img), img.shape)

    #getting the x, y for plot
    radii, radialprofile = radial_profile(img, center=(x0,y0))

    #changing it to cm^-2        
    radial_profile_cm = radialprofile * 1e-4

    #saving the label and using that for the legend
    base = os.path.basename(filename)
    label = os.path.splitext(base)[0]
    print("label: ", label)

    ax.plot(radii, radial_profile_cm, label=label)
    
ax.set_xlabel("Radius [\u03bcm]")
ax.set_ylabel("Areal Electron Density [cm^-2]")
ax.yaxis.get_offset_text().set_visible(False)
plt.legend(loc="upper right")
plt.grid()

filepath = os.path.join(outputfolder, "radial_profile.png")

os.makedirs(outputfolder, exist_ok=True)

plt.savefig(filepath)

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
