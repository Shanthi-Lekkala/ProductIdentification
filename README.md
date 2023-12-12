## Shelfhelp - Fall 2023 Product identification

Setup:
1. Clone the repository
2. Install the requirements with python==3.9.12
3. Set the OpenAI API key in utils/config.py
4. Run main.py

Process:
1. As the camera starts, scan the product in the camera's viewpoint to detect the barcode and once the barcode is detected the program automatically stops and proceeds to the next step.
2. Internally the barcode is used to get the product information
3. User can then ask a question after beep, the voice is recorded, converted to text and sent to chatgpt to get responses.
4. Further the responses are converted to audio and the process can be repeated.

![Pipeline](images/Pipeline_diagram.png)