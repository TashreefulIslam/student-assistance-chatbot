from dotenv import load_dotenv
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_cors import CORS
from groq import Groq

load_dotenv()

# Import local modules
from config import config
from models import db, User, ChatHistory
from intent_classifier import QueryClassifier
from rule_based_engine import RuleBasedEngine
from utils import (
    format_rule_based_response, format_error_response, 
    sanitize_input, validate_email, validate_password
)
from admin_routes import admin_bp
from teacher_routes import teacher_bp

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(config[os.getenv('FLASK_ENV', 'development')])
app.secret_key = app.config.get('SECRET_KEY', 'dev-key-change-in-production')

# Enable CORS
CORS(app)

# Initialize database
db.init_app(app)

# Register blueprints
app.register_blueprint(admin_bp)
app.register_blueprint(teacher_bp)

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'Please log in to access this page.'

# Initialize Groq client (lazy - will be initialized on first use)
groq_client = None

def get_groq_client():
    global groq_client
    if groq_client is None:
        try:
            api_key = os.getenv("GROQ_API_KEY")
            if not api_key:
                print("ERROR: GROQ_API_KEY not found in environment variables")
                return None
            if not api_key.startswith('gsk_'):
                print(f"WARNING: GROQ_API_KEY format looks incorrect")
            groq_client = Groq(api_key=api_key)
        except Exception as e:
            print(f"ERROR: Groq initialization failed: {e}")
            groq_client = None
    return groq_client

# Initialize intent classifier
classifier = QueryClassifier()
rule_engine = RuleBasedEngine()

# ==================== Login Manager ====================
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ==================== Authentication Routes ====================
@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register new user (for future use)"""
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        full_name = data.get('full_name', '').strip()
        
        # Validate
        if not validate_email(email):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        is_valid, msg = validate_password(password)
        if not is_valid:
            return jsonify({'success': False, 'message': msg}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email already registered'}), 400
        
        # Create user
        user = User(email=email, full_name=full_name, role='student')
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        login_user(user)
        return jsonify({'success': True, 'message': 'Registration successful'}), 201
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email', '').strip()
        password = data.get('password', '')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user, remember=data.get('remember', False))
            return jsonify({
                'success': True,
                'message': 'Login successful',
                'redirect': url_for('admin_dashboard' if user.is_admin() else 'teacher_dashboard' if user.is_teacher() else 'home')
            }), 200
        
        return jsonify({'success': False, 'message': 'Invalid email or password'}), 401
    
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    """Logout route"""
    logout_user()
    return redirect(url_for('home'))

# ==================== Main Chat Routes ====================
@app.route('/')
def home():
    """Home page with chatbot"""
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    """
    Hybrid chatbot endpoint that routes to rule-based or API responses
    """
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({'reply': 'Please enter a message.', 'type': 'error'}), 400
        
        # Sanitize input
        user_message = sanitize_input(user_message)
        
        # Classify query intent
        classification = classifier.classify(user_message)
        intent = classification['intent']
        params = classification['parameters']
        confidence = classification['confidence']
        
        # Determine response source
        response_source = 'rule_based' if confidence > 0.15 else 'api'
        
        # Process based on intent
        if intent == 'exam' and confidence > 0.15:
            result = rule_engine.process_exam_query(params)
            response = format_rule_based_response('exam', result['data'], result['message'])
            response_type = 'table'
        
        elif intent == 'class' and confidence > 0.15:
            result = rule_engine.process_class_query(params)
            response = format_rule_based_response('class', result['data'], result['message'])
            response_type = 'table'
        
        elif intent == 'ct' and confidence > 0.15:
            result = rule_engine.process_ct_query(params)
            response = format_rule_based_response('ct', result['data'], result['message'])
            response_type = 'table'
        
        elif intent == 'assignment' and confidence > 0.15:
            result = rule_engine.process_assignment_query(params)
            response = format_rule_based_response('assignment', result['data'], result['message'])
            response_type = 'table'
        
        else:
            # Use API for general queries
            response = get_ai_response(user_message)
            response_source = 'api'
            response_type = 'text'
            intent = 'general'
        
        # Save to chat history
        if current_user.is_authenticated:
            chat_record = ChatHistory(
                user_id=current_user.id,
                message=user_message,
                response=response,
                query_type=intent,
                response_source=response_source
            )
            db.session.add(chat_record)
            db.session.commit()
        
        return jsonify({
            'reply': response,
            'type': response_type,
            'intent': intent,
            'source': response_source,
            'confidence': confidence
        })
    
    except Exception as e:
        return jsonify({
            'reply': f'Error: {str(e)}',
            'type': 'error'
        }), 500

def get_ai_response(message: str) -> str:
    """
    Get response from Groq API for general queries
    """
    try:
        client = get_groq_client()
        if client is None:
            return "Groq API is not available. Please check your GROQ_API_KEY in .env file."
        
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "system",
                    "content": """You are a helpful Student Assistant Chatbot. 
                    Help students with academic queries, study tips, subject explanations, 
                    and exam preparation. Keep responses concise and educational. 
                    Always be encouraging and supportive."""
                },
                {"role": "user", "content": message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return completion.choices[0].message.content
    
    except Exception as e:
        return f"Sorry, I couldn't process your request. Error: {str(e)}"

# ==================== Admin Routes ====================
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    """Admin dashboard"""
    if not current_user.is_admin():
        return redirect(url_for('home'))
    return render_template('admin/dashboard.html')

@app.route('/admin/exam-routine', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def admin_exam_routine():
    """Manage exam routines"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Implementation in next section
    return jsonify({'success': True})

@app.route('/admin/class-routine', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def admin_class_routine():
    """Manage class routines"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Implementation in next section
    return jsonify({'success': True})

@app.route('/admin/teachers', methods=['GET', 'POST'])
@login_required
def admin_teachers():
    """Create and manage teacher accounts"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Implementation in next section
    return jsonify({'success': True})

# ==================== Teacher Routes ====================
@app.route('/teacher/dashboard')
@login_required
def teacher_dashboard():
    """Teacher dashboard"""
    if not current_user.is_teacher():
        return redirect(url_for('home'))
    return render_template('teacher/dashboard.html')

@app.route('/teacher/ct', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def teacher_ct():
    """Teacher manage CT details"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Implementation in next section
    return jsonify({'success': True})

@app.route('/teacher/assignment', methods=['GET', 'POST', 'PUT', 'DELETE'])
@login_required
def teacher_assignment():
    """Teacher manage assignments"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    # Implementation in next section
    return jsonify({'success': True})

# ==================== Utility Routes ====================
@app.route('/api/user/profile')
@login_required
def get_profile():
    """Get current user profile"""
    return jsonify({
        'id': current_user.id,
        'email': current_user.email,
        'full_name': current_user.full_name,
        'role': current_user.role
    })

@app.route('/api/user/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update user profile"""
    data = request.get_json()
    
    if 'email' in data and data['email'] != current_user.email:
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email already in use'}), 400
        current_user.email = data['email']
    
    if 'full_name' in data:
        current_user.full_name = data['full_name']
    
    if 'password' in data:
        is_valid, msg = validate_password(data['password'])
        if not is_valid:
            return jsonify({'success': False, 'message': msg}), 400
        current_user.set_password(data['password'])
    
    db.session.commit()
    return jsonify({'success': True, 'message': 'Profile updated'})

@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.utcnow().isoformat()})

# ==================== Error Handlers ====================
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# ==================== Database Initialization ====================
@app.cli.command()
def init_db():
    """Initialize database and create default admin"""
    with app.app_context():
        db.create_all()
        
        # Create default admin if not exists
        admin = User.query.filter_by(email='admin@university.com').first()
        if not admin:
            admin = User(
                email='admin@university.com',
                full_name='System Administrator',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✓ Database initialized")
            print("✓ Default admin created: admin@university.com / admin123")
        else:
            print("✓ Database already initialized")

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    
    app.run(debug=True)
