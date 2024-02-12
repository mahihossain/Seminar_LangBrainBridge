#imports libraries that you will need
import os
import numpy as np
import dataloader
import argparse

if __name__ == "__main__":
    """
    To load the brain dataset, users need to pass four main attributes
    1. Datasent Name: {'harry_potter','subset_moth_radio','full_moth_radio','little_prince','zhang','narratives'}
    2. Modality: {'reading','listening'}
    3. Subject Number
    {'harry_potter': ['F','H','I','J','K','L','M','N'],
    'subset_moth_radio_hour': ['01','02','03','05','07','08'],
    'full_moth_radio_hour': [],
    'narratives': []
    'little_prince': [57 - 115]}
    4. Dataset location

    e.g.: python main_dataloader.py harry_potter reading H 

    """
    parser = argparse.ArgumentParser(description = "Brain datasets argparser")
    parser.add_argument("--dataset_name", default='harry_potter', help="Choose Dataset", type = str)
    parser.add_argument("--modality", default='reading', help="Choose Modality either reading or listening", type = str)
    parser.add_argument("--subject_number", help="Choose Particular Subjects or All", type = str)
    parser.add_argument("--dataset_location", help="Choose Directory location where files are present", type = str)
    
    args = parser.parse_args()
    print(args)

    if args.dataset_name=='harry_potter':
        harry_data_object = dataloader.harry_potter_data()
        brain_data = harry_data_object.get_harry_potter_data(args.dataset_name, args.modality, args.subject_number, args.dataset_location)
        print(brain_data.shape)

    elif args.dataset_name=='subset_moth_radio_hour':
        subset_moth_radio_object = dataloader.subset_moth_radio_hour()
        brain_data = subset_moth_radio_object.get_subset_moth_radio_hour(args.dataset_name, args.modality, args.subject_number, args.dataset_location)
        print(brain_data[0].shape)
        print(brain_data[1].shape)

    elif args.dataset_name=='narratives':
        brain_data = dataloader.get_narratives()

    elif args.dataset_name=='full_moth_radio_hour':
        brain_data = dataloader.get_full_moth_radio_hour()

    elif args.dataset_name=='little_prince':
        brain_data = dataloader.get_little_prince_data()

    elif args.dataset_name=='zhang_dataset':
        brain_data = dataloader.get_zhang_data()

    else:
        print('The required dataset {} is not found here'.format(args.dataset_name))

