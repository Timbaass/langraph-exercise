from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from pydantic import BaseModel

from app_agents.runner import run_graph

async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    This is where you can initialize resources, such as database connections,
    before the application starts serving requests.
    """
    print("Starting up the FastAPI application...")
    # Initialize resources here (e.g., database connections)
    yield
    # Clean up resources here (e.g., close database connections)
    print("Shutting down the FastAPI application...")

app = FastAPI(
    title="LangGraph Trip Agent",
    description="A flight agent built with LangGraph and LangChain.",
    version="1.0.0",
    lifespan=lifespan
)

class GraphRequest(BaseModel):
    session_thread_id: str
    query: str


@app.get("/chat")
async def root():
    try:
        result = await run_graph(
            session_thread_id="conversation-1", query="Hello, I want to plan a trip."
        )
        return JSONResponse(content={"response": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
