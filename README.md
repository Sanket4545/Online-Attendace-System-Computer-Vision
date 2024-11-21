
# Online Attendance System

An automated attendance system using computer vision that allows users to upload training images of students, test images for attendance prediction, and download the attendance in an Excel file.

## Features
- Train the system using images labeled with student names.
- Upload testing images to predict attendance automatically.
- View attendance results directly in the application.
- Download attendance records in an Excel file.

## Technologies Used
- **Backend:** Python, Flask
- **Frontend:** HTML
- **Computer Vision:** OpenCV

## Prerequisites
- Python 3.8+ installed on your system.

## Setup Instructions

### Clone the Repository
```bash
git clone <repository_url>
cd <repository_name>
```

### Install Dependencies
Make sure you are in the project directory, then run:
```bash
pip install -r requirements.txt
```

### Run the Application
Execute the following command to start the application:
```bash
python app.py
```

### Access the Application
- Open your web browser and navigate to `http://127.0.0.1:5000/`.

## Usage
1. **Train the System:**
   - Upload training images with filenames corresponding to student names.

2. **Test Attendance:**
   - Upload testing images for attendance prediction.

3. **View Attendance:**
   - See the attendance records on the dashboard.

4. **Download Attendance:**
   - Click the download button to save attendance as an Excel file.


