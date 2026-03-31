# 🧹 Data Cleaner App

A Streamlit application to upload, clean, and analyze CSV datasets through an interactive user interface.

The goal of this project is to provide a simple yet robust tool where users can configure data cleaning steps without touching code, and immediately obtain both a cleaned dataset and a structured HTML report.

---

## 📌 What this app does

The application follows a very straightforward flow:
```
Upload a CSV file  
        ↓  
Preview the original data  
        ↓  
Configure cleaning options from the sidebar  
        ↓  
Run the cleaning pipeline  
        ↓  
Preview cleaned data  
        ↓  
Download cleaned CSV + HTML report  
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

## 📊 Outputs

The system generates two outputs:

**1. Cleaned CSV**  
A cleaned version of the dataset, ready for further analysis.

**2. HTML Data Profile Report**  
A structured report describing the dataset.

There are two possible modes:

 |**Advanced mode** | **Fallback mode**|
 |-------------|-------------|
 |uses `ydata-profiling` to generate a detailed report | generates a simplified HTML report based on pandas summaries |
    
The application prioritizes **advanced profiling** and only falls back to a simplified report when necessary, ensuring both rich insights and robustness.

---

## 🧠 Design approach

This project is intentionally structured in layers to keep the code clean and maintainable.

Instead of mixing everything in one file, the application separates:

    - UI logic (Streamlit)  
    - Data cleaning logic  
    - Reporting logic  
    - Utility functions  

The cleaning pipeline works directly on in-memory pandas DataFrames, which is more natural for web-based workflows compared to file-based pipelines.

The reporting layer is centered around **ydata-profiling** for advanced analysis, while maintaining a simplified fallback mechanism to guarantee stability across different environments.

The cleaning pipeline is dynamically configured through the user interface, allowing flexible combinations of steps without modifying the code.

---

# 📁 Project structure

```text
data-cleaner-app/
│
├── app/
│   └── streamlit_app.py
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
├── outputs/
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

Create a virtual environment:

> python -m venv .venv

Activate it (PowerShell):

> .\.venv\Scripts\Activate.ps1

Install dependencies:

> pip install --upgrade pip setuptools wheel
> pip install -r requirements.txt

Run the application:

> python main.py

or directly:

> python -m streamlit run app/streamlit_app.py
---
## 🖥️ How to use the app

1. Upload a CSV file
2. Use the sidebar to configure cleaning options
3. Click "Run Cleaning"
4. Review the results (metrics + tables)
5. Download the cleaned CSV and HTML report
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
- Clear separation between UI and logic
- Reusable cleaning pipeline
- Configuration fully driven by the user interface
- Advanced HTML profiling support
- Simple, readable, and maintainable structure
- Automated tests for core functionality
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