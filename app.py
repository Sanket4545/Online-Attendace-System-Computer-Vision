from flask import Flask, render_template, request, redirect, url_for, send_file, flash
import os
import cv2
import numpy as np
import face_recognition
import pandas as pd
from tabulate import tabulate

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flash messages

# Set the paths for storing uploaded files
UPLOAD_FOLDER_TRAIN = './uploads/train/'
UPLOAD_FOLDER_TEST = './uploads/test/'

# Ensure the folders exist
os.makedirs(UPLOAD_FOLDER_TRAIN, exist_ok=True)
os.makedirs(UPLOAD_FOLDER_TEST, exist_ok=True)

known_names = []
known_name_encodings = []

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/upload_train', methods=['POST'])
def upload_train():
    train_files = request.files.getlist('train_images')
    for file in train_files:
        file.save(os.path.join(UPLOAD_FOLDER_TRAIN, file.filename))
    flash('Training images uploaded successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/upload_test', methods=['POST'])
def upload_test():
    test_file = request.files['test_image']
    test_file.save(os.path.join(UPLOAD_FOLDER_TEST, test_file.filename))
    flash('Test image uploaded successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/get_attendance', methods=['GET'])
def get_attendance():
    global known_names, known_name_encodings
    known_names = []
    known_name_encodings = []

    # Load training images
    for filename in os.listdir(UPLOAD_FOLDER_TRAIN):
        image_path = os.path.join(UPLOAD_FOLDER_TRAIN, filename)
        image = face_recognition.load_image_file(image_path)
        encoding = face_recognition.face_encodings(image)[0]
        
        known_name_encodings.append(encoding)
        known_names.append(os.path.splitext(filename)[0].capitalize())

    # Process the test image
    test_image_path = os.path.join(UPLOAD_FOLDER_TEST, os.listdir(UPLOAD_FOLDER_TEST)[0])
    image = cv2.imread(test_image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(image_rgb)
    face_encodings = face_recognition.face_encodings(image_rgb, face_locations)

    attendance = {}
    recognized_names = []

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_name_encodings, face_encoding)
        name = ""

        face_distances = face_recognition.face_distance(known_name_encodings, face_encoding)
        best_match = np.argmin(face_distances)

        if matches[best_match]:
            name = known_names[best_match]

        attendance[name] = "Present"
        recognized_names.append(name)

        # Draw rectangles on the faces
        cv2.rectangle(image, (left, top), (right, bottom), (0, 0, 255), 2)
        cv2.rectangle(image, (left, bottom - 15), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(image, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    # Create attendance DataFrame
    attendance_df = pd.DataFrame({
        "Name": known_names,
        "Attendance": ["Present" if name in recognized_names else "Absent" for name in known_names]
    })

    # Save attendance to Excel
    attendance_df.to_excel("attendance.xlsx", index=False)

    # Save the output image
    output_path = "./static/output.jpg"
    cv2.imwrite(output_path, image)

    # Display attendance as HTML table
    attendance_data = attendance_df.values.tolist()
    attendance_table = tabulate(attendance_data, headers=["Name", "Attendance"], tablefmt="html")

    # test_file = request.files['test_image']
    # os.remove(os.path.join(UPLOAD_FOLDER_TRAIN, test_file.filename))

    return f"""
    <style>
        body {{
            font-family: 'Poppins', sans-serif;
            background-color: #f5f7fa;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        h2 {{
            color: #333;
            margin-bottom: 20px;
        }}
        table {{
            margin: 0 auto;
            border-collapse: collapse;
            width: 50%;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: center;
        }}
        th {{
            background-color: #4CAF50;
            color: white;
        }}
        tr:nth-child(even) {{background-color: #f2f2f2;}}
        tr:hover {{background-color: #ddd;}}
        img {{
            margin-top: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }}
        a {{
            display: inline-block;
            margin-top: 20px;
            padding: 10px 20px;
            background-color: #4CAF50;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }}
        a:hover {{
            background-color: #45a049;
        }}
    </style>

    <h2>Attendance</h2>
    {attendance_table}
    <br><img src="/static/output.jpg" width="600">
    <br><a href="/download_excel">Download Attendance Excel</a>
    """

@app.route('/download_excel', methods=['GET'])
def download_excel():
    return send_file("attendance.xlsx", as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
