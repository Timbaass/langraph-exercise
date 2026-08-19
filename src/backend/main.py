from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from pydantic import BaseModel

from app_agents.runner import run_graph

from config import get_settings

from app_agents.app import build_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    This is where you can initialize resources, such as database connections,
    before the application starts serving requests.
    """
    print("Starting up the FastAPI application...")

    settings = get_settings()

    async with AsyncPostgresSaver.from_conn_string(
        settings.POSTGRES_DB_URI
    ) as checkpointer:
        try:
            await checkpointer.setup()

            graph = build_graph(checkpointer=checkpointer)

            app.state.graph = graph
        except Exception as e:
            print(f"Error during application startup: {e}")
            raise

        yield
    # Initialize resources here (e.g., database connections)
    
    # Clean up resources here (e.g., close database connections)
    print("Shutting down the FastAPI application...")


app = FastAPI(
    title="LangGraph Trip Agent",
    description="A flight agent built with LangGraph and LangChain.",
    version="1.0.0",
    lifespan=lifespan,
)


class GraphRequest(BaseModel):
    session_thread_id: str
    query: str


@app.get("/chat")
async def root():
    try:
        result = await run_graph(
            session_thread_id="conversation-1",
            query="Hello, can you remind me where do i want to go in last chat?",
            graph=app.state.graph,
        )
        return JSONResponse(content={"response": result})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
