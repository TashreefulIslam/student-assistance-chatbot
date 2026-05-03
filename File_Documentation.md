# 📁 Complete File Documentation

## 🐍 PYTHON BACKEND FILES

### 1. **app.py** (280+ lines)
**Location:** Root directory  
**What's Inside:**
- Flask application initialization
- CORS configuration
- User authentication setup (Flask-Login)
- Main `/chat` endpoint for hybrid query routing
- Groq API client initialization with lazy loading
- Blueprint registration for admin and teacher routes

**What It Does:**
- Serves as the main Flask application entry point
- Routes student chat queries to either database or Groq API based on confidence score
- Handles user authentication and session management
- Manages API responses with metadata (source, intent type)

---

### 2. **main.py** (50+ lines)
**Location:** Root directory  
**What's Inside:**
- Application entry point
- Development/production server configuration
- Debug mode settings
- Port configuration

**What It Does:**
- Runs the Flask development server
- Sets up debugging and environment settings
- Launches the chatbot application

---

### 3. **config.py** (58 lines)
**Location:** Root directory  
**What's Inside:**
- Base configuration class
- Environment-specific configs (Development, Production, Testing)
- Database connection strings with environment variables
- API keys and secrets configuration
- SQLAlchemy settings

**What It Does:**
- Manages all application configuration based on environment
- Loads environment variables from .env file
- Provides MySQL connection URL for SQLAlchemy
- Centralizes secret management

---

### 4. **models.py** (220+ lines)
**Location:** Root directory  
**What's Inside:**
- 6 SQLAlchemy ORM models:
  1. **User** - Student/Teacher/Admin accounts with password hashing
  2. **ExamRoutine** - Exam schedule data (semester, section, exam_type)
  3. **ClassRoutine** - Class schedule data (day, time, section)
  4. **CTDetails** - Continuous Test information (course, section, date)
  5. **Assignment** - Assignment data (deadline, submission status)
  6. **ChatHistory** - Conversation logs for analytics
- Database indexes for optimized queries
- Relationships between models

**What It Does:**
- Defines database schema and structure
- Manages all data types and constraints
- Indexes search columns for fast retrieval
- Establishes relationships between tables

---

### 5. **intent_classifier.py** (360+ lines)
**Location:** Root directory  
**What's Inside:**
- NLP engine for query understanding
- 5 intent categories: exam, class, ct, assignment, general
- Multi-factor scoring algorithm for confidence calculation
- Keyword sets for each intent type
- Regex patterns for parameter extraction:
  - Section extraction (handles "of 3c" pattern)
  - Course code extraction
  - Semester extraction
- Helper functions for query preprocessing

**What It Does:**
- Analyzes student queries to determine intent
- Extracts parameters (section, course, semester) from queries
- Calculates confidence score (0-1)
- Routes queries intelligently:
  - High confidence → Database query
  - Low confidence → General LLM query

---

### 6. **rule_based_engine.py** (290+ lines)
**Location:** Root directory  
**What's Inside:**
- Expert system with 4 main query processors:
  1. `process_exam_query()` - Filters exam routines
  2. `process_class_query()` - Handles day-based class queries
  3. `process_ct_query()` - Retrieves CT details
  4. `process_assignment_query()` - Shows assignment deadlines
- Database query logic with SQLAlchemy
- Response formatting helper functions
- Time-based filtering (today, tomorrow, etc.)

**What It Does:**
- Executes structured database queries based on classified intent
- Filters results by semester, section, course, date
- Calculates dynamic information (days remaining to deadline)
- Returns formatted, readable responses

---

### 7. **admin_routes.py** (320+ lines)
**Location:** Root directory  
**What's Inside:**
- 14 REST API endpoints for admin operations
- CRUD operations for:
  - Exam routines (create, read, update, delete)
  - Class routines (create, read, update, delete)
  - Teacher accounts (create, read, soft-delete)
  - CT details (create, read, update)
- Role-based access control (@login_required, role checks)
- Input validation and error handling

**What It Does:**
- Provides API endpoints for admin dashboard
- Manages all system data (exams, classes, teachers, CTs)
- Enforces authentication and authorization
- Returns JSON responses for frontend consumption

---

### 8. **teacher_routes.py** (280+ lines)
**Location:** Root directory  
**What's Inside:**
- 8 REST API endpoints for teacher operations
- CRUD operations for:
  - CT details (create, read, update, delete)
  - Assignments (create, read, update, delete)
- `parse_datetime_flexible()` function - Handles both ISO and standard datetime formats
- Ownership verification (created_by == current_user.id)
- Profile management endpoints

**What It Does:**
- Provides API endpoints for teacher dashboard
- Enables teachers to create and manage CTs and assignments
- Validates datetime input from HTML forms
- Enforces data ownership (users can only edit their own data)

---

### 9. **utils.py** (210+ lines)
**Location:** Root directory  
**What's Inside:**
- Response formatting functions:
  - `format_exam_response()` - Markdown table for exams
  - `format_class_response()` - Grouped class schedule
  - `format_ct_response()` - CT list with dates
  - `format_assignment_response()` - Assignments with countdown
- Validation functions:
  - `validate_email()` - Email regex validation
  - `validate_password()` - Password strength check
- Helper functions:
  - `sanitize_input()` - Remove special characters
  - `parse_datetime()` - Standard datetime conversion

**What It Does:**
- Formats database responses for readable display
- Validates user inputs (emails, passwords)
- Sanitizes queries to prevent injection
- Provides reusable utility functions across the application

---

## 📄 CONFIGURATION & DATA FILES

### 10. **requirements.txt**
**Location:** Root directory  
**What's Inside:**
- Complete list of Python dependencies:
  - Flask 3.0.0 (web framework)
  - Flask-Login (authentication)
  - Flask-CORS (cross-origin requests)
  - SQLAlchemy 2.0.23 (ORM)
  - pymysql 1.1.0 (MySQL driver)
  - Groq 0.11.0 (LLM API)
  - httpx 0.24.1 (HTTP client)
  - python-dotenv (environment variables)
  - werkzeug (password hashing)

**What It Does:**
- Specifies all required Python packages and versions
- Used for `pip install -r requirements.txt`
- Ensures environment consistency across machines

---

### 11. **.env** (Not in repo - user creates)
**Location:** Root directory  
**What's Inside:**
- Environment variables:
  - DATABASE_URL - MySQL connection string
  - GROQ_API_KEY - API key from Groq console
  - FLASK_ENV - Development/Production mode
  - SECRET_KEY - Flask session secret

**What It Does:**
- Stores sensitive credentials securely
- Provides environment-specific configuration
- Prevents hardcoding secrets in source code

---

### 12. **data/knowledge.json**
**Location:** data/ directory  
**What's Inside:**
- Structured domain knowledge data
- Course information
- Predefined responses
- System knowledge base

**What It Does:**
- Stores static knowledge for reference
- Used as backup for intent classification
- Provides context for expert system

---

## 🌐 FRONTEND FILES

### 13. **templates/index.html** (main chat interface)
**Location:** templates/  
**What's Inside:**
- Chat interface HTML structure
- Message display area (chat bubbles)
- Input form for student queries
- User menu (login/logout)
- Real-time message updates
- Bootstrap/Tailwind styling integration

**What It Does:**
- Main student chatbot page
- Displays chat history
- Collects and sends student queries
- Shows responses from backend

---

### 14. **templates/login.html**
**Location:** templates/  
**What's Inside:**
- Login form HTML
- Email and password input fields
- Role selection (student/teacher/admin)
- Submit button
- Tailwind CSS styling
- Error message display

**What It Does:**
- Provides authentication interface
- Routes users to role-specific dashboards
- Handles login form submission

---

### 15. **templates/admin/dashboard.html**
**Location:** templates/admin/  
**What's Inside:**
- 4-tab admin interface:
  1. Exam Routines - Create/Edit/Delete exams
  2. Class Routines - Create/Edit/Delete classes
  3. Teachers - Create/Manage teacher accounts
  4. CTs - View and manage CT details
- Data tables with CRUD buttons
- Form modals for create/edit
- Tailwind CSS styling

**What It Does:**
- Provides admin management interface
- Allows system-wide data management
- Creates teacher accounts
- Manages all academic schedules

---

### 16. **templates/teacher/dashboard.html**
**Location:** templates/teacher/  
**What's Inside:**
- 3-tab teacher interface:
  1. CTs - Create/Edit/Delete CT details
  2. Assignments - Create/Edit/Delete assignments
  3. Profile - Teacher profile and account settings
- Data tables with management buttons
- Form modals for create/edit
- Tailwind CSS styling

**What It Does:**
- Provides teacher management interface
- Enables CT and assignment creation
- Allows profile management
- Shows teacher-specific information

---

### 17. **static/script.js** (1000+ lines)
**Location:** static/  
**What's Inside:**
- Frontend JavaScript functions:
  - Chat message handling
  - API request/response management
  - User authentication
  - Admin dashboard CRUD operations
  - Teacher dashboard CRUD operations
  - Form validation
  - Real-time UI updates
  - Modal dialogs
- Event listeners for buttons and forms
- Fetch calls to Flask backend
- DOM manipulation and updates

**What It Does:**
- Handles all frontend interactivity
- Sends/receives data from backend APIs
- Updates UI based on server responses
- Manages user interactions and navigation

---

### 18. **static/style.css** (800+ lines)
**Location:** static/  
**What's Inside:**
- Custom CSS styling:
  - Chat interface styling (bubbles, messages)
  - Dashboard layouts (tables, forms)
  - Modal dialogs and popups
  - Responsive design (mobile-friendly)
  - Color scheme and typography
  - Button styles and hover effects
  - Form input styling
- Tailwind CSS integration
- Custom utility classes

**What It Does:**
- Styles all HTML elements
- Provides responsive design
- Creates professional appearance
- Enhances user experience

---

## 📚 DOCUMENTATION FILES

### 19. **README.md**
**Location:** Root directory  
**What's Inside:**
- Project overview and description
- Installation instructions
- Setup steps (environment, database, dependencies)
- Usage guide
- API endpoints documentation
- Features list
- Future improvements
- Troubleshooting tips

**What It Does:**
- Provides project documentation
- Guides new users through setup
- Explains how to use the system
- Documents all features and APIs

---

### 20. **docs/domain_definition.md**
**Location:** docs/  
**What's Inside:**
- Domain definition and terminology
- Academic terminology (CT, exam, assignment)
- Business logic rules
- Data model descriptions
- System constraints and limitations

**What It Does:**
- Defines domain knowledge
- Explains academic concepts
- Provides context for developers
- Documents business rules

---

### 21. **PRESENTATION_GUIDE.md** (3000+ lines)
**Location:** Root directory  
**What's Inside:**
- Comprehensive presentation preparation guide
- 10 sections covering:
  - AI technologies used
  - Core AI system components
  - How hybrid routing works
  - Intent classification algorithm
  - Expert system design
  - Confidence-based routing
  - Slide-by-slide guidance
  - Key points for AI course
  - Example queries and responses
  - Demo script preparation

**What It Does:**
- Guides presentation creation for AI course
- Provides talking points for each slide
- Explains technical concepts simply
- Prepares for live demonstrations

---

### 22. **PRESENTATION_VISUALS.md** (created)
**Location:** Root directory  
**What's Inside:**
- ASCII diagrams and visual representations:
  - System architecture diagram
  - Intent classification flow
  - Expert system design
  - Query flow comparison
  - File responsibility map
- Real example queries with outputs
- 10 slide template summaries
- Presentation tips and timing

**What It Does:**
- Provides visual aids for presentation slides
- Shows architectural diagrams
- Gives concrete examples of system in action
- Suggests slide content structure

---

### 23. **FIXES_APPLIED.md**
**Location:** Root directory  
**What's Inside:**
- Documentation of all bugs fixed
- Issues encountered during development
- Solutions implemented
- Testing procedures
- Deployment checklist

**What It Does:**
- Records debugging history
- Documents lessons learned
- Provides reference for future maintenance
- Shows debugging and testing approach

---

## 📊 SUMMARY TABLE

| Category | File Count | Purpose |
|----------|-----------|---------|
| **AI/NLP** | 3 | Intent classification, rule-based processing, hybrid routing |
| **Backend API** | 3 | Admin routes, teacher routes, utilities |
| **Database** | 2 | Models, configuration |
| **Frontend HTML** | 4 | Chat, login, admin dashboard, teacher dashboard |
| **Frontend JS/CSS** | 2 | Interactivity and styling |
| **Configuration** | 3 | App config, requirements, environment variables |
| **Data/Knowledge** | 2 | Knowledge base, domain definitions |
| **Documentation** | 5 | README, guides, visuals, fixes documentation |
| **Entry Point** | 1 | main.py |
| **TOTAL** | **25** | Complete AI student assistant system |

---

## 🎯 KEY FILE RELATIONSHIPS

```
ENTRY POINT:
main.py
    ↓
app.py (Flask app + /chat endpoint)
    ├─ intent_classifier.py (NLP analysis)
    ├─ rule_based_engine.py (Database queries)
    ├─ admin_routes.py (Admin API)
    ├─ teacher_routes.py (Teacher API)
    ├─ models.py (Database schema)
    ├─ config.py (Configuration)
    └─ utils.py (Helper functions)

FRONTEND:
    ├─ templates/ (HTML pages)
    ├─ static/script.js (API calls & UI logic)
    └─ static/style.css (Styling)

DATA:
    ├─ models.py (Schema)
    ├─ data/knowledge.json (Knowledge base)
    └─ .env (Credentials)
```

---

**Total System: 25 files working together to provide an intelligent student assistant chatbot! 🚀**
