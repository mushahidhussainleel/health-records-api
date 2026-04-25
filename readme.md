# 🏥 Health Records API

[![Interactive Summary](https://img.shields.io/badge/Interactive-Summary-blue?style=for-the-badge&logo=react)](https://claude.ai/public/artifacts/3bd85bef-4e12-4776-98fe-8aec39268b73)
> Click the badge above to explore the **full interactive infographic** summarizing the Health Records API project.

<div align="center">

![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104+-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Status](https://img.shields.io/badge/Status-Active-success.svg)

**A secure, audit-friendly backend API for managing Health Records and Medicine History**

[Features](#-features) • [Installation](#-installation) • [API Documentation](#-api-documentation) • [Architecture](#-architecture) • [Contributing](#-contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Project Demo](#-project-demo)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [API Documentation](#-api-documentation)
- [Architecture](#-architecture)
- [Security](#-security)
- [Database Schema](#-database-schema)
- [Usage Examples](#-usage-examples)
- [Testing](#-testing)
- [Future Enhancements](#-future-enhancements)
- [Disclamier](#️-disclaimer)
- [License](#-license)
- [Author](#-author)
- [Support](#-support)

---

## 🎯 Overview

The **Health Records API** is a production-ready backend system built with FastAPI for **secure, versioned, and auditable management of patient health records and medicine history**.

It supports JWT authentication, file versioning, and comprehensive audit trails to ensure integrity and compliance.

### Why This Project?

Healthcare data requires:
- ✅ **Security**: Patient data must be protected
- ✅ **Auditability**: Every change must be tracked
- ✅ **Integrity**: No data loss or corruption
- ✅ **Traceability**: Complete history of all changes

---
## 🎥 Project Demo

Watch the full demo walkthrough of the **Health Records API**:

[![Health Records API Demo](https://img.youtube.com/vi/HHL9LozL0jE/0.jpg)](https://youtu.be/HHL9LozL0jE)

📌 **Demo Highlights**
- FastAPI backend running with Swagger UI
- JWT Authentication flows
- Health Records CRUD with file versioning
- Medicine Records CRUD with history and snapshots
- Secure, production-ready project showcase

👉 Click the thumbnail to watch the video directly on YouTube.

---

## ✨ Features

### 🔐 Authentication & Authorization
- JWT-based authentication (access + refresh tokens)
- Role-based access control (RBAC)
- User isolation (users access only their data)
- Secure password hashing with bcrypt

### 🏥 Health Records
- CRUD operations with file attachments
- One record per type per user (prevents duplicates)
- File versioning (track previous uploads)
- Update records with automatic version tracking
- Delete records with file cleanup
- Filtering & retrieval options

### 💊 Medicine Records
- CRUD with automatic snapshots
- Full audit trail & historical timeline
- Partial updates supported (PATCH)
- Append-only history (no overwrites)

### 📁 File Management
- Multi-version file storage
- PDF, images, documents supported
- Automatic cleanup on deletion
- Latest file always accessible

---

## 🛠️ Tech Stack

| Category | Technologies |
|----------|-------------|
| Backend Framework | FastAPI 0.104+ |
| Language | Python 3.9+ |
| Authentication | JWT (JSON Web Tokens) |
| Password Hashing | Bcrypt |
| Data Validation | Pydantic v2 |
| API Documentation | OpenAPI (Swagger UI) |
| File Storage | Local FileSystem (AWS S3-ready) |
| Database | In-memory (PostgreSQL-ready) |

---

## 📁 Project Structure

```
health-records-api/
│
├── app/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py              # Environment configuration
│   │   ├── security.py            # JWT & password hashing
│   │   └── dependencies.py        # FastAPI dependencies
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py                # User schemas
│   │   ├── health_record.py       # Health record schemas
│   │   └── medicine.py            # Medicine schemas
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth_service.py        # Authentication logic
│   │   ├── health_record_service.py
│   │   └── medicine_service.py
│   │
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── auth.py                # Auth endpoints
│   │   ├── health_record.py       # Health record endpoints
│   │   └── medicine_record.py     # Medicine endpoints
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── user_store.py
│   │   ├── health_record_store.py
│   │   └── medicine_store.py
│   │
│   └── utils/
│       ├── __init__.py
│       ├── file_handler.py
│       └── cleanup_file_storage.py
│
├── storage/
│   └── health-record/             # Health record file uploads
│
├── .env.example                   # Environment variables template
├── .gitignore
├── requirements.txt
├── main.py                        # Application entry point
└── README.md
```

---

## 🚀 Installation

### Prerequisites
- Python 3.9+
- pip
- Virtual environment (recommended)

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/mushahidhussainleel/health-records-api.git
cd health-records-api

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Create .env file
cp .env.example .env
# Edit .env with your configurations

# 6. Run the application
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API Base**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---

## ⚙️ Configuration

Create a `.env` file in the root directory:

```env
# Application Settings
APP_NAME=Health Records API
APP_VERSION=1.0.0
DEBUG=True

# Security
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Storage
UPLOAD_DIRECTORY=./storage
```

---

## 📚 API Documentation

### Authentication Endpoints

#### Register User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

#### Login
```http
POST /auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=SecurePass123
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

---

### Health Records Endpoints

#### Create Health Record
```http
POST /health-records
Authorization: Bearer {token}
Content-Type: multipart/form-data

record_type: "Blood Test"
notes: "Annual checkup"
file: [binary file]
```

#### Get All Records
```http
GET /health-records
Authorization: Bearer {token}
```

#### Get Single Record
```http
GET /health-records/{id}
Authorization: Bearer {token}
```

#### Update Record
```http
PUT /health-records/{id}
Authorization: Bearer {token}
Content-Type: multipart/form-data

notes: "Updated notes"
file: [binary file]  # Optional
```

#### Delete Record
```http
DELETE /health-records/{id}
Authorization: Bearer {token}
```

---

### Medicine Records Endpoints

#### Create Medicine
```http
POST /medicines
Authorization: Bearer {token}
Content-Type: application/json

{
  "medicine_name": "Aspirin",
  "dosage": "100mg",
  "frequency": "Once daily",
  "start_date": "2024-01-01",
  "end_date": "2024-03-01",
  "notes": "Take after breakfast"
}
```

#### Get All Medicines
```http
GET /medicines
Authorization: Bearer {token}
```

#### Get Single Medicine
```http
GET /medicines/{id}
Authorization: Bearer {token}
```

#### Update Medicine (Creates Snapshot)
```http
PUT /medicines/{id}
Authorization: Bearer {token}
Content-Type: application/json

{
  "dosage": "150mg",
  "frequency": "Twice daily"
}
```

#### Get Medicine History
```http
GET /medicines/{id}/history
Authorization: Bearer {token}
```

#### Delete Medicine
```http
DELETE /medicines/{id}
Authorization: Bearer {token}
```

---

## 🏗️ Architecture

### Layered Architecture

```
┌─────────────────────────────────────┐
│         Client Applications         │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│          Router Layer               │
│   (HTTP Handling, Validation)       │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│         Service Layer               │
│     (Business Logic)                │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│        Data Access Layer            │
│   (Storage & Persistence)           │
└─────────────────────────────────────┘
                 ↓
┌─────────────────────────────────────┐
│          Storage                    │
│   (In-Memory / Database)            │
└─────────────────────────────────────┘
```

### Design Principles
- **Separation of Concerns**: Each layer has specific responsibility
- **Dependency Injection**: FastAPI's dependency system
- **Single Responsibility**: Each module handles one aspect
- **Open/Closed Principle**: Easy to extend without modifying

---

## 🔒 Security

### Security Features

✅ **JWT Tokens**: Stateless authentication with expiration
✅ **Password Hashing**: Bcrypt with salt
✅ **User Isolation**: Database-level separation
✅ **Input Validation**: Pydantic schemas
✅ **File Type Validation**: Whitelist-based
✅ **File Size Limits**: Prevent DOS attacks

### Authentication Flow

1. User registers → Password hashed → Stored
2. User logs in → Credentials verified → JWT generated
3. Protected requests → Token validated → User identified

---

## 💾 Database Schema

### User Model
```python
{
  "id": "uuid",
  "email": "string (unique)",
  "hashed_password": "string",
  "full_name": "string",
  "is_active": "boolean",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Health Record Model
```python
{
  "id": "uuid",
  "user_id": "uuid (foreign key)",
  "record_type": "string (unique per user)",
  "notes": "string (optional)",
  "file_url": "string (latest version)",
  "file_versions": [
    {
      "version": "integer",
      "file_path": "string",
      "uploaded_at": "datetime"
    }
  ],
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Medicine Record Model
```python
{
  "id": "uuid",
  "user_id": "uuid (foreign key)",
  "medicine_name": "string",
  "dosage": "string",
  "frequency": "string",
  "start_date": "date",
  "end_date": "date (optional)",
  "notes": "string (optional)",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

### Medicine History Model
```python
{
  "id": "uuid",
  "medicine_id": "uuid (foreign key)",
  "snapshot_data": "json",
  "snapshot_timestamp": "datetime",
  "change_type": "enum (created, updated)"
}
```

---

## 💡 Usage Examples

### Using Python Requests

```python
import requests

BASE_URL = "http://localhost:8000"

# 1. Register
response = requests.post(f"{BASE_URL}/auth/register", json={
    "email": "john@example.com",
    "password": "SecurePass123",
    "full_name": "John Doe"
})

# 2. Login
response = requests.post(f"{BASE_URL}/auth/login", data={
    "username": "john@example.com",
    "password": "SecurePass123"
})
token = response.json()["access_token"]

# 3. Create Health Record
headers = {"Authorization": f"Bearer {token}"}
files = {"file": open("blood_test.pdf", "rb")}
data = {"record_type": "Blood Test", "notes": "Annual checkup"}
response = requests.post(
    f"{BASE_URL}/health-records",
    headers=headers,
    data=data,
    files=files
)

# 4. Create Medicine
response = requests.post(
    f"{BASE_URL}/medicines",
    headers=headers,
    json={
        "medicine_name": "Aspirin",
        "dosage": "100mg",
        "frequency": "Once daily",
        "start_date": "2024-01-01"
    }
)

# 5. Get Medicine History
medicine_id = response.json()["id"]
response = requests.get(
    f"{BASE_URL}/medicines/{medicine_id}/history",
    headers=headers
)
```


---

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Run all tests
pytest

# Run with coverage
pytest --cov=app tests/

# Run specific test file
pytest tests/test_health_records.py -v
```

---

### Production Checklist
- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS/TLS
- [ ] Set up database (PostgreSQL)
- [ ] Configure cloud storage (AWS S3)
- [ ] Implement rate limiting
- [ ] Set up logging and monitoring
- [ ] Enable CORS with specific origins

---

## 🔮 Future Enhancements

### Phase 1: Database Integration
- [ ] PostgreSQL for persistent storage
- [ ] Database migrations (Alembic)
- [ ] Connection pooling
- [ ] Query optimization

### Phase 2: Cloud Storage
- [ ] AWS S3 integration
- [ ] Pre-signed URLs for secure access
- [ ] CDN for faster delivery

### Phase 3: Advanced Features
- [ ] Pagination and filtering
- [ ] Search functionality (Elasticsearch)
- [ ] Email notifications
- [ ] SMS reminders for medicines
- [ ] Export records to PDF
- [ ] Admin dashboard

### Phase 4: Analytics & AI
- [ ] Health trends visualization
- [ ] Medicine adherence tracking
- [ ] AI-powered health insights
- [ ] OCR for medical documents

### Phase 5: Compliance
- [ ] HIPAA compliance
- [ ] Two-factor authentication (2FA)
- [ ] Audit logging
- [ ] Data encryption at rest

---

## ⚠️ Disclaimer 
Currently, all health record files uploaded to the system are stored locally on the development server for testing purposes, and the application uses in-memory storage for all records.  
This means that any data created during a session will be lost once the application is stopped or restarted.  

In a production environment, it is highly recommended to:  

- Migrate files to a secure cloud storage service (e.g., AWS S3, Google Cloud Storage) for proper access control, security, and scalability.  
- Use a persistent database (e.g., PostgreSQL) to ensure data is not lost between sessions.  

These enhancements will be implemented in future updates to make the system fully production-ready.

---

### Coding Standards
- Write docstrings for functions
- Add type hints
- Write unit tests
- Update documentation

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Mushahid Hussain**

- Backend Developer (FastAPI / Python)
- GitHub: [@mushahidhussainleel](https://github.com/mushahidhussainleel)
- Email: mushahidh442007@gmail.com

---

## 🙏 Acknowledgments

- FastAPI framework and community
- Pydantic for data validation
- JWT for authentication
- All contributors

---

## 📞 Support

Need help?

- 📧 Open an issue on GitHub
- 📧 Contact via email
- ⭐ Star this repository if helpful!

---

<div align="center">

**Built with ❤️ for Healthcare Data Management**

Made with [FastAPI](https://fastapi.tiangolo.com/) | Powered by [Python](https://www.python.org/)

</div>
