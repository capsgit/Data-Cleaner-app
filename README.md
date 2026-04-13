# 🧹 Data Cleaner App

A fullstack data cleaning application built with Streamlit (frontend) and FastAPI (backend).

This project allows users to upload CSV files, configure cleaning operations through an intuitive UI, and process data via a scalable backend service.

---

## 📌 What this app does

The application follows a very straightforward flow:

```
User uploads CSV 
       ↓ 
Frontend (Streamlit UI)
       ↓ 
Request sent to FastAPI backend
       ↓ 
Backend runs cleaning pipeline 
       ↓ 
Returns results (metrics + preview) 
       ↓ 
User downloads cleaned data + report
```
---

## ⚙️ Main features

The cleaning process is fully configurable through the UI. The user can:

    - Remove fully empty rows  
    - Remove repeated header rows inside the dataset  
    - Convert selected columns to numeric  
    - Convert a column to datetime  
    - Remove rows with missing values  
    - Remove duplicate rows (optionally based on specific columns)  
    - Drop selected columns  

After running the pipeline, the app provides:

    - A cleaned version of the dataset  
    - A summary of applied steps  
    - A preview of the cleaned data  
    - Downloadable outputs  

---

## 📊 Results

After processing:

- Dataset metrics (before / after + delta)
- Step-by-step cleaning summary
- Preview of cleaned dataset
- Downloadable outputs

---

## 📥 Downloads
    
+ Cleaned CSV

+ HTML Data Profile Report
---
## 🧠 Design Philosophy

This project is built around clean architecture principles:

### 🔹 Separation of concerns
- Frontend → UI only
- Backend → orchestration + API
- Core (src/) → pure logic

### 🔹 Scalable backend

The backend exposes independent endpoints:

- /cleaning/preview → fast preview
- /cleaning/download-csv → CSV generation
- /cleaning/download-report → HTML report

#### This allows:

- performance optimization
- async scaling
- future integrations (mobile, APIs, etc.)

### 🔹 Robustness
- Graceful fallback when profiling fails
- Error handling between frontend ↔ backend
- Timeout-safe operations
---

# 📁 Project structure

```text
data-cleaner-app/
│
├── frontend
│   ├── app.py  
│   ├── api/
│   ├── ui/
│   ├── utils/
│   └── config.py
│
├── backend/
│   ├── main.py
│   ├── routes/
│   │   └── cleaning.py
│   ├── schemas/
│   │   └── cleaning.py
│   └── services/ 
│       ├── cleaning_pipeline.py 
│       └── cleaning_service.py
│
├── src/
│   ├── cleaning/
│   │   ├── cleaner.py
│   │   ├── options.py
│   │   └── steps.py
│   │
│   ├── reporting/
│   │   └── profiler.py
│   │
│   └── utils/
│       └── logger.py
│
├── tests/
│   ├── test_cleaner.py
│   └── test_steps.py
│
├── logs/
├── data/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
└── main.py
```
---
## 🛠️ Technologies used
    Python
    Pandas
    Streamlit
    ydata-profiling (advanced reporting)
    Pytest (testing) 
---
## ▶️ How to run the project
#### 1. Create a virtual environment
> python -m venv .venv

#### 2. Activate it
>PowerShell (Windows):
>.\.venv\Scripts\Activate.ps1

#### 3. Install dependencies
>pip install --upgrade pip setuptools wheel
>pip install -r requirements.txt

### 🚀 Run the full application (recommended)

The project provides a development launcher that starts both:

- FastAPI backend
- Streamlit frontend

with a single command:

>python run_dev.py

After running:

- Backend → http://127.0.0.1:8000
- API Docs → http://127.0.0.1:8000/docs
- Frontend → http://localhost:8501

### ⚙️ Run services separately (optional)

If needed, both services can be started independently:

#### Backend (FastAPI)
>python -m uvicorn backend.main:app --reload

#### Frontend (Streamlit)
>python -m streamlit run frontend/app.py
---
## 🖥️ How to use the app

1. Upload a CSV file
2. Use the sidebar to configure cleaning options
3. Click "Run Cleaning"
4. Review the results (metrics + tables)
5. Download the cleaned CSV and/or HTML report
---

## 🧪 Testing

The project includes automated tests for the core cleaning logic.

Tests cover:

- individual cleaning steps  
- pipeline execution  
- expected transformations on rows and columns  

Run tests with:

> pytest
---

## ✅ Key strengths of this implementation
- Fullstack architecture (UI + API separation)
- Modular and maintainable design
- Reusable cleaning pipeline
- Backend-driven processing (scalable)
- Clean UI/UX with Streamlit
- Robust error handling
- Testable core logic
---

## 🚀 Possible improvements
- Fill missing values from UI
- Rename columns
- Normalize column names
- Export to Excel
- Display HTML report inside the app
---
## 📄 License

This project is for educational purposes.

---