"""
Teacher Dashboard API Routes
Handles CT and assignment management for teachers
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from datetime import datetime
from models import db, CTDetails, Assignment

def parse_datetime_flexible(date_str: str, time_str: str = None):
    """Parse datetime from either ISO format or separate date/time strings"""
    if time_str is None:
        # Handle ISO format: '2026-05-05T10:30' or standard format
        if 'T' in date_str:
            return datetime.fromisoformat(date_str)
        else:
            return datetime.strptime(date_str, '%Y-%m-%d %H:%M')
    else:
        return datetime.strptime(f"{date_str} {time_str}", '%Y-%m-%d %H:%M')

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

# ==================== CT Management ====================
@teacher_bp.route('/ct', methods=['GET'])
@login_required
def get_my_ct():
    """Get CT details created by current teacher"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        course_code = request.args.get('course_code')
        section = request.args.get('section')
        
        query = CTDetails.query.filter_by(created_by=current_user.id)
        
        if course_code:
            query = query.filter_by(course_code=course_code)
        if section:
            query = query.filter_by(section=section)
        
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

@teacher_bp.route('/ct', methods=['POST'])
@login_required
def create_ct():
    """Create CT details"""
    if not current_user.is_teacher():
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

@teacher_bp.route('/ct/<int:ct_id>', methods=['PUT'])
@login_required
def update_ct(ct_id):
    """Update CT details"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        ct = CTDetails.query.get(ct_id)
        if not ct or ct.created_by != current_user.id:
            return jsonify({'success': False, 'message': 'CT not found or unauthorized'}), 404
        
        data = request.get_json()
        
        if 'course_code' in data:
            ct.course_code = data['course_code'].upper()
        if 'course_name' in data:
            ct.course_name = data['course_name']
        if 'section' in data:
            ct.section = data['section'].upper()
        if 'ct_number' in data:
            ct.ct_number = data['ct_number']
        if 'date' in data:
            ct.date = datetime.strptime(data['date'], '%Y-%m-%d').date()
        if 'time' in data:
            ct.time = datetime.strptime(data['time'], '%H:%M').time()
        if 'duration_minutes' in data:
            ct.duration_minutes = data['duration_minutes']
        if 'room' in data:
            ct.room = data['room']
        if 'topics_syllabus' in data:
            ct.topics_syllabus = data['topics_syllabus']
        if 'total_marks' in data:
            ct.total_marks = data['total_marks']
        if 'is_completed' in data:
            ct.is_completed = data['is_completed']
        
        ct.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'CT details updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/ct/<int:ct_id>', methods=['DELETE'])
@login_required
def delete_ct(ct_id):
    """Delete CT details"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        ct = CTDetails.query.get(ct_id)
        if not ct or ct.created_by != current_user.id:
            return jsonify({'success': False, 'message': 'CT not found or unauthorized'}), 404
        
        db.session.delete(ct)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'CT details deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Assignment Management ====================
@teacher_bp.route('/assignment', methods=['GET'])
@login_required
def get_my_assignments():
    """Get assignments created by current teacher"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        course_code = request.args.get('course_code')
        section = request.args.get('section')
        is_submitted = request.args.get('is_submitted')
        
        query = Assignment.query.filter_by(created_by=current_user.id)
        
        if course_code:
            query = query.filter_by(course_code=course_code)
        if section:
            query = query.filter_by(section=section)
        if is_submitted is not None:
            query = query.filter_by(is_submitted=is_submitted.lower() == 'true')
        
        assignments = query.order_by(Assignment.submission_deadline).all()
        
        return jsonify({
            'success': True,
            'data': [{
                'id': a.id,
                'course_code': a.course_code,
                'course_name': a.course_name,
                'section': a.section,
                'assignment_title': a.assignment_title,
                'description': a.description,
                'submission_deadline': a.submission_deadline.isoformat(),
                'total_marks': a.total_marks,
                'is_submitted': a.is_submitted
            } for a in assignments]
        })
    
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/assignment', methods=['POST'])
@login_required
def create_assignment():
    """Create new assignment"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        required = ['course_code', 'course_name', 'section', 'assignment_title', 'submission_deadline']
        if not all(field in data for field in required):
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        try:
            deadline = parse_datetime_flexible(data['submission_deadline'])
        except Exception as e:
            return jsonify({'success': False, 'message': f'Invalid deadline format: {str(e)}'}), 400
        
        assignment = Assignment(
            course_code=data['course_code'].upper(),
            course_name=data['course_name'],
            section=data['section'].upper(),
            assignment_title=data['assignment_title'],
            description=data.get('description'),
            submission_deadline=deadline,
            total_marks=data.get('total_marks', 10),
            created_by=current_user.id
        )
        
        db.session.add(assignment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Assignment created', 'id': assignment.id}), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/assignment/<int:assignment_id>', methods=['PUT'])
@login_required
def update_assignment(assignment_id):
    """Update assignment"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment or assignment.created_by != current_user.id:
            return jsonify({'success': False, 'message': 'Assignment not found or unauthorized'}), 404
        
        data = request.get_json()
        
        if 'course_code' in data:
            assignment.course_code = data['course_code'].upper()
        if 'course_name' in data:
            assignment.course_name = data['course_name']
        if 'section' in data:
            assignment.section = data['section'].upper()
        if 'assignment_title' in data:
            assignment.assignment_title = data['assignment_title']
        if 'description' in data:
            assignment.description = data['description']
        if 'submission_deadline' in data:
            try:
                assignment.submission_deadline = parse_datetime_flexible(data['submission_deadline'])
            except Exception as e:
                return jsonify({'success': False, 'message': f'Invalid deadline format: {str(e)}'}), 400
        if 'total_marks' in data:
            assignment.total_marks = data['total_marks']
        if 'is_submitted' in data:
            assignment.is_submitted = data['is_submitted']
        
        assignment.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Assignment updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@teacher_bp.route('/assignment/<int:assignment_id>', methods=['DELETE'])
@login_required
def delete_assignment(assignment_id):
    """Delete assignment"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        assignment = Assignment.query.get(assignment_id)
        if not assignment or assignment.created_by != current_user.id:
            return jsonify({'success': False, 'message': 'Assignment not found or unauthorized'}), 404
        
        db.session.delete(assignment)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Assignment deleted'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

# ==================== Profile Management ====================
@teacher_bp.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get teacher profile"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    return jsonify({
        'success': True,
        'data': {
            'id': current_user.id,
            'email': current_user.email,
            'full_name': current_user.full_name,
            'teacher_id': current_user.teacher_id,
            'department': current_user.department,
            'created_at': current_user.created_at.isoformat()
        }
    })

@teacher_bp.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update teacher profile"""
    if not current_user.is_teacher():
        return jsonify({'success': False, 'message': 'Unauthorized'}), 403
    
    try:
        data = request.get_json()
        
        if 'full_name' in data:
            current_user.full_name = data['full_name']
        
        if 'email' in data and data['email'] != current_user.email:
            from utils import validate_email
            if not validate_email(data['email']):
                return jsonify({'success': False, 'message': 'Invalid email format'}), 400
            if User.query.filter_by(email=data['email']).first():
                return jsonify({'success': False, 'message': 'Email already in use'}), 400
            current_user.email = data['email']
        
        if 'password' in data:
            from utils import validate_password
            is_valid, msg = validate_password(data['password'])
            if not is_valid:
                return jsonify({'success': False, 'message': msg}), 400
            current_user.set_password(data['password'])
        
        if 'department' in data:
            current_user.department = data['department']
        
        current_user.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Profile updated'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500
