from fastapi import APIRouter, HTTPException, status, Query
from typing import List, Optional
from ..models.project import (
    Project, ProjectCreate, ProjectUpdate, ProjectList,
    ProjectStatus, ProjectPriority
)
from ..database import (
    db, DatabaseError, ProjectNotFoundError, DuplicateTitleError,
    InvalidStatusTransitionError, ConcurrentModificationError
)

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
    responses={
        404: {"description": "Projeto não encontrado"},
        409: {"description": "Conflito (ex: título duplicado)"},
        422: {"description": "Erro de validação"},
        423: {"description": "Recurso bloqueado (modificação concorrente)"},
        500: {"description": "Erro interno do servidor"}
    }
)

@router.get(
    "/",
    response_model=ProjectList,
    summary="Listar projetos",
    description="""
    Retorna uma lista paginada de projetos.
    
    - **page**: Número da página (começa em 1)
    - **size**: Tamanho da página (padrão: 10, máximo: 100)
    - **status**: Filtrar por status
    - **priority**: Filtrar por prioridade
    - **search**: Buscar por título ou descrição
    """
)
async def list_projects(
    page: int = Query(1, ge=1, description="Número da página"),
    size: int = Query(10, ge=1, le=100, description="Tamanho da página"),
    status: Optional[ProjectStatus] = Query(None, description="Filtrar por status"),
    priority: Optional[ProjectPriority] = Query(None, description="Filtrar por prioridade"),
    search: Optional[str] = Query(None, description="Buscar por título ou descrição")
):
    try:
        return db.get_projects(
            page=page,
            size=size,
            status=status,
            priority=priority,
            search=search
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao listar projetos"
        )

@router.get(
    "/{project_id}",
    response_model=Project,
    summary="Obter projeto",
    description="Retorna os detalhes de um projeto específico pelo ID."
)
async def get_project(project_id: int):
    try:
        return db.get_project(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao obter projeto"
        )

@router.post(
    "/",
    response_model=Project,
    status_code=status.HTTP_201_CREATED,
    summary="Criar projeto",
    description="""
    Cria um novo projeto.
    
    - O ID é gerado automaticamente
    - A data de criação é registrada automaticamente
    - O status padrão é 'Planejado'
    - Título e descrição são validados e sanitizados
    """
)
async def create_project(project: ProjectCreate):
    try:
        return db.create_project(project)
    except DuplicateTitleError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao criar projeto"
        )

@router.put(
    "/{project_id}",
    response_model=Project,
    summary="Atualizar projeto",
    description="""
    Atualiza os dados de um projeto existente.
    
    - Não é possível alterar o ID ou a data de criação
    - A data de atualização é registrada automaticamente
    - Apenas os campos fornecidos serão atualizados
    - Título e descrição são validados e sanitizados
    """
)
async def update_project(project_id: int, project: ProjectUpdate):
    try:
        return db.update_project(project_id, project)
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except DuplicateTitleError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except InvalidStatusTransitionError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e)
        )
    except ConcurrentModificationError as e:
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao atualizar projeto"
        )

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover projeto",
    description="Remove um projeto existente do sistema."
)
async def delete_project(project_id: int):
    try:
        db.delete_project(project_id)
    except ProjectNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao remover projeto"
        ) 