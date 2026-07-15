from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlite3 # මෙතන sqlite3 වෙන්නම ඕනේ

app = Flask(__name__)
app.config['SECRET_KEY'] = 'my-secret-travel-key-123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///destinations.db'
app.secret_key = 'shehani2004'

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    budget = db.Column(db.String(20))
    weather = db.Column(db.String(20))
    travel_method = db.Column(db.String(20))
    duration = db.Column(db.Integer)
    image_name = db.Column(db.String(100))
    description = db.Column(db.String(500))  # අලුතින් එකතු කළා
    location = db.Column(db.String(100))     # අලුතින් එකතු කළා
    rating = db.Column(db.Float, default=0.0) # rating එක සඳහා

    # Booking සඳහා අලුත් Table එක
class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_name = db.Column(db.String(100), nullable=False)
    user_name = db.Column(db.String(100), nullable=False)
    travel_date = db.Column(db.String(20), nullable=False)
    people = db.Column(db.Integer, nullable=False)

def init_db():
    conn = sqlite3.connect('destinations.db') 
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS feedbacks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def init_db():
    
    conn = sqlite3.connect('destination.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS subscribers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE
        )
    ''')
    conn.commit()
    conn.close()

    init_db()

# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/explore')
def explore():
    # Database එකෙන් දත්ත ගන්නා ආකාරය
    destinations = Place.query.all()
    return render_template('explore.html', destinations=destinations)

@app.route('/subscribe', methods=['POST'])
def subscribe():
    email = request.form.get('email')
    try:
        conn = sqlite3.connect('destination.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO subscribers (email) VALUES (?)", (email,))
        conn.commit()
        conn.close()
        return jsonify({"status": "success"})
    except sqlite3.IntegrityError:
        return jsonify({"status": "error", "message": "Already subscribed!"})

@app.route('/planner', methods=['GET', 'POST'])
def planner():
    destinations = None
    stats = None
    
    if request.method == 'POST':
        user_budget = request.form.get('budget', '').strip()
        user_weather = request.form.get('weather', '').strip()
        user_transport = request.form.get('transport', '').strip()
        try:
            user_days = int(request.form.get('days', 3))
        except:
            user_days = 3

        # Filtering
        results = Place.query.filter(
            Place.budget == user_budget,
            Place.weather == user_weather,
            Place.travel_method == user_transport,
            Place.duration <= user_days
        ).order_by(Place.duration.desc()).all() 
        
        # දත්ත Dictionary වලට හැරවීම
        destinations = []
        for p in results:
            destinations.append({
                'Destination': p.name,
                'Duration': p.duration,
                'Budget': p.budget,
                'Weather': p.weather,
                'Travel_Method': p.travel_method
            })
            
        if results:
            total_days = sum(p.duration for p in results)
            stats = {
                'total_found': len(results),
                'avg_days': round(total_days / len(results), 1),
                'top_pick': results[0].name
            }
            
    return render_template('planner.html', destinations=destinations, stats=stats)

@app.route('/trending')
def trending():
    trending_destinations = [
        {"name": "Sigiriya", "image_name": "sigiriya.jpg", "description": "Ancient rock fortress and palace ruins.", "location": "Matale", "rating": "4.8"},
        {"name": "Ella", "image_name": "ella.jpg", "description": "Beautiful hill country village with scenic views.", "location": "Badulla", "rating": "4.9"},
        {"name": "Kandy", "image_name": "kandy.jpg", "description": "Cultural capital and home to the Temple of the Tooth.", "location": "Kandy", "rating": "4.6"},
        {"name": "Nuwara Eliya", "image_name": "nuwara_eliya.jpg", "description": "Little England with tea plantations and cool climate.", "location": "Nuwara Eliya", "rating": "4.8"},
        {"name": "Galle Fort", "image_name": "galle_fort.jpg", "description": "Historical fort with colonial architecture and sea views.", "location": "Galle", "rating": "4.7"},
        {"name": "Yala National Park", "image_name": "yala.jpg", "description": "Famous wildlife sanctuary for leopards and elephants.", "location": "Hambantota", "rating": "4.5"},
        {"name": "Bentota", "image_name": "bentota.jpg", "description": "Popular beach destination for water sports.", "location": "Galle", "rating": "4.4"},
        {"name": "Mirissa", "image_name": "mirissa.jpg", "description": "Stunning beach and whale watching spot.", "location": "Matara", "rating": "4.7"},
        {"name": "Trincomalee", "image_name": "trincomalee.jpg", "description": "Pristine beaches and historical temples by the sea.", "location": "Trincomalee", "rating": "4.6"}
    ]
    
    return render_template('trending.html', destinations=trending_destinations)

@app.route('/booking')
def booking():
    place_name = request.args.get('place') # modal එකෙන් එන නම අල්ලගන්නවා
    return render_template('booking.html', place=place_name)

@app.route('/rate_place/<place_name>')
def rate_page(place_name):
    return render_template('rate.html', place_name=place_name)


@app.route('/save_rating', methods=['POST'])
def save_rating():
    data = request.get_json() # JavaScript එකෙන් එන දත්ත අල්ලගන්නවා
    place = data.get('place')
    rating = data.get('rating')
    
    print(f"Received rating: {rating} for {place}") # මේක terminal එකේ පේනවා
    
   
    return jsonify({"status": "success"})

from flask import jsonify 

@app.route('/confirm_booking', methods=['POST'])
def confirm_booking():
    data = request.get_json() 
    
   
    new_booking = Booking(
        place_name=data.get('place_name'),
        user_name=data.get('user_name'),
        travel_date=data.get('travel_date'),
        people=data.get('people')
    )
    
   
    db.session.add(new_booking)
    db.session.commit()
    
    return jsonify({"message": f"Success! Your booking for {data.get('place_name')} is confirmed."})

@app.route('/submit-feedback', methods=['POST'])
def submit_feedback():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')
    
   
    conn = sqlite3.connect('ceylon_vibe.db') 
    cursor = conn.cursor()
    cursor.execute("INSERT INTO feedbacks (name, email, message) VALUES (?, ?, ?)", (name, email, message))
    conn.commit()
    conn.close()
    
    return jsonify({"status": "success", "message": "Thank you for your feedback!"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    
    user_password = request.form.get('password')
    
    if user_password == "shenu2004": 
        session['logged_in'] = True  
        return jsonify(status='success')
    else:
        return jsonify(status='error')

@app.route('/admin/feedbacks')
def view_feedbacks():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    
    
    conn = sqlite3.connect('ceylon_vibe.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, email, message FROM feedbacks")
    feedbacks = cursor.fetchall()
    conn.close()
    
    return render_template('admin_feedback.html', feedbacks=feedbacks)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('explore')) 

@app.route('/best-time')
def best_time():
    return render_template('best_time.html')

@app.route('/food-guide')
def food_guide():
    return render_template('food_guide.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all() # Database එක මුලින්ම හදනවා
    app.run(debug=True)