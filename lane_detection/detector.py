import cv2
import numpy as np
from .preprocessor import preprocess_image
from .utils import draw_lane_lines

class LaneDetector:
    def __init__(self):
        """Initialize the LaneDetector."""
        pass

    def detect_lane(self, image):
        """
        Detect lanes in the input image.

        Args:
            image (numpy.ndarray): Input image.

        Returns:
            Tuple[numpy.ndarray, numpy.ndarray]: Tuple containing:
                - Image with detected lane lines overlaid.
                - Binary mask of the lane lines.
        """
        try:
            # Step 1: Preprocess the input image
            processed_image, mask = preprocess_image(image)

            # Step 2: Create a blank canvas for lane lines
            lane_image = np.zeros_like(image)

            # Step 3: Draw lane lines on the canvas
            lane_image = draw_lane_lines(processed_image, lane_image)

            # Step 4: Overlay the lane lines on the original image
            detected_image = cv2.addWeighted(image, 0.8, lane_image, 1.0, 0)

            return detected_image, mask
        except Exception as e:
            print(f"Error during lane detection: {e}")
            # Return the original image and a black mask if detection fails
            blank_mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
            return image, blank_mask
