import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import dotenv
import uvicorn

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(BACKEND_DIR))

from Backend.Database import init_db
from Backend.routes.auth_routes import authrouter
from Backend.routes.workflow_routes import router as workflowrouter
from Backend.routes.data_routes import router as datarouter

PORT = int(dotenv.get_key(".env", "PORT") or 8000)
# Bind to all interfaces so the nginx container / EC2 can reach the API.
# (Backend_url in .env is a public URL, not a bind address.)
host = dotenv.get_key(".env", "HOST") or "0.0.0.0"

app = FastAPI(title="AI Procurement API")

# CORS — allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database tables on startup
init_db()

# Register routers
app.include_router(authrouter, prefix="/auth", tags=["Authentication"])
app.include_router(workflowrouter, prefix="/workflow", tags=["Workflow"])
app.include_router(datarouter, tags=["Data"])


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "AI Procurement API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    print(f"Server is running on http://{host}:{PORT}")
    uvicorn.run(app, host=host, port=PORT)
