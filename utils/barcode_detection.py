import cv2
from detection.mser import find_barcodes, get_barcode
import numpy as np


def draw_bbox(image, points, barcode_text):
    # Convert the list of points to NumPy array
    points = np.array(points, dtype=np.int32)

    # Reshape the array to a 2D array
    points = points.reshape((-1, 1, 2))

    # Draw a polygon (bbox) on the image
    cv2.polylines(image, [points], isClosed=True, color=(0, 255, 0), thickness=2)

    # Get the position to write the text
    text_position = (points[0][0][0], points[0][0][1] - 10)

    # Write the barcode data above the bounding box
    cv2.putText(image, barcode_text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return image

def barcode_scanner():
    new_barcode = ""
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        return None, "Error: Could not open camera."

    while True:
        ret, frame = cap.read()
        if not ret:
            return None, "Error: Couldn't read frame."
            # break
        x = get_barcode(frame)
        if x:
            barcode, bbox = get_barcode(frame)
            frame_with_barcode = draw_bbox(frame, bbox, barcode)
            # Display the frame with detected barcodes
            cv2.imshow("Barcode Detection", frame_with_barcode)
            if new_barcode!=barcode:
                # print(barcode)
                new_barcode = barcode
            break
        else:
            cv2.imshow("Barcode Detection", frame)
        # Break the loop if 'q' key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the video capture object and close all windows
    cap.release()
    cv2.destroyAllWindows()

    return new_barcode, "Success"
    # start_conversation(new_barcode)


if __name__ == "__main__":
    img_file = "test_samples/test_2.jpeg"
    img = cv2.imread(img_file)
    barcode, bbox = get_barcode(img)
    print(barcode)
