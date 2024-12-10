from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

db_url = 'sqlite:///./todo_db.db'
try:
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
except Exception as e:
    print(f"Error creating database engine: {e}")
    raise

session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# def create_db_and_tables():
#     SQLModel.metadata.create_all(engine)


# def get_session():
#     with Session(engine) as session:
#         yield session


# SessionDep = Annotated[Session, Depends(get_session)]


Base = declarative_base()

# Dependency for DB connection
def get_db_connection():
    db = session_local()
    try:
        yield db
    finally:
        db.close()