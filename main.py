from utils.barcode_detection import barcode_scanner
from utils.product_info import get_product_json
from utils.utils import send_first_message, chat_with_gpt, text_to_audio, record_and_transcribe
import time
from roboflow import Roboflow

def load_model():
    rf = Roboflow(api_key="vQ6l6Ky2d9IQN5H6sNDH")
    project = rf.workspace().project("barcodes-zmxjq")
    model = project.version(4).model
    return model

model=load_model()

welcomeMessage = "Hello, please start scanning the product"

text_to_audio(welcomeMessage)
try:
    barcode, msg = barcode_scanner(model)
    print(barcode, msg)
    if barcode is None:
        text_to_audio("Barcode not found")

    product_info = get_product_json(barcode)
    text_to_audio("You are holding " + product_info['name'])
    text_to_audio("")
    input_message = "Initiate"

    user_input = send_first_message(product_info)
    conversation_history = [{"role":"assistant", "content":user_input}]

    while True:
        text_to_audio("Please ask your question after beep")
        time.sleep(1)
        text_to_audio("beep")
        
        user_input = record_and_transcribe()
        if "end" in user_input.lower(): break
        print(user_input)
        text_to_audio("Thank you")

        # Send user input to ChatGPT
        conversation_history, response = chat_with_gpt(conversation_history, user_input)
        print(response)

        text_to_audio(response)

except Expection as e:
    print(f"An unexpected error occurred: {e}")




