import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from datetime import datetime
from ultralytics import YOLO
import csv
import os

# Load the trained YOLOv8 model
MODEL_PATH = "best.pt"  # Replace with the path to your YOLOv8 trained model
trained_model = YOLO(MODEL_PATH)

# Initialize session data tracking
session_items = []  # To track items classified during a session
history_count = 1  # Tracks session history across runs

# Load or initialize session_data.csv
CSV_FILE = "session_data.csv"
if os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode="r") as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        rows = list(reader)
        if rows:
            history_count = int(rows[-1][0]) + 1  # Set history count to last recorded session + 1
else:
    # Create the file and add the header
    with open(CSV_FILE, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["History", "Type", "Fresh", "Rotten", "Date & Time"])  # Header

def load_interface(root, load_main_menu):
    global session_items

    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Configure the window
    root.title("Image Detector Interface")
    root.configure(bg="#121212")

    # Add detector-specific content
    title = tk.Label(
        root,
        text="Image Detector Interface",
        font=("Arial", 24, "bold"),
        fg="#ffffff",
        bg="#121212",
    )
    title.pack(pady=20)

    # Add 'Choose Image' button to upload an image
    choose_button = tk.Button(
        root,
        text="Choose Image",
        font=("Arial", 14),
        bg="#1f1f1f",
        fg="#ffffff",
        activebackground="#333333",
        activeforeground="#ffffff",
        command=lambda: choose_image(),
    )
    choose_button.pack(pady=20)

    # Frame to hold the image and the additional information
    info_frame = tk.Frame(root, bg="#121212")
    info_frame.pack(pady=20)

    # Label to display the chosen image
    image_label = tk.Label(info_frame, bg="#121212")
    image_label.grid(row=0, column=0, padx=20)

    # Labels to display additional information (image name, date, time, and classification result)
    info_label = tk.Label(info_frame, bg="#121212", fg="#ffffff", font=("Arial", 12))
    info_label.grid(row=0, column=1, padx=20)

    def choose_image():
        # Open a file dialog to choose an image
        file_path = filedialog.askopenfilename(
            title="Select an Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")]
        )
        if file_path:
            # Open the image and convert it to a format suitable for Tkinter
            img = Image.open(file_path)
            img = img.resize((400, 300))  # Resize the image to fit in the UI
            img_tk = ImageTk.PhotoImage(img)

            # Update the image_label with the chosen image
            image_label.imgtk = img_tk
            image_label.configure(image=img_tk)

            # Classify the image
            fresh_count, rotten_count = classify_image(file_path)

        # Update session items
            session_items.append((fresh_count, rotten_count))

            # Update the info_label with classification result
            info_text = f"Fresh: {fresh_count}\nRotten: {rotten_count}"
            info_label.configure(text=info_text)


    def classify_image(image_path):
        # Use YOLOv8 to predict the class of the image
        results = trained_model.predict(source=image_path, save=False, conf=0.5)
        fresh_count = 0
        rotten_count = 0

        if results:
            for result in results:
                for cls, box in zip(result.boxes.cls, result.boxes):
                    # Extract the class name
                    class_name = result.names[int(cls)]
                    # Check if the item is fresh or rotten
                    if "good" in class_name.lower():
                        fresh_count += 1
                    elif "bad" in class_name.lower():
                        rotten_count += 1
                    elif "rotten" in class_name.lower():
                        rotten_count += 1
                    elif "fresh" in class_name.lower():
                        fresh_count += 1
                    elif "goods" in class_name.lower():
                        fresh_count += 1
                    elif "bads" in class_name.lower():
                        rotten_count += 1

            # Log the detection results
            print(
                f"image {image_path}: Fresh = {fresh_count}, Rotten = {rotten_count}"
            )

        return fresh_count, rotten_count


    def save_session_data():
        global session_items, history_count

        # Aggregate counts of fresh and rotten items
        total_fresh = sum(item[0] for item in session_items)
        total_rotten = sum(item[1] for item in session_items)
        date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Write session data to CSV
        with open(CSV_FILE, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([history_count, "Detector", total_fresh, total_rotten, date_time])

        # Increment history count and reset session_items
        history_count += 1
        session_items = []

    # Back to Main Menu button
    back_button = tk.Button(
        root,
        text="Back to Main Menu",
        font=("Arial", 14),
        bg="#1f1f1f",
        fg="#ffffff",
        activebackground="#333333",
        activeforeground="#ffffff",
        command=lambda: (save_session_data(), load_main_menu()),
    )
    back_button.pack(pady=20)
