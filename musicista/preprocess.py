import librosa
import math
import numpy as np

SAMPLE_RATE = 22050
TRACK_DURATION = 30  # measured in seconds
SAMPLES_PER_TRACK = SAMPLE_RATE * TRACK_DURATION

def preprocess_audio(file_path, target_time_steps=65, num_mfcc=13, n_fft=2048, hop_length=512, num_segments=1):
    """Preprocesses an audio file for music genre prediction.

    :param file_path: Path to the audio file
    :param target_time_steps: Desired number of time steps
    :param num_mfcc: Number of MFCC coefficients to extract
    :param n_fft: Interval for applying FFT (measured in number of samples)
    :param hop_length: Sliding window for FFT (measured in number of samples)
    :param num_segments: Number of segments to divide the audio file into
    :return: Preprocessed MFCC features
    """
    try:
        # Load audio file
        signal, sample_rate = librosa.load(file_path, sr=None)

        # Initialize an empty list to store MFCC features
        mfccs = []
        samples_per_segment = int(SAMPLES_PER_TRACK / num_segments)
        num_mfcc_vectors_per_segment = math.ceil(samples_per_segment / hop_length)

        # Process each segment of the audio file
        for d in range(num_segments):
            # Calculate start and finish sample for the current segment
            start = samples_per_segment * d
            finish = start + samples_per_segment

            # Extract MFCC features
            mfcc = librosa.feature.mfcc(y=signal[start:finish], sr=sample_rate, n_mfcc=num_mfcc, n_fft=n_fft, hop_length=hop_length)

            # Trim or pad the time steps to match the target number
            if mfcc.shape[1] >= target_time_steps:
                mfcc = mfcc[:, :target_time_steps]
            else:
                pad_width = target_time_steps - mfcc.shape[1]
                mfcc = np.pad(mfcc, pad_width=((0, 0), (0, pad_width)))

            # Append MFCC features to the list
            mfccs.append(mfcc.T)

        processed_data = np.vstack(mfccs)

        return processed_data

    except Exception as e:
        print(f"Error preprocessing audio file: {str(e)}")
        return None

# Example usage:
# processed_data = preprocess_audio(r"C:\Users\BHAGYABEE\OneDrive\Desktop\music genre prediction\Data\genres_original\blues\blues.00000.wav")
#
# if processed_data is not None:
#     # Reshape the processed data to match the model's input shape
#     processed_data_reshaped = np.reshape(processed_data, (1, processed_data.shape[0], processed_data.shape[1]))
#
#     # Now, you can use processed_data_reshaped as input for predicting the genre
#
#     print(f"Processed data shape: {processed_data_reshaped.shape}")
