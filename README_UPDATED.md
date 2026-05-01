# 🎓 Student Assistant Chatbot - Hybrid AI System

A sophisticated hybrid AI system that intelligently combines rule-based query processing with API-based AI responses for comprehensive student support.

## ✨ Key Features

### Hybrid Intelligence
- **Rule-Based Engine**: Answers structured queries about exams, classes, CTs, and assignments from database
- **AI-Powered Responses**: Uses Groq API for general academic queries and explanations
- **Intelligent Routing**: Automatically determines the best response source

### User Roles & Access Control
- **Admin Dashboard**: Manage exam routines, class schedules, create teacher accounts, and oversee CT/assignment data
- **Teacher Dashboard**: Update course materials, create CTs, manage assignments
- **Student Chatbot**: Access information through natural language queries

### Smart Features
- **Intent Classification**: Understands informal student queries ("7c final routine", "ai ct kobe?", "cse4111 assignment deadline")
- **Formatted Responses**: Clean, professional table-based output
- **Real-time Data**: All queries fetch current data from database
- **Secure Authentication**: Password hashing, role-based session management

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- MySQL 5.7+
- Groq API Key (get from https://console.groq.com)

### Installation

1. **Clone/Extract the project**
   ```bash
   cd student_assistant_chatbot
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Windows
   # or
   source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python main.py init-db
   ```

6. **Start the application**
   ```bash
   python main.py
   ```

   Access at: **http://localhost:5000**

## 🔐 Default Credentials

After initialization:
- **Email**: admin@university.com
- **Password**: admin123

⚠️ **IMPORTANT**: Change the admin password immediately after first login!

## 📋 Database Setup

### MySQL Configuration

Create a MySQL database:
```sql
CREATE DATABASE student_chatbot;
USE student_chatbot;
```

Update `.env`:
```
DATABASE_URL=mysql+pymysql://root:password@localhost/student_chatbot
```

### Tables Created Automatically

- **users** - Admin, Teacher, and Student accounts
- **exam_routines** - Exam schedules
- **class_routines** - Class timetables
- **ct_details** - Class test information
- **assignments** - Assignment details
- **chat_history** - Query logs and analytics

## 👥 User Workflows

### Admin
1. Login with admin credentials
2. Access Admin Dashboard
3. Manage exam routines, class schedules
4. Create teacher accounts
5. Upload CT and assignment data

### Teacher
1. Login with credentials (created by admin)
2. Access Teacher Dashboard
3. Create/update CTs for their courses
4. Manage assignments and deadlines
5. Update profile information

### Student
1. Open chatbot interface
2. Ask about:
   - Exam schedules ("When is the final exam for CSE4111?")
   - Class routines ("What's today's class routine for 7C?")
   - CT info ("Upcoming CT of AI for 7C")
   - Assignments ("Deadline for CSE4111 assignment")
3. Get AI help for general academic queries

## 🎯 Query Examples

### Rule-Based Queries (Database)

#### Exam Routine
- "Term final exam schedule for Fall 2025 of 7C"
- "Mid exam routine of section 7A"
- "Final exam of CSE department Fall 2025"
- "When is the CSE4111 exam?"

#### Class Routine
- "Today class routine of 7C"
- "Weekly class schedule for 6A"
- "Monday classes for section 7C"
- "What's my class today?"

#### Class Tests
- "Upcoming CT of CSE4111"
- "CT of AI for 7C"
- "Next CT exam of section 7C"
- "First CT of database course"

#### Assignments
- "Assignment of AI course"
- "Upcoming assignment for 7C"
- "Deadline of CSE4111 assignment"
- "What assignments are due?"

### General Queries (AI API)

- "What is artificial intelligence?"
- "How to prepare for exams?"
- "Explain machine learning"
- "Study tips for programming"

## 🏗️ System Architecture

```
┌─────────────────┐
│  Student Chat   │
│   (Frontend)    │
└────────┬────────┘
         │
    ┌────▼─────────────────┐
    │  Intent Classifier   │
    │  (Query Analysis)    │
    └────┬──────────────┬──┘
         │              │
    ┌────▼────┐    ┌───▼──────┐
    │Rule-Based│   │ AI/Groq  │
    │  Engine  │   │   API    │
    └────┬────┘    └───┬──────┘
         │             │
    ┌────▼──────────┬──▼───┐
    │   MySQL DB   │Response│
    │              │ Former │
    └──────────────┴────────┘
```

## 📁 Project Structure

```
student_assistant_chatbot/
├── app.py                      # Main Flask application
├── main.py                     # Entry point & CLI
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── intent_classifier.py        # Query intent detection
├── rule_based_engine.py        # Database query processor
├── admin_routes.py             # Admin API endpoints
├── teacher_routes.py           # Teacher API endpoints
├── utils.py                    # Utility functions
├── requirements.txt            # Python dependencies
├── templates/
│   ├── index.html              # Student chatbot UI
│   ├── login.html              # Login page
│   ├── admin/
│   │   └── dashboard.html      # Admin dashboard
│   └── teacher/
│       └── dashboard.html      # Teacher dashboard
├── static/
│   ├── script.js               # Frontend logic
│   └── style.css               # Custom styles
└── data/
    └── knowledge.json          # Fallback knowledge base
```

## 🔧 API Endpoints

### Authentication
- `POST /login` - User login
- `POST /logout` - User logout
- `GET /api/user/profile` - Get user profile
- `PUT /api/user/profile` - Update profile

### Chat
- `POST /chat` - Send message to hybrid chatbot

### Admin Routes (`/api/admin/`)
- `GET /exam-routines` - List all exams
- `POST /exam-routines` - Create exam
- `PUT /exam-routines/<id>` - Update exam
- `DELETE /exam-routines/<id>` - Delete exam
- `GET /class-routines` - List all classes
- `POST /class-routines` - Create class
- `GET /teachers` - List all teachers
- `POST /teachers` - Create teacher account
- `GET /ct-details` - List CTs
- `POST /ct-details` - Create CT

### Teacher Routes (`/api/teacher/`)
- `GET /ct` - List my CTs
- `POST /ct` - Create CT
- `PUT /ct/<id>` - Update CT
- `DELETE /ct/<id>` - Delete CT
- `GET /assignment` - List my assignments
- `POST /assignment` - Create assignment
- `GET /profile` - Get profile
- `PUT /profile` - Update profile

## 🔐 Security Features

- ✅ Password hashing with werkzeug
- ✅ Session-based authentication
- ✅ Role-based access control
- ✅ SQL injection prevention (SQLAlchemy ORM)
- ✅ CSRF protection ready
- ✅ Input sanitization
- ✅ Secure password validation

## 📊 Query Classification

The system uses multi-factor classification:
1. **Keyword Matching** - Identifies intent keywords
2. **Pattern Recognition** - Extracts parameters (section, course, date)
3. **Confidence Scoring** - Determines if rule-based or API response
4. **Fallback Handling** - Routes to AI if confidence is low

## 🎨 Frontend Technology

- **Tailwind CSS** - Modern responsive design
- **Vanilla JavaScript** - No external dependencies
- **Markdown to HTML** - Professional response formatting

## 🚦 Environment Variables

Create `.env` file:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key
DATABASE_URL=mysql+pymysql://root:@localhost/student_chatbot
GROQ_API_KEY=your_groq_api_key
```

## 📝 Troubleshooting

### Database Connection Error
- Ensure MySQL is running
- Check DATABASE_URL format
- Verify credentials in .env

### Groq API Error
- Verify GROQ_API_KEY is valid
- Check API rate limits
- Ensure internet connection

### Login Issues
- Run `python main.py init-db` again
- Check user role in database
- Verify password requirements

## 🔄 Workflow Diagram

```
User Query
    ↓
Intent Classification
    ↓
    ├─→ [Confidence > 0.15]
    │       ↓
    │   Database Query
    │       ↓
    │   Format Response
    │       ↓
    │   Rule-Based Result
    │
    └─→ [Confidence < 0.15]
            ↓
        Groq API Call
            ↓
        AI Response
```

## 📈 Performance Optimization

- Database indexes on frequently searched columns
- Query caching for repeated patterns
- Lazy loading of relationships
- Connection pooling for database

## 🤝 Contributing

To extend the system:

1. **Add new intent**: Modify `intent_classifier.py`
2. **Add database fields**: Update `models.py`
3. **Add API endpoints**: Create routes in `admin_routes.py` or `teacher_routes.py`
4. **Update UI**: Modify HTML templates in `templates/`

## 📄 License

Educational Project - CSE 4111 Artificial Intelligence

## 👨‍💼 Support

For issues or questions:
1. Check the troubleshooting section
2. Review API documentation
3. Check database logs
4. Verify environment configuration

---

**Built with ❤️ for Academic Excellence**

Version: 2.0 (Hybrid AI System)
Last Updated: 2025
