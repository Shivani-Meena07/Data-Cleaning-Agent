web: uvicorn scripts.backend:app --host 0.0.0.0 --port $PORT
ui: streamlit run app/app.py --server.port=$PORT --server.address=0.0.0.0 --logger.level=error
