"""
Utility functions for response formatting, date handling, and validation
"""
from datetime import datetime
from typing import List, Dict, Any

def format_exam_response(exams: List[Dict]) -> str:
    """Format exam data into readable response"""
    if not exams:
        return "No exam records found."
    
    # Group by exam type and date
    grouped = {}
    for exam in exams:
        key = f"{exam['exam_type']} - {exam['date']}"
        if key not in grouped:
            grouped[key] = []
        grouped[key].append(exam)
    
    response = "📚 **EXAM ROUTINE**\n"
    response += "=" * 50 + "\n\n"
    
    for group_key, group_exams in sorted(grouped.items()):
        response += f"**{group_key}**\n"
        response += "-" * 50 + "\n"
        response += "| Course | Section | Time | Room |\n"
        response += "|--------|---------|------|------|\n"
        
        for exam in group_exams:
            response += f"| {exam['course_code']} | {exam['section']} | {exam['time']} | {exam['room']} |\n"
        
        response += "\n"
    
    return response


def format_class_response(classes: List[Dict]) -> str:
    """Format class routine into readable response"""
    if not classes:
        return "No class routine found."
    
    # Group by day
    grouped = {}
    for cls in classes:
        day = cls['day']
        if day not in grouped:
            grouped[day] = []
        grouped[day].append(cls)
    
    response = "📅 **CLASS ROUTINE**\n"
    response += "=" * 60 + "\n\n"
    
    days_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    for day in days_order:
        if day not in grouped:
            continue
        
        response += f"**{day}**\n"
        response += "-" * 60 + "\n"
        response += "| Time | Course | Room | Teacher |\n"
        response += "|------|--------|------|----------|\n"
        
        for cls in sorted(grouped[day], key=lambda x: x['start_time']):
            response += f"| {cls['start_time']}-{cls['end_time']} | {cls['course_code']} | {cls['room']} | {cls['teacher'] or 'N/A'} |\n"
        
        response += "\n"
    
    return response


def format_ct_response(cts: List[Dict]) -> str:
    """Format CT details into readable response"""
    if not cts:
        return "No upcoming CT found."
    
    response = "✏️ **UPCOMING CLASS TESTS (CT)**\n"
    response += "=" * 60 + "\n\n"
    
    for ct in cts:
        response += f"**{ct['course_code']} - CT {ct['ct_number']}**\n"
        response += f"📅 Date: {ct['date']}\n"
        response += f"⏰ Time: {ct['time']} (Duration: {ct['duration']} mins)\n"
        response += f"📍 Room: {ct['room']}\n"
        response += f"📝 Total Marks: {ct['total_marks']}\n"
        
        if ct['topics']:
            response += f"📚 Topics: {ct['topics']}\n"
        
        response += "\n"
    
    return response


def format_assignment_response(assignments: List[Dict]) -> str:
    """Format assignment details into readable response"""
    if not assignments:
        return "No assignments found."
    
    response = "📝 **ASSIGNMENTS**\n"
    response += "=" * 60 + "\n\n"
    
    for assign in assignments:
        response += f"**{assign['title']}**\n"
        response += f"Course: {assign['course_code']} ({assign['course_name']})\n"
        response += f"Section: {assign['section']}\n"
        response += f"📅 Deadline: {assign['deadline']}\n"
        response += f"⏳ Days Remaining: {assign['days_remaining']}\n"
        response += f"📊 Marks: {assign['total_marks']}\n"
        
        if assign['description']:
            response += f"📋 Details: {assign['description']}\n"
        
        response += "\n"
    
    return response


def format_error_response(message: str) -> str:
    """Format error message"""
    return f"❌ **Error**: {message}"


def format_rule_based_response(query_type: str, data: List[Dict], message: str) -> str:
    """Format rule-based response based on query type"""
    if query_type == 'exam':
        return format_exam_response(data)
    elif query_type == 'class':
        return format_class_response(data)
    elif query_type == 'ct':
        return format_ct_response(data)
    elif query_type == 'assignment':
        return format_assignment_response(data)
    else:
        return message


def parse_datetime(date_str: str, time_str: str) -> datetime:
    """Parse date and time strings to datetime"""
    try:
        datetime_str = f"{date_str} {time_str}"
        return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError(f"Invalid date/time format: {date_str} {time_str}")


def get_current_semester() -> str:
    """Get current semester"""
    month = datetime.now().month
    year = datetime.now().year
    
    if month >= 9:  # September onwards is Fall
        return f"Fall {year}"
    elif month >= 6:  # June onwards is Summer
        return f"Summer {year}"
    else:  # Before June is Spring
        return f"Spring {year}"


def validate_email(email: str) -> bool:
    """Validate email format"""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_password(password: str) -> tuple[bool, str]:
    """Validate password strength"""
    if len(password) < 6:
        return False, "Password must be at least 6 characters long"
    
    if not any(char.isupper() for char in password):
        return False, "Password must contain at least one uppercase letter"
    
    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one digit"
    
    return True, "Password is strong"


def get_days_until(deadline_datetime: datetime) -> int:
    """Calculate days until deadline"""
    now = datetime.utcnow()
    delta = deadline_datetime - now
    return max(0, delta.days)


def format_time_remaining(deadline_datetime: datetime) -> str:
    """Format time remaining until deadline"""
    now = datetime.utcnow()
    delta = deadline_datetime - now
    
    if delta.total_seconds() < 0:
        return "Deadline passed"
    
    days = delta.days
    hours = delta.seconds // 3600
    
    if days > 0:
        return f"{days}d {hours}h remaining"
    else:
        return f"{hours}h remaining"


def truncate_text(text: str, max_length: int = 500) -> str:
    """Truncate text to max length"""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def sanitize_input(user_input: str) -> str:
    """Sanitize user input to prevent injection"""
    # Remove extra whitespace
    sanitized = ' '.join(user_input.split())
    
    # Remove special characters that might cause issues
    # Keep alphanumeric, spaces, and common punctuation
    import re
    sanitized = re.sub(r'[<>\"\\\'%;()&+]', '', sanitized)
    
    return sanitized
