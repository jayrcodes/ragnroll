import torch
import time
from transformers import pipeline
import sys
import os
import subprocess

source = sys.argv[1]
source_dir = os.path.dirname(source)
source_filename = os.path.basename(source)

# ffmpeg -i input_video.mp4 -q:a 0 -map a output_audio.mp3
output_audio_filename = f"{source_filename}.mp3"

print(f"\n\nConverting {source} to {output_audio_filename}\n\n")

subprocess.run(["ffmpeg", "-i", source, "-q:a", "0", "-map", "a", os.path.join(source_dir, output_audio_filename)])

print(f"\n\nTranscribing {output_audio_filename}\n\n")

output_filename = f"{source_filename}_transcribed.txt"
output_path = os.path.join(source_dir, output_filename)

start_time = time.time()

whisper = pipeline(
    "automatic-speech-recognition", 
    "openai/whisper-small", 
    torch_dtype=torch.float16, 
    device="mps",
    return_timestamps=True
)

output_audio_path = os.path.join(source_dir, output_audio_filename)

transcription = whisper(output_audio_path)

end_time = time.time()

transcription = transcription["text"]

# print(transcription["text"])

# write to file
with open(output_path, "w") as f:
    f.write(transcription)

print(f"\n\nDone. Time taken: {end_time - start_time} seconds\n\n")

