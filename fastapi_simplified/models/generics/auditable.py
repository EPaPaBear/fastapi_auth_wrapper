# import statements
from sqlalchemy.schema import Column
from sqlalchemy.types import *
from sqlalchemy.sql import func
from fastapi_simplified.config.database_config import Base


class Auditable(Base):
    """
    Abstract base class to add auditing fields to entities. All entities in the
    system should extend this class.

    Attributes
    ----------
    * created_by : `String`\\
        Who created the entity
    * created_date: `DateTime`\\
        The date the entity was created
    * last_modified_by: `String`\\
        The identity of whoever performed the most recent operation on the entity
    * last_modified_date: `DateTime`\\
        The date the entity was last modified 
    """
    __abstract__ = True

    created_by = Column(String(255))
    created_date = Column(DateTime, default=func.now())
    last_modified_by = Column(String(255))
    last_modified_date = Column(DateTime, onupdate=func.now())
