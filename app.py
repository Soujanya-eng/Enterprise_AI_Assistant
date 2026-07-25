from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from google import genai
import datetime

app = Flask(__name__)
# Secure encryption session keys
app.config['SECRET_KEY'] = 'enterprise_ai_secure_session_key_987'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Google GenAI client (Paste your working Gemini Key right here)
ai_client = genai.Client(api_key="add your api here")

# User Profiles Table Structure
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    messages = db.relationship('ChatMessage', backref='user', lazy=True)

# Single Chat History Database Table
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_prompt = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)

# Application Page Routes
@app.route('/')
def home(): 
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fullname = request.form.get('fullname')
        email = request.form.get('email')
        password = request.form.get('password')
        if User.query.filter_by(email=email).first(): 
            return redirect(url_for('signup'))
        new_user = User(fullname=fullname, email=email, password_hash=generate_password_hash(password, method='scrypt'))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form.get('email')).first()
        if user and check_password_hash(user.password_hash, request.form.get('password')):
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Stable Dashboard: Pulls flat chat logs in chronological order
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: 
        return redirect(url_for('login'))
    user = db.get_or_404(User, session['user_id'])
    
    # Standard stable sorting method
    past_chats = ChatMessage.query.filter_by(user_id=user.id).order_by(ChatMessage.timestamp.asc()).all()
    return render_template('dashboard.html', user_name=user.fullname, past_chats=past_chats)

# Real-time Gemini Interaction API Engine
@app.route('/ask', methods=['POST'])
def ask_ai():
    if 'user_id' not in session:
        return jsonify({'error': 'Unauthorized'}), 401
    
    data = request.get_json()
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'error': 'Empty prompt'}), 400

    try:
        # Calls the updated, free tier model smoothly
        response = ai_client.models.generate_content(
            model='gemini-3.5-flash',
            contents=user_message,
        )
        ai_reply = response.text
    except Exception as e:
        ai_reply = f"System Error processing AI request: {str(e)}"

    # Save log parameters directly into the SQLite database record
    log_entry = ChatMessage(
        user_id=session['user_id'],
        user_prompt=user_message,
        ai_response=ai_reply
    )
    db.session.add(log_entry)
    db.session.commit()
    
    return jsonify({'reply': ai_reply})

with app.app_context(): 
    db.create_all()

if __name__ == '__main__': 
    app.run(debug=True)
