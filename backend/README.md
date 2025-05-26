# 🏨 Hotel Management Dashboard API

A backend service built with **FastAPI**, powering the Hotel Management Dashboard.

## 🧱 Virtual Environment Setup

1. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Starting the Application

### Option 1: Run Locally with FastAPI

Start the development server:

```bash
fastapi dev main.py
```

Then access the application at:
➡️ [http://127.0.0.1:8000](http://127.0.0.1:8000)

You can also view the interactive API documentation at:
➡️ [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) (Swagger UI)

## 📄 PDF Generation (WeasyPrint)

This project uses [WeasyPrint](https://weasyprint.org) to generate high-quality PDFs.

### 🛠️ System Dependencies

WeasyPrint requires some additional **system-level libraries** (like Cairo, Pango, and GDK-PixBuf) that must be installed before usage.

### ✅ Setup Instructions

Follow the official platform-specific installation guide here:
👉 [WeasyPrint Installation Guide](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html)

> Failure to install these dependencies will result in PDF generation errors.
