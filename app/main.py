from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import projects

app = FastAPI(
    title="DevMasters API",
    description="API desenvolvida com FastAPI",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique as origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo os routers
app.include_router(projects.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à DevMasters API!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 