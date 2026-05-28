from sqlalchemy.orm import Session
from app.models.models import Fornecedor
from app.schemas.schemas import FornecedorCreate, FornecedorUpdate


class FornecedorRepository:

    def create(self, db: Session, data: FornecedorCreate) -> Fornecedor:
        fornecedor = Fornecedor(**data.model_dump())
        db.add(fornecedor)
        db.commit()
        db.refresh(fornecedor)
        return fornecedor

    def find_all(self, db: Session) -> list[Fornecedor]:
        return db.query(Fornecedor).order_by(Fornecedor.nome).all()

    def find_by_id(self, db: Session, fornecedor_id: int) -> Fornecedor | None:
        return db.query(Fornecedor).filter(Fornecedor.id == fornecedor_id).first()

    def find_by_cnpj(self, db: Session, cnpj: str) -> Fornecedor | None:
        return db.query(Fornecedor).filter(Fornecedor.cnpj == cnpj).first()

    def update(self, db: Session, fornecedor: Fornecedor, data: FornecedorUpdate) -> Fornecedor:
        for field, value in data.model_dump(exclude_none=True).items():
            setattr(fornecedor, field, value)
        db.commit()
        db.refresh(fornecedor)
        return fornecedor

    def delete(self, db: Session, fornecedor: Fornecedor) -> None:
        fornecedor.ativo = False
        db.commit()
