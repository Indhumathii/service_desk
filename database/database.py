from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from urllib.parse import quote_plus

username="postgres"
password=quote_plus("IB@123")
ip_address="localhost"
port=5432
database="service_desk"
# use this for local
db_string = f"postgresql://{username}:{password}@{ip_address}:{port}/{database}"

engine = create_engine(db_string, pool_size=20, max_overflow=0)

Base = declarative_base()
session = scoped_session(sessionmaker(bind=engine))


def get_db():
    Session = sessionmaker(bind=engine)
    session = Session()
    session.autoflush = False

    try:
        yield session
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
