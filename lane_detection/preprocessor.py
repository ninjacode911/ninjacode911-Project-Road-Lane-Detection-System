import cv2
import numpy as np

def preprocess_image(image):
    """
    Preprocess the input image before lane detection.

    Steps:
    - Convert image to HSV color space.
    - Create a mask to detect yellow lanes.
    - Invert the mask for additional flexibility.
    - Color detected areas for visualization.

    Args:
        image (numpy.ndarray): Input image.

    Returns:
        Tuple[numpy.ndarray, numpy.ndarray]: 
            - The processed image with visualization.
            - The binary mask of detected yellow lanes.
    """
    if image is None:
        raise ValueError("Input image is None.")

    # Ensure the image has 3 channels
    if len(image.shape) != 3 or image.shape[2] != 3:
        raise ValueError("Input image must be a color image (3 channels).")

    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Define range for detecting yellow
    lower_yellow = np.array([10, 90, 100])
    upper_yellow = np.array([30, 255, 255])
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Optional visualization: highlight detected lane area in green
    output_image = image.copy()
    output_image[mask > 0] = (0, 255, 0)

    return output_image, mask
