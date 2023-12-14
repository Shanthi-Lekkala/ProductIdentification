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
    live_video = False # Set it to True to test on a live video
    product_no = 1
    while True:
        barcode, msg = barcode_scanner(model, live_video, product_no, False)
        print(barcode, msg)
        if not barcode:
            text_to_audio("Barcode not found, please scan again.")
            continue
        product_info = get_product_json(barcode)
        text_to_audio("You are holding {}, say continue to keep looking".format(product_info['name']))
        print(product_info['name'])
        user_input = record_and_transcribe()
        print(user_input)
        if "continue" in user_input.lower(): 
            product_no += 1
            continue
        text_to_audio("You can use this interface to query any information about the product")
        break
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

except Exception as e:
    print(f"An unexpected error occurred: {e}")




