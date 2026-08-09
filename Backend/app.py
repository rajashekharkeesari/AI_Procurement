import sys
from pathlib import Path
from fastapi import FastAPI
import dotenv
import uvicorn

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent
sys.path.append(str(ROOT_DIR))
sys.path.append(str(BACKEND_DIR))

from routes.auth_routes import authrouter
from routes.workflow_routes import router as workflowrouter

PORT = int(dotenv.get_key(".env", "PORT") or 8000)
host = dotenv.get_key(".env", "Backend_url") or "127.0.0.1"

app = FastAPI(title="AI Procurement API")


app.include_router(authrouter, prefix="/auth", tags=["Authentication"])



@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "AI Procurement API is running"}


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


if __name__ == "__main__":
    print(f"Server is running on http://{host}:{PORT}")
    uvicorn.run(app, host=host, port=PORT)