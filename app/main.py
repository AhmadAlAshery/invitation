from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.core.logging_config import get_logger
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings

# Setup logging
logger = get_logger()


@asynccontextmanager
async def lifespan(app: FastAPI):
    print("App starting...")
    yield
    print("App shutting down...")


app = FastAPI(title=settings.PROJECT_NAME, lifespan=lifespan)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def main():
    logger.warning("Hello From Template")
    return "Hello From Template"
