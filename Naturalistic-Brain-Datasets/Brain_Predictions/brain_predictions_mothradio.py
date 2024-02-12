#!/usr/bin/env python

# This cell imports libraries that you will need
# Run this.
from matplotlib.pyplot import figure, cm
import numpy as np
import logging
import argparse
logging.basicConfig(level=logging.DEBUG)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description = "CheXpert NN argparser")
    parser.add_argument("subjectNum", help="Choose subject", type = int)
    parser.add_argument("featurename", help="Choose feature", type = str)
    parser.add_argument("dirname", help="Choose Directory", type = str)
    parser.add_argument("numlayers", help="Number of Layers", type = int)
    args = parser.parse_args()
    word_level_features = np.load(args.featurename, allow_pickle=True)
    print(word_level_features.item().keys())
    num_layers = args.numlayers


    stories = list(word_level_features.item().keys())

    import feature_spaces
    # These are lists of the stories
    # Rstories are the names of the training (or Regression) stories, which we will use to fit our models
    Rstories = ['adollshouse','adventuresinsayingyes','alternateithicatom', 'avatar', 'buck',
                'exorcism', 'eyespy','fromboyhoodtofatherhood', 'hangtime', 'haveyoumethimyet', 'howtodraw', 'inamoment', 
                'itsabox','legacy', 'life', 'myfirstdaywiththeyankees', 'naked', 'odetostepfather','sloth', 'souls',
                'stagefright', 'swimmingwithastronauts', 'thatthingonmyarm','theclosetthatateeverything',
                'tildeath', 'undertheinfluence']

    # Pstories are the test (or Prediction) stories (well, story), which we will use to test our models
    Pstories = ['wheretheressmoke']

    allstories = Rstories + Pstories

    # # Make word and phoneme datasequences
    # from dsutils import make_word_ds, make_phoneme_ds
    wordseqs = feature_spaces.get_story_wordseqs(allstories) # dictionary of {storyname : word DataSequence}



    naked = wordseqs["naked"]
    # The DataSequence stores a lot of information
    # naked.data is a list of all the words in the story
    print ("There are %d words in the story called 'naked'" % len(list(naked.data)))


    for eachstory in allstories:
        print(eachstory,len(list(wordseqs[eachstory].data)))


    word_vectors = {}
    for eachlayer in np.arange(num_layers):
        word_vectors[eachlayer] = {}
        for eachstory in allstories:
            word_vectors[eachlayer][eachstory] = np.nan_to_num(word_level_features.item()[eachstory][eachlayer])


    downsampled_stories = {}
    for eachlayer in np.arange(num_layers):
        downsampled_stories[eachlayer] = feature_spaces.downsample_word_vectors(allstories,word_vectors[eachlayer],wordseqs)

    # Combine stimuli
    from npp import zscore
    trim = 5
    Rstim = {}
    Pstim = {}
    for eachlayer in np.arange(num_layers):
        Rstim[eachlayer] = []
        Rstim[eachlayer].append(np.vstack([zscore(downsampled_stories[eachlayer][story][5+trim:-trim]) for story in Rstories]))

    for eachlayer in np.arange(num_layers):
        Pstim[eachlayer] = []
        Pstim[eachlayer].append(np.vstack([zscore(downsampled_stories[eachlayer][story][5+trim:-trim]) for story in Pstories]))


    storylens = [len(downsampled_stories[1][story][5+trim:-trim]) for story in Rstories]
    print(storylens)

    print(np.cumsum(storylens))


    # Delay stimuli
    from util import make_delayed
    ndelays = 6
    delays = range(1, ndelays+1)

    print ("FIR model delays: ", delays)

    delRstim = []
    for eachlayer in np.arange(12):
        delRstim.append(make_delayed(np.array(Rstim[eachlayer])[0], delays))
        
    delPstim = []
    for eachlayer in np.arange(12):
        delPstim.append(make_delayed(np.array(Pstim[eachlayer])[0], delays))


    # Print the sizes of these matrices
    print ("delRstim shape: ", delRstim[1].shape)
    print ("delPstim shape: ", delPstim[1].shape)

    # Load responses
    # Load training data for subject 1, reading dataset 
    import os
    import utils1
    fdir = 'UTS0'+str(args.subjectNum)+'/'
    trndata = {}
    for eachstory in Rstories:
        fname_tr5 = os.path.join(fdir, eachstory+'.hf5')
        trndata5 = utils1.load_data(fname_tr5)
        trndata[eachstory]=trndata5
    print(trndata.keys())

    tstdata = {}
    for eachstory in Pstories:
        fname_te5 = os.path.join(fdir, eachstory+'.hf5')
        tstdata5 = utils1.load_data(fname_te5)
        tstdata[eachstory]=tstdata5
    print(tstdata.keys())


    from npp import zscore
    trim = 5
    zRresp = np.vstack([zscore(trndata[story]['data']) for story in trndata.keys()])
    zPresp = np.vstack([zscore(tstdata[story]['data']) for story in tstdata.keys()])


    # In[ ]:


    # Print matrix shapes
    print ("zRresp shape (num time points, num voxels): ", zRresp.shape)
    print ("zPresp shape (num time points, num voxels): ", zPresp.shape)

    subject = '0'+str(args.subjectNum)
    # Run regression
    from ridge_utils.ridge import bootstrap_ridge

    nboots = 5 # Number of cross-validation runs.
    chunklen = 40 # 
    nchunks = 20
    main_dir = args.dirname+'/'+subject
    if not os.path.exists(main_dir):
        os.makedirs(main_dir)
    for eachlayer in np.arange(num_layers):
        alphas = np.logspace(1, 3, 10) # Equally log-spaced alphas between 10 and 1000. The third number is the number of alphas to test.
        all_corrs = []
        save_dir = str(eachlayer)
        if not os.path.exists(main_dir+'/'+save_dir):
            os.mkdir(main_dir+'/'+save_dir)
        wt, corr, alphas, bscorrs, valinds = bootstrap_ridge(delRstim[eachlayer], zRresp, delPstim[eachlayer], zPresp,
                                                             alphas, nboots, chunklen, nchunks,
                                                             singcutoff=1e-10, single_alpha=True)
        pred = np.dot(delPstim[eachlayer], wt)

        print ("pred has shape: ", pred.shape)
        voxcorrs = np.zeros((zPresp.shape[1],)) # create zero-filled array to hold correlations
        for vi in range(zPresp.shape[1]):
            voxcorrs[vi] = np.corrcoef(zPresp[:,vi], pred[:,vi])[0,1]
        print (voxcorrs)

        np.save(os.path.join(main_dir+'/'+save_dir, "layer_"+str(eachlayer)),voxcorrs)
