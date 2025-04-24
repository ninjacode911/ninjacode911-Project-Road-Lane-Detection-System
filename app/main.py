import sys
import os
import cv2
import time
from datetime import datetime

# Ensure the current working directory is in sys.path
try:
    path = os.getcwd()
    if path not in sys.path:
        sys.path.insert(1, path)
except Exception as e:
    print(f"[ERROR] Failed to insert current path: {e}")

# Import custom modules
from lane_detection.detector import LaneDetector
from app.gen_log import Logger


def ensure_directory(path):
    """Create the directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)


def process_image(detector, logger, input_path, output_dir):
    logger.log_info('Processing image...')

    image = cv2.imread(input_path)
    if image is None:
        logger.log_error(f"Could not read image from {input_path}")
        return

    try:
        detected_image, mask = detector.detect_lane(image)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_img_path = os.path.join(output_dir, f"detected_lane_{timestamp}.jpg")
        output_mask_path = os.path.join(output_dir, f"lane_mask_{timestamp}.jpg")

        ensure_directory(output_dir)
        cv2.imwrite(output_img_path, detected_image)
        cv2.imwrite(output_mask_path, mask)

        logger.log_info(f"Image saved at: {output_img_path}")
        logger.log_info(f"Mask saved at: {output_mask_path}")
    except Exception as e:
        logger.log_error(f"Error during image processing: {e}")


def process_video(detector, logger, input_path, output_dir):
    logger.log_info('Processing video...')

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        logger.log_error(f"Failed to open video file: {input_path}")
        return

    try:
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        video_out_path = os.path.join(output_dir, f"detected_lane_{timestamp}.mp4")
        mask_out_path = os.path.join(output_dir, f"lane_mask_{timestamp}.mp4")

        ensure_directory(output_dir)
        out = cv2.VideoWriter(video_out_path, fourcc, fps, (width, height))
        out_mask = cv2.VideoWriter(mask_out_path, fourcc, fps, (width, height))

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            try:
                detected_frame, mask = detector.detect_lane(frame)
                out.write(detected_frame)
                out_mask.write(mask)
            except Exception as frame_error:
                logger.log_error(f"Error processing frame: {frame_error}")

        logger.log_info(f"Video saved at: {video_out_path}")
        logger.log_info(f"Mask video saved at: {mask_out_path}")

    except Exception as e:
        logger.log_error(f"Unexpected error during video processing: {e}")
    finally:
        cap.release()
        out.release()
        out_mask.release()
        cv2.destroyAllWindows()


def main():
    logger = Logger()
    logger.log_info('--- Lane Detection Script Started ---')

    try:
        detector = LaneDetector()
    except Exception as e:
        logger.log_error(f"Failed to initialize LaneDetector: {e}")
        return

    # Paths
    test_image_path = 'data/test_images/example5.jpg'
    test_video_path = 'data/test_videos/example1.mp4'
    image_output_dir = 'results/images'
    video_output_dir = 'results/videos'
    mask_output_dir = 'results/masks'

    # Process Image
    process_image(detector, logger, test_image_path, image_output_dir)
    
    # Process Video
    process_video(detector, logger, test_video_path, video_output_dir)

    logger.log_info('--- Lane Detection Script Completed ---')

    # Print Log File
    try:
        with open(logger.get_log_file_path(), 'r') as log_file:
            print("\n--- Log Output ---")
            print(log_file.read())
    except Exception as e:
        print(f"[ERROR] Unable to read log file: {e}")


if __name__ == "__main__":
    main()
