# Installation
-----------
Datalad can be installed using pip (required for Narratives, Little Prince and Moth-Radio-Hour):

```bash
python -m pip install datalad
```
- It is highly recommended to configure Git before using DataLad. Set both 'user.name' and 'user.email' configuration variables.
```bash
- git config --global user.name "username"
- git config --global user.email emailid
```
- git-annex installation is required for downloading the dataset
```bash
sudo apt-get install git-annex
```

# Naturalistic-Brain-Datasets

## Language Task
### Naturalistic Story Reading
**[Harry-Potter]**(https://drive.google.com/drive/folders/1Q6zVCAJtKuLOh-zWpkS3lH8LBvHcEOE8)
- 8 subjects
- fMRI brain recordings
- Reading harry potter story (each word lasted for 0.5 secs)
- TR = 2 secs
- subjects: ['F', 'H', 'I', 'J', 'K', 'L', 'M', 'N']

```bash
python main_dataloader.py harry_potter reading H ./data/fMRI
```

**[Subset-Moth-Radio-Hour]**(https://berkeley.app.box.com/v/Deniz-et-al-2019/folder/91885397358)
- 6 subjects
- fMRI brain recordings
- 11 stories (10 stories for training + 1 story for testing)
- TR = 2.0045 secs
- subjects: ['01', '02', '03', '05', '07', '08']

```bash
python main_dataloader.py subset_moth_radio_hour reading 1 ./data/
```

### Naturalistic Story Listening

**[Moth-Radio-Hour]**(https://openneuro.org/datasets/ds003020)
- 8 subjects
- fMRI brain recordings
- 27 stories
- TR = 2.0045 secs
- subjects: ['01', '02', '03', '04', '05', '06', '07', '08']

```bash
python main_dataloader.py moth_radio_hour listening 1 ./ds003020/derivative/preprocessed_data/
```
  
**Download the dataset using either datalad or git**
- datalad install https://github.com/OpenNeuroDatasets/ds003020.git
- git clone https://github.com/OpenNeuroDatasets/ds003020.git

**[Subset-Moth-Radio-Hour]**(https://berkeley.app.box.com/v/Deniz-et-al-2019/folder/91885397358)
- 6 subjects
- fMRI brain recordings
- 11 stories (10 stories for training + 1 story for testing)
- TR = 2.0045 secs
- subjects: ['01', '02', '03', '05', '07', '08']

```bash
python main_dataloader.py subset_moth_radio_hour listening 1 ./data/
```

**[Narratives]**(https://datasets.datalad.org/?dir=/labs/hasson/narratives/)
- 345 subjects
- fMRI brain recordings
- 27 stories
- TR = 1.5 secs
  
**Download the dataset using either datalad**
```bash
* datalad install https://datasets.datalad.org/labs/hasson/narratives/derivatives/afni-nosmooth
* cd afni-nosmooth
* bash download_data.sh
```


**[Little-Prince]**(https://openneuro.org/datasets/ds003643)
- 49 subjects
- fMRI brain recordings
- English audiobook is 94 minutes long, translated by David Wilkinson and read by Karen Savage
- TR = 2 secs
- 9 runs, and each lasted for about 10 minutes.
- Participants listened passively to 1 section of the audiobook in each run and completed 4 quiz questions after each run (36 questions in total).

**Download the dataset using either datalad or git**
```bash
- datalad install https://github.com/OpenNeuroDatasets/ds003643.git
- git clone https://github.com/OpenNeuroDatasets/ds003643.git
```


## Naturalistic Images

**[BOLD5000]**

**[Natural Scenes Dataset (NSD)]**

**[Things]**

**[Generic Object Dataset]**
