
Download video from youtube

```
yt -f '139+134' --merge-output-format mp4 --output video.mp4 https://www.youtube.com/watch?v=
```

Convert video to audio

```
ffmpeg -i video.mp4 -q:a 0 -map a audio.mp3
```

Edge cases encountered fix:

PermissionError: [Errno 13] Permission denied: '/home/jayrpc/.cache/huggingface/hub/models--openai--whisper-small'

```
chmod -R 755 /home/jayrpc/.cache/huggingface
sudo chown -R $USER:$USER /home/jayrpc/.cache/huggingface
```

Transcribe audio

```
python test_transcribe.py
```
