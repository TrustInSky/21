import functools
import logging
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.connection import async_session

logger = logging.getLogger(__name__)

def db_session(func):
    """
    Decorator to provide a database session to the decorated function.
    Automatically handles session creation and cleanup.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session() as session:
            try:
                # Add session to kwargs
                kwargs['session'] = session
                # Call the original function
                result = await func(*args, **kwargs)
                # Commit the session
                await session.commit()
                return result
            except Exception as e:
                # Rollback on error
                await session.rollback()
                logger.error(f"Database error in {func.__name__}: {str(e)}")
                raise
    return wrapper

def db_transaction(func):
    """
    Decorator to wrap the function in a database transaction.
    Requires a session to be provided in kwargs.
    """
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        if 'session' not in kwargs:
            raise ValueError("Session required for db_transaction decorator")
        
        session = kwargs['session']
        try:
            # Call the original function
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            # Rollback on error
            await session.rollback()
            logger.error(f"Transaction error in {func.__name__}: {str(e)}")
            raise
    return wrapper