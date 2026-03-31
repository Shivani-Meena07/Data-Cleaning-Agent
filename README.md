# 🧹 AI-Powered Data Cleaning Agent

An intelligent data cleaning platform that leverages AI and rule-based methods to automatically detect and fix data quality issues across multiple data sources.

## 📋 Overview

The **Data Cleaning Agent** is a full-stack web application that helps users clean and prepare data for analysis. It combines:
- **Rule-based cleaning** for common data quality issues (missing values, duplicates, formatting)
- **AI-powered processing** using machine learning for intelligent data transformation
- **Multi-source support** for CSV, Excel, databases, and APIs
- **User-friendly interface** built with Streamlit
- **Scalable backend** powered by FastAPI

## ✨ Features

- **📁 File Upload** - Clean CSV and Excel files with AI
- **🗄️ Database Integration** - Connect to PostgreSQL and clean data directly from tables
- **🌐 API Data Fetching** - Ingest and clean data from REST APIs
- **🤖 AI Processing** - Intelligent data transformation using machine learning
- **📊 Data Preview** - View raw and cleaned data side-by-side
- **💾 Export Results** - Download cleaned data in multiple formats
- **🔍 Data Quality Metrics** - See what was fixed and correction statistics

## 🏗️ Architecture

```
┌─────────────────────────────────────┐
│   Streamlit Frontend (Port 8501)    │
│   User Interface & Visualization    │
└────────────┬────────────────────────┘
             │ HTTP Requests
             ▼
┌─────────────────────────────────────┐
│   FastAPI Backend (Port 8000)       │
│   • Data Cleaning Pipeline          │
│   • AI Agent Integration            │
│   • Database Connectors             │
└────────────┬────────────────────────┘
             │
        ┌────┴────┐
        ▼         ▼
    PostgreSQL  External APIs
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL (optional, for database features)

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd data_cleaning_agent
   ```

2. **Create virtual environment**
   ```bash
   python -m venv data_cleaning_agent_env
   data_cleaning_agent_env\Scripts\activate  # Windows
   # or
   source data_cleaning_agent_env/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

Start both the backend and frontend:

**Terminal 1 - Start FastAPI Backend:**
```bash
data_cleaning_agent_env\Scripts\activate
cd scripts
python backend.py
```
Backend runs on: `http://localhost:8000`

**Terminal 2 - Start Streamlit Frontend:**
```bash
data_cleaning_agent_env\Scripts\activate
streamlit run app/app.py
```
Frontend runs on: `http://localhost:8501`

The application will automatically open in your browser at `http://localhost:8501`

## 📖 Usage

### 1. **Clean CSV/Excel Files**
   - Select "CSV/Excel" from the sidebar
   - Upload your file
   - Review the raw data preview
   - Click "Clean Data" to process
   - Download the cleaned file

### 2. **Query Database**
   - Select "Database Query" from the sidebar
   - Configure your database connection
   - Write SQL query to fetch data
   - Apply cleaning and AI processing
   - Export results

### 3. **Process API Data**
   - Select "API Data" from the sidebar
   - Enter API endpoint URL
   - Fetch and clean data in one step
   - View and export results

## 📁 Project Structure

```
data_cleaning_agent/
├── app/
│   └── app.py                 # Streamlit UI application
├── scripts/
│   ├── main.py                # Main entry point
│   ├── backend.py             # FastAPI server
│   ├── data_cleaning.py       # Rule-based cleaning logic
│   ├── data_ingestions.py     # Data loading from various sources
│   ├── ai_agent.py            # AI processing pipeline
│   └── test_postgres_connection.py  # Database testing
├── data/
│   └── sample_data.csv        # Sample dataset for testing
├── ui/                        # UI resources (if any)
├── requirements.txt           # Python dependencies
├── README.md                  # This file
└── notes.txt                  # Additional notes
```

## 🔧 Configuration

### Database Connection
Edit `scripts/main.py` to configure your PostgreSQL connection:
```python
DB_USER = "postgres"
DB_PASSWORD = "your_password"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "your_database"
```

### API Endpoints
Modify API URLs in `scripts/data_ingestions.py` or in the Streamlit UI

## 📦 Dependencies

- **FastAPI** - Modern web framework for building APIs
- **Streamlit** - Rapid data app development
- **Pandas** - Data manipulation and analysis
- **NumPy** - Numerical computing
- **Scikit-learn** - Machine learning algorithms
- **SQLAlchemy** - SQL toolkit and ORM
- **psycopg2** - PostgreSQL adapter
- **Great Expectations** - Data validation and documentation
- **Requests** - HTTP library for API calls

## 🔄 Data Cleaning Pipeline

1. **Data Ingestion** - Load from CSV, Excel, Database, or API
2. **Rule-Based Cleaning** - Handle missing values, duplicates, formatting
3. **AI Processing** - Apply machine learning models for intelligent transformation
4. **Validation** - Ensure data quality standards are met
5. **Export** - Save cleaned data in desired format

## 🐛 Troubleshooting

### Port Already in Use
- **FastAPI (8000):** `netstat -ano | findstr :8000` (Windows) or `lsof -i :8000` (Mac/Linux)
- **Streamlit (8501):** `netstat -ano | findstr :8501` (Windows) or `lsof -i :8501` (Mac/Linux)

### Database Connection Failed
- Verify PostgreSQL is running
- Check credentials in `scripts/main.py`
- Ensure database exists and is accessible

### Missing Dependencies
```bash
pip install --upgrade -r requirements.txt
```

## 📝 Sample Data

A sample dataset (`sample_data.csv`) is included for testing. Use it to:
- Explore the UI functionality
- Test the cleaning pipeline
- Verify API endpoints work correctly

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

## 📄 License

This project is open source and available under the MIT License.

## 👨‍💻 Support

For issues or questions, check the `notes.txt` file or create an issue in the repository.
