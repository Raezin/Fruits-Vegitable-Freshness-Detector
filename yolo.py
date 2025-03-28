# from ultralytics import YOLO
# import cv2

# # Load the YOLOv8 model
# model = YOLO('best.pt')

# # Open the webcam
# cap = cv2.VideoCapture(0)  # 0 for the default webcam; change to 1 or 2 for external cameras

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         print("Failed to grab frame")
#         break

#     # Perform detection on the current frame
#     results = model.predict(source=frame, save=False, conf=0.5, show=True)

#     # Display the live detections
#     cv2.imshow("YOLOv8 Live Detection", frame)

#     # Break the loop on pressing 'q'
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

# # Release resources
# cap.release()
# cv2.destroyAllWindows()


# # from ultralytics import YOLO

# # # Load your fine-tuned model
# # model = YOLO('best.pt')

# # # Run inference
# # results = model.predict('download.jpeg')
# # result = results[0]
# # result.show()


# from inference import InferencePipeline
# from inference.core.interfaces.stream.sinks import render_boxes
 
# pipeline = InferencePipeline.init(
#     model_id="yolov8n-640",
#     video_reference=0,
#     on_prediction=render_boxes
# )
# pipeline.start()
# pipeline.join()

import csv

def create_csv_file(file_path):
    # Sample data to write to the CSV file
    data = [
        ["History No", "Type", "Fresh", "Rotten", "Date and Time"],  # Header row
        [1, "Scanner", 10, 2, "2021-08-01 12:00:00"],
        [2, "Detector", 8, 4, "2021-08-02 13:30:00"],
        [3, "Scanner", 6, 6, "2021-08-03 15:45:00"],
        [4, "Scanner", 9, 3, "2021-08-04 10:15:00"],
        [5, "Detector", 7, 5, "2021-08-05 11:20:00"]
    ]

    # Open the CSV file in write mode and create a writer object
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the rows of data to the CSV file
        writer.writerows(data)

    print(f"CSV file created successfully at: {file_path}")

# Call the function to create a CSV file
create_csv_file("session_data.csv")
