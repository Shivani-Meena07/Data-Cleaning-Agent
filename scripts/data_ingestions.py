import os
import pandas as pd
from sqlalchemy import create_engine
import requests

DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../data')

class DataIngestion:
    def __init__(self, db_url=None):
        """Initializes the DataIngestion with an optional database connection."""
        self.engine = create_engine(db_url) if db_url else None
        
    def load_csv(self,file_name):
        """Loads a CSV file into a pandas DataFrame."""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_csv(file_path)
            print(f"✅Successfully loaded: {file_path}")
            return df
        except Exception as e:
            print(f"❌Error loading CSV: {e}")
            return None
        
    def load_excel(self, file_name, sheet_name=0):
        """Loads an Excel file into a pandas DataFrame."""
        file_path = os.path.join(DATA_DIR, file_name)
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"✅Successfully loaded: {file_path}")
            return df
        except Exception as e:
            print(f"❌Error loading Excel: {e}")
            return None 
            
    def connect_database(self, db_url):
        """Establishes a connection to the database."""
        try:
            self.engine = create_engine(db_url)
            print("✅Database connection established.")
        except Exception as e:
            print(f"❌Error connecting to database: {e}")
                    
    def load_from_database(self, query):
        """Loads data from the database using a SQL query."""
        if not self.engine:
            print("❌No database connection. Please connect to a database first.")
            return None
        try:
            df = pd.read_sql(query, self.engine)
            print("✅Successfully loaded data from database.")
            return df
        except Exception as e:
            print(f"❌Error loading data from database: {e}")
            return None
                
    def fetch_from_api(self, api_url, params=None):
        """Fetches data from an API endpoint and returns it as a pandas DataFrame."""
        try:
            response = requests.get(api_url, params=params)
            if response.status_code == 200:
                data = response.json()
                df = pd.DataFrame(data)
                print(f"✅Successfully fetched data from API: {api_url}")
                return df
            else:
                print(f"❌API request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"❌Error fetching data from API: {e}")
            return None
                