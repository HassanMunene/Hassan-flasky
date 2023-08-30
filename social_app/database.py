from sqlalchemy import create_engine

engine = create_engine(
    'mysql+pymysql://hassan:munene14347@localhost:3306/flasky',
    pool_recycle=3600
)
connection = engine.connect()
