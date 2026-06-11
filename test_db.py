import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from db.database import DATABASE_URL, init_db

load_dotenv()

def test_db_connection():
    print("=== PostgreSQL DB Connection Test ===")
    try:
        engine = create_engine(DATABASE_URL)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            print("✅ Connected successfully!")
            print("PostgreSQL Version:", result.scalar())
            
            # Test table creation
            init_db()
            print("✅ Tables initialized (ChatHistory)")
            
            # Simple query test
            with engine.connect() as conn:
                result = conn.execute(text("SELECT COUNT(*) FROM chat_history;"))
                count = result.scalar()
                print(f"✅ Chat history table exists. Record count: {count}")
                
        print("\n🎉 DB setup complete! Ready for AI Agent.")
        
    except Exception as e:
        print("❌ DB Connection Failed:", str(e))
        print("\nTips:")
        print("1. Run: docker-compose up -d")
        print("2. Check .env DATABASE_URL")
        print("3. Ensure Postgres is running on port 5432")

if __name__ == "__main__":
    test_db_connection()