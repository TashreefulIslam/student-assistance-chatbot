from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for Admin, Teacher, and Students"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='student')  # admin, teacher, student
    teacher_id = db.Column(db.String(50), unique=True, nullable=True)
    department = db.Column(db.String(100), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    exam_routines = db.relationship('ExamRoutine', backref='created_by_user', lazy=True)
    class_routines = db.relationship('ClassRoutine', backref='created_by_user', lazy=True)
    ct_details = db.relationship('CTDetails', backref='created_by_user', lazy=True)
    assignments = db.relationship('Assignment', backref='created_by_user', lazy=True)
    
    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password"""
        return check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_teacher(self):
        return self.role == 'teacher'
    
    def is_student(self):
        return self.role == 'student'


class ExamRoutine(db.Model):
    """Exam routine/schedule table"""
    __tablename__ = 'exam_routines'
    
    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(50), nullable=False)  # Fall 2025, Spring 2025, etc.
    exam_type = db.Column(db.String(20), nullable=False)  # Mid, Final, Term Final
    section = db.Column(db.String(10), nullable=False)  # 7A, 7B, 7C, etc.
    course_code = db.Column(db.String(20), nullable=False)  # CSE4111
    course_name = db.Column(db.String(120), nullable=False)  # AI, DBMS, etc.
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(50), nullable=False)  # Room number
    duration_minutes = db.Column(db.Integer, default=60)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_exam_search', 'semester', 'section', 'exam_type'),
        db.Index('idx_course_exam', 'course_code', 'semester'),
    )


class ClassRoutine(db.Model):
    """Class routine/schedule table"""
    __tablename__ = 'class_routines'
    
    id = db.Column(db.Integer, primary_key=True)
    semester = db.Column(db.String(50), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    course_code = db.Column(db.String(20), nullable=False)
    course_name = db.Column(db.String(120), nullable=False)
    day = db.Column(db.String(20), nullable=False)  # Monday, Tuesday, etc.
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    room = db.Column(db.String(50), nullable=False)
    teacher_name = db.Column(db.String(120), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_class_search', 'semester', 'section'),
        db.Index('idx_class_day', 'day', 'section'),
    )


class CTDetails(db.Model):
    """Class Test (CT) details table"""
    __tablename__ = 'ct_details'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False)
    course_name = db.Column(db.String(120), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    ct_number = db.Column(db.Integer, nullable=False)  # 1st CT, 2nd CT, etc.
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, default=30)
    room = db.Column(db.String(50), nullable=True)
    topics_syllabus = db.Column(db.Text, nullable=True)  # Topics to cover
    total_marks = db.Column(db.Integer, default=20)
    is_completed = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_ct_search', 'course_code', 'section'),
        db.Index('idx_ct_upcoming', 'date', 'is_completed'),
    )


class Assignment(db.Model):
    """Assignment details table"""
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(20), nullable=False)
    course_name = db.Column(db.String(120), nullable=False)
    section = db.Column(db.String(10), nullable=False)
    assignment_title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    submission_deadline = db.Column(db.DateTime, nullable=False)
    total_marks = db.Column(db.Integer, default=10)
    is_submitted = db.Column(db.Boolean, default=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_assignment_search', 'course_code', 'section'),
        db.Index('idx_assignment_deadline', 'submission_deadline', 'is_submitted'),
    )


class ChatHistory(db.Model):
    """Chat history for analytics and user context"""
    __tablename__ = 'chat_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # Optional: for logged-in users
    message = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    query_type = db.Column(db.String(50), nullable=False)  # exam, class, ct, assignment, general
    response_source = db.Column(db.String(20), nullable=False)  # rule_based, api
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    __table_args__ = (
        db.Index('idx_chat_user', 'user_id', 'created_at'),
        db.Index('idx_chat_type', 'query_type', 'response_source'),
    )
