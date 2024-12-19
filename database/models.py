from sqlalchemy import (
    Column,
    String,
    Integer,
)
from database.database import Base


class ServiceDesk(Base):
    __tablename__ = "service_desk"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    priority = Column(String, nullable=False)
    status = Column(String, nullable=False)