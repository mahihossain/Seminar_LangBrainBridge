import whisper
import argparse
import pandas as pd
import numpy as np
import os

def extract_features_audio(audio_file, model_name, alignment_file):
    model = whisper.load_model(model_name)

    # Load Audio (Adapt if you load differently)
    audio = whisper.load_audio(audio_file)

    # Load Audio-Word Alignment 
    alignment_data = pd.read_csv(alignment_file)

    # Segment-wise Feature Extraction
    features = []
    for _, row in alignment_data.iterrows():
        start_time = row['start_time']
        end_time = row['end_time']
        segment = audio[start_time * 16000: end_time * 16000]
        segment_features = model.encode(segment)
        features.append(segment_features)

    return np.array(features)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--audio_dir', type=str, default="data/audio")
    parser.add_argument('--alignment_dir', type=str, default="data/alignments")
    parser.add_argument('--model', type=str, default="base", choices=whisper.available_models())
    parser.add_argument('--output_dir', type=str, default="data/features")
    args = parser.parse_args()

    for audio_file in os.listdir(args.audio_dir):
        if audio_file.endswith(".wav"): 
            audio_path = os.path.join(args.audio_dir, audio_file)
            alignment_file = os.path.join(args.alignment_dir, audio_file.replace(".wav", ".csv"))
            features = extract_features_audio(audio_path, args.model, alignment_file)

            output_file = os.path.join(args.output_dir, audio_file.replace(".wav", ".npy"))
            np.save(output_file, features) 
