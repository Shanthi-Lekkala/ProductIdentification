import subprocess

def text_to_audio(text):
    # Use the 'say' command on macOS
    subprocess.call(['say', text])

# Example usage
# text_to_audio("Hello, please start scanning the product")


# from gtts import gTTS
# import os
# import tempfile

# def text_to_audio(text, language='en'):
#     # Create a gTTS object
#     tts = gTTS(text=text, lang=language, slow=False)

#     # Save the audio file to a temporary file
#     temp_file = tempfile.NamedTemporaryFile(delete=False)
#     tts.save(temp_file.name)

#     # Play the audio using osascript
#     os.system(f"osascript -e 'do shell script \"afplay {temp_file.name}\"'")

#     # Delete the temporary file
#     os.remove(temp_file.name)

# # Example usage
# text = "Hello, this is a sample text to be converted to audio."
# text_to_audio(text)

