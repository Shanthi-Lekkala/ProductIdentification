from openai import OpenAI
import sounddevice as sd
from scipy.io.wavfile import write
import subprocess
import json
import config

client = OpenAI(api_key = config.key)
model = "gpt-3.5-turbo"

def chat_with_gpt(history, prompt):
	history += [{"role":"user", "content":prompt}]
	response = client.chat.completions.create(
		model=model,
		messages=history
	)
	output_text = response.choices[0].message.content
	history += [{"role":"assistant", "content":output_text}]
	return history, output_text

def send_first_message(msg):
	return "Product Information:" + json.dumps(msg) + "Please help me answer the following questions"

def record_and_transcribe(filename="output.mp3", duration=5, sample_rate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    print("Recording complete.")

    write(filename, sample_rate, audio_data)

    audio_file= open(filename, "rb")
    transcript = client.audio.transcriptions.create(
      model="whisper-1", 
      file=audio_file
    )

    return transcript.text

def text_to_audio(text):
    # Use the 'say' command on macOS
    subprocess.call(['say', text])