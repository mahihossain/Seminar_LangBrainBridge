#!/usr/bin/env python
# coding: utf-8

import argparse
import os
import numpy as np
from utilsnew.utils import run_class_time_CV_fmri_crossval_ridge

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "argparser")
    parser.add_argument("subjectNum", help="Choose subject", type = str)
    parser.add_argument("featurename", help="Choose feature", type = str)
    parser.add_argument("dirname", help="Choose Directory", type = str)
    parser.add_argument("numlayers", help="Number of Layers", type = int)
    parser.add_argument("numdelays", help="Number of Delays", type = int)

    args = parser.parse_args()
    save_dir = args.dirname
    if not os.path.exists(save_dir):
        os.mkdir(save_dir)

    num_layers = args.numlayers
    feat = np.load(args.featurename, allow_pickle=True)
    target_subject = args.subjectNum

    data = np.load('./data/fMRI/data_subject_'+args.subjectNum+'.npy')
    for eachlayer in np.arange(num_layers):
        corrs_t, _, _, preds_t, test_t = run_class_time_CV_fmri_crossval_ridge(data,
                                                                    np.array(feat.item()[eachlayer]),args.numdelays)
        np.save(os.path.join(save_dir, "{}_y_pred_{}".format(target_subject, eachlayer)),preds_t)
        np.save(os.path.join(save_dir, "{}_y_test_{}".format(target_subject, eachlayer)),test_t)
        np.save(os.path.join(save_dir, "{}_y_corr_{}".format(target_subject, eachlayer)),corrs_t)
