## Noise-Ceiling Estimate ##
- To estimate noise-ceiling for each brain dataset, we need to perform two steps:
1. After subsampling of all the participants, predict target participant using each source participant
```
python brain_predictions_subjects_harrypotter.py H
```
2. Estimate noise-ceiling for each voxel 
```
python noise_ceiling_harrypotter.py H
```
