import tkinter as tk
from tkinter import PhotoImage
import csv
from PIL import Image, ImageTk
from scanner import load_interface as load_scanner_interface
from detector import load_interface as load_detector_interface
from report import load_interface as load_report_interface

def create_main_menu():
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Main menu title
    root.title("Fruit Freshness Detector")
    root.geometry("1000x600")
    root.configure(bg="#121212")

    project_title = tk.Label(
        root,
        text="Fruit Freshness Detector",
        font=("Arial", 24, "bold"),
        fg="#ffffff",
        bg="#121212",
    )
    project_title.pack(pady=20)

    # Buttons
    button_frame = tk.Frame(root, bg="#121212")
    button_frame.pack(side="left", padx=50, pady=50)

    button_style = {
        "font": ("Arial", 14, "bold"),
        "bg": "#1f1f1f",
        "fg": "#ffffff",
        "activebackground": "#333333",
        "activeforeground": "#ffffff",
        "width": 20,
        "height": 2,
        "relief": "flat",
    }

    scanner_button = tk.Button(
        button_frame,
        text="Scanner",
        **button_style,
        command=lambda: load_scanner_interface(root, create_main_menu),
    )
    scanner_button.pack(pady=10)

    image_detector_button = tk.Button(
        button_frame,
        text="Image Detector",
        **button_style,
        command=lambda: load_detector_interface(root, create_main_menu),
    )
    image_detector_button.pack(pady=10)

    report_button = tk.Button(
        button_frame,
        text="Report",
        **button_style,
        command=lambda: load_report_interface(root, create_main_menu, get_session_data('session_data.csv')),
    )
    report_button.pack(pady=10)

    exit_button = tk.Button(
        button_frame,
        text="Exit",
        **button_style,
        command=root.destroy,
    )
    exit_button.pack(pady=10)

    # Project image
    try:
        # Open the image using PIL
        img = Image.open("project_image.png")
        img = img.resize((300, 300))  # Resize image to 300x300, adjust as needed

        # Convert the resized image to a format Tkinter can use
        img_tk = ImageTk.PhotoImage(img)

        # Create a label to display the image
        image_label = tk.Label(root, image=img_tk, bg="#121212")
        image_label.image = img_tk  # Keep a reference to avoid garbage collection
        image_label.pack(side="right", padx=50, pady=50)
    except Exception as e:
        error_label = tk.Label(
            root,
            text="Error: Unable to load the image.",
            font=("Arial", 12),
            fg="#ff4444",
            bg="#121212",
        )
        error_label.pack(side="right", padx=50, pady=50)


    copyright_label = tk.Label(
        root,
        text="© All rights belong to Raezin",
        font=("Arial", 10),
        fg="#777777",
        bg="#121212",
        anchor="center",
    )
    copyright_label.pack(side="bottom", pady=20, fill="x")


def get_session_data(csv_file_path):
    # Load session data from a file or database
    # For demonstration purposes, we will use a hardcoded list of tuples
    session_data = []
    
    # Open the CSV file and read the contents
    with open(csv_file_path, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.reader(file)
        
        # Skip the header row if present
        next(reader)
        
        # Read each row and add to session_data list
        for row in reader:
            # Assuming the CSV columns match the format: (History No, Type, Fresh, Rotten, Date and Time)
            history_no = int(row[0])  # Convert History No to integer
            item_type = row[1]        # Type as string
            fresh = int(row[2])       # Fresh as integer
            rotten = int(row[3])      # Rotten as integer
            date_time = row[4]        # Date and Time as string
            
            session_data.append((history_no, item_type, fresh, rotten, date_time))
    
    return session_data

if __name__ == "__main__":
    root = tk.Tk()
    create_main_menu()
    root.mainloop()
