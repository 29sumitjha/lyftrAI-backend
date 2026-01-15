# Lyftr.ai – Backend Assignment Solution

🚀 **Overview** This repository contains my solution for the Lyftr.ai Backend Engineering Assignment. The project implements a production-style backend service that ingests WhatsApp-like message webhooks, validates signatures, stores messages idempotently, and exposes robust APIs for analytics and monitoring.

---

## ✔️ Features Implemented

* **Webhook Ingestion:** `/webhook` endpoint with HMAC-SHA256 signature validation via `X-Signature`.
* **Idempotency:** Message storage logic using DB primary keys to prevent duplicates.
* **Database:** Persistent storage using **SQLite** with SQLAlchemy.
* **Message APIs:** `/messages` endpoint supporting:
    * Pagination (`limit`, `offset`)
    * Text search (`q`)
    * Filters (`from`, `since` timestamp)
* **Analytics:** `/stats` endpoint for message and sender insights.
* **Observability:** * Health probes: `/health/live` and `/health/ready`.
    * Metrics: `/metrics` in Prometheus format.
    * Structured JSON logging with `request_id`.
* **Deployment:** Fully containerized using Docker & Docker Compose.

---

## 🛠️ Tech Stack

* **Framework:** Python 3.12+, FastAPI, Uvicorn
* **Database:** SQLite + SQLAlchemy + aiosqlite
* **Infrastructure:** Docker, Docker Compose
* **Monitoring:** Prometheus-style metrics

---

## Setup Instructions

### Pre-requisites

- Docker Desktop installed and running.
- Open windows powershell as administrator & set default to WSL2.

### Clone the Repository

```bash
git clone https://github.com/29sumitjha/lyftrAI-backend.git
```

Create a virtual environment and activate it **(recommended)**

Open your command prompt and change your project directory to ```lyftr-backend``` and run the following command 
```bash
python -m venv venvapp

source venv/Scripts/activate
```
you should see (venv) at the beginning of your terminal prompt

Downloading packages from ```requirements.txt```
```bash
pip install -r requirements.txt
```

After installation is finished run the backend
```bash
docker compose up -d --build
```
This will:
1.Build the FastAPI service
2.Start PostgreSQL
3.Apply database initialization
4.Expose the API on port 8000

Then test the following url in any browser:
http://localhost:8000/health/live
http://localhost:8000/health/ready

Respose:
{"status": "live"}
{"status": "ready"}

Then check all the routes on by one:
/messages
/stats
/mertics
Also Send POST request on /webhooks with correct signature

Stop the services:
```bash
docker compose down
```

---

# 🧪 Running Tests

Tests are written using pytest and pytest-asyncio.

### Run all test
```bash
pytest --vv
```
Expected Output:
collected 4 items
tests/test_messages.py PASSED
tests/test_stats.py PASSED
tests/test_webhook.py PASSED

### ✅ Final Verification Checklist
Before submission, the following were verified:

-  Docker build succeeds.
- API runs successfully.
- /health endpoint responds correctly
- All tests pass
- Webhook idempotency handled
- Clean and readable code structure

### 👨‍💻 Author

Sumit Kumar Jha
B.Tech – Computer Science & Engineering
