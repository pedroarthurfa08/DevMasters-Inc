from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, status
from uuid import UUID

from app.models.project import ProjectCreate, ProjectUpdate, ProjectResponse

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={
        404: {"description": "Projeto não encontrado"},
        400: {"description": "Dados inválidos"},
        409: {"description": "Conflito de dados"}
    },
)

# Simulando um banco de dados em memória
projects_db = {}

def check_title_exists(title: str, exclude_id: Optional[UUID] = None) -> bool:
    """Verifica se já existe um projeto com o mesmo título."""
    for project in projects_db.values():
        if project.titulo.lower() == title.lower() and (exclude_id is None or project.id != exclude_id):
            return True
    return False

@router.get("/", response_model=List[ProjectResponse])
async def list_projects(
    status: Optional[str] = Query(None, pattern="^(Planejado|Em Andamento|Concluído|Cancelado)$"),
    prioridade: Optional[int] = Query(None, ge=1, le=3),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    order_by: str = Query("data_criacao", pattern="^(data_criacao|titulo|prioridade)$"),
    order_direction: str = Query("desc", pattern="^(asc|desc)$")
):
    """
    Lista todos os projetos com suporte a filtros, paginação e ordenação.
    """
    try:
        filtered_projects = list(projects_db.values())
        
        # Aplicando filtros
        if status:
            filtered_projects = [p for p in filtered_projects if p.status == status]
        if prioridade:
            filtered_projects = [p for p in filtered_projects if p.prioridade == prioridade]
        
        # Ordenação
        reverse = order_direction == "desc"
        filtered_projects.sort(
            key=lambda x: getattr(x, order_by),
            reverse=reverse
        )
        
        # Paginação
        return filtered_projects[skip:skip + limit]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao listar projetos: {str(e)}"
        )

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    """
    Cria um novo projeto.
    """
    try:
        if check_title_exists(project.titulo):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um projeto com este título"
            )
        
        project_response = ProjectResponse(**project.model_dump())
        projects_db[project_response.id] = project_response
        return project_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao criar projeto: {str(e)}"
        )

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: UUID):
    """
    Retorna os detalhes de um projeto específico.
    """
    try:
        if project_id not in projects_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        return projects_db[project_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao buscar projeto: {str(e)}"
        )

@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(project_id: UUID, project_update: ProjectUpdate):
    """
    Atualiza os campos editáveis de um projeto.
    """
    try:
        if project_id not in projects_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        
        current_project = projects_db[project_id]
        update_data = project_update.model_dump(exclude_unset=True)
        
        # Verifica se o novo título já existe em outro projeto
        if "titulo" in update_data and check_title_exists(update_data["titulo"], project_id):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um projeto com este título"
            )
        
        updated_project = current_project.model_copy(update=update_data)
        projects_db[project_id] = updated_project
        
        return updated_project
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao atualizar projeto: {str(e)}"
        )

@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project(project_id: UUID):
    """
    Remove um projeto do sistema.
    """
    try:
        if project_id not in projects_db:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Projeto não encontrado"
            )
        
        del projects_db[project_id]
        return None
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Erro ao deletar projeto: {str(e)}"
        ) 