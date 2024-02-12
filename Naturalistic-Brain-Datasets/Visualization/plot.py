import cortex
import numpy as np
sub = 'I'

surfaces = dict( F = 'fMRI_story_F',
G = 'fMRI_story_G',
H = 'fMRI_story_H',
I = 'fMRI_story_I',
J = 'fMRI_story_J',
K = 'fMRI_story_K',
L = 'fMRI_story_L',
M = 'fMRI_story_M',
N = 'fMRI_story_N')

transforms = dict( F = 'F_ars',
G = 'G_ars',
H = 'H_ars',
I = 'I_ars',
J = 'J_ars',
K = 'K_ars',
L = 'L_ars',
M = 'M_ars',
N = 'N_ars')



mask = cortex.db.get_mask(surfaces[sub], transforms[sub], 'thin')
print('num voxels in transform for I: {}'.format(np.sum(mask)))

# plot
vols = {}
voxel_values_to_plot = np.zeros((np.sum(mask))) # replace with the voxel values you want to plot
vols[sub] = cortex.Volume(voxel_values_to_plot, surfaces[sub],transforms[sub], vmin=0, vmax=0.2, cmap='viridis')
cortex.webshow(vols,open_browser=False)
input()
