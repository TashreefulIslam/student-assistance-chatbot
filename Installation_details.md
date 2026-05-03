# 🚀 Complete Setup & Deployment Guide

## Step 1: Prerequisites Installation

### Windows
```bash
# Install Python 3.8+
# Download from https://www.python.org/downloads/

# Install MySQL Community Server
# Download from https://dev.mysql.com/downloads/mysql/

# Verify installations
python --version
mysql --version
```

### Linux/Mac
```bash
# macOS
brew install python3
brew install mysql

# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-venv python3-pip
sudo apt install mysql-server
```

## Step 2: Project Setup

### 2.1 Extract & Navigate
```bash
cd student_assistant_chatbot
```

### 2.2 Create Virtual Environment
```bash
python -m venv venv

# Activate
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate
```

### 2.3 Install Dependencies
```bash
pip install -r requirements.txt
```

## Step 3: Database Configuration

### 3.1 Create MySQL Database
```bash
mysql -u root -p

# In MySQL console:
CREATE DATABASE student_chatbot;
USE student_chatbot;
EXIT;
```

### 3.2 Configure Environment Variables
```bash
# Copy example file
cp .env.example .env

# Edit .env with your settings
```

### .env Template
```
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-12345
DATABASE_URL=mysql+pymysql://root:yourpassword@localhost/student_chatbot
GROQ_API_KEY=your_groq_api_key_here
```

**Where to get GROQ_API_KEY:**
1. Visit https://console.groq.com
2. Sign up (free account)
3. Create an API key
4. Copy and paste in .env

## Step 4: Initialize System

### 4.1 Initialize Database
```bash
python main.py init-db
```

You should see:
```
✓ Database initialized
✓ Default admin created:
  Email: admin@university.com
  Password: admin123
```

### 4.2 Start Application
```bash
python main.py
```

Server starts at: **http://localhost:5000**

## Step 5: First Time Setup (Admin)

### 5.1 Login
1. Click **Login** button
2. Email: `admin@university.com`
3. Password: `admin123`

### 5.2 Change Admin Password
1. Go to **Profile** section
2. Enter new password (min 6 chars, 1 uppercase, 1 digit)
3. Save

### 5.3 Create Teacher Accounts
1. Go to **Admin Dashboard**
2. Click **👨‍🏫 Teachers** tab
3. Click **+ Add Teacher**
4. Fill form:
   - Email (unique)
   - Password
   - Full Name
   - Teacher ID (optional)
   - Department

### 5.4 Add Sample Data

#### Add Exam Routine
1. Go to **Admin Dashboard**
2. Click **📚 Exam Routines**
3. Click **+ Add Exam**
4. Example:
   - Semester: Fall 2025
   - Exam Type: Mid
   - Section: 7C
   - Course Code: CSE4111
   - Course Name: Artificial Intelligence
   - Date: 2025-05-15
   - Time: 10:00
   - Room: Lab-203

#### Add Class Routine
1. **📅 Class Routines** tab
2. **+ Add Class**
3. Example:
   - Semester: Fall 2025
   - Section: 7C
   - Course Code: CSE4111
   - Day: Monday
   - Start: 09:00
   - End: 11:00
   - Room: Lab-201

#### Add CT Details
1. **✏️ CT Details** tab
2. **+ Add CT**
3. Example:
   - Course Code: CSE4111
   - Section: 7C
   - CT Number: 1
   - Date: 2025-04-20
   - Time: 14:00
   - Topics: Chapter 1-3: Introduction to AI

## Step 6: Teacher Workflow

### 6.1 Teacher Login
- Email: (created by admin)
- Password: (created by admin)

### 6.2 Create CT
1. Go to **Teacher Dashboard**
2. **✏️ Class Tests** tab
3. **+ Add CT**

### 6.3 Create Assignment
1. **📝 Assignments** tab
2. **+ Add Assignment**

## Step 7: Student Interaction

### 7.1 Query the Chatbot
Open http://localhost:5000 and try:

**Rule-Based Queries:**
- "7c final routine"
- "Monday class routine"
- "upcoming ct of cse4111"
- "assignment deadline"

**General Queries:**
- "What is artificial intelligence?"
- "How to prepare for exams?"

## Verification Checklist

- [ ] Python & MySQL installed
- [ ] Virtual environment created & activated
- [ ] Dependencies installed (`pip list` shows all packages)
- [ ] `.env` configured with API keys
- [ ] Database initialized (`python main.py init-db`)
- [ ] Application running (`python main.py`)
- [ ] Can access http://localhost:5000
- [ ] Admin login works (admin@university.com)
- [ ] Can create teacher account
- [ ] Can add exam routine
- [ ] Chatbot responds to queries
- [ ] Responses show correct data

## Troubleshooting

### "No module named 'app'"
```bash
# Ensure you're in the correct directory
cd student_assistant_chatbot
# Activate virtual environment
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### "MySQL connection refused"
```bash
# Check MySQL is running
# Windows: Services > MySQL80
# Mac: brew services start mysql
# Linux: sudo service mysql start
```

### "Database 'student_chatbot' doesn't exist"
```bash
mysql -u root -p
CREATE DATABASE student_chatbot;
EXIT;
```

### "GROQ_API_KEY not found"
1. Check `.env` file exists
2. Verify API key is there (not empty)
3. Restart application

### "500 Error on login"
1. Check database is initialized
2. Check `.env` DATABASE_URL is correct
3. Check MySQL credentials

## Production Deployment

### Gunicorn (WSGI Server)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
    }
}
```

### Environment for Production
```
FLASK_ENV=production
DEBUG=False
SQLALCHEMY_ECHO=False
SESSION_COOKIE_SECURE=True
```

## Performance Tips

1. **Database Optimization**
   - Indexes are pre-created
   - Use EXPLAIN for slow queries

2. **API Rate Limiting**
   - Groq has rate limits
   - Consider caching responses

3. **Server Configuration**
   - Use 4+ worker processes
   - Enable gzip compression

## Monitoring & Logs

### Application Logs
```bash
# Tail logs in development
FLASK_DEBUG=True python main.py
```

### Database Logs
Check MySQL error log for issues

### Chat History
Query `chat_history` table for analytics

## Backup & Maintenance

### Regular Backups
```bash
# Backup database
mysqldump -u root -p student_chatbot > backup.sql

# Restore from backup
mysql -u root -p student_chatbot < backup.sql
```

## Next Steps

1. Customize response formatting
2. Add more intents to classifier
3. Implement analytics dashboard
4. Set up automated tests
5. Configure CI/CD pipeline

## Support & Documentation

- **API Docs**: See `README_UPDATED.md`
- **Code Documentation**: Check inline comments
- **Groq API**: https://console.groq.com/docs
- **Flask**: https://flask.palletsprojects.com/
- **SQLAlchemy**: https://www.sqlalchemy.org/

---

**Good luck with your deployment! 🚀**
