import tkinter as tk
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
from ultralytics import YOLO
from datetime import datetime
import csv

# CSV file path
CSV_FILE = "session_data.csv"

def load_interface(root, load_main_menu):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Configure the window
    root.title("Scanner Interface")
    root.configure(bg="#121212")

    # Add scanner-specific content
    title = tk.Label(
        root,
        text="Scanner Interface",
        font=("Arial", 24, "bold"),
        fg="#ffffff",
        bg="#121212",
    )
    title.pack(pady=20)

    info_label = tk.Label(
        root,
        text="Live scanning for fresh and rotten items.",
        font=("Arial", 14),
        fg="#ffffff",
        bg="#121212",
    )
    info_label.pack(pady=10)

    # Frame to display the video feed
    video_frame = tk.Label(root, bg="#121212")
    video_frame.pack(pady=20)

    # Desired size for the scanner feed
    scanner_width = 640
    scanner_height = 480

    # Load the YOLO model
    MODEL_PATH = "best.pt"  # Path to your trained YOLOv8 model
    model = YOLO(MODEL_PATH)

    # Tracking variables
    detected_objects = {}
    detection_threshold = 0.5  # Confidence threshold
    object_timeout = 2  # Time (in seconds) before a detected object can be counted again
    session_fresh = 0
    session_rotten = 0

    # Variable to control the video feed
    running = False
    cap = None

    def start_scanner():
        nonlocal running, cap
        if running:
            messagebox.showinfo("Info", "Scanner is already running!")
            return

        # Start the video feed
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Unable to access the camera.")
            return

        running = True
        update_video_feed()

    def update_video_feed():
        nonlocal running, cap, session_fresh, session_rotten
        if not running:
            return

        ret, frame = cap.read()
        if not ret:
            print("Failed to capture frame from camera.")
            stop_scanner()
            return

        # Resize the frame
        frame = cv2.resize(frame, (scanner_width, scanner_height))

        if model:
            # Perform YOLO detection
            results = model(frame, stream=True)
            current_time = datetime.now()

            for result in results:
                for box in result.boxes:
                    # Extract bounding box and class information
                    x1, y1, x2, y2 = map(int, box.xyxy[0])  # Bounding box coordinates
                    confidence = float(box.conf[0]) if hasattr(box, 'conf') else 0.0
                    class_id = int(box.cls[0]) if hasattr(box, 'cls') else -1

                    # Skip if confidence is below threshold
                    if confidence < detection_threshold:
                        continue

                    # Generate a unique identifier for the object
                    object_id = f"{class_id}_{x1}_{y1}_{x2}_{y2}"

                    # Check if the object is new or has timed out
                    if object_id in detected_objects:
                        last_seen = detected_objects[object_id]
                        if (current_time - last_seen).total_seconds() < object_timeout:
                            continue

                    # Update detected_objects with the current time
                    detected_objects[object_id] = current_time

                    # Get label if class_id is valid
                    label = model.names[class_id] if class_id in model.names else "Unknown"

                    # Update fresh/rotten counts based on label
                    if "good" in label.lower():
                        session_fresh += 1
                    elif "bad" in label.lower():
                        session_rotten += 1

                    # Draw bounding box and label
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                    cv2.putText(frame, f"{label}: {confidence:.2f}", (x1, y1 - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Convert the frame to ImageTk format
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        video_frame.imgtk = imgtk
        video_frame.configure(image=imgtk)

        # Call this function again after a short delay
        root.after(10, update_video_feed)

    def stop_scanner():
        nonlocal running, cap, session_fresh, session_rotten
        if running and cap is not None:
            running = False
            cap.release()

        # Save session data to CSV
        save_session_data(session_fresh, session_rotten)
        session_fresh, session_rotten = 0, 0

    def save_session_data(fresh, rotten):
        history_count = 1
        try:
            with open(CSV_FILE, mode="r") as file:
                history_count = sum(1 for _ in file)
        except FileNotFoundError:
            pass

        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            if history_count == 1:  # Add header if the file is new
                writer.writerow(["History", "Type", "Fresh", "Rotten", "Date & Time"])
            writer.writerow([history_count, "Scanner", fresh, rotten, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    def back_to_main_menu():
        stop_scanner()
        load_main_menu()

    # Frame to hold the buttons
    button_frame = tk.Frame(root, bg="#121212")
    button_frame.pack(pady=10)

    # Button to start the scanner
    start_button = tk.Button(
        button_frame,
        text="Start Scanner",
        font=("Arial", 14),
        bg="#1f1f1f",
        fg="#ffffff",
        activebackground="#333333",
        activeforeground="#ffffff",
        command=start_scanner,
    )
    start_button.grid(row=0, column=0, padx=10)

    # Back to Main Menu button
    back_button = tk.Button(
        button_frame,
        text="Back to Main Menu",
        font=("Arial", 14),
        bg="#1f1f1f",
        fg="#ffffff",
        activebackground="#333333",
        activeforeground="#ffffff",
        command=back_to_main_menu,
    )
    back_button.grid(row=0, column=1, padx=10)
