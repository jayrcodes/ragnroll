import torch
import time
from transformers import pipeline

whisper = pipeline(
    "automatic-speech-recognition", 
    "openai/whisper-small", 
    torch_dtype=torch.float16, 
    device="mps",
    return_timestamps=True
)

start_time = time.time()

transcription = whisper("data/audio.mp3")

end_time = time.time()

print(transcription["text"])

print(f"Time taken: {end_time - start_time} seconds")
