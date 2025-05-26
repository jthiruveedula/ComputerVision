# Face Detection with MediaPipe

This project implements real-time face detection from various input sources (webcam, video files, or static image files) using Google's MediaPipe library. It counts and displays the number of faces detected in the input.

This version utilizes MediaPipe for its robust and accurate face detection capabilities, replacing an earlier implementation that used Haar Cascades.

## Dependencies

The project relies on the following Python libraries:

-   `opencv-python`: For image and video processing, and for displaying the output.
-   `mediapipe`: For the core face detection functionality.

These dependencies are listed in `requirements.txt` and can be easily installed using pip:

```bash
pip install -r requirements.txt
```

## How to Run

The script `faceDetectCount.py` is executed from the command line, with arguments specifying the input type and source.

**General command structure:**

```bash
python faceDetectCount.py --input_type <type> --source <source_path_or_id>
```

**Arguments:**

-   `--input_type`: Specifies the source of the visual input.
    -   `webcam`: For live feed from a connected webcam.
    -   `video`: For processing a video file.
    -   `image`: For processing a static image file.
-   `--source`: Specifies the identifier for the input.
    -   For `webcam`: A numerical ID for the camera (e.g., `0` for the default webcam).
    -   For `video`: The file path to the video (e.g., `path/to/your/video.mp4`).
    -   For `image`: The file path to the image (e.g., `path/to/your/image.jpg`).

**Examples:**

1.  **Using a webcam:**
    ```bash
    python faceDetectCount.py --input_type webcam --source 0
    ```

2.  **Using a video file:**
    ```bash
    python faceDetectCount.py --input_type video --source "path/to/your/video.mp4"
    ```
    (Replace `"path/to/your/video.mp4"` with the actual path to your video file.)

3.  **Using an image file:**
    ```bash
    python faceDetectCount.py --input_type image --source "path/to/your/image.jpg"
    ```
    (Replace `"path/to/your/image.jpg"` with the actual path to your image file.)

Upon execution, a window will appear displaying the input with detected faces highlighted by bounding boxes and labeled with a "Face No:". For webcam and video, press the **Enter** key in the display window to quit. For images, press any key.
