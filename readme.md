# 💲 Supermarket Purchase Tracker

A complete **FastAPI + PostgreSQL + Docker + Frontend** system that manages supermarket purchases, users, and analytics.

It includes:
- 🗃️ PostgreSQL database with CSV auto-load on first run  
- ⚙️ Backend API built with FastAPI  
- 💿 Secure credentials using **Docker Secrets**  
- 🧮 Analytics microservice for supermarket stats  
- 🖼️ Simple JavaScript frontend with dropdown UI  

---

## 🧩 Project Structure

```
.
├── backend/                  # FastAPI app (main service)
│   ├── app/
│   │   ├── main.py
│   │   ├── routes.py
│   │   ├── models.py
│   │   ├── db.py
│   │   ├── lifespan.py
│   │   └── config.py
│   └── Dockerfile
│
├── analytics/                # Analytics microservice
│   ├── app/
│   │   ├── main.py
│   │   ├── router.py
│   │   └── analytics_service.py
│   └── Dockerfile
│
├── frontend/                 # Simple static frontend (HTML, JS, CSS)
│   ├── index.html
│   ├── stats.html
│   ├── main.js
│   └── Dockerfile
│
├── db/                       # Database initialization files
│   ├── 01_init.sql
│   ├── 02_load_data.sql
│   ├── products_list.csv
│   └── purchases.csv
│
├── secrets/                  # Docker secrets (NOT versioned)
│   ├── db_name.txt
│   ├── db_user.txt
│   ├── db_password.txt
│   └── .gitkeep
│
├── docker-compose.yml
├── .gitignore
└── README.md
```

---

## 🔐 Secrets Setup (MUST DO BEFORE RUNNING)

Your project uses **Docker Secrets** for database credentials.  
These files are **NOT stored in Git** for security reasons.

### 1️⃣ Create the `secrets/` folder
```bash
mkdir -p secrets
```

### 2️⃣ Create the following files:

| File | Description | Example content |
|------|--------------|----------------|
| `secrets/db_name.txt` | Database name | `appdb` |
| `secrets/db_user.txt` | PostgreSQL username | `user` |
| `secrets/db_password.txt` | PostgreSQL password | `pass123` |

⚠️ These files are **referenced** in your `docker-compose.yml` and **mounted securely** into the containers under `/run/secrets`.

---

## 🐳 Running the Project

### 1️⃣ Build and start all services
```bash
docker compose up --build
```

This starts:
- 🔄 **PostgreSQL** (`db`)
- ⚙️ **FastAPI Backend** (`backend`)
- 📊 **Analytics Service** (`analytics`)
- 🖼️ **Frontend** (`frontend`)

---

### 2️⃣ Access the apps

| Service | URL |
|----------|-----|
| 🧠 Backend API (FastAPI docs) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| 📊 Analytics API | [http://localhost:8001/docs](http://localhost:8001/docs) |
| 🖼️ Frontend UI | [http://localhost:8080](http://localhost:8080) |
| 🗃️ PostgreSQL DB | port `5432` |

---

## 📦 Database Behavior

- On first startup, Docker’s `initdb.d` folder loads:
  - `01_init.sql` → creates all tables
  - `02_load_data.sql` → loads data from CSV files
- CSVs are mounted inside `/docker-entrypoint-initdb.d/`
- Foreign keys are temporarily disabled during loading to avoid dependency errors.

---

## 💡 Backend Highlights

### `/init`
Returns cached data:
```json
{
  "products": [{"id":1,"name":"bread","price":2.5}],
  "supermarkets": ["SMKT001","SMKT002"],
  "users": ["uuid1","uuid2"]
}
```

### `/add_item`
Creates or reuses a user and logs a purchase:
```json
{
  "supermarket_id": "SMKT001",
  "user_id": null,
  "items": [1, 2]
}
```

Response:
```json
{
  "purchase_id": 1,
  "user_id": "9b8a60d6-70c4-4ed1-a2de-7c4749b8b5e3",
  "items": ["bread","milk"],
  "total_amount": 4.5,
  "timestamp": "2025-05-26T19:51:00.539354"
}
```

---

## 📊 Analytics API

### `/analytics/{supermarket_id}`

Returns:
```json
{
  "unique_buyers": 18,
  "special_users": [
    {"user_id":"9b8a60d6-...","purchase_count":5}
  ],
  "top_items": ["milk","bread","eggs"]
}
```

---

## 🖼️ Frontend Behavior

### Main Page (`index.html`)
- Dropdowns for supermarkets and users
- Multi-select for products
- “🆕 Create new user” option auto-generates a new user
- Displays purchase confirmation with:
  - ✅ Status
  - 🢍 User ID
  - 📺 Items
  - 💰 Total amount
  - 🕒 Timestamp

### Analytics Page (`stats.html`)
- Dropdown for supermarkets
- Button: **"Get Supermarket Statistics"**
- Displays:
  - Unique buyers
  - Frequent buyers
  - Top products

---

## ⚙️ Docker Compose Services Overview

| Service | Purpose | Ports |
|----------|----------|-------|
| **frontend** | Static UI served by lightweight HTTP | `8080:80` |
| **backend** | Main FastAPI app | `8000:8000` |
| **analytics** | Analytics API | `8001:8001` |
| **db** | PostgreSQL database | `5432:5432` |

---

## 🚨 Common Issues

| Problem | Fix |
|----------|-----|
| `Connection refused: db` | Add `depends_on: [db]` in backend and analytics |
| `relation "products_list" does not exist` | Ensure `db/01_init.sql` and CSV files exist |
| `could not open file ...csv` | Check file path inside `/db` and permissions |
| `user_id` missing | Ensure frontend sends `null` when dropdown empty |
| No analytics data | Make purchases first for that supermarket |

---

## 🧹 Cleanup
To remove all containers, networks, and volumes:
```bash
docker compose down -v
```

---

## 🛡️ Security Notes
- Secrets are never stored in git (`.gitignore` covers them)
- Use Docker secrets or environment variables for credentials
- Avoid hardcoding passwords in `.env` or `config.ini`
