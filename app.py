from flask import Flask, render_template, request, redirect, url_for ,session , jsonify
from flask_mysqldb import MySQL
import os
from sklearn.preprocessing import StandardScaler
import pickle
import pandas as pd
from flask_cors import CORS
from inference_sdk import InferenceHTTPClient  # Import the SDK client

app = Flask(__name__)
app.secret_key = "your_secret_key"

CORS(app)


# MySQL configuration
app.config['MYSQL_HOST'] = 'localhost'  # Replace with your MySQL host
app.config['MYSQL_USER'] = 'root'       # Replace with your MySQL username
app.config['MYSQL_PASSWORD'] = 'mighty@098'       # Replace with your MySQL password
app.config['MYSQL_DB'] = 'mental_health_db'

df = pd.read_csv('mental_health_data.csv')
print(df.head())


# Secret Key for Sessions
app.config['SECRET_KEY'] = os.urandom(24)


# Initialize MySQL
mysql = MySQL(app)


questions_list = [
    {"id": 1, "text": "Over the past two weeks, how often have you felt little interest or pleasure in doing things?", "scale": "0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day"},
    {"id": 2, "text": "How often have you felt down, depressed, or hopeless?", "scale": "0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day"},
    {"id": 3, "text": "Over the past two weeks, how often have you felt nervous, anxious, or on edge?", "scale": "0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day"},
    {"id": 4, "text": "How often do you feel overwhelmed by stress or responsibilities in your daily life?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 5, "text": "In the past week, how often have you experienced difficulty falling asleep or staying asleep?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 6, "text": "How often have you felt like a failure or that you have let yourself or others down?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 7, "text": "Have you had trouble concentrating on tasks such as reading, watching TV, or working?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 8, "text": "In the past two weeks, how often have you felt restless or unable to relax?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 9, "text": "Do you find it hard to enjoy time with friends or family, even when you’re with them?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 10, "text": "How often have you experienced physical symptoms like fatigue, headaches, or upset stomach due to stress?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 11, "text": "Have you ever felt like life is not worth living or had thoughts of self-harm?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 12, "text": "How often do you feel confident in your ability to cope with challenges in your life?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 13, "text": "In the past week, have you felt sudden and intense fear or panic without an obvious cause?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 14, "text": "How often have you felt lonely or isolated from others?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 15, "text": "Do you feel physically or emotionally exhausted most of the time?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 16, "text": "How often do you feel irritated or frustrated over small things?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 17, "text": "Have you avoided social situations due to fear of judgment or embarrassment?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 18, "text": "How often do you feel like your mind is racing or you can't slow your thoughts?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 19, "text": "Do you struggle to feel motivated, even for tasks you used to enjoy?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"},
    {"id": 20, "text": "Do you feel detached or disconnected from your surroundings or yourself?", "scale": "0 = Never, 1 = Rarely, 2 = Sometimes, 3 = Often, 4 = Always"}
]










# Initialize the inference client
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="qsYSUO7B0OsAF1if0AVE"
)

# Function to generate recommendations based on skin type
def generate_recommendations(skin_type):
    skin_type = skin_type.strip().lower()  # Normalize input to lowercase

    if "oily" in skin_type:
        return ["Oil-free moisturizer", "Gentle cleanser", "SPF 50 sunscreen"]
    elif "dry" in skin_type:
        return ["Hydrating serum", "Moisturizing cream", "Gentle cleanser"]
    elif "combination" in skin_type:
        return ["Balancing toner", "Lightweight moisturizer", "SPF 30 sunscreen"]
    elif "sensitive" in skin_type:
        return ["Soothing gel", "Fragrance-free moisturizer", "Mineral sunscreen"]
    else:
        return ["We couldn't confidently determine your skin type from the provided image. Please try using a clearer, well-lit photo or retake the picture. This helps our AI model provide more accurate recommendations"]

@app.route('/')
def home():
    return render_template('frontpage.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route("/Mental")
def Mental():
    session['responses'] = []  # Reset responses for new user
    return redirect(url_for('question', qid=1))

@app.route("/question/<int:qid>", methods=["GET", "POST"])
def question(qid):
    if qid > len(questions_list):  # If all questions answered, redirect to results
        return redirect(url_for('results'))
    
    question = questions_list[qid - 1]

    if request.method == "POST":
        response = int(request.form['response'])
        session['responses'].append(response)
        session.modified = True
        return redirect(url_for('question', qid=qid + 1))

    return render_template("question.html", question=question)

@app.route("/results")
def results():
    responses = session.get('responses', [])
    
    # Insert into the database
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO responses (answers) VALUES (%s)", (str(responses),))
    mysql.connection.commit()
    cursor.close()

    # Analyze or Predict based on responses (placeholder prediction logic)
    prediction = sum(responses)  # Example: sum of responses
    return render_template("result.html", prediction=prediction)

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s AND password = %s", (email, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['user_id'] = user[0]  # Store the user_id in session
            return redirect(url_for('home'))  # Redirect to assessment page after login
        else:
            return 'Invalid credentials, please try again.', 401
    return render_template('login.html')


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Insert new user into the database
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, password))
        mysql.connection.commit()
        cursor.close()
        
        return redirect(url_for('login'))  # Redirect to login after registration
    return render_template('register.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear the session
    return redirect(url_for('home'))  # Redirect to home or login page


@app.route('/contact')
def contact():
    return render_template('contact.html')

# @app.route('/Mental')
# def Mental():
#     return render_template('Mental _Health.html')


@app.route('/Doctor')
def Doctor():
    return render_template('AI_Doctor.html')

@app.route('/Wellness')
def Wellness():
     return render_template('Wellness.html')
 
@app.route('/aboutus')
def aboutus():
     return render_template('aboutus.html')

 

# Route to handle image upload and skin type detection
@app.route('/check_skin_type', methods=['POST'])
def check_skin_type():
    
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    
    # Save the uploaded file temporarily
    file_path = "temp_image.jpg"
    file.save(file_path)
    
    # Use InferenceHTTPClient to get the prediction from Roboflow's API
    try:
        result = CLIENT.infer(file_path, model_id="skin-type-detection/2")  # Specify your model ID
    except Exception as e:
        return jsonify({"error": f"Failed to process image: {str(e)}"}), 500
    
    # Extract skin type and confidence from the result
    predictions = result.get("predictions", [])
    if predictions:
        skin_type = predictions[0].get("class", "Unknown")
        confidence = predictions[0].get("confidence", 0) * 100  # Convert to percentage
    else:
        skin_type = "Unknown"
        confidence = 0

    recommendations = generate_recommendations(skin_type)
    
    # Return the response as JSON
    return jsonify({
        "skin_type": skin_type,
        "confidence": confidence,
        "recommendations": recommendations
    })

if __name__ == '__main__':
    app.run(debug=True)
