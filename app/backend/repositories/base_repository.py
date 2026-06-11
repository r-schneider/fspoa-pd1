from typing import Generic, TypeVar, Type, Optional, List
from sqlalchemy.orm import Session

from app.backend.core.database import BaseDados

ModelType = TypeVar("ModelType", bound=BaseDados)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: Session):
        self.model = model
        self.db = db

    def buscar_por_id(self, id: int) -> Optional[ModelType]:
        return self.db.query(self.model).filter(self.model.id == id).first()

    def buscar_todos(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        return self.db.query(self.model).offset(skip).limit(limit).all()

    def criar(self, obj: ModelType) -> ModelType:
        self.db.add(obj)
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def atualizar(self, obj: ModelType) -> ModelType:
        self.db.commit()
        self.db.refresh(obj)
        return obj

    def deletar(self, obj: ModelType) -> None:
        self.db.delete(obj)
        self.db.commit()

    def contar(self) -> int:
        return self.db.query(self.model).count()
