#!/usr/bin/env python
# coding: utf-8


import argparse
import os
import numpy as np
from utilsnew.utils import run_fmri_pair_subjects_crossval_ridge, run_kernel_ridge
from scipy import stats


# make all possible combinations of size s from the listed subjects
def get_all_combinations(subjects, s):
    from itertools import combinations 
    comb = combinations(subjects, s) 
    return comb


subs = ['H','I','J','K','L','M','N','F']
n_voxels = [24983, 25263, 29650, 25003, 24678, 28752, 24397, 27905]
voxels_dict = {}
for s, sub in enumerate(subs):
    voxels_dict[sub] = n_voxels[s]

np.random.seed(42)


save_dir = 'predictions_results_harrypotter/noise_ceiling/'
if not os.path.exists(save_dir):
    os.makedirs(save_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "argparser")
    parser.add_argument("subjectNum", help="Choose subject", type = str)
    args = parser.parse_args()
    target_subject = args.subjectNum
    source_subjects = [i for i in subs if i != target_subject]
    targetdata = np.load('./data/fMRI/data_subject_'+target_subject+'.npy')
    for source_subject in source_subjects:
        sourcedata = np.load('./data/fMRI/data_subject_'+source_subject+'.npy')
        corrs_t = run_kernel_ridge(sourcedata,targetdata)
        np.save(os.path.join(save_dir, "predict_{}_with_{}_{}pcs.npy".format(target_subject, source_subject, voxels_dict[source_subject])),corrs_t)





