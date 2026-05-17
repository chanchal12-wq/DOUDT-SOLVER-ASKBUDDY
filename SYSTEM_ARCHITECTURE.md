# AskBuddy - System Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      AskBuddy Platform                       │
│              Smart Student Doubt Exchange System             │
└─────────────────────────────────────────────────────────────┘
```

## Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                        CLIENT LAYER                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  Browser   │  │   Mobile   │  │   Tablet   │            │
│  │  (Chrome,  │  │  (Safari,  │  │   (iPad,   │            │
│  │  Firefox)  │  │  Chrome)   │  │  Android)  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└──────────────────────────────────────────────────────────────┘
                            │
                            │ HTTP/HTTPS
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    PRESENTATION LAYER                         │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              HTML Templates (Jinja2)                   │  │
│  │  • Base Template (Navigation, Footer)                  │  │
│  │  • Student Pages (Dashboard, Ask, Questions)           │  │
│  │  • Teacher Pages (Dashboard, Upload, Materials)        │  │
│  │  • Admin Pages (Dashboard, User Management)            │  │
│  │  • Shared Pages (Login, Register, Profile)             │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Static Assets                              │  │
│  │  • CSS (Bootstrap 5 + Custom Styles)                   │  │
│  │  • JavaScript (Chart.js + Custom Scripts)              │  │
│  │  • Icons (Font Awesome)                                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                          │
│  ┌────────────────────────────────────────────────────────┐  │
│  │                  Flask Application                      │  │
│  │                                                         │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │           Route Handlers                         │  │  │
│  │  │  • Authentication Routes                         │  │  │
│  │  │  • Student Routes                                │  │  │
│  │  │  • Teacher Routes                                │  │  │
│  │  │  • Admin Routes                                  │  │  │
│  │  │  • API Routes                                    │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │           Business Logic                         │  │  │
│  │  │  • User Authentication                           │  │  │
│  │  │  • Question Management                           │  │  │
│  │  │  • Answer Management                             │  │  │
│  │  │  • Voting System                                 │  │  │
│  │  │  • Reputation Calculator                         │  │  │
│  │  │  • File Upload Handler                           │  │  │
│  │  │  • Search & Filter Logic                         │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  │  ┌──────────────────────────────────────────────────┐  │  │
│  │  │           Middleware & Security                  │  │  │
│  │  │  • Session Management                            │  │  │
│  │  │  • Role-Based Access Control                     │  │  │
│  │  │  • Password Hashing (Werkzeug)                   │  │  │
│  │  │  • CSRF Protection                               │  │  │
│  │  │  • File Validation                               │  │  │
│  │  └──────────────────────────────────────────────────┘  │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                       DATA LAYER                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              Database Models                            │  │
│  │  • User Model                                          │  │
│  │  • Question Model                                      │  │
│  │  • Answer Model                                        │  │
│  │  • Vote Model                                          │  │
│  │  • Study Material Model                                │  │
│  └────────────────────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              SQLite Database                            │  │
│  │  • users table                                         │  │
│  │  • questions table                                     │  │
│  │  • answers table                                       │  │
│  │  • votes table                                         │  │
│  │  • study_materials table                               │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌──────────────────────────────────────────────────────────────┐
│                      STORAGE LAYER                            │
│  ┌────────────────────────────────────────────────────────┐  │
│  │              File System                                │  │
│  │  • Question Images (static/uploads/questions/)         │  │
│  │  • Study Materials (static/uploads/materials/)         │  │
│  │  • Database File (database/askbuddy.db)                │  │
│  └────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
```

## User Flow Diagrams

### Student User Flow

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────────┐      ┌──────────┐
│ Register/   │─────▶│  Login   │
│   Login     │      └────┬─────┘
└─────────────┘           │
                          ▼
                  ┌───────────────┐
                  │    Student    │
                  │   Dashboard   │
                  └───────┬───────┘
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Ask Question │  │   Browse     │  │   Answer     │
│              │  │  Questions   │  │  Questions   │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘
       │                 │                 │
       │                 ▼                 │
       │         ┌──────────────┐          │
       │         │ View Question│          │
       │         │   Details    │          │
       │         └──────┬───────┘          │
       │                │                 │
       └────────────────┼─────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
        ▼               ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Vote on      │ │ Mark Best    │ │ View Profile │
│ Answers      │ │ Answer       │ │ & Leaderboard│
└──────────────┘ └──────────────┘ └──────────────┘
```

### Teacher User Flow

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────────┐
│   Login     │
└─────┬───────┘
      │
      ▼
┌───────────────┐
│    Teacher    │
│   Dashboard   │
└───────┬───────┘
        │
    ┌───┼───┐
    │   │   │
    ▼   ▼   ▼
┌────┐ ┌────┐ ┌────┐
│View│ │Ans-│ │Mod-│
│Ques│ │wer │ │erate│
└─┬──┘ └─┬──┘ └─┬──┘
  │      │      │
  └──────┼──────┘
         │
    ┌────┼────┐
    │    │    │
    ▼    ▼    ▼
┌────┐ ┌────┐ ┌────┐
│Mark│ │Upl-│ │View│
│Best│ │oad │ │Ana-│
│Ans │ │Mat │ │lyt-│
└────┘ └────┘ │ics │
              └────┘
```

### Admin User Flow

```
┌─────────┐
│  Start  │
└────┬────┘
     │
     ▼
┌─────────────┐
│   Login     │
└─────┬───────┘
      │
      ▼
┌───────────────┐
│     Admin     │
│   Dashboard   │
└───────┬───────┘
        │
    ┌───┼───┐
    │   │   │
    ▼   ▼   ▼
┌────┐ ┌────┐ ┌────┐
│View│ │Man-│ │Mod-│
│Sta-│ │age │ │erate│
│tis-│ │Use-│ │Con-│
│tics│ │rs  │ │tent│
└────┘ └─┬──┘ └────┘
        │
    ┌───┼───┐
    │   │   │
    ▼   ▼   ▼
┌────┐ ┌────┐ ┌────┐
│Del-│ │Cha-│ │View│
│ete │ │nge │ │Cha-│
│Use-│ │Rol-│ │rts │
│rs  │ │es  │ │    │
└────┘ └────┘ └────┘
```

## Data Flow

### Question Posting Flow

```
Student → Ask Question Form → Flask Route → Validate Data
                                                  │
                                                  ▼
                                          Upload Image (if any)
                                                  │
                                                  ▼
                                          Save to Database
                                                  │
                                                  ▼
                                    Check Similar Questions
                                                  │
                                                  ▼
                                          Return Success
                                                  │
                                                  ▼
                                    Redirect to Dashboard
```

### Answer & Voting Flow

```
User → Submit Answer → Flask Route → Save Answer → Update Reputation (+5)
                                                          │
                                                          ▼
                                                    Notify Question Author
                                                          │
                                                          ▼
User → Vote on Answer → Flask Route → Check Existing Vote
                                              │
                                              ▼
                                    Update Vote Count
                                              │
                                              ▼
                                    Update Author Reputation (±2)
                                              │
                                              ▼
                                    Return Updated Count
```

### Best Answer Selection Flow

```
Question Author/Teacher → Mark Best Answer → Validate Permission
                                                      │
                                                      ▼
                                            Remove Previous Best
                                                      │
                                                      ▼
                                            Mark New Best Answer
                                                      │
                                                      ▼
                                            Update Question Status
                                                      │
                                                      ▼
                                            Award Reputation (+15)
                                                      │
                                                      ▼
                                            Return Success
```

## Database Relationships

```
┌──────────────┐
│    users     │
│──────────────│
│ id (PK)      │◄─────────┐
│ name         │          │
│ email        │          │
│ password     │          │
│ role         │          │
│ reputation   │          │
└──────────────┘          │
       │                  │
       │ 1:N              │ 1:N
       │                  │
       ▼                  │
┌──────────────┐          │
│  questions   │          │
│──────────────│          │
│ id (PK)      │          │
│ user_id (FK) │──────────┘
│ title        │
│ description  │
│ subject      │
│ tags         │
│ image        │
│ status       │
└──────────────┘
       │
       │ 1:N
       │
       ▼
┌──────────────┐
│   answers    │
│──────────────│
│ id (PK)      │◄─────────┐
│ question_id  │          │
│ user_id (FK) │          │
│ answer_text  │          │
│ votes        │          │
│ is_best      │          │
└──────────────┘          │
       │                  │
       │ 1:N              │
       │                  │
       ▼                  │
┌──────────────┐          │
│    votes     │          │
│──────────────│          │
│ id (PK)      │          │
│ answer_id(FK)│──────────┘
│ user_id (FK) │
│ vote_type    │
└──────────────┘

┌──────────────┐
│study_materials│
│──────────────│
│ id (PK)      │
│ teacher_id   │
│ title        │
│ file         │
│ subject      │
└──────────────┘
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Security Layers                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Layer 1: Authentication                                 │
│  ┌────────────────────────────────────────────────┐     │
│  │ • Password Hashing (Werkzeug)                  │     │
│  │ • Session Management (Flask)                   │     │
│  │ • Login Required Decorator                     │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  Layer 2: Authorization                                  │
│  ┌────────────────────────────────────────────────┐     │
│  │ • Role-Based Access Control                    │     │
│  │ • Permission Checks                            │     │
│  │ • Resource Ownership Validation                │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  Layer 3: Data Protection                                │
│  ┌────────────────────────────────────────────────┐     │
│  │ • SQL Injection Prevention                     │     │
│  │ • XSS Protection                               │     │
│  │ • CSRF Protection                              │     │
│  │ • Input Validation                             │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
│  Layer 4: File Security                                  │
│  ┌────────────────────────────────────────────────┐     │
│  │ • File Type Validation                         │     │
│  │ • File Size Limits                             │     │
│  │ • Secure File Names                            │     │
│  │ • Upload Directory Isolation                   │     │
│  └────────────────────────────────────────────────┘     │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Deployment Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Production Deployment                   │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  ┌────────────┐                                         │
│  │   Nginx    │  (Reverse Proxy, SSL, Static Files)    │
│  └─────┬──────┘                                         │
│        │                                                 │
│        ▼                                                 │
│  ┌────────────┐                                         │
│  │  Gunicorn  │  (WSGI Server)                         │
│  └─────┬──────┘                                         │
│        │                                                 │
│        ▼                                                 │
│  ┌────────────┐                                         │
│  │   Flask    │  (Application)                         │
│  │    App     │                                         │
│  └─────┬──────┘                                         │
│        │                                                 │
│        ▼                                                 │
│  ┌────────────┐                                         │
│  │ PostgreSQL │  (Production Database)                 │
│  │  or MySQL  │                                         │
│  └────────────┘                                         │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

## Technology Stack Details

```
┌─────────────────────────────────────────────────────────┐
│                   Technology Stack                       │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  Backend                                                 │
│  ├── Python 3.7+                                        │
│  ├── Flask 3.0.0                                        │
│  ├── Werkzeug 3.0.1                                     │
│  └── SQLite (Development)                               │
│                                                          │
│  Frontend                                                │
│  ├── HTML5                                              │
│  ├── CSS3                                               │
│  ├── JavaScript (ES6+)                                  │
│  ├── Bootstrap 5.3.0                                    │
│  ├── Chart.js                                           │
│  └── Font Awesome 6.4.0                                 │
│                                                          │
│  Development Tools                                       │
│  ├── Git (Version Control)                              │
│  ├── pip (Package Manager)                              │
│  └── Virtual Environment                                │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

**AskBuddy System Architecture**  
*Designed for scalability, security, and maintainability*
