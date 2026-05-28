from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user_model import User
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserCreate, UserResponse, TokenResponse, UserUpdate

router = APIRouter(prefix="/auth", tags=["Autenticação"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Cadastra novo usuário"""
    service = AuthService(db)
    return service.register(data)


@router.post("/login", response_model=TokenResponse)
def login(form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login com e-mail e senha (retorna JWT)"""
    service = AuthService(db)
    return service.login(form.username, form.password)


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    """Retorna dados do usuário logado"""
    return current_user


@router.put("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Atualiza dados do usuário logado"""
    service = AuthService(db)
    return service.update_user(current_user, data)
