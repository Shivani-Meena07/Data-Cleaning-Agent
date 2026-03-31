import openai
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# Load API key from the environment
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Define AI Model
llm = OpenAI(openai_api_key=openai.api_key, temperature=0)

class CleaningState(BaseModel):
    """State schema defining input and output for the LanggGraph agent."""
    input_text: str
    structured_response: str = ""
    
class AIAgent:
    def __init__(self):
        self.graph = self.create_graph()
        
    def create_graph(self):
        """Creates a LanggGraph with defined states and transitions."""
        graph = StateGraph(CleaningState)
        
        def agent_logic(state: CleaningState) -> CleaningState:
            """Processes input and returns a structured response"""
            response = llm.invoke(state.input_text)
            return CleaningState(input_text=state.input_text, structured_response=response)
        
        graph.add_node("CleaningAgent", agent_logic)
        graph.add_edge("CleaningAgent", END)
        graph.set_entry_point("CleaningAgent")
        return graph.compile()

    def process_data(self, df, batch_size=20):
        """Processes the DataFrame in batches using the LanggGraph agent."""
        try:
            # Handle missing values
            for column in df.columns:
                if df[column].dtype in ['float64', 'int64']:  # Numeric columns
                    df[column].fillna(df[column].mean(), inplace=True)
                else:  # Text columns
                    df[column].fillna(df[column].mode()[0] if len(df[column].mode()) > 0 else 'Unknown', inplace=True)
            
            # Remove duplicates
            df = df.drop_duplicates()
            
            # Reset index
            df = df.reset_index(drop=True)
            
            # Return the cleaned DataFrame as CSV string
            return df.to_csv(index=False)
        except Exception as e:
            print(f"Error in AI agent processing: {e}")
            # Return the original dataframe as fallback
            return df.to_csv(index=False)
            
        