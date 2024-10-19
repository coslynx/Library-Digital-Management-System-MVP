from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .utils.database import SessionLocal, engine
from .utils.config import settings
from .utils.auth import create_access_token, ALGORITHM, SECRET_KEY
from .dependencies import get_db
from .routes.auth_routes import router as auth_router
from .routes.book_routes import router as book_router
from .routes.user_routes import router as user_router

# Initialize the FastAPI application
app = FastAPI(
    title="Efficient Library Digital Management System API",
    description="This API provides functionalities for managing library resources, user accounts, and borrowing processes."
)

# Create database tables if they don't exist
import models
models.Base.metadata.create_all(bind=engine)

# Load environment variables from .env
# ... (Load environment variables as necessary)

# Configure middleware
# ... (Configure authentication middleware, logging, or other middleware as needed)

# Mount API routes
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(book_router, prefix="/api/books", tags=["Books"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])

# Start the FastAPI server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "api.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True
    )