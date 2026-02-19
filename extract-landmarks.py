import cv2
import mediapipe as mp
import json

from pathlib import Path

# Initialize MediaPipe Holistic solution (which internally uses MediaPipe Hands for detailed hand tracking)
mp_holistic = mp.solutions.holistic
holistic = mp_holistic.Holistic(
    static_image_mode=False,
    model_complexity=1,
    smooth_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Set the path to your directory containing the videos
directory = Path("videos")

# Create landmarks folder if it doesn't exist**
output_dir = Path("landmarks")
output_dir.mkdir(exist_ok=True)


# Loop through all files matching the pattern "*-isl.mp4"
for file in directory.glob("*.mp4"):
    # Create the new file name by replacing "-isl.mp4" with ".mp4"
    word = file.name.split(".")[0]

    output_path = output_dir / f"{word}.json"
    # Skip video if its JSON already exists**
    if output_path.exists():
        print(f"Skipping {word}.json (already exists)")
        continue

    print(f"Extracting {word} landmarks...")
    video_path = f"videos/{word}.mp4"
    cap = cv2.VideoCapture(video_path)

    # List to store the extracted landmarks for each frame
    skeleton_data = []
    frame_index = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the frame from BGR to RGB (MediaPipe expects RGB)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Process the image to extract landmarks
        results = holistic.process(image_rgb)

        # Create a dictionary to store landmarks for this frame
        frame_landmarks = {"frame": frame_index}

        # Extract pose landmarks (if available)
        if results.pose_landmarks:
            frame_landmarks["pose_landmarks"] = [
                {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z,
                    "visibility": lm.visibility
                }
                for lm in results.pose_landmarks.landmark
            ]
        else:
            frame_landmarks["pose_landmarks"] = None

        # Extract left hand landmarks (if available)
        # Each hand provides 21 landmarks including finger joints (wrist, thumb, index, middle, ring, and pinky)
        if results.left_hand_landmarks:
            frame_landmarks["left_hand_landmarks"] = [
                {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z
                }
                for lm in results.left_hand_landmarks.landmark
            ]
        else:
            frame_landmarks["left_hand_landmarks"] = None

        # Extract right hand landmarks (if available)
        if results.right_hand_landmarks:
            frame_landmarks["right_hand_landmarks"] = [
                {
                    "x": lm.x,
                    "y": lm.y,
                    "z": lm.z
                }
                for lm in results.right_hand_landmarks.landmark
            ]
        else:
            frame_landmarks["right_hand_landmarks"] = None

        # Append this frame's landmarks to the overall data list
        skeleton_data.append(frame_landmarks)
        frame_index += 1

    # Clean up resources
    cap.release()

    # Save the extracted data to a JSON file
    with open(f"landmarks/{word}.json", "w") as f:
        json.dump(skeleton_data, f, indent=2)

    print(f"Landmark extraction complete for {word}. Data saved to {word}.json")

holistic.close()
print(f"Landmark extraction complete.")
