from app.database import engine
from app.models import Base

# Creates database table 'Documents'
Base.metadata.create_all(bind=engine)


