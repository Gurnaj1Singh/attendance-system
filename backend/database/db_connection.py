from sqlalchemy import create_engine
import urllib.parse
encoded_password = urllib.parse.quote_plus("Mannsard@@r@1984")

# Database credentials
DB_USER = "root"
DB_PASSWORD = encoded_password  # Make sure this matches what worked with PyMySQL
DB_HOST = "127.0.0.1"  # Use 127.0.0.1 instead of localhost
DB_PORT = "3306"  # Confirmed MySQL port
DB_NAME = "smart_hostel"

# Corrected SQLAlchemy connection string
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create database engine
engine = create_engine(DATABASE_URL, echo=True)

# Test connection
try:
    with engine.connect() as connection:
        print("✅ SQLAlchemy successfully connected to MySQL database!")
except Exception as e:
    print(f"❌ SQLAlchemy Error: {e}")
