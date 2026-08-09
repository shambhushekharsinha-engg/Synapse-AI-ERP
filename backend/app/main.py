from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Synapse AI ERP API",
    description="Backend API for the Next-Gen AI ERP System",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to Synapse AI ERP API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
