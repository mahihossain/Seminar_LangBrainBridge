import numpy as np
from sklearn.decomposition import PCA
from scipy.stats import zscore
import time
import csv
import os
import nibabel
from sklearn.metrics.pairwise import euclidean_distances
from scipy.ndimage.filters import gaussian_filter

from utilsnew.ridge_tools import cross_val_ridge, corr
import time as tm
from sklearn.kernel_ridge import KernelRidge

    
def load_transpose_zscore(file): 
    dat = nibabel.load(file).get_data()
    dat = dat.T
    return zscore(dat,axis = 0)

def smooth_run_not_masked(data,smooth_factor):
    smoothed_data = np.zeros_like(data)
    for i,d in enumerate(data):
        smoothed_data[i] = gaussian_filter(data[i], sigma=smooth_factor, order=0, output=None,
                 mode='reflect', cval=0.0, truncate=4.0)
    return smoothed_data

def delay_one(mat, d):
        # delays a matrix by a delay d. Positive d ==> row t has row t-d
    new_mat = np.zeros_like(mat)
    if d>0:
        new_mat[d:] = mat[:-d]
    elif d<0:
        new_mat[:d] = mat[-d:]
    else:
        new_mat = mat
    return new_mat

def delay_mat(mat, delays):
        # delays a matrix by a set of delays d.
        # a row t in the returned matrix has the concatenated:
        # row(t-delays[0],t-delays[1]...t-delays[last] )
    new_mat = np.concatenate([delay_one(mat, d) for d in delays],axis = -1)
    return new_mat      # (1351,40)

# train/test is the full NLP feature
# train/test_pca is the NLP feature reduced to 10 dimensions via PCA that has been fit on the training data
# feat_dir is the directory where the NLP features are stored
# train_indicator is an array of 0s and 1s indicating whether the word at this index is in the training set
def get_nlp_features_fixed_length(loaded, train_indicator, SKIP_WORDS=20, END_WORDS=5176):
    
    #loaded = np.load( os.path.join(feat_dir, feat_type + '_length_'+str(seq_len)+ '_layer_' + str(layer) + '.npy') )
    # For now, all models should be processed the same way
    # In future, if there are newer models that are processed differently, can add additional if-branch 
    if True:
        train = loaded[SKIP_WORDS:END_WORDS,:][train_indicator]         # (~3877, 768)
        test = loaded[SKIP_WORDS:END_WORDS,:][~train_indicator]         # (~1279, 768)
    else:
        print('Unrecognized NLP feature type {}.'.format(feat_type))
    
    pca = PCA(n_components=10, svd_solver='full')
    pca.fit(train)
    train_pca = pca.transform(train)                                    # (~3877, 10)
    test_pca = pca.transform(test)                                      # (~1279, 10)

    return train, test, train_pca, test_pca 

def CV_ind(n, n_folds):
    ind = np.zeros((n))                         # (1211,)
    n_items = int(np.floor(n/n_folds))          # 302
    for i in range(0,n_folds -1):               # Folds 0,1,2
        ind[i*n_items:(i+1)*n_items] = i
    ind[(n_folds-1)*n_items:] = (n_folds-1)     # Fold 3
    return ind                                  # [0,0,...,0,1,1,...,1,2,2,...,2,3,3,...3]

def TR_to_word_CV_ind(TR_train_indicator,SKIP_WORDS=20,END_WORDS=5176):
    time = np.load('./data/fMRI/time_fmri.npy')                 # (1351,) => [0, 2, 4, ...]
    runs = np.load('./data/fMRI/runs_fmri.npy')                 # (1351,) => [1,...,2,...,3,...,4]
    time_words = np.load('./data/fMRI/time_words_fmri.npy')     # (5176,) => [20., 20.5, ..., 2693.0]
    time_words = time_words[SKIP_WORDS:END_WORDS]               # (5156,) => [30., 30.5, ..., 2693.0]
        
    word_train_indicator = np.zeros([len(time_words)], dtype=bool)  # (5156,) => [False, False, ..., False]
    words_id = np.zeros([len(time_words)],dtype=int)                # (5156,) => [0, 0, ..., 0]
    # w=find what TR each word belongs to
    for i in range(len(time_words)):                
        words_id[i] = np.where(time_words[i]> time)[0][-1]          # (5156,) => [14, ..., 1346] first word belongs to TR 14
        
        if words_id[i] <= len(runs) - 15:
            offset = runs[int(words_id[i])]*20 + (runs[int(words_id[i])]-1)*15
            if TR_train_indicator[int(words_id[i])-offset-1] == 1:
                word_train_indicator[i] = True
    return word_train_indicator        


def prepare_fmri_features(train_features, test_features, word_train_indicator, TR_train_indicator, SKIP_WORDS=20, END_WORDS=5176):
        
    time = np.load('./data/fMRI/time_fmri.npy')
    runs = np.load('./data/fMRI/runs_fmri.npy') 
    time_words = np.load('./data/fMRI/time_words_fmri.npy')
    time_words = time_words[SKIP_WORDS:END_WORDS]
        
    words_id = np.zeros([len(time_words)])
    # w=find what TR each word belongs to
    for i in range(len(time_words)):
        words_id[i] = np.where(time_words[i]> time)[0][-1]
        
    all_features = np.zeros([time_words.shape[0], train_features.shape[1]]) # (5156, 10)
    all_features[word_train_indicator] = train_features
    all_features[~word_train_indicator] = test_features
        
    p = all_features.shape[1]
    tmp = np.zeros([time.shape[0], p])                                      # (1351, 10)
    for i in range(time.shape[0]):
        tmp[i] = np.mean(all_features[(words_id<=i)*(words_id>i-1)],0)
    tmp = delay_mat(tmp, np.arange(1,3))                                    # (1351, 40)

    # remove the edges of each run
    tmp = np.vstack([zscore(tmp[runs==i][20:-15]) for i in range(1,7)])     # (1211, 40) ==> IMPORTANT how 1351 --> 1211
    tmp = np.nan_to_num(tmp)
        
    return tmp[TR_train_indicator], tmp[~TR_train_indicator]

  

def run_class_time_CV_fmri_crossval_ridge(data, predict_feat_dict,
                                          regress_feat_names_list = [],method = 'kernel_ridge', 
                                          lambdas = np.array([0.1,1,10,100,1000]),
                                          detrend = False, n_folds = 4, skip=5):
    
    #nlp_feat_type = predict_feat_dict['nlp_feat_type']
    #feat_dir = predict_feat_dict['nlp_feat_dir']
    #layer = predict_feat_dict['layer']
    #seq_len = predict_feat_dict['seq_len']
        
        
    n_words = data.shape[0]     # (1211)
    n_voxels = data.shape[1]    # (~27905)

    ind = CV_ind(n_words, n_folds=n_folds)      # (1211,) => [0., 0., 0., ..., 3., 3., 3.]

    corrs = np.zeros((n_folds, n_voxels))
    acc = np.zeros((n_folds, n_voxels))
    acc_std = np.zeros((n_folds, n_voxels))

    all_test_data = []
    all_preds = []
    
    
    for ind_num in range(n_folds):
        train_ind = ind!=ind_num                # (1211,) => [False, False, False, ...,  True,  True,  True]
        test_ind = ind==ind_num                 # (1211,) => [ True,  True,  True, ..., False, False, False]
        
        word_CV_ind = TR_to_word_CV_ind(train_ind)
        
        _,_,tmp_train_features,tmp_test_features = get_nlp_features_fixed_length(predict_feat_dict, word_CV_ind)
        train_features,test_features = prepare_fmri_features(tmp_train_features, tmp_test_features, word_CV_ind, train_ind)
        
        # split data
        train_data = data[train_ind]
        test_data = data[test_ind]

        # skip TRs between train and test data
        if ind_num == 0: # just remove from front end
            train_data = train_data[skip:,:]
            train_features = train_features[skip:,:]
        elif ind_num == n_folds-1: # just remove from back end
            train_data = train_data[:-skip,:]
            train_features = train_features[:-skip,:]
        else:
            test_data = test_data[skip:-skip,:]
            test_features = test_features[skip:-skip,:]

        # normalize data
        train_data = np.nan_to_num(zscore(np.nan_to_num(train_data)))
        test_data = np.nan_to_num(zscore(np.nan_to_num(test_data)))
        all_test_data.append(test_data)
        
        train_features = np.nan_to_num(zscore(train_features))
        test_features = np.nan_to_num(zscore(test_features)) 
        
        start_time = tm.time()
        weights, chosen_lambdas = cross_val_ridge(train_features,train_data, n_splits = 10, lambdas = np.array([10**i for i in range(-6,10)]), method = 'plain',do_plot = False)

        preds = np.dot(test_features, weights)
        corrs[ind_num,:] = corr(preds,test_data)
        all_preds.append(preds)
            
        print('fold {} completed, took {} seconds'.format(ind_num, tm.time()-start_time))
        del weights

    return corrs, acc, acc_std, np.vstack(all_preds), np.vstack(all_test_data)

def binary_classify_neighborhoods(Ypred, Y, n_class=20, nSample = 1000,pair_samples = [],neighborhoods=[]):
    # n_class = how many words to classify at once
    # nSample = how many words to classify
    # Ypred, Y: (297, 27905)

    voxels = Y.shape[-1]
    neighborhoods = np.asarray(neighborhoods, dtype=int)

    import time as tm

    acc = np.full([nSample, Y.shape[-1]], np.nan)       # (1000, 27905)
    acc2 = np.full([nSample, Y.shape[-1]], np.nan)      # (1000, 27905)
    test_word_inds = []

    if len(pair_samples)>0:
        Ypred2 = Ypred[pair_samples>=0]
        Y2 = Y[pair_samples>=0]
        pair_samples2 = pair_samples[pair_samples>=0]
    else:
        Ypred2 = Ypred
        Y2 = Y
        pair_samples2 = pair_samples
    n = Y2.shape[0]                                     # (297)
    start_time = tm.time()
    for idx in range(nSample):
        
        idx_real = np.random.choice(n, n_class)         # (20,) => [248, 185, 25, 110, 79, ...]

        sample_real = Y2[idx_real]                      # (20, 27905)
        sample_pred_correct = Ypred2[idx_real]          # (20, 27905)

        if len(pair_samples2) == 0:
            idx_wrong = np.random.choice(n, n_class)    # (20,) => [248, 185, 25, 110, 79, ...]
        else:
            idx_wrong = sample_same_but_different(idx_real,pair_samples2)
        sample_pred_incorrect = Ypred2[idx_wrong]

        #print(sample_pred_incorrect.shape)

        # compute distances within neighborhood
        dist_correct = np.sum((sample_real - sample_pred_correct)**2,0)     # (27905,)
        dist_incorrect = np.sum((sample_real - sample_pred_incorrect)**2,0) # (27905,)

        neighborhood_dist_correct = np.array([np.sum(dist_correct[neighborhoods[v,neighborhoods[v,:]>-1]]) for v in range(voxels)])
        neighborhood_dist_incorrect = np.array([np.sum(dist_incorrect[neighborhoods[v,neighborhoods[v,:]>-1]]) for v in range(voxels)])


        acc[idx,:] = (neighborhood_dist_correct < neighborhood_dist_incorrect)*1.0 + (neighborhood_dist_correct == neighborhood_dist_incorrect)*0.5

        test_word_inds.append(idx_real)
    print('Classification for fold done. Took {} seconds'.format(tm.time()-start_time))
    return np.nanmean(acc,0), np.nanstd(acc,0), acc, np.array(test_word_inds)

def run_fmri_pair_subjects_crossval_ridge(sourcedata, targetdata,
                                          regress_feat_names_list = [],method = 'kernel_ridge', 
                                          lambdas = np.array([0.1,1,10,100,1000]),
                                          detrend = False, n_folds = 4):    
        
    n_sourcevoxels = sourcedata.shape[1]    # (~27905)
    n_targetvoxels = targetdata.shape[1]    # (~24983)

    ind = CV_ind(sourcedata.shape[0], n_folds=n_folds)      # (1211,) => [0., 0., 0., ..., 3., 3., 3.]

    corrs = np.zeros((n_folds, n_targetvoxels))
    acc = np.zeros((n_folds, n_targetvoxels))
    acc_std = np.zeros((n_folds, n_targetvoxels))

    all_test_data = []
    all_preds = []
    
    
    for ind_num in range(n_folds):
        train_ind = ind!=ind_num                # (1211,) => [False, False, False, ...,  True,  True,  True]
        test_ind = ind==ind_num                 # (1211,) => [ True,  True,  True, ..., False, False, False]
        
        # normalize source data
        source_train_data = np.nan_to_num(zscore(np.nan_to_num(sourcedata[train_ind])))
        source_test_data = np.nan_to_num(zscore(np.nan_to_num(sourcedata[test_ind])))

        # normalize target data
        target_train_data = np.nan_to_num(zscore(np.nan_to_num(targetdata[train_ind])))
        target_test_data = np.nan_to_num(zscore(np.nan_to_num(targetdata[test_ind])))
        all_test_data.append(target_test_data) 
        
        start_time = tm.time()
        weights, chosen_lambdas = cross_val_ridge(source_train_data,target_train_data, n_splits = 10, lambdas = np.array([10**i for i in range(-6,10)]), method = 'plain',do_plot = False)

        preds = np.dot(source_test_data, weights)
        corrs[ind_num,:] = corr(preds,target_test_data)
        all_preds.append(preds)
            
        print('fold {} completed, took {} seconds'.format(ind_num, tm.time()-start_time))
        del weights

    return corrs, acc, acc_std, np.vstack(all_preds), np.vstack(all_test_data)


def run_kernel_ridge(sourcedata, targetdata,
                                          regress_feat_names_list = [],method = 'kernel_ridge', 
                                          lambdas = np.array([0.1,1,10,100,1000]),
                                          detrend = False, n_folds = 4, skip=5):    
        
    n_words = sourcedata.shape[0]     # (1211)
    n_voxels = targetdata.shape[1]    # (~27905)

    ind = CV_ind(n_words, n_folds=n_folds)      # (1211,) => [0., 0., 0., ..., 3., 3., 3.]

    corrs = np.zeros((n_folds, n_voxels))
    acc = np.zeros((n_folds, n_voxels))
    acc_std = np.zeros((n_folds, n_voxels))

    all_test_data = []
    all_preds = []
    
    
    for ind_num in range(n_folds):
        train_ind = ind!=ind_num                # (1211,) => [False, False, False, ...,  True,  True,  True]
        test_ind = ind==ind_num                 # (1211,) => [ True,  True,  True, ..., False, False, False]

        # split data
        source_train_data = sourcedata[train_ind]
        source_test_data = sourcedata[test_ind]

        target_train_data = targetdata[train_ind]
        target_test_data = targetdata[test_ind]

        # normalize data
        source_train_data = np.nan_to_num(zscore(np.nan_to_num(source_train_data)))
        source_test_data = np.nan_to_num(zscore(np.nan_to_num(source_test_data)))

        target_train_data = np.nan_to_num(zscore(np.nan_to_num(target_train_data)))
        target_test_data = np.nan_to_num(zscore(np.nan_to_num(target_test_data)))
        all_test_data.append(target_test_data) 
        
        start_time = tm.time()
        #weights, chosen_lambdas = cross_val_ridge(train_features,train_data, n_splits = 10, lambdas = np.array([10**i for i in range(-6,10)]), method = 'plain',do_plot = False)
        kernel_ridge_tuned = KernelRidge()
        kernel_ridge_tuned.fit(np.nan_to_num(source_train_data), np.nan_to_num(target_train_data))
        y_pred = kernel_ridge_tuned.predict(np.nan_to_num(source_test_data))
        corrs[ind_num,:] = corr(y_pred,target_test_data)
        all_preds.append(y_pred)
            
        print('fold {} completed, took {} seconds'.format(ind_num, tm.time()-start_time))

    return corrs