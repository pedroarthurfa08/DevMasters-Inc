from typing import Dict, List, Optional, Tuple
from datetime import datetime
import threading
from .models.project import (
    Project, ProjectCreate, ProjectUpdate, ProjectStatus,
    ProjectPriority, ProjectFilter, ProjectList
)

class DatabaseError(Exception):
    """Exceção base para erros do banco de dados."""
    pass

class ProjectNotFoundError(DatabaseError):
    """Exceção lançada quando um projeto não é encontrado."""
    pass

class DuplicateTitleError(DatabaseError):
    """Exceção lançada quando um título de projeto já existe."""
    pass

class InvalidStatusTransitionError(DatabaseError):
    """Exceção lançada quando uma transição de status é inválida."""
    pass

class ConcurrentModificationError(DatabaseError):
    """Exceção lançada quando há tentativa de modificação concorrente."""
    pass

class Database:
    def __init__(self):
        self.projects: Dict[int, Project] = {}
        self._counter = 0
        self._lock = threading.Lock()
        self._project_locks: Dict[int, threading.Lock] = {}

    def _get_project_lock(self, project_id: int) -> threading.Lock:
        """Obtém ou cria um lock para um projeto específico."""
        with self._lock:
            if project_id not in self._project_locks:
                self._project_locks[project_id] = threading.Lock()
            return self._project_locks[project_id]

    def _validate_title_unique(self, title: str, exclude_id: Optional[int] = None) -> None:
        """Valida se o título é único."""
        for project in self.projects.values():
            if project.title.lower() == title.lower() and project.id != exclude_id:
                raise DuplicateTitleError(f"Já existe um projeto com o título '{title}'")

    def _filter_projects(
        self,
        status: Optional[ProjectStatus] = None,
        priority: Optional[ProjectPriority] = None,
        search: Optional[str] = None
    ) -> List[Project]:
        """Filtra projetos com base nos critérios fornecidos."""
        filtered = list(self.projects.values())
        
        if status:
            filtered = [p for p in filtered if p.status == status]
        
        if priority:
            filtered = [p for p in filtered if p.priority == priority]
        
        if search:
            search = search.lower()
            filtered = [
                p for p in filtered
                if search in p.title.lower() or search in p.description.lower()
            ]
        
        return filtered

    def get_projects(
        self,
        page: int = 1,
        size: int = 10,
        status: Optional[ProjectStatus] = None,
        priority: Optional[ProjectPriority] = None,
        search: Optional[str] = None
    ) -> ProjectList:
        """Retorna projetos paginados e filtrados."""
        with self._lock:
            filtered = self._filter_projects(status, priority, search)
            total = len(filtered)
            
            # Calcula o número total de páginas
            pages = (total + size - 1) // size
            
            # Ajusta a página para o intervalo válido
            page = max(1, min(page, pages)) if pages > 0 else 1
            
            # Calcula o índice inicial e final
            start = (page - 1) * size
            end = start + size
            
            return ProjectList(
                items=filtered[start:end],
                total=total,
                page=page,
                size=size,
                pages=pages
            )

    def get_project(self, project_id: int) -> Project:
        """Retorna um projeto específico."""
        with self._lock:
            if project_id not in self.projects:
                raise ProjectNotFoundError(f"Projeto com ID {project_id} não encontrado")
            return self.projects[project_id]

    def create_project(self, project: ProjectCreate) -> Project:
        """Cria um novo projeto."""
        with self._lock:
            self._validate_title_unique(project.title)
            
            self._counter += 1
            now = datetime.now()
            db_project = Project(
                id=self._counter,
                created_at=now,
                updated_at=now,
                **project.model_dump()
            )
            self.projects[db_project.id] = db_project
            return db_project

    def update_project(self, project_id: int, project: ProjectUpdate) -> Project:
        """Atualiza um projeto existente."""
        project_lock = self._get_project_lock(project_id)
        
        with project_lock:
            if project_id not in self.projects:
                raise ProjectNotFoundError(f"Projeto com ID {project_id} não encontrado")
            
            db_project = self.projects[project_id]
            update_data = project.model_dump(exclude_unset=True)
            
            # Valida título único se estiver sendo atualizado
            if 'title' in update_data:
                self._validate_title_unique(update_data['title'], project_id)
            
            # Valida transição de status
            if 'status' in update_data:
                current_status = db_project.status
                new_status = update_data['status']
                if new_status not in ProjectStatus.get_valid_transitions(current_status):
                    raise InvalidStatusTransitionError(
                        f"Não é possível alterar o status de '{current_status}' para '{new_status}'"
                    )
            
            for field, value in update_data.items():
                setattr(db_project, field, value)
            
            db_project.updated_at = datetime.now()
            return db_project

    def delete_project(self, project_id: int) -> None:
        """Remove um projeto."""
        with self._lock:
            if project_id not in self.projects:
                raise ProjectNotFoundError(f"Projeto com ID {project_id} não encontrado")
            
            # Remove o lock do projeto
            if project_id in self._project_locks:
                del self._project_locks[project_id]
            
            del self.projects[project_id]

# Instância global do banco de dados
db = Database() 