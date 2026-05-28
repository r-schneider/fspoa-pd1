from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.security import verify_password, get_password_hash, create_access_token
from app.models.user_model import User
from app.repositories.user_repository import UserRepository
from app.schemas.user_schema import UserCreate, UserUpdate, TokenResponse, UserResponse


class AuthService:
    def __init__(self, db: Session):
        self.repo = UserRepository(db)

    def register(self, data: UserCreate) -> User:
        if self.repo.email_exists(data.email):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="E-mail já cadastrado",
            )
        user = User(
            name=data.name,
            email=data.email,
            hashed_password=get_password_hash(data.password),
        )
        return self.repo.create(user)

    def login(self, email: str, password: str) -> TokenResponse:
        user = self.repo.get_by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="E-mail ou senha inválidos",
            )
        if not user.active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Usuário inativo",
            )
        token = create_access_token({"sub": str(user.id)})
        return TokenResponse(access_token=token, user=UserResponse.model_validate(user))

    def update_user(self, user: User, data: UserUpdate) -> User:
        if data.email and self.repo.email_exists(data.email, exclude_id=user.id):
            raise HTTPException(status_code=409, detail="E-mail já em uso")
        if data.name is not None:
            user.name = data.name
        if data.email is not None:
            user.email = data.email
        if data.password is not None:
            user.hashed_password = get_password_hash(data.password)
        if data.active is not None:
            user.active = data.active
        return self.repo.update(user)
