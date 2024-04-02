from typing import Generic, TypeVar
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import Engine
from fastapi_simplified.config.database_config import *
from sqlalchemy.exc import IntegrityError
from fastapi_simplified.exceptions.resource_exceptions import *

T = TypeVar("T")

class GenericRepository(Generic[T]):
    """
    A repository class that is built on generics. It consumes a generic model and uses it as its basis for CRUD operations.

    Attributes
    ----------
    * model : `T` \\
        The model object. This is expected to be an object of type `Auditable`.

    Methods
    -------
    * __init__(model: `T`) \\
        Initializes a new GenericRepository instance with the provided model object.
    * create_tables() -> `None` \\
        Creates tables in the database for the model associated with this repository.
    * get_db() -> `Session` \\
        Returns a session for database operations.
    * find_all(limit: `int`, offset: `int`) -> `list[T]` \\
        Finds all instances of the entity in the database.
    * find_by_id(id: `int`) -> `T` \\
        Finds a specific instance of the entity in the database by ID.
    * save(item: `T`) -> `T` \\
        Saves an instance of the entity object to the database.
    * update(updateItem: `T`) -> `None` \\
        Updates the properties of an entity and persists it to the database.
    * delete_by_id(id: `int`) -> `None` \\
        Deletes a specific instance of the entity from the database by ID.
    """
    def __init__(self, model:T) -> None:
        self.model : T = model

        # Get the engine, session and base attributes for db connection
        self.engine: Engine = DbEngine
        self.db: Session = SessionLocal()
        self.base : any = Base

        # Create tables and get database when object is created
        self.create_tables()
        self.get_db()

    def create_tables(self) -> None:
        """
        Creates tables in the database for the model associated with this repository.
        """
        self.base.metadata.create_all(bind = self.engine)

    def get_db(self):
        """
        Returns a session for database operations.

        Returns
        -------
        * `Session` \\
            A database session.
        """
        try:
            yield self.db
        finally:
            self.db.close()

    def find_all(self, limit:int, offset:int) -> list[T]:
        """
        Finds all instances of entity in database

        Parameters
        -----------
        * limit : `int`\\
            Maximum number of items to return
        * offset : `int`\\
            Value to skip collection by
        
        Returns
        --------
        * list[T] : `list`\\
            A list of the entities
        """
        # Handle exceptions
        return self.db.query(self.model).offset(offset).limit(limit).all()

    def find_by_id(self, id:int) -> T:
        """
        Finds specific instance of entity in database by `id`

        Parameters
        -----------
        * id : `int`\\
            Identifying number of row in table
        
        Returns
        --------
        * T : `Auditable`\\
            The found entity
        """
        # Handle exceptions
        return self.db.query(self.model).get(id)

    def save(self, item:T) -> T:
        """
        Saves instance of entity object to database

        Parameters
        -----------
        * item : `T`\\
            The entity to be saved to db
        
        Returns
        --------
        * T : `Auditable`\\
            The saved entity
        """
        try:
            self.db.add(item)
            self.db.commit()
            self.db.refresh(item)
            return item
        except IntegrityError:
            self.db.rollback()
            raise UsernameOrEmailAlreadyExistsException()


    def update(self, updateItem:T) -> None:
        """
        Updates the properties of an entity and persists it to the database

        Parameters
        -----------
        * updateItem : `T`\\
            The updated information pertaining to an entity
        
        Returns
        --------
        `None`
        """
        if updateItem is not None:
            self.db.commit()
            self.db.refresh(updateItem)
        # Handle exceptions later

    def delete_by_id(self, id:int) -> None:
        """
        Deletes specific instance of entity from database by `id`

        Parameters
        -----------
        * id : `int`\\
            Identifying number of row in table
        
        Returns
        --------
        * `None`
        """
        item:T = self.find_by_id(id)

        if item is not None:
            self.db.delete(item)
            self.db.commit()
        # Handle exceptions later

