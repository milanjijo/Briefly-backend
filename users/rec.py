import openai
openai.api_key = "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"
f = open("harvard.wav", "rb")
transcript = openai.Audio.transcribe("whisper-1", f)
print(transcript['text'])