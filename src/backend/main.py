from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse

from langfuse import Langfuse, get_client
from langfuse.langchain import CallbackHandler
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from pydantic import BaseModel

from app_agents.runner import stream_graph

from config import get_settings

from app_agents.graph import build_graph


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.
    This is where you can initialize resources, such as database connections,
    before the application starts serving requests.
    """
    print("Starting up the FastAPI application...")

    settings = get_settings()
    
    Langfuse(
        public_key=settings.LANGFUSE_PUBLIC_KEY,
        secret_key=settings.LANGFUSE_SECRET_KEY,
        host=settings.LANGFUSE_BASE_URL,
    )
    app.state.langfuse_handler = CallbackHandler()

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
    get_client().flush()
    # Clean up resources here (e.g., close database connections)
    print("Shutting down the FastAPI application...")


app = FastAPI(
    title="LangGraph Trip Agent",
    description="A flight agent built with LangGraph and LangChain.",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3001",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class GraphRequest(BaseModel):
    session_thread_id: str
    query: str


@app.post("/chat")
async def chat(request: GraphRequest):
    try:
        response_stream = stream_graph(
            session_thread_id=request.session_thread_id,
            query=request.query,
            graph=app.state.graph,
            callback_handler=app.state.langfuse_handler,
        )
        return StreamingResponse(
            response_stream,
            media_type="text/plain; charset=utf-8",
            headers={"Cache-Control": "no-cache"},
        )
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
