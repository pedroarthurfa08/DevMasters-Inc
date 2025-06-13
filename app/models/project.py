from enum import Enum
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime
import re
from .base import BaseSchema

class ProjectPriority(int, Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3

    @classmethod
    def get_values(cls) -> List[int]:
        return [priority.value for priority in cls]

class ProjectStatus(str, Enum):
    PLANNED = "Planejado"
    IN_PROGRESS = "Em Andamento"
    COMPLETED = "Concluído"
    CANCELLED = "Cancelado"

    @classmethod
    def get_values(cls) -> List[str]:
        return [status.value for status in cls]

    @classmethod
    def get_valid_transitions(cls, current_status: str) -> list[str]:
        """Define as transições válidas de status."""
        transitions = {
            cls.PLANNED: [cls.IN_PROGRESS, cls.CANCELLED],
            cls.IN_PROGRESS: [cls.COMPLETED, cls.CANCELLED],
            cls.COMPLETED: [],
            cls.CANCELLED: []
        }
        return transitions.get(current_status, [])

class ProjectBase(BaseModel):
    title: str = Field(
        ...,
        min_length=3,
        max_length=100,
        description="Título do projeto"
    )
    description: str = Field(
        ...,
        min_length=10,
        max_length=2000,
        description="Descrição detalhada do projeto"
    )
    priority: ProjectPriority = Field(
        ...,
        description="Prioridade do projeto (1-Alta, 2-Média, 3-Baixa)"
    )
    status: ProjectStatus = Field(
        default=ProjectStatus.PLANNED,
        description="Status atual do projeto"
    )

    @validator('title')
    def validate_title(cls, v):
        # Remove caracteres especiais e emojis
        v = re.sub(r'[^\w\s-]', '', v)
        # Remove espaços extras
        v = ' '.join(v.split())
        if not v:
            raise ValueError("O título não pode conter apenas caracteres especiais")
        return v

    @validator('description')
    def validate_description(cls, v):
        # Remove caracteres de controle
        v = re.sub(r'[\x00-\x1F\x7F]', '', v)
        return v

    @validator('title')
    def title_must_be_unique(cls, v):
        # Esta validação será implementada no nível do banco de dados
        return v

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, min_length=10, max_length=2000)
    priority: Optional[ProjectPriority] = None
    status: Optional[ProjectStatus] = None

    @validator('title')
    def validate_title(cls, v):
        if v is not None:
            # Remove caracteres especiais e emojis
            v = re.sub(r'[^\w\s-]', '', v)
            # Remove espaços extras
            v = ' '.join(v.split())
            if not v:
                raise ValueError("O título não pode conter apenas caracteres especiais")
        return v

    @validator('description')
    def validate_description(cls, v):
        if v is not None:
            # Remove caracteres de controle
            v = re.sub(r'[\x00-\x1F\x7F]', '', v)
        return v

    @validator('status')
    def validate_status_transition(cls, v, values, **kwargs):
        if v is not None and 'status' in values:
            current_status = values['status']
            if v not in ProjectStatus.get_valid_transitions(current_status):
                raise ValueError(
                    f"Não é possível alterar o status de '{current_status}' para '{v}'"
                )
        return v

class Project(ProjectBase, BaseSchema):
    @validator('updated_at')
    def validate_updated_at(cls, v, values):
        if 'created_at' in values and v < values['created_at']:
            raise ValueError("A data de atualização não pode ser anterior à data de criação")
        if v > datetime.now():
            raise ValueError("A data de atualização não pode ser futura")
        return v

class ProjectFilter(BaseModel):
    status: Optional[ProjectStatus] = Field(None, description="Filtrar por status")
    priority: Optional[ProjectPriority] = Field(None, description="Filtrar por prioridade")
    search: Optional[str] = Field(None, description="Buscar por título ou descrição")

class ProjectList(BaseModel):
    items: List[Project]
    total: int
    page: int
    size: int
    pages: int 