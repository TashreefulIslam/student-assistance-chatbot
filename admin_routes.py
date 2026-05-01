"""
Admin Dashboard API Routes
Handles exam routines, class routines, teacher management, CT and assignment data
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models import db, User, ExamRoutine, ClassRoutine, CTDetails, Assignment
from utils import validate_email, validate_password, parse_datetime

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

# ==================== Exam Routine Management ====================
@admin_bp.route('/exam-routines', methods=['GET'])
@login_required
def get_exam_routines():
    """Get all exam routines with filters"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        # Query parameters for filtering
        semester = request.args.get('semester')
        section = request.args.get('section')
        exam_type = request.args.get('exam_type')
        
        query = ExamRoutine.query
        
        if semester:
            query = query.filter_by(semester=semester)
        if section:
            query = query.filter_by(section=section)
        if exam_type:
            query = query.filter_by(exam_type=exam_type)
        
        exams = query.order_by(ExamRoutine.date).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': e.id,
                'semester': e.semester,
                'exam_type': e.exam_type,
                'section': e.section,
                'course_code': e.course_code,
                'course_name': e.course_name,
                'date': e.date.isoformat(),
                'time': e.time.isoformat(),
                'room': e.room,
                'duration_minutes': e.duration_minutes
            } for e in exams]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/exam-routines', methods=['POST'])
@login_required
def create_exam_routine():
    """Create new exam routine"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required = ['semester', 'exam_type', 'section', 'course_code', 'course_name', 'date', 'time', 'room']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Parse date and time
        exam_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        exam_time = datetime.strptime(data['time'], '%H:%M').time()
        
        exam = ExamRoutine(
            semester=data['semester'],
            exam_type=data['exam_type'],
            section=data['section'].upper(),
            course_code=data['course_code'].upper(),
            course_name=data['course_name'],
            date=exam_date,
            time=exam_time,
            room=data['room'],
            duration_minutes=data.get('duration_minutes', 60),
            created_by=current_user.id
        )
        
        db.session.add(exam)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Exam routine created', 'id': exam.id}), 201
    
    except ValueError as e:
        return jsonify({'success': False, 'message': f'Invalid date/time format: {str(e)}'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/exam-routines/<int:exam_id>', methods=['PUT'])
@login_required
def update_exam_routine(exam_id):
    """Update exam routine"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        exam = ExamRoutine.query.get(exam_id)
        if not exam:
            return jsonify({'success': False, 'message': 'Exam not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'semester' in data:
            exam.semester = data['semester']
        if 'exam_type' in data:
            exam.exam_type = data['exam_type']
        if 'section' in data:
            exam.section = data['section'].upper()
        if 'course_code' in data:
            exam.course_code = data['course_code'].upper()
        if 'course_name' in data:
            exam.course_name = data['course_name']
        if 'date' in data:
            exam.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            exam.time = datetime.strptime(data['time'], '%H:%M').time()
        if 'room' in data:
            exam.room = data['room']
        if 'duration_minutes' in data:
            exam.duration_minutes = data['duration_minutes']
        
        exam.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Exam routine updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/exam-routines/<int:exam_id>', methods=['DELETE'])
@login_required
def delete_exam_routine(exam_id):
    """Delete exam routine"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        exam = ExamRoutine.query.get(exam_id)
        if not exam:
            return jsonify({'success': False, 'message': 'Exam not found'}), 404
        
        db.session.delete(exam)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Exam routine deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Class Routine Management ====================
@admin_bp.route('/class-routines', methods=['GET'])
@login_required
def get_class_routines():
    """Get all class routines with filters"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        semester = request.args.get('semester')
        section = request.args.get('section')
        day = request.args.get('day')
        
        query = ClassRoutine.query
        
        if semester:
            query = query.filter_by(semester=semester)
        if section:
            query = query.filter_by(section=section)
        if day:
            query = query.filter_by(day=day)
        
        classes = query.order_by(ClassRoutine.day, ClassRoutine.start_time).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': c.id,
                'semester': c.semester,
                'section': c.section,
                'course_code': c.course_code,
                'course_name': c.course_name,
                'day': c.day,
                'start_time': c.start_time.isoformat(),
                'end_time': c.end_time.isoformat(),
                'room': c.room,
                'teacher_name': c.teacher_name
            } for c in classes]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/class-routines', methods=['POST'])
@login_required
def create_class_routine():
    """Create new class routine"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        required = ['semester', 'section', 'course_code', 'course_name', 'day', 'start_time', 'end_time', 'room']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        
        cls = ClassRoutine(
            semester=data['semester'],
            section=data['section'].upper(),
            course_code=data['course_code'].upper(),
            course_name=data['course_name'],
            day=data['day'],
            start_time=start_time,
            end_time=end_time,
            room=data['room'],
            teacher_name=data.get('teacher_name'),
            created_by=current_user.id
        )
        
        db.session.add(cls)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Class routine created', 'id': cls.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/class-routines/<int:class_id>', methods=['PUT'])
@login_required
def update_class_routine(class_id):
    """Update class routine"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        cls = ClassRoutine.query.get(class_id)
        if not cls:
            return jsonify({'success': False, 'message': 'Class not found'}), 404
        
        data = request.get_json()
        
        if 'semester' in data:
            cls.semester = data['semester']
        if 'section' in data:
            cls.section = data['section'].upper()
        if 'course_code' in data:
            cls.course_code = data['course_code'].upper()
        if 'course_name' in data:
            cls.course_name = data['course_name']
        if 'day' in data:
            cls.day = data['day']
        if 'start_time' in data:
            cls.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        if 'end_time' in data:
            cls.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        if 'room' in data:
            cls.room = data['room']
        if 'teacher_name' in data:
            cls.teacher_name = data['teacher_name']
        
        cls.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Class routine updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/class-routines/<int:class_id>', methods=['DELETE'])
@login_required
def delete_class_routine(class_id):
    """Delete class routine"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        cls = ClassRoutine.query.get(class_id)
        if not cls:
            return jsonify({'success': False, 'message': 'Class not found'}), 404
        
        db.session.delete(cls)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Class routine deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Teacher Account Management ====================
@admin_bp.route('/teachers', methods=['GET'])
@login_required
def get_teachers():
    """Get all teacher accounts"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        teachers = User.query.filter_by(role='teacher').all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': t.id,
                'email': t.email,
                'full_name': t.full_name,
                'teacher_id': t.teacher_id,
                'department': t.department,
                'is_active': t.is_active,
                'created_at': t.created_at.isoformat()
            } for t in teachers]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/teachers', methods=['POST'])
@login_required
def create_teacher():
    """Create new teacher account"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        # Validate
        if not data.get('email') or not data.get('password') or not data.get('full_name'):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        if not validate_email(data['email']):
            return jsonify({'success': False, 'message': 'Invalid email format'}), 400
        
        is_valid, msg = validate_password(data['password'])
        if not is_valid:
            return jsonify({'success': False, 'message': msg}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'message': 'Email already exists'}), 400
        
        # Create teacher
        teacher = User(
            email=data['email'],
            full_name=data['full_name'],
            teacher_id=data.get('teacher_id'),
            department=data.get('department'),
            role='teacher',
            is_active=True
        )
        teacher.set_password(data['password'])
        
        db.session.add(teacher)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Teacher account created',
            'id': teacher.id
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/teachers/<int:teacher_id>', methods=['PUT'])
@login_required
def update_teacher(teacher_id):
    """Update teacher account"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        teacher = User.query.get(teacher_id)
        if not teacher or teacher.role != 'teacher':
            return jsonify({'success': False, 'message': 'Teacher not found'}), 404
        
        data = request.get_json()
        
        if 'full_name' in data:
            teacher.full_name = data['full_name']
        if 'teacher_id' in data:
            teacher.teacher_id = data['teacher_id']
        if 'department' in data:
            teacher.department = data['department']
        if 'is_active' in data:
            teacher.is_active = data['is_active']
        if 'password' in data:
            teacher.set_password(data['password'])
        
        teacher.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Teacher account updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/teachers/<int:teacher_id>', methods=['DELETE'])
@login_required
def delete_teacher(teacher_id):
    """Delete teacher account"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        teacher = User.query.get(teacher_id)
        if not teacher or teacher.role != 'teacher':
            return jsonify({'success': False, 'message': 'Teacher not found'}), 404
        
        # Soft delete: mark as inactive instead of deleting
        teacher.is_active = False
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Teacher account deactivated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== CT Management ====================
@admin_bp.route('/ct-details', methods=['GET'])
@login_required
def get_ct_details():
    """Get CT details with filters"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        course_code = request.args.get('course_code')
        section = request.args.get('section')
        is_completed = request.args.get('is_completed')
        
        query = CTDetails.query
        
        if course_code:
            query = query.filter_by(course_code=course_code)
        if section:
            query = query.filter_by(section=section)
        if is_completed is not None:
            query = query.filter_by(is_completed=is_completed.lower() == 'true')
        
        cts = query.order_by(CTDetails.date).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': c.id,
                'course_code': c.course_code,
                'course_name': c.course_name,
                'section': c.section,
                'ct_number': c.ct_number,
                'date': c.date.isoformat(),
                'time': c.time.isoformat(),
                'duration_minutes': c.duration_minutes,
                'room': c.room,
                'topics_syllabus': c.topics_syllabus,
                'total_marks': c.total_marks,
                'is_completed': c.is_completed
            } for c in cts]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@admin_bp.route('/ct-details', methods=['POST'])
@login_required
def create_ct_details():
    """Create CT details"""
    if not current_user.is_admin():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        required = ['course_code', 'course_name', 'section', 'ct_number', 'date', 'time']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        ct_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        ct_time = datetime.strptime(data['time'], '%H:%M').time()
        
        ct = CTDetails(
            course_code=data['course_code'].upper(),
            course_name=data['course_name'],
            section=data['section'].upper(),
            ct_number=data['ct_number'],
            date=ct_date,
            time=ct_time,
            duration_minutes=data.get('duration_minutes', 30),
            room=data.get('room'),
            topics_syllabus=data.get('topics_syllabus'),
            total_marks=data.get('total_marks', 20),
            created_by=current_user.id
        )
        
        db.session.add(ct)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'CT details created', 'id': ct.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
