import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import csv

# Configurable graph and table dimensions
GRAPH_WIDTH = 5  # Default width of the bar graph (in inches)
GRAPH_HEIGHT = 3  # Default height of the bar graph (in inches)
TABLE_ROWS = 6  # Default number of rows in the table

# Function to load the report interface
def load_interface(root, load_main_menu, session_data):
    # Clear existing widgets
    for widget in root.winfo_children():
        widget.destroy()

    # Configure the window
    root.title("Session Report")
    root.configure(bg="#121212")

    # Add report title
    title = tk.Label(
        root,
        text="Session Report",
        font=("Arial", 24, "bold"),
        fg="#ffffff",
        bg="#121212",
    )
    title.pack(pady=20)

    # Generate summary data
    total_items = len(session_data)

    # Add summary section
    summary_label = tk.Label(
        root,
        text=f"Summary:\nTotal Items: {total_items} .",
        font=("Arial", 14),
        fg="#ffffff",
        bg="#121212",
    )
    summary_label.pack(pady=10)

    # Create a frame for graph and table
    content_frame = tk.Frame(root, bg="#121212")
    content_frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add graph
    def show_graph(frame):
        # Extract data for the bar chart
        history_numbers = [item[0] for item in session_data]  # Extract "History No"
        fresh_values = [item[2] for item in session_data]     # Extract "Fresh" values
        rotten_values = [item[3] for item in session_data]    # Extract "Rotten" values

        # Create the figure and bar chart
        fig, ax = plt.subplots(figsize=(GRAPH_WIDTH, GRAPH_HEIGHT), dpi=100)
        x_indices = range(len(history_numbers))  # Indices for the bars

        bar_width = 0.4  # Width of each bar

        # Plot Fresh and Rotten bars
        ax.bar(
            [x - bar_width / 2 for x in x_indices], fresh_values,
            width=bar_width, label="Fresh", color="#4CAF50"
        )
        ax.bar(
            [x + bar_width / 2 for x in x_indices], rotten_values,
            width=bar_width, label="Rotten", color="#FF5252"
        )

        # Set x-ticks and labels
        ax.set_xticks(x_indices)
        ax.set_xticklabels(history_numbers)

        # Set labels and title
        ax.set_xlabel("History", fontsize=12)
        ax.set_ylabel("Number of Items", fontsize=12)
        ax.set_title("Fresh vs. Rotten Items by History", fontsize=14)

        # Add a grid and legend
        ax.grid(axis="y", linestyle="--", alpha=0.7)
        ax.legend()

        # Customize y-axis with 10-gap increments
        max_value = max(max(fresh_values), max(rotten_values)) + 10
        ax.set_yticks(range(0, max_value + 1, 10))

        # Draw the chart on the Tkinter canvas
        canvas = FigureCanvasTkAgg(fig, frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    graph_frame = tk.Frame(content_frame, bg="#121212")
    graph_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    show_graph(graph_frame)

    # Add table
    table_frame = tk.Frame(content_frame, bg="#121212")
    table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    # Create Treeview for the table
    table = ttk.Treeview(
        table_frame,
        columns=("History No", "Type", "Fresh", "Rotten", "Date and Time"),
        show="headings",
        height=TABLE_ROWS,
    )

    # Define column headings
    for col in ["History No", "Type", "Fresh", "Rotten", "Date and Time"]:
        table.heading(col, text=col)

    # Define column widths
    for col, width in zip(["History No", "Type", "Fresh", "Rotten", "Date and Time"], [100, 150, 100, 100, 200]):
        table.column(col, width=width, anchor="center")

    # Insert data into the table
    for row in session_data:
        table.insert("", "end", values=row)

    table.pack(fill="both", expand=True)

    # Configure grid weights
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=2)  # Adjust weight for table width
    content_frame.grid_rowconfigure(0, weight=1)

    # Export session data to CSV
    def export_to_csv():
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save Report as CSV",
        )
        if file_path:
            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["History No", "Type", "Fresh", "Rotten", "Date and Time"])
                writer.writerows(session_data)
            messagebox.showinfo("Export Successful", f"Report saved to {file_path}")

    # Create a frame for buttons
    buttons_frame = tk.Frame(root, bg="#121212")
    buttons_frame.pack(pady=20)

    # Export button
    export_button = tk.Button(
        buttons_frame,
        text="Export to CSV",
        font=("Arial", 14),
        bg="#1f1f1f",
        fg="#ffffff",
        activebackground="#333333",
        activeforeground="#ffffff",
        command=export_to_csv,
    )
    export_button.pack(side="left", padx=10)

    # Back to Main Menu button
    back_button = tk.Button(
        buttons_frame,
        text="Back to Main Menu",
        font=("Arial", 14),
        bg="#1f1f1f",
        fg="#ffffff",
        activebackground="#333333",
        activeforeground="#ffffff",
        command=lambda: load_main_menu(),
    )
    back_button.pack(side="left", padx=10)
