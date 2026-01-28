# 🏥 Health Records API (FastAPI)

A **secure, audit‑friendly backend API** for managing **Health Records** and **Medicine History** with proper authentication, authorization, file versioning, and snapshot-based change tracking.

This project is designed as a **POC → production‑ready foundation**, focusing on **data integrity, security, and traceability**.

---

## 🚀 Key Features

### 🔐 Authentication & Security

* JWT‑based authentication
* User‑level authorization on every resource
* No user can access or modify another user’s data

---

### 🧾 Health Records Module

#### ✔ Create Health Record

* Each user can create **one record per record_type**
* Duplicate record_type creation is **blocked**
* Optional file upload support

#### ✔ Update Health Record

* Record **must exist** before update
* Only record owner can update
* Supports **file versioning**

#### ✔ File Versioning

* Every uploaded file is stored as a **new version**
* Previous files are never overwritten
* Latest file is always accessible via `file_url`

#### ✔ Delete Health Record (Clean Delete)

* Deletes:

  * Health record data
  * All associated file versions from storage
* Prevents orphan files (no storage leaks)

---

### 💊 Medicine Records Module

#### ✔ Create Medicine Record

* Stores current medicine data
* Automatically creates the **first snapshot** in `medicine_history`

#### ✔ Update Medicine Record (Partial Update)

* Supports PATCH‑style partial updates
* Only provided fields are modified
* **Every update appends a snapshot**

#### ✔ Medicine History (Audit Trail)

* Snapshot‑based history system
* Preserves:

  * Initial POST state
  * Every PUT update state
  * Exact timestamps of changes

This guarantees:

* No data loss
* Full medical change traceability

---

## 🧠 Architecture Overview

```text
Client
  ↓
Router Layer (FastAPI)
  ↓
Service Layer (Business Logic)
  ↓
In‑Memory Store (POC)
```

* **Router Layer**: HTTP, validation, auth handling
* **Service Layer**: Core business logic
* **Storage Layer**: In‑memory dicts (replaceable with DB)

---

## 📂 Project Structure

```text
app/
├── core/
│   └── security.py          # JWT handling
├── models/
│   ├── health_record.py     # Health record schemas
│   └── medicine.py          # Medicine schemas
├── services/
│   ├── health_record_service.py
│   └── medicine_service.py
├── routers/
│   ├── health_record.py
│   └── medicine_record.py
├── database/
│   ├── health_record_store.py
│   └── medicine_store.py
├── utils/
│   └── cleanup_file_storage.py
└── main.py
```

---

## 🧪 API Capabilities Summary

### Health Records

* `POST   /health-records` – Create
* `GET    /health-records` – List user records
* `GET    /health-records/{id}` – Get single record
* `PUT    /health-records/{id}` – Update
* `DELETE /health-records/{id}` – Delete (with file cleanup)

### Medicine Records

* `POST   /medicines` – Create medicine
* `GET    /medicines` – List medicines
* `GET    /medicines/{id}` – Get medicine
* `PUT    /medicines/{id}` – Update (snapshot stored)
* `DELETE /medicines/{id}` – Delete

---

## 🧾 Data Integrity Guarantees

✔ No duplicate health record types per user
✔ No update without prior creation
✔ No unauthorized access
✔ No orphan files after delete
✔ No history overwrite (append‑only snapshots)

---

## 🔮 Future Improvements (Optional)

* Replace in‑memory store with PostgreSQL / MongoDB
* File storage via S3 / GCS
* Pagination & filtering
* Soft delete support
* Admin audit dashboard

---

## 📌 Project Status

✅ Core features complete
✅ Security enforced
✅ Audit trails implemented
🚀 Ready for GitHub push & further scaling

**Disclaimer:**  
Currently, all uploaded health record files are stored locally on the development server for testing purposes. In a production environment, these files should be migrated to a secure cloud storage service (e.g., AWS S3, Google Cloud Storage) to ensure proper access, security, and scalability.


---

## 👤 Author

**Mushahid Hussain**
Backend Developer (FastAPI / Python)

---

> This project prioritizes **clarity, safety, and correctness** over shortcuts — making it suitable for real‑world healthcare data handling at a foundational level.