from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query
from uuid import UUID

from app.models.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={404: {"description": "Projeto não encontrado"}},
)

# Simulando um banco de dados em memória
projects_db = {}

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    status: Optional[str] = Query(None, pattern="^(Planejado|Em Andamento|Concluído|Cancelado)$"),
    prioridade: Optional[int] = Query(None, ge=1, le=3),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """
    Lista todos os projetos com suporte a filtros e paginação.
    """
    filtered_projects = list(projects_db.values())
    
    if status:
        filtered_projects = [p for p in filtered_projects if p.status == status]
    if prioridade:
        filtered_projects = [p for p in filtered_projects if p.prioridade == prioridade]
    
    return filtered_projects[skip:skip + limit]

@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(project: ProjectCreate):
    """
    Cria um novo projeto.
    """
    project_response = ProjectResponse(**project.model_dump())
    projects_db[project_response.id] = project_response
    return project_response

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID):
    """
    Retorna os detalhes de um projeto específico.
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    return projects_db[project_id]

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, project_update: ProjectUpdate):
    """
    Atualiza os campos editáveis de um projeto.
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    current_project = projects_db[project_id]
    update_data = project_update.model_dump(exclude_unset=True)
    updated_project = current_project.model_copy(update=update_data)
    projects_db[project_id] = updated_project
    
    return updated_project

@router.delete("/{project_id}", status_code=204)
async def delete_project(project_id: UUID):
    """
    Remove um projeto do sistema.
    """
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Projeto não encontrado")
    
    del projects_db[project_id]
    return None 