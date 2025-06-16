from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, UUID4, validator
from uuid import uuid4

# Constantes para validação
PRIORIDADES_VALIDAS = [1, 2, 3]
STATUS_VALIDOS = ["Planejado", "Em Andamento", "Concluído", "Cancelado"]

class ProjectBase(BaseModel):
    """Modelo base para projetos"""
    titulo: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Título do projeto"
    )
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Descrição do projeto"
    )
    prioridade: int = Field(
        ...,
        description="Prioridade do projeto (1, 2 ou 3)"
    )
    status: str = Field(
        ...,
        description="Status do projeto"
    )

    @validator('prioridade')
    def validar_prioridade(cls, v):
        if v not in PRIORIDADES_VALIDAS:
            raise ValueError(f'Prioridade deve ser um dos valores: {PRIORIDADES_VALIDAS}')
        return v

    @validator('status')
    def validar_status(cls, v):
        if v not in STATUS_VALIDOS:
            raise ValueError(f'Status deve ser um dos valores: {STATUS_VALIDOS}')
        return v

class ProjectCreate(ProjectBase):
    """Modelo para criação de projeto"""
    pass

class ProjectUpdate(BaseModel):
    """Modelo para atualização de projeto"""
    titulo: Optional[str] = Field(
        None,
        min_length=3,
        max_length=100,
        description="Título do projeto"
    )
    descricao: Optional[str] = Field(
        None,
        max_length=500,
        description="Descrição do projeto"
    )
    prioridade: Optional[int] = Field(
        None,
        description="Prioridade do projeto (1, 2 ou 3)"
    )
    status: Optional[str] = Field(
        None,
        description="Status do projeto"
    )

    @validator('prioridade')
    def validar_prioridade(cls, v):
        if v is not None and v not in PRIORIDADES_VALIDAS:
            raise ValueError(f'Prioridade deve ser um dos valores: {PRIORIDADES_VALIDAS}')
        return v

    @validator('status')
    def validar_status(cls, v):
        if v is not None and v not in STATUS_VALIDOS:
            raise ValueError(f'Status deve ser um dos valores: {STATUS_VALIDOS}')
        return v

class ProjectResponse(ProjectBase):
    """Modelo para resposta de projeto"""
    id: UUID4 = Field(
        default_factory=uuid4,
        description="ID único do projeto (UUID)"
    )
    data_criacao: datetime = Field(
        default_factory=datetime.utcnow,
        description="Data de criação do projeto"
    )

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "titulo": "Projeto Exemplo",
                "descricao": "Descrição do projeto exemplo",
                "prioridade": 2,
                "status": "Em Andamento",
                "data_criacao": "2024-03-16T14:30:00"
            }
        } 