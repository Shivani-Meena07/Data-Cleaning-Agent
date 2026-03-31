import psycopg2

# Update these credentials
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'postgres'
DB_USER = 'postgres'
DB_PASSWORD = 'admin'

#DB_URL = "postgresql://postgres:admin@localhost:5432/postgres"
try:
    # Connect to the PostgreSQL database
    connection = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT
    )
    cursor = connection.cursor()
    print("✅PostgreSQL connection successful!")
    
    # Execute a simple query to test the connection
    cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    tables = cursor.fetchall()
    print("✅Tables in the database:")
    for table in tables:
        print(table[0])
        
    # Close connection
    cursor.close()
    connection.close()
    print("✅Connection closed successfully.")
    
except Exception as e:
    print(f"❌Error connecting to PostgreSQL:{e}")