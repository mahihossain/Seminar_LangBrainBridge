#imports libraries that you will need
import os
import numpy as np
import h5py
from utils1 import *
from npp import zscore
import nibabel as nib
from nibabel.testing import data_path
from nilearn.masking import apply_mask
import nilearn

#main class 
class dataloader:
  """
  dataloader class is called when a user wants to load the brain dataset.
  To load the brain dataset, users need to pass four main attributes
  1. Datasent Name: {'harry_potter','subset_moth_radio','full_moth_radio','little_prince','zhang','narratives'}
  2. Modality: {'reading','listening'}
  3. Subject Number
  4. Dataset location
  """
  def __init__(self):
    self.dataset_name = ''
    self.modality = ''
    self.subject = ''
    self.directory = ''

  def printname(self):
    print(self.dataset_name, self.modality)


class subset_moth_radio_hour(dataloader):
  """
  subset_moth_radio_hour dataset is called when a user wants to load dataset where participants 
  involved in reading and listening same narrtive story. The dataset consits of 6 subjects,
  11 narrative stories from Moth-Radio-Hour, where 10 stories used for training and 1 story
  used for testing.
  To load the subset_moth_radio_hour dataset, users need to pass four main attributes
  1. Dataset Name: {'subset_moth_radio_hour'}
  2. Modality: {'reading','listening'}, default modality is 'reading'
  3. Subject Number: {'01', '02', '03', '05', '07', '08'}, default subject is '01'
  4. Dataset location: the directory where the files are located, e.g. subject01_reading_fmri_data_trn.hdf,
  subject01_reading_fmri_data_val.hdf 
  """
  def __init__(self):
    self.trim = 5
    self.modality = 'reading'
    self.subject = '1'

  def get_subset_moth_radio_hour(self, dataset_name, modality, subject, directory):
    self.dataset_name = dataset_name
    self.modality = modality
    self.subject = subject
    self.directory = directory
    
    fname_tr5 = os.path.join(self.directory, 'subject0{}_{}_fmri_data_trn.hdf'.format(self.subject, self.modality))
    trndata5 = utils1.load_data(fname_tr5)
    print(trndata5.keys())

    fname_te5 = os.path.join(self.directory, 'subject0{}_{}_fmri_data_val.hdf'.format(self.subject, self.modality))
    tstdata5 = utils1.load_data(fname_te5)
    print(tstdata5.keys())
    
    zRresp = np.vstack([zscore(trndata5[story][5+self.trim:-self.trim-5]) for story in trndata5.keys()])
    zPresp = np.vstack([zscore(tstdata5[story][0][5+self.trim:-self.trim-5]) for story in tstdata5.keys()])

    return zRresp, zPresp


class harry_potter_data(dataloader):
  """
  Harry Potter dataset is called when a user wants to load dataset where participants 
  involved in reading harry potter story. The dataset consits of 8 subjects.
  To load the harry potter dataset, users need to pass four main attributes
  1. Dataset Name: {'harry_potter'}
  2. Modality: {'reading'}, default modality is 'reading'
  3. Subject Number: {'F', 'H', 'I', 'J', 'K', 'L', 'M', 'N'}, default subject is 'H'
  4. Dataset location: the directory where the files are located, e.g. data_subject_H.npy
  """
  def __init__(self):
    self.modality = 'reading'
    self.subject = 'H'

  def get_harry_potter_data(self, dataset_name, modality, subject, directory):
    self.dataset_name = dataset_name
    self.subject = subject
    self.directory = directory

    data = np.load(os.path.join(self.directory,'data_subject_{}.npy'.format(self.subject)))
    return data


class full_moth_radio_hour(dataloader):
  """
  full_moth_radio_hour dataset is called when a user wants to load dataset where participants 
  involved in listening moth-radio-hour narrtive stories. The dataset consits of 8 subjects,
  27 narrative stories from Moth-Radio-Hour, where 26 stories used for training and 1 story
  used for testing.
  To load the full_moth_radio_hour dataset, users need to pass four main attributes
  1. Dataset Name: {'full_moth_radio_hour'}
  2. Modality: {'listening'}, default modality is 'listening'
  3. Subject Number: {'01', '02', '03', '04', '05', '06', '07', '08'}, default subject is '01'
  4. Dataset location: the directory where the files are located, e.g. adollshouse.hf5 is fMRI response of adollshouse story 
  """
  def __init__(self):
    self.modality = 'listening'
    self.subject = '1'

  def get_full_moth_radio_hour_data(self, dataset_name, modality, subject, directory):
    self.dataset_name = dataset_name
    self.subject = subject
    self.directory = directory

    fdir = 'UTS0'+str(args.subjectNum)+'/'
    allstories = sorted(os.listdir(fdir))

    trndata = {}
    for eachstory in allstories[:-1]:
        fname_tr5 = os.path.join(fdir, eachstory+'.hf5')
        trndata5 = utils1.load_data(fname_tr5)
        trndata[eachstory]=trndata5
    print(trndata.keys())

    tstdata = {}
    for eachstory in allstories[-1]:
        fname_te5 = os.path.join(fdir, eachstory+'.hf5')
        tstdata5 = utils1.load_data(fname_te5)
        tstdata[eachstory]=tstdata5
    print(tstdata.keys())

    trim = 5
    zRresp = np.vstack([zscore(trndata[story]['data']) for story in trndata.keys()])
    zPresp = np.vstack([zscore(tstdata[story]['data']) for story in tstdata.keys()])

    return zRresp, zPresp

class narratives(dataloader):
  """
  narratives dataset is called when a user wants to load dataset where participants 
  involved in listening narrtive stories. The dataset consits of 345 subjects,
  27 narrative stories.

  To load the narratives dataset, users need to pass four main attributes
  1. Dataset Name: {'narratives_pieman'}
  2. Modality: {'listening'}, default modality is 'listening'
  3. Subject Number: {'01', '02', '03', '04', '05', '06', '07', '08'}, default subject is '01'
  4. Dataset location: the directory where the files are located, e.g. adollshouse.hf5 is fMRI response of adollshouse story 
  """
  def __init__(self):
    self.modality = 'listening'
    self.subject = '1'

  def get_narratives_data(self, dataset_name, modality, subject, directory):
    self.dataset_name = dataset_name
    self.subject = subject
    self.directory = directory

    # Load training data for subject 1, reading dataset
    dataset_path = os.path.join(self.directory, eachstory+'.hf5') 
    roi_voxels = np.load('./tunnel/sub_'+str(args.subjectNum)+'.npy',allow_pickle=True)
    roi_voxels = roi_voxels[2:-15,:]
    print(roi_voxels.shape)

    from npp import zscore
    zRresp = []
    for eachsubj in np.arange(roi_voxels.shape[0]):
        zRresp.append(roi_voxels[eachsubj])
    zRresp = np.array(zRresp)

    return zRresp

class little_prince(dataloader):
  """
  little_prince dataset is called when a user wants to load dataset where participants 
  involved in listening narrtive stories. The dataset consits of 49 subjects,
  27 narrative stories from Moth-Radio-Hour, where 26 stories used for training and 1 story
  used for testing.
  To load the little_prince dataset, users need to pass four main attributes
  1. Dataset Name: {'little_prince'}
  2. Modality: {'listening'}, default modality is 'listening'
  3. Subject Number: {57 -- }, default subject is 57
  4. Dataset location: the directory where the files are located, e.g. adollshouse.hf5 is fMRI response of adollshouse story 
  """
  def __init__(self):
    self.modality = 'listening'
    self.subject = 57

  def get_little_prince_data(self, modality, subject, directory):
    self.subject = subject
    self.directory = directory

    fdir = self.directory+str(args.subjectNum)+'/'
    allstories = sorted(os.listdir(fdir))

    trndata = {}
    for eachstory in allstories[:-1]:
        fname_tr5 = os.path.join(fdir, eachstory+'.hf5')
        trndata5 = utils1.load_data(fname_tr5)
        trndata[eachstory]=trndata5
    print(trndata.keys())

    tstdata = {}
    for eachstory in allstories[-1]:
        fname_te5 = os.path.join(fdir, eachstory+'.hf5')
        tstdata5 = utils1.load_data(fname_te5)
        tstdata[eachstory]=tstdata5
    print(tstdata.keys())

    trim = 5
    zRresp = np.vstack([zscore(trndata[story]['data']) for story in trndata.keys()])
    zPresp = np.vstack([zscore(tstdata[story]['data']) for story in tstdata.keys()])

    return zRresp, zPresp