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

def record_and_transcribe(filename="output/output.mp3", duration=5, sample_rate=44100):
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


# def draw_bbox(image, x, y, width, height):

#     # Calculate the top-left and bottom-right points of the rectangle based on the center
#     x_top_left = int(x - width / 2)
#     y_top_left = int(y - height / 2)
#     x_bottom_right = int(x + width / 2)
#     y_bottom_right = int(y + height / 2)

#     # Draw a rectangle on the image
#     cv2.rectangle(image, (x_top_left, y_top_left), (x_bottom_right, y_bottom_right), (255, 0, 0), 2)

    return image


def draw_bbox(image, x1, x2, y1, y2, barcode_text):
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Get the position to write the text
    text_position = (x1, y1-10)

    # Write the barcode data above the bounding box
    cv2.putText(image, barcode_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image