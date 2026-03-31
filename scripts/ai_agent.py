import openai
import pandas as pd
from dotenv import load_dotenv
import os
from langchain_openai import OpenAI
from langgraph.graph import StateGraph, END
from pydantic import BaseModel

# Load API key from the environment
load_dotenv()
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
        cleaned_responses = []
        
        for i in range(0, len(df), batch_size):
            df_batch = df.iloc[i:i+batch_size]  # Process 20 rows at a time
            
            prompt = f"""
            You are an AI Data Cleaning Agent. Analyse the dataset:

            {df_batch.to_string()}
            
            Identify the missing values, choose the best imputation strategy (mean, median, mode, or drop) for each column, remove duplicates and format text correctly.
            Return the cleaned data as structured text."""
            
            state = CleaningState(input_text=prompt, structured_response="")
            response = self.graph.invoke(state)
            
            if isinstance(response, dict):
                response = CleaningState(**response)
                
            cleaned_responses.append(response.structured_response)  # store results
            
        return "\n".join(cleaned_responses)  # Combine all responses into a single string
            
        