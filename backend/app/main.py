print("MAIN START")

from fastapi import FastAPI

print("FASTAPI IMPORTED")

from fastapi.middleware.cors import CORSMiddleware

print("CORS IMPORTED")

from app.api import upload

print("UPLOAD ROUTER IMPORTED")

app = FastAPI(
    title="AI Contract Analyzer"
)

print("FASTAPI APP CREATED")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("MIDDLEWARE ADDED")

app.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"]
)

print("ROUTER INCLUDED")

@app.get("/")
def root():
    return {
        "status": "running"
    }