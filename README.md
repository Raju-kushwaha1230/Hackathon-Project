## Skin Type Checker - Web Application
This is a web application that allows users to upload an image or take a photo using their camera to check their skin type. Based on the skin type, it will recommend products to enhance the user's skin health.

## Features:
Upload a clear photo of your skin.
Take a picture using your device's camera.
Detect skin type using a pre-trained machine learning model.
Display the skin type with confidence percentage.
Recommend products for the detected skin type.

-----------
1. Clone the repository
```
git clone https://github.com/your-username/skin-type-checker.git
```
-----------
2. Navigate to the project folder
```
cd skin-type-checker
 Set up a virtual environment (optional but recommended)
 python3 -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
````
-------------
4. Install required dependencies


```pip install -r requirements.txt```



## RUNNING FLASK SERVER
1. Run the Flask server
```python app.py```


 2. Open a web browser and navigate to http://127.0.0.1:500

 Project Structure
```
 skin-type-checker/
│
├── app.py              # Main Flask backend
├── static/
│   ├── app.js          # JavaScript for frontend functionality
│   ├── styles.css      # CSS for styling
│
├── templates/
│   └── index.html
 └── frontend.html       # Main HTML for the frontend
│
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```
Backend (Flask):
app.py: Handles the backend logic, including serving the web pages and handling image uploads for processing via the machine learning model.
Frontend:
index.html: Contains the HTML structure and forms.
app.js: JavaScript logic for opening the camera, capturing images, and uploading them to the backend.
Dependencies:
Flask: Python web framework for serving the web app.
Flask-Cors: To handle cross-origin requests if the frontend and backend are hosted separately.

Dependencies
pip install -r requirements.txt
