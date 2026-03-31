from data_ingestions import DataIngestion
from data_cleaning import DataCleaning
from ai_agent import AIAgent
from test_postgres_connection import DB_USER

# Database Configuration
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "postgres"

DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"





# Initialize Data Ingestion and Cleaning
data_ingestion = DataIngestion()
cleaner = DataCleaning()
ai_agent = AIAgent()

# Load and clean csv data
df_csv = data_ingestion.load_csv('sample_data.csv')
if df_csv is not None:
    print("\nCleaning CSV data...")
    df_csv = cleaner.clean_data(df_csv)
    df_csv = ai_agent.process_data(df_csv)
    print("\nAI Cleaned CSV Data:\n", df_csv)
    
# === Load and clean excel data ===
df_excel = data_ingestion.load_excel('sample_data.xlsx')
if df_excel is not None:
    print("\nCleaning Excel data...")
    df_excel = cleaner.clean_data(df_excel)
    df_excel = ai_agent.process_data(df_excel)
    print("\nAI Cleaned Excel Data:\n", df_excel)
    
# === Load and clean database data ===
df_db = data_ingestion.load_from_database("SELECT * FROM your_table")  # change table names
if df_db is not None:
    print("\n Cleaning Database data...")
    df_db = cleaner.clean_data(df_db)
    df_db = ai_agent.process_data(df_db)
    print("\n AI Cleaned Database Data:\n", df_db)

# === Fetch and clean API data ===
# fetch api data
API_URL = "https://jsonplaceholder.typicode.com/posts"  # change to actual API endpoint
df_api = data_ingestion.fetch_from_api(API_URL)
if df_api is not None:
    print("\nCleaning API data...")
    
    # Keep only first N rows for cleaning to avoid overwhelming the AI agent
    df_api_sample = df_api.head(30)  # adjust this value based on your dataset size
    
    # reduce long text fields before sending to OpenAI
    if "body" in df_api.columns:
        df_api["body"] = df_api["body"].apply(lambda x: x[:100] + "..." if isinstance(x, str) else x)  # limit text length
        
    df_api = cleaner.clean_data(df_api)
    df_api = ai_agent.process_data(df_api)
    
    print("\nAI Cleaned API Data:\n", df_api)
    