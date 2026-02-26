# Knowledge-Base-and-Document-Management-System

A comprehensive web-based document management system built with FastAPI that enables users to upload, organize, version control, and manage documents securely. This system provides a centralized knowledge base with user authentication, document versioning, and file management capabilities.

## Features

- **User Authentication & Authorization**: Secure login system with password hashing using Argon2
- **Document Management**: Upload, retrieve, update, and delete documents
- **Version Control**: Track document versions and maintain revision history
- **File Handling**: Robust file upload and management with unique ID generation
- **Web Interface**: User-friendly templates for authentication and document interaction
- **RESTful API**: Complete REST API endpoints for programmatic access
- **Security**: JWT-based token authentication for API endpoints
- **Static Assets**: CSS styling for enhanced UI/UX

## Tech Stack

- **Backend Framework**: FastAPI (Python web framework)
- **Database ORM**: SQLAlchemy (SQL toolkit and Object-Relational Mapping)
- **Data Validation**: Pydantic (data validation using Python type annotations)
- **Web Server**: Uvicorn (ASGI server)
- **Templating**: Jinja2 (template engine)
- **Authentication**: python-jose (JWT token handling)
- **Password Hashing**: pwdlib with Argon2 (secure password storage)
- **File Upload**: python-multipart (form data handling)

## Project Structure

```
Knowledge-Base-and-Document-Management-System/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── App/                      # Main application package
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database configuration and session setup
│   ├── dependency.py        # Dependency injection utilities
│   ├── core/
│   │   └── security.py      # Security utilities and authentication logic
│   ├── models/              # SQLAlchemy database models
│   │   ├── User.py          # User model definition
│   │   ├── Documents.py     # Document model definition
│   │   └── Versions.py      # Document version model definition
│   ├── routers/             # API endpoint routers
│   │   ├── User.py          # User authentication endpoints
│   │   └── Documents.py     # Document management endpoints
│   ├── schemas/             # Pydantic schemas for request/response validation
│   │   ├── user.py          # User request/response schemas
│   │   └── documents.py     # Document request/response schemas
│   ├── templates/           # HTML templates for web interface
│   │   ├── index.html       # Main document dashboard
│   │   └── login.html       # User login page
│   ├── static/              # Static assets (CSS, JS, images)
│   │   ├── style.css        # Main stylesheet
│   │   └── docs.css         # Document-specific styles
│   └── utils/
│       └── filehandler.py   # File upload and management utilities
└── Uploads/                 # Directory for storing uploaded files
```

## Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Knowledge-Base-and-Document-Management-System
   ```

2. **Create a virtual environment** (if not already created)
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

1. **Start the FastAPI server**
   ```bash
   uvicorn App.main:app --reload
   ```
   - The application will be available at `http://localhost:8000`
   - API documentation at `http://localhost:8000/docs` (Swagger UI)
   - Alternative API docs at `http://localhost:8000/redoc` (ReDoc)

2. **Access the web interface**
   - Navigate to `http://localhost:8000/`
   - You will be redirected to the login page at `/auth/`

## API Endpoints

### Authentication Routes (User Router)
- `GET /auth/` - Login page
- `POST /auth/login` - User login endpoint
- `POST /auth/register` - User registration endpoint
- `GET /auth/logout` - User logout endpoint

### Document Routes (Documents Router)
- `GET /documents/` - List all documents
- `POST /documents/upload` - Upload a new document
- `GET /documents/{document_id}` - Retrieve specific document
- `PUT /documents/{document_id}` - Update document metadata
- `DELETE /documents/{document_id}` - Delete a document
- `GET /documents/{document_id}/versions` - Get document version history

## Usage

### User Registration & Login
1. Navigate to the login page
2. Click on "Register" to create a new account
3. Enter credentials and submit
4. Use credentials to login

### Document Management
1. After login, access the document dashboard
2. Use the upload form to add new documents
3. View, download, or delete existing documents
4. Track document versions through the version history

### API Usage Example
```bash
# Login and get token
curl -X POST "http://localhost:8000/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user&password=password"

# Upload a document
curl -X POST "http://localhost:8000/documents/upload" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "file=@document.pdf"

# Retrieve documents
curl -X GET "http://localhost:8000/documents/" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Database Models

### User Model
- `id`: Unique user identifier
- `username`: User's login name (unique)
- `email`: User's email address
- `password_hash`: Hashed password
- `created_at`: Account creation timestamp

### Document Model
- `id`: Unique document identifier
- `filename`: Original filename
- `owner_id`: ID of the user who owns the document
- `file_path`: Path to stored file
- `created_at`: Document upload timestamp
- `updated_at`: Last modification timestamp

### Version Model
- `id`: Unique version identifier
- `document_id`: Associated document ID
- `version_number`: Version sequence number
- `file_path`: Path to versioned file
- `created_at`: Version creation timestamp

## Security Considerations

- Passwords are hashed using Argon2 algorithm for secure storage
- JWT tokens are used for API authentication
- File uploads are stored with unique identifiers
- SQL injection is prevented through SQLAlchemy ORM
- CORS and security headers can be configured as needed

## Environment Variables

Create a `.env` file in the project root (optional):
```
DATABASE_URL=sqlite:///./test.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Acknowledgments

- FastAPI documentation and community
- SQLAlchemy for excellent ORM functionality
- Pydantic for robust data validation