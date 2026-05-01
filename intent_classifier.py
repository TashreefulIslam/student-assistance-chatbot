"""
Intent Classification Engine
Detects user query intent and extracts relevant parameters
"""
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime

class QueryClassifier:
    """Classify student queries into exam, class, ct, assignment, or general"""
    
    # Keywords for different intents
    EXAM_KEYWORDS = {
        'exam', 'routine', 'schedule', 'timetable', 'final', 'mid', 'test',
        'when', 'what time', 'which room', 'exam date', 'exam time',
        'term final', 'midterm', 'examination', 'slot', 'timing'
    }
    
    CLASS_KEYWORDS = {
        'class', 'routine', 'schedule', 'timetable', 'when', 'what time',
        'which room', 'lecture', 'session', 'period', 'slot', 'timing',
        'tomorrow', 'today', 'monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday', 'daily', 'weekly'
    }
    
    CT_KEYWORDS = {
        'ct', 'class test', 'quiz', 'test', 'exam', 'upcoming', 'next',
        'when', 'date', 'time', 'first ct', 'second ct', 'first exam',
        'second exam', 'assessment', 'evaluation'
    }
    
    ASSIGNMENT_KEYWORDS = {
        'assignment', 'homework', 'task', 'project', 'deadline', 'submission',
        'due', 'when due', 'when submit', 'description', 'requirements',
        'marks', 'assessment'
    }
    
    SECTION_PATTERN = r'(\d+[A-Za-z]|\d+)'  # 7A, 7B, 7C, 6A, etc.
    COURSE_CODE_PATTERN = r'(CSE\d+|BBA\d+|[A-Z]+\d+)'  # CSE4111, BBA5000
    SEMESTER_PATTERN = r'(fall|spring|summer)\s*(\d{4})?'
    
    def __init__(self):
        """Initialize the classifier"""
        self.exam_keywords = self.EXAM_KEYWORDS
        self.class_keywords = self.CLASS_KEYWORDS
        self.ct_keywords = self.CT_KEYWORDS
        self.assignment_keywords = self.ASSIGNMENT_KEYWORDS
    
    def classify(self, query: str) -> Dict:
        """
        Classify a query and extract parameters
        
        Returns:
            {
                'intent': 'exam' | 'class' | 'ct' | 'assignment' | 'general',
                'confidence': float (0-1),
                'parameters': {
                    'section': str,
                    'course_code': str,
                    'course_name': str,
                    'semester': str,
                    'exam_type': str,  # for exam queries
                    'day': str,  # for class queries
                    'ct_number': int,  # for ct queries
                    # ... other params
                },
                'original_query': str
            }
        """
        query_lower = query.lower()
        
        # Extract parameters
        params = self._extract_parameters(query, query_lower)
        
        # Determine intent
        intent, confidence = self._determine_intent(query_lower, params)
        
        return {
            'intent': intent,
            'confidence': confidence,
            'parameters': params,
            'original_query': query
        }
    
    def _extract_parameters(self, query: str, query_lower: str) -> Dict:
        """Extract relevant parameters from query"""
        params = {}
        
        # Extract section (e.g., 7C, 6A)
        # First try to find section after 'of' (e.g., 'ct of 3c')
        of_match = re.search(r'of\s+([\d]+[A-Za-z])', query_lower)
        if of_match:
            params['section'] = of_match.group(1).upper()
        else:
            section_match = re.search(self.SECTION_PATTERN, query_lower)
            if section_match:
                params['section'] = section_match.group(1).upper()
        
        # Extract course code (e.g., CSE4111)
        course_match = re.search(self.COURSE_CODE_PATTERN, query_lower, re.IGNORECASE)
        if course_match:
            params['course_code'] = course_match.group(1).upper()
        
        # Extract course name keywords
        course_names = self._extract_course_name(query_lower)
        if course_names:
            params['course_name'] = course_names[0]
        
        # Extract semester
        semester_match = re.search(self.SEMESTER_PATTERN, query_lower)
        if semester_match:
            season = semester_match.group(1).capitalize()
            year = semester_match.group(2) if semester_match.group(2) else str(datetime.now().year)
            params['semester'] = f"{season} {year}"
        
        # Extract exam type
        if 'final' in query_lower or 'term final' in query_lower:
            params['exam_type'] = 'Final'
        elif 'mid' in query_lower or 'midterm' in query_lower:
            params['exam_type'] = 'Mid'
        elif 'term' in query_lower:
            params['exam_type'] = 'Term Final'
        
        # Extract day of week
        days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
        for day in days:
            if day in query_lower:
                params['day'] = day.capitalize()
                break
        
        # Check for "today", "tomorrow"
        if 'today' in query_lower:
            params['day_reference'] = 'today'
        elif 'tomorrow' in query_lower:
            params['day_reference'] = 'tomorrow'
        
        # Extract CT number
        ct_match = re.search(r'(\d+)(?:st|nd|rd|th)?\s*ct', query_lower)
        if ct_match:
            params['ct_number'] = int(ct_match.group(1))
        elif 'next ct' in query_lower or 'upcoming ct' in query_lower:
            params['ct_order'] = 'next'
        elif 'first ct' in query_lower:
            params['ct_number'] = 1
        elif 'second ct' in query_lower:
            params['ct_number'] = 2
        
        return params
    
    def _extract_course_name(self, query_lower: str) -> List[str]:
        """Extract course names from query"""
        known_courses = {
            'ai': 'Artificial Intelligence',
            'dbms': 'Database Management System',
            'dsa': 'Data Structures and Algorithms',
            'oop': 'Object-Oriented Programming',
            'web': 'Web Development',
            'ml': 'Machine Learning',
            'dl': 'Deep Learning',
            'nlp': 'Natural Language Processing',
            'compiler': 'Compiler Design',
            'os': 'Operating Systems',
            'network': 'Computer Networks',
            'security': 'Cybersecurity',
            'cloud': 'Cloud Computing'
        }
        
        matches = []
        for keyword, full_name in known_courses.items():
            if keyword in query_lower:
                matches.append(full_name)
        
        return matches
    
    def _determine_intent(self, query_lower: str, params: Dict) -> Tuple[str, float]:
        """Determine query intent and confidence"""
        
        # Count keyword matches
        exam_score = self._score_keywords(query_lower, self.exam_keywords)
        class_score = self._score_keywords(query_lower, self.class_keywords)
        ct_score = self._score_keywords(query_lower, self.ct_keywords)
        assignment_score = self._score_keywords(query_lower, self.assignment_keywords)
        
        # Boost scores based on extracted parameters
        if 'exam_type' in params:
            exam_score += 0.3
        if 'day' in params or 'day_reference' in params:
            class_score += 0.3
        if 'ct_number' in params or 'ct_order' in params:
            ct_score += 0.3
        if 'submission_deadline' in query_lower or 'due date' in query_lower:
            assignment_score += 0.3
        
        # Determine final intent
        scores = {
            'exam': exam_score,
            'class': class_score,
            'ct': ct_score,
            'assignment': assignment_score
        }
        
        intent = max(scores, key=scores.get)
        confidence = scores[intent]
        
        # Normalize confidence to 0-1 range
        max_possible = len(self.exam_keywords) + 0.3  # Approximate
        confidence = min(confidence / max_possible, 1.0)
        
        # If confidence is too low, classify as general
        if confidence < 0.15:
            intent = 'general'
            confidence = 0.0
        
        return intent, confidence
    
    def _score_keywords(self, query: str, keywords: set) -> float:
        """Score query based on keyword matches"""
        score = 0
        words = query.split()
        
        for word in words:
            # Remove punctuation
            cleaned_word = word.strip('.,!?;:')
            if cleaned_word in keywords:
                score += 1
        
        # Also check for keyword sequences
        for keyword in keywords:
            if keyword in query:
                score += 0.5
        
        return score
    
    def extract_filters(self, params: Dict) -> Dict:
        """Convert parameters to database query filters"""
        filters = {}
        
        if 'section' in params:
            filters['section'] = params['section']
        
        if 'course_code' in params:
            filters['course_code'] = params['course_code']
        
        if 'course_name' in params:
            filters['course_name'] = params['course_name']
        
        if 'semester' in params:
            filters['semester'] = params['semester']
        
        if 'exam_type' in params:
            filters['exam_type'] = params['exam_type']
        
        if 'day' in params:
            filters['day'] = params['day']
        
        return filters
