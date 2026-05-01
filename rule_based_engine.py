"""
Rule-Based Query Engine
Fetches structured data from database based on classified intent
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from models import db, ExamRoutine, ClassRoutine, CTDetails, Assignment

class RuleBasedEngine:
    """Process rule-based queries and fetch from database"""
    
    @staticmethod
    def process_exam_query(params: Dict) -> Optional[Dict]:
        """
        Process exam routine query
        
        Returns:
            {
                'success': bool,
                'data': list of exam records,
                'message': str
            }
        """
        try:
            query = ExamRoutine.query
            
            # Apply filters
            if 'section' in params:
                query = query.filter_by(section=params['section'])
            
            if 'course_code' in params:
                query = query.filter_by(course_code=params['course_code'])
            
            if 'semester' in params:
                query = query.filter_by(semester=params['semester'])
            
            if 'exam_type' in params:
                query = query.filter_by(exam_type=params['exam_type'])
            
            results = query.all()
            
            if not results:
                return {
                    'success': False,
                    'data': [],
                    'message': 'No exam routine found matching your criteria.'
                }
            
            # Format results
            formatted_data = []
            for exam in results:
                formatted_data.append({
                    'course_code': exam.course_code,
                    'course_name': exam.course_name,
                    'section': exam.section,
                    'exam_type': exam.exam_type,
                    'date': exam.date.strftime('%Y-%m-%d'),
                    'time': exam.time.strftime('%H:%M'),
                    'room': exam.room,
                    'duration': exam.duration_minutes
                })
            
            return {
                'success': True,
                'data': formatted_data,
                'message': f'Found {len(formatted_data)} exam record(s).'
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error querying exam data: {str(e)}'
            }
    
    @staticmethod
    def process_class_query(params: Dict) -> Optional[Dict]:
        """
        Process class routine query
        
        Returns structured class schedule data
        """
        try:
            query = ClassRoutine.query
            
            # Apply filters
            if 'section' in params:
                query = query.filter_by(section=params['section'])
            
            if 'course_code' in params:
                query = query.filter_by(course_code=params['course_code'])
            
            if 'day' in params:
                query = query.filter_by(day=params['day'])
            
            if 'semester' in params:
                query = query.filter_by(semester=params['semester'])
            
            # Handle "today" and "tomorrow" references
            if params.get('day_reference') == 'today':
                today = datetime.now().strftime('%A')
                query = query.filter_by(day=today)
            elif params.get('day_reference') == 'tomorrow':
                tomorrow = (datetime.now() + timedelta(days=1)).strftime('%A')
                query = query.filter_by(day=tomorrow)
            
            results = query.order_by(ClassRoutine.start_time).all()
            
            if not results:
                return {
                    'success': False,
                    'data': [],
                    'message': 'No class routine found matching your criteria.'
                }
            
            # Format results
            formatted_data = []
            for cls in results:
                formatted_data.append({
                    'course_code': cls.course_code,
                    'course_name': cls.course_name,
                    'section': cls.section,
                    'day': cls.day,
                    'start_time': cls.start_time.strftime('%H:%M'),
                    'end_time': cls.end_time.strftime('%H:%M'),
                    'room': cls.room,
                    'teacher': cls.teacher_name
                })
            
            return {
                'success': True,
                'data': formatted_data,
                'message': f'Found {len(formatted_data)} class(es).'
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error querying class data: {str(e)}'
            }
    
    @staticmethod
    def process_ct_query(params: Dict) -> Optional[Dict]:
        """
        Process CT (Class Test) query
        
        Returns upcoming CT details
        """
        try:
            query = CTDetails.query
            
            # Only show upcoming/not completed CTs by default
            query = query.filter_by(is_completed=False)
            
            # Apply filters
            if 'section' in params:
                query = query.filter_by(section=params['section'])
            
            if 'course_code' in params:
                query = query.filter_by(course_code=params['course_code'])
            
            if 'ct_number' in params:
                query = query.filter_by(ct_number=params['ct_number'])
            
            # Order by date
            results = query.order_by(CTDetails.date).all()
            
            if not results:
                return {
                    'success': False,
                    'data': [],
                    'message': 'No upcoming CT found matching your criteria.'
                }
            
            # Format results
            formatted_data = []
            for ct in results:
                formatted_data.append({
                    'course_code': ct.course_code,
                    'course_name': ct.course_name,
                    'section': ct.section,
                    'ct_number': ct.ct_number,
                    'date': ct.date.strftime('%Y-%m-%d'),
                    'time': ct.time.strftime('%H:%M'),
                    'duration': ct.duration_minutes,
                    'room': ct.room,
                    'topics': ct.topics_syllabus,
                    'total_marks': ct.total_marks
                })
            
            return {
                'success': True,
                'data': formatted_data,
                'message': f'Found {len(formatted_data)} CT(s).'
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error querying CT data: {str(e)}'
            }
    
    @staticmethod
    def process_assignment_query(params: Dict) -> Optional[Dict]:
        """
        Process assignment query
        
        Returns assignment details and deadlines
        """
        try:
            query = Assignment.query
            
            # By default show pending assignments
            query = query.filter_by(is_submitted=False)
            
            # Apply filters
            if 'section' in params:
                query = query.filter_by(section=params['section'])
            
            if 'course_code' in params:
                query = query.filter_by(course_code=params['course_code'])
            
            if 'course_name' in params:
                query = query.filter(
                    Assignment.course_name.ilike(f"%{params['course_name']}%")
                )
            
            # Order by deadline
            results = query.order_by(Assignment.submission_deadline).all()
            
            if not results:
                return {
                    'success': False,
                    'data': [],
                    'message': 'No assignment found matching your criteria.'
                }
            
            # Format results
            formatted_data = []
            for assign in results:
                deadline = assign.submission_deadline
                is_upcoming = deadline > datetime.utcnow()
                
                formatted_data.append({
                    'course_code': assign.course_code,
                    'course_name': assign.course_name,
                    'section': assign.section,
                    'title': assign.assignment_title,
                    'description': assign.description,
                    'deadline': deadline.strftime('%Y-%m-%d %H:%M'),
                    'total_marks': assign.total_marks,
                    'is_upcoming': is_upcoming,
                    'days_remaining': (deadline - datetime.utcnow()).days
                })
            
            return {
                'success': True,
                'data': formatted_data,
                'message': f'Found {len(formatted_data)} assignment(s).'
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': [],
                'message': f'Error querying assignment data: {str(e)}'
            }
    
    @staticmethod
    def get_student_dashboard_data(section: str, semester: Optional[str] = None) -> Dict:
        """
        Get all relevant data for a student dashboard
        
        Returns exams, classes, CTs, and assignments for a section
        """
        try:
            semester = semester or f"Fall {datetime.now().year}"
            
            data = {
                'exams': ExamRoutine.query.filter_by(section=section, semester=semester).all(),
                'classes': ClassRoutine.query.filter_by(section=section, semester=semester).all(),
                'cts': CTDetails.query.filter_by(section=section, is_completed=False)
                        .order_by(CTDetails.date).all(),
                'assignments': Assignment.query.filter_by(section=section, is_submitted=False)
                             .order_by(Assignment.submission_deadline).all()
            }
            
            return {
                'success': True,
                'data': data
            }
        
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'message': f'Error fetching dashboard data: {str(e)}'
            }
