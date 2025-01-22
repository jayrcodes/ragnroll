import torch
from transformers import pipeline

whisper = pipeline(
    "automatic-speech-recognition", 
    "openai/whisper-small", 
    torch_dtype=torch.float16, 
    device="cuda:0",
    return_timestamps=True
)

transcription = whisper("data/audio.mp3")

print(transcription["text"])
