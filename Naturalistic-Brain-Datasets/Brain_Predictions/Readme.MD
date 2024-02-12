## Brain Predictions for each dataset ##

* Harry-Potter (Reading)
```
python brain_predictions_harrypotter.py H bert-base-harrypotter.npy predictions_bert 12 2
```

* Subset-Moth-Radio-Hour (Reading and Listening)
```
python brain_predictions_subset_mothradio.py 1 bert-subset-moth-radio.npy reading bert-predictions 12
python brain_predictions_subset_mothradio.py 1 bert-subset-moth-radio.npy listening bert-predictions 12
```

* Moth-Radio-Hour (Listening)

```
python brain_predictions_mothradio.py 1 bert-moth-radio.npy bert-predictions 12
```
