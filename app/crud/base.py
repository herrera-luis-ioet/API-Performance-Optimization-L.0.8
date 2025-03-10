from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import select, update, delete, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi.encoders import jsonable_encoder
import logging

from app.db.base import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)
ReadSchemaType = TypeVar("ReadSchemaType", bound=BaseModel)

logger = logging.getLogger(__name__)


class BaseCRUD(Generic[ModelType, CreateSchemaType, UpdateSchemaType, ReadSchemaType]):
    """
    Base class for CRUD operations.
    
    Provides common create, read, update, and delete operations.
    """
    
    def __init__(self, model: Type[ModelType]):
        """
        Initialize the CRUD object with the SQLAlchemy model.
        
        Args:
            model: The SQLAlchemy model class
        """
        self.model = model
    
    # PUBLIC_INTERFACE
    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        """
        Create a new record in the database.
        
        Args:
            db: Database session
            obj_in: Input data for creating the record
            
        Returns:
            The created record
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        """
        Get a record by ID.
        
        Args:
            db: Database session
            id: ID of the record to get
            
        Returns:
            The record if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).where(self.model.id == id)
            result = await db.execute(query)
            return result.scalars().first()
        except SQLAlchemyError as e:
            logger.error(f"Error getting {self.model.__name__} with id {id}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def get_multi(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of records
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(self.model).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except SQLAlchemyError as e:
            logger.error(f"Error getting multiple {self.model.__name__}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def update(
        self, db: AsyncSession, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        Update a record.
        
        Args:
            db: Database session
            db_obj: Database object to update
            obj_in: New data to update the record with
            
        Returns:
            The updated record
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.model_dump(exclude_unset=True)
            
            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])
            
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            return db_obj
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error updating {self.model.__name__}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def remove(self, db: AsyncSession, *, id: Any) -> Optional[ModelType]:
        """
        Remove a record by ID.
        
        Args:
            db: Database session
            id: ID of the record to remove
            
        Returns:
            The removed record if found, None otherwise
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            obj = await self.get(db=db, id=id)
            if obj:
                await db.delete(obj)
                await db.commit()
            return obj
        except SQLAlchemyError as e:
            await db.rollback()
            logger.error(f"Error removing {self.model.__name__} with id {id}: {str(e)}")
            raise
    
    # PUBLIC_INTERFACE
    async def count(self, db: AsyncSession) -> int:
        """
        Count the total number of records.
        
        Args:
            db: Database session
            
        Returns:
            Total number of records
            
        Raises:
            SQLAlchemyError: If there's an error during database operation
        """
        try:
            query = select(func.count()).select_from(self.model)
            result = await db.execute(query)
            return result.scalar()
        except SQLAlchemyError as e:
            logger.error(f"Error counting {self.model.__name__}: {str(e)}")
            raise