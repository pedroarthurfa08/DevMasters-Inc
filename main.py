from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import projects

app = FastAPI(
    title="DevMasters API",
    description="API RESTful desenvolvida com FastAPI",
    version="1.0.0"
)

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluindo as rotas
app.include_router(projects.router)

@app.get("/")
async def root():
    return {"message": "Bem-vindo à DevMasters API!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 