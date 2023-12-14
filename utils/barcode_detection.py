import cv2
from detection.mser import find_barcodes, get_barcode
import numpy as np
import matplotlib.pyplot as plt
from pyzxing import BarCodeReader
from statistics import mode


def draw_bbox(image, x1, x2, y1, y2, barcode_text):
    image = cv2.rectangle(image, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Get the position to write the text
    text_position = (x1, y1-10)

    # Write the barcode data above the bounding box
    cv2.putText(image, barcode_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image

def get_coordinates(image, x, y, width, height):

    # Calculate the top-left and bottom-right points of the rectangle based on the center
    x_top_left = int(x - width / 2)
    y_top_left = int(y - height / 2)
    x_bottom_right = int(x + width / 2)
    y_bottom_right = int(y + height / 2)

    return (x_top_left, y_top_left, x_bottom_right, y_bottom_right)


def get_rotation_angle(image):
    blurred = cv2.GaussianBlur(image, (5, 5), 0)
    edges = cv2.Canny(blurred, 50, 150)

    lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=50)
    angles = []
    if lines is not None:
        for line in lines:
            rho, theta = line[0]
            angle = np.degrees(theta)
            angles.append(int(angle))

    most_angle = mode(angles) if len(angles)>0 else None
    return most_angle

def rotate_image(image, angle):
    height, width = image.shape[:2]

    rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), angle, 1)

    # Calculate the size of the rotated image
    new_width = int(np.ceil(width * abs(np.cos(np.radians(angle)))) + np.ceil(height * abs(np.sin(np.radians(angle)))))
    new_height = int(np.ceil(width * abs(np.sin(np.radians(angle)))) + np.ceil(height * abs(np.cos(np.radians(angle)))))

    # Update the rotation matrix to take into account the new image size
    rotation_matrix[0, 2] += (new_width - width) / 2
    rotation_matrix[1, 2] += (new_height - height) / 2

    # Apply the rotation without cropping
    rotated_image = cv2.warpAffine(image, rotation_matrix, (new_width, new_height), borderMode=cv2.BORDER_CONSTANT, borderValue=(255, 255, 255))

    # rotated_image = cv2.warpAffine(image, rotation_matrix, (width, height))

    # Display the original and rotated images
    # plt.imshow(rotated_image)
    # plt.axis('off')  # Turn off axis labels
    # plt.show()

    return rotated_image

def process_frame(model, frame):
    pred = model.predict(frame, confidence=60, overlap=30).json()['predictions']
    if len(pred)<=0: return None, frame

    bbox = (pred[0]['x'], pred[0]['y'], pred[0]['width'], pred[0]['height'])
    int_bbox = tuple(int(value) for value in bbox)

    x1, y1, x2, y2 = get_coordinates(frame, *int_bbox)
    roi = frame[y1:y2, x1:x2]

    angle = get_rotation_angle(roi)
    if angle is None: return None, frame
    rotated_barcode = rotate_image(roi, angle)

    reader = BarCodeReader()
    barcode = reader.decode_array(rotated_barcode)

    if not barcode or 'raw' not in barcode[0]: return None, frame

    barcode = str(barcode[0]['raw'].decode('utf-8'))
    frame_with_barcode = draw_bbox(frame, x1, x2, y1, y2, barcode)

    # Display the frame with detected barcodes
    cv2.namedWindow("Barcode Detection", cv2.WINDOW_NORMAL)  # Use this line before cv2.imshow
    cv2.imshow("Barcode Detection", frame_with_barcode)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    # plt.imshow(frame_with_barcode)
    # plt.axis('off')  # Turn off axis labels
    plt.show()

    return barcode, frame_with_barcode

    

def barcode_scanner(model, live_video, product_no, save_output=False):
    new_barcode = ""
    video_path = "test_samples/product_{}.mov".format(product_no) if not live_video else 0
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        return None, "Error: Could not open camera."

    if save_output:
        # Get video properties
        fps = cap.get(cv2.CAP_PROP_FPS)
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)+0.5)
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)+0.5)

        # Create a VideoWriter object to save the processed video
        output_path = "output/product_{}.MOV".format(product_no)  # Replace with your desired output path
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out_vid = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            return new_barcode, "Error: Couldn't read frame."
        frame_count += 1

        # Process every 30 frames
        if frame_count % 30 == 0:
            barcode, frame=process_frame(model, frame)
            if barcode: 
                new_barcode = barcode
                break

        # cv2.imshow("Barcode Detection", frame)
        if save_output: out_vid.write(frame)
        
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    if save_output: out_vid.release()
    cv2.destroyAllWindows()

    return new_barcode, "Success"


if __name__ == "__main__":
    img_file = "test_samples/test_2.jpeg"
    img = cv2.imread(img_file)
    barcode, bbox = get_barcode(img)
    print(barcode)
