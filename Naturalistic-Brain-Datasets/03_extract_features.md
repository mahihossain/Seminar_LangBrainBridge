# How to extract model representations

You can use the script `./Stimuli/extract_features_words.py`. The script use the file `./Stimuli/text_model_config.json` to get the model configuration. You can also add entries in this file.

To test this script run:
`./.venv/bin/python3 ./Stimuli/extract_features_words.py --input_file ./Stimuli/Harry_Potter/stimuli_words.npy --model bert-base --sequence_length 20 --output_file harrypotter
./Stimuli/Harry_Potter/stimuli_words.npy`.
This command will save bert representations of harry potter text for each layer with the given sequence length