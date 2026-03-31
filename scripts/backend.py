import sys
import os
import pandas as pd
import io
import aiohttp
from fastapi import FastAPI, UploadFile, File, Query, HTTPException
from sqlalchemy import create_engine
from pydantic import BaseModel
import requests

# Ensure the scripts folder is in Python's Path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from ai_agent import AIAgent
from data_ingestions import DataIngestion
from data_cleaning import DataCleaning

app = FastAPI()

# Initialize AI agent and rule based cleaner
ai_agent = AIAgent()
data_ingestion = DataIngestion()
cleaner = DataCleaning()

#--------CSV/Excel Cleaning Endpoint--------#
@app.post("/clean-data")
async def clean_data(file: UploadFile = File(...)):
    """Recieve files from UI, cleans it using rule-based & AI methods, and returns the cleaned file."""
    try:
        contents = await file.read()
        file_extension = file.filename.split('.')[-1]
        
        #load file into DataFrame
        if file_extension == 'csv':
            df = pd.read_csv(io.StringIO(contents.decode('utf-8')))
        elif file_extension == 'xlsx':
            df = pd.read_excel(io.BytesIO(contents))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload a CSV or Excel file.")
        
        # Step 1: Rule-based cleaning
        df_cleaned = cleaner.clean_data(df)
        
        # Step 2: AI-based cleaning
        df_ai_cleaned = ai_agent.process_data(df_cleaned)
        
        # Ensure AI output is a DataFrame
        if isinstance(df_ai_cleaned, str):
            from io import StringIO
            df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
            
        return {"cleaned_data": df_ai_cleaned.to_dict(orient='records')}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {e}")


class DBQuery(BaseModel):
    db_url: str
    query: str


@app.post("/clean-db")
async def clean_db(query: DBQuery):
    """Fectches data from database, cleans it using AI agent, and returns the cleaned data."""
    try:
        engine = create_engine(query.db_url)
        df = pd.read_sql(query.query, engine)
        
        # Step 1: Rule-based cleaning
        df_cleaned = cleaner.clean_data(df)
        
        # Step 2: AI-based cleaning
        df_ai_cleaned = ai_agent.process_data(df_cleaned)
        
        # Convert AI cleaned data to DataFrame
        if isinstance(df_ai_cleaned, str):
            from io import StringIO
            df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
            
        return {"cleaned_data": df_ai_cleaned.to_dict(orient='records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing database query: {str(e)}")


class APIRequest(BaseModel):
    api_url: str


@app.post("/clean-api")
async def clean_api(api_request: APIRequest):
    """Fetches data from an API, cleans it using AI agent, and returns the cleaned data."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_request.api_url) as response:
                if response.status != 200:
                    raise HTTPException(status_code=400, detail="Failed to fetch data from API")
                
                data = await response.json()
                df = pd.DataFrame(data)
                
                # Step 1: Rule-based cleaning
                df_cleaned = cleaner.clean_data(df)
                
                # Step 2: AI-based cleaning
                df_ai_cleaned = ai_agent.process_data(df_cleaned)
                
                # Convert AI cleaned data to DataFrame
                if isinstance(df_ai_cleaned, str):
                    from io import StringIO
                    df_ai_cleaned = pd.read_csv(StringIO(df_ai_cleaned))
                    
                return {"cleaned_data": df_ai_cleaned.to_dict(orient='records')}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing API data: {str(e)}")
    
# -------- Run Server --------#
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
                
                