from sqlalchemy import create_engine

DATABASE_URL = "mysql+pymysql://root:smartie@123.@127.0.0.1:3306/price_intelligence_v2"
engine = create_engine(DATABASE_URL)
conn = engine.connect()
print("SQLAlchemy connection successful!")
conn.close()