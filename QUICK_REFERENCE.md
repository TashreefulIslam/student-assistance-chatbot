# ⚡ Quick Reference Guide

## 🚀 Quick Start (30 seconds)

```bash
# 1. Create virtual environment
python -m venv venv && source venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure .env
cp .env.example .env
# Edit .env with your GROQ_API_KEY and DATABASE_URL

# 4. Initialize database
python main.py init-db

# 5. Run
python main.py
```

Visit: **http://localhost:5000**

---

## 🔐 Default Credentials

| Role | Email | Password | Action |
|------|-------|----------|--------|
| Admin | admin@university.com | admin123 | Login → Change ASAP |
| Teacher | (created by admin) | (set by admin) | Ask admin for credentials |
| Student | (public) | N/A | Direct to chatbot |

---

## 🎯 Key URLs

| Page | URL | Access |
|------|-----|--------|
| Chatbot | http://localhost:5000 | Public |
| Login | http://localhost:5000/login | Public |
| Admin Dashboard | http://localhost:5000/admin/dashboard | Admin only |
| Teacher Dashboard | http://localhost:5000/teacher/dashboard | Teacher only |

---

## 📊 Sample Queries to Try

### Rule-Based (Database)
```
"7c final routine"
"Monday class schedule"
"upcoming ct for cse4111"
"assignment deadline for ai"
```

### General (AI via Groq)
```
"What is artificial intelligence?"
"How to study for exams?"
"Explain machine learning"
```

---

## 🗄️ Database Tables

```sql
-- User Management
SELECT * FROM users WHERE role = 'admin';

-- View all exams
SELECT * FROM exam_routines ORDER BY date;

-- View class routine
SELECT * FROM class_routines ORDER BY day;

-- View CTs
SELECT * FROM ct_details ORDER BY date;

-- View assignments
SELECT * FROM assignments ORDER BY submission_deadline;

-- Chat analytics
SELECT query_type, response_source, COUNT(*) 
FROM chat_history GROUP BY query_type;
```

---

## 🛠️ Admin Tasks

### Create Teacher Account
1. Login as admin
2. Go to **Admin Dashboard** → **👨‍🏫 Teachers**
3. Click **+ Add Teacher**
4. Fill form and submit
5. Share credentials with teacher

### Add Exam Schedule
1. **📚 Exam Routines** tab
2. **+ Add Exam**
3. Fill: Semester, Type, Section, Course, Date, Time, Room
4. Submit

### Add Class Routine
1. **📅 Class Routines** tab
2. **+ Add Class**
3. Fill: Semester, Day, Section, Course, Time, Room
4. Submit

### Add CT Details
1. **✏️ CT Details** tab
2. **+ Add CT**
3. Fill: Course, Section, Date, Time, Topics
4. Submit

---

## 👨‍🏫 Teacher Tasks

### Create CT
1. Login to **Teacher Dashboard**
2. **✏️ Class Tests** tab
3. **+ Add CT**
4. Fill: Course, Section, Date, Time, Topics, Marks
5. Submit

### Create Assignment
1. **📝 Assignments** tab
2. **+ Add Assignment**
3. Fill: Course, Title, Deadline, Marks, Description
4. Submit

### Update Profile
1. **👤 Profile** tab
2. Edit: Name, Email, Password, Department
3. Save Changes

---

## 🧠 Intent Classification Logic

### How Queries Are Classified

```
Query: "7c final routine"
    ↓
Keyword Matching: 'final' (exam keyword)
    ↓
Parameter Extraction: section='7C', exam_type='Final'
    ↓
Confidence Scoring: 0.8 (HIGH)
    ↓
Route: Database (Rule-Based)
    ↓
Response: "Final Exam Routine for Section 7C"
```

```
Query: "What is AI?"
    ↓
Keyword Matching: No rule-based keywords
    ↓
Confidence Scoring: 0.05 (LOW)
    ↓
Route: Groq API (General)
    ↓
Response: AI definition from Groq
```

---

## 🔧 Common Commands

### Database
```bash
# Initialize
python main.py init-db

# Backup
mysqldump -u root -p student_chatbot > backup.sql

# Restore
mysql -u root -p student_chatbot < backup.sql

# View database
mysql -u root -p -e "USE student_chatbot; SHOW TABLES;"
```

### Python
```bash
# Check Python version
python --version

# Activate venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Deactivate
deactivate

# Check packages
pip list
```

### Flask
```bash
# Run development
python main.py

# Debug mode
FLASK_DEBUG=True python main.py

# Init database
python main.py init-db
```

---

## ❌ Troubleshooting Quick Fixes

| Problem | Solution |
|---------|----------|
| "No module 'app'" | Activate venv: `source venv/bin/activate` |
| "MySQL connection error" | Check MySQL running: `mysql -u root -p` |
| "Database doesn't exist" | Run: `python main.py init-db` |
| "API key not found" | Check `.env` file exists and has GROQ_API_KEY |
| "Login fails" | Ensure database initialized: `python main.py init-db` |
| "Can't access localhost:5000" | Check port 5000 is free, try different: `python app.py --port 5001` |

---

## 📈 Performance Tuning

```python
# Enable query logging
SQLALCHEMY_ECHO = True

# Check slow queries in MySQL
SHOW PROCESSLIST;
SHOW SLOW LOG;

# Database indexes are auto-created on:
- exam_routines: (semester, section, exam_type)
- class_routines: (semester, section)
- ct_details: (course_code, section)
- assignments: (course_code, section)
```

---

## 🔐 Security Checklist

- [ ] Change admin password after first login
- [ ] Update SECRET_KEY in production
- [ ] Enable HTTPS (SSL) in production
- [ ] Use strong passwords for all accounts
- [ ] Backup database regularly
- [ ] Monitor error logs
- [ ] Restrict API keys (Groq)
- [ ] Use environment variables for secrets

---

## 📱 API Examples

### Login
```javascript
fetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        email: 'admin@university.com',
        password: 'admin123'
    })
})
```

### Send Chat
```javascript
fetch('/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        message: '7c final routine'
    })
})
```

### Get Profile
```javascript
fetch('/api/user/profile')
    .then(r => r.json())
    .then(data => console.log(data))
```

---

## 🎓 Code Structure

```
app.py              ← Main Flask app, routes
config.py           ← Configuration settings
models.py           ← Database models (SQLAlchemy)
intent_classifier.py ← Query classification logic
rule_based_engine.py ← Database query processor
admin_routes.py     ← Admin API endpoints
teacher_routes.py   ← Teacher API endpoints
utils.py            ← Helper functions
```

---

## 🚨 Error Codes

| Code | Meaning | Solution |
|------|---------|----------|
| 200 | OK | Request successful |
| 201 | Created | New resource created |
| 400 | Bad Request | Check input format |
| 401 | Unauthorized | Login required |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Check logs, restart |

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| README_UPDATED.md | Complete feature documentation |
| SETUP_GUIDE.md | Step-by-step installation |
| ARCHITECTURE.md | System design & components |
| QUICK_REFERENCE.md | This file (quick lookup) |

---

## 🌐 Environment Variables

```
FLASK_ENV           → development | production
FLASK_APP           → app.py (entry point)
SECRET_KEY          → Random string for sessions
DATABASE_URL        → MySQL connection string
GROQ_API_KEY        → API key from console.groq.com
DEBUG               → True | False
TESTING             → True | False
```

---

## 📞 Support Resources

- **Groq API**: https://console.groq.com
- **Flask Docs**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/
- **MySQL**: https://dev.mysql.com/doc/
- **Tailwind CSS**: https://tailwindcss.com/docs

---

## ✨ Pro Tips

1. **Use browser dev tools** (F12) to inspect API responses
2. **Enable SQL logging** to understand queries: `SQLALCHEMY_ECHO = True`
3. **Test intents** by enabling debug mode
4. **Monitor chat history** for user patterns
5. **Regular backups** prevent data loss
6. **Use consistent data** (sections, course codes) for better classification

---

**Last Updated:** 2025
**Version:** 2.0 (Hybrid AI System)
