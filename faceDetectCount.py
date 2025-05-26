# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 01:49:14 2020
@author: Jagadeesh Thiruveedula
""" 

import cv2
import mediapipe as mp
import argparse
import sys

# Initialize MediaPipe Face Detection solution
mp_face_detection = mp.solutions.face_detection
# mp_drawing = mp.solutions.drawing_utils # For drawing face landmarks, if needed in future

def process_frame(frame, face_detection_model):
    """Processes a single frame to detect faces, draw bounding boxes, and count faces."""
    idx = 0 # Counter for detected faces in the frame
    # Convert the BGR image to RGB, as MediaPipe expects RGB input.
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the RGB frame with the MediaPipe Face Detection model.
    results = face_detection_model.process(rgb_frame)

    # If detections are present, iterate through them.
    if results.detections:
        for detection in results.detections:
            idx += 1
            # Extract normalized bounding box coordinates from the detection.
            bboxC = detection.location_data.relative_bounding_box
            ih, iw, _ = frame.shape # Get frame dimensions for coordinate conversion.
            # Convert normalized bounding box coordinates to pixel coordinates.
            x, y, w, h = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                         int(bboxC.width * iw), int(bboxC.height * ih)
            
            # Draw the bounding box rectangle on the frame.
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Put text indicating the face number, positioned below the bounding box.
            cv2.putText(frame, "Face No: " + str(idx), (x, y + h + 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (150, 150, 0), 2)
    return frame

def main():
    # Set up command-line argument parsing to allow flexible input sources.
    parser = argparse.ArgumentParser(description="Face detection using MediaPipe from various input sources.")
    parser.add_argument('--input_type', type=str, default='webcam',
                        choices=['webcam', 'video', 'image'],
                        help="Specify the type of input: 'webcam', 'video', or 'image'. Default is 'webcam'.")
    parser.add_argument('--source', type=str, default='0',
                        help="Specify the source: path to video/image file, or webcam ID (e.g., '0', '1'). Default is '0' for webcam.")
    args = parser.parse_args()

    video_capture = None # Initialize video_capture; used for webcam/video streams.

    # Initialize MediaPipe FaceDetection model using a context manager for resource handling.
    # model_selection=0 targets faces within 2 meters; min_detection_confidence for filtering weak detections.
    with mp_face_detection.FaceDetection(
        model_selection=0, min_detection_confidence=0.5) as face_detection:

        if args.input_type == 'image':
            # Processing logic for a single image file.
            frame = cv2.imread(args.source)
            if frame is None:
                print(f"Error: Could not read image from path: {args.source}")
                sys.exit(1) # Exit if image loading fails.
            
            print(f"Processing image: {args.source}")
            processed_frame = process_frame(frame, face_detection) # Detect faces in the image.
            cv2.imshow('Face Detector', processed_frame)
            print("Press any key to close the image window.")
            cv2.waitKey(0) # Wait indefinitely until a key is pressed.

        elif args.input_type in ['webcam', 'video']:
            # Processing logic for video input (webcam or file).
            source_for_capture = args.source
            if args.input_type == 'webcam':
                try:
                    # Convert webcam source to an integer ID.
                    source_for_capture = int(args.source)
                except ValueError:
                    print(f"Error: Invalid webcam ID '{args.source}'. Must be an integer (e.g., 0, 1).")
                    sys.exit(1)
            
            video_capture = cv2.VideoCapture(source_for_capture)
            if not video_capture.isOpened(): # Check if the video source was opened successfully.
                print(f"Error: Could not open {args.input_type} source: {args.source}")
                sys.exit(1)
            
            if args.input_type == 'webcam':
                 # Set buffer size for webcam; can help reduce lag on some systems/backends.
                video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

            print(f"Processing {args.input_type} from: {args.source}. Press Enter in the window to exit.")
            while True:
                ret, frame = video_capture.read() # Read a frame from the video source.
                if not ret: # If frame reading fails (e.g., end of video, camera error).
                    if args.input_type == 'video':
                        print("End of video file reached.")
                    else: # For webcam, this might indicate a problem or disconnection.
                        print("Error: Could not read frame from webcam. Exiting.")
                    break # Exit the loop.
                
                processed_frame = process_frame(frame, face_detection) # Detect faces in the current frame.
                cv2.imshow('Face Detector', processed_frame)
                
                # Check for Enter key (ASCII 13) press to exit the loop.
                # cv2.waitKey(5) provides a small delay, allowing time for key presses and window updates.
                if cv2.waitKey(5) & 0xFF == 13: 
                    break
        else:
            # This case should not be reached if argparse 'choices' are correctly defined and handled.
            print(f"Internal Error: Invalid input_type '{args.input_type}'.")
            sys.exit(1)

    # Clean up: close all OpenCV windows and release the video capture object if it was used.
    cv2.destroyAllWindows()
    if video_capture and video_capture.isOpened(): 
        video_capture.release()

if __name__ == '__main__':
    main() # Execute the main function when the script is run directly.
