from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from typing import Union
from fastapi import Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
import os

import crud, models, schemas
from database import SessionLocal, engine


SECRET_KEY = os.environ['SECRET_KEY']  # シークレットキー
ALGORITHM = os.environ['ALGORITHM']  # JWTの署名アルゴリズム


# テーブルを作成
models.Base.metadata.create_all(bind=engine)

# FastAPIクラスのインスタンス作成
app = FastAPI()

# セッションを作成する関数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

###### 認証関係のインスタンス ######
# パスワードのハッシュ化用インスタンス作成（パスワード登録を含む場合のみ）
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# OAuth2認証用Bearerトークンのスキーマ
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
# アクセストークンのスキーマ
class Token(BaseModel):
    access_token: str
    token_type: str
# トークンの中身
class TokenData(BaseModel):
    username: Union[str, None] = None
# 取得したDBセッションとユーザ情報を格納するクラス
class SessionUser():
    def __init__(self, user: schemas.User, db: Session):
        self.user = user
        self.db = db
# JWTトークンの認証情報に基づきユーザ情報とDBセッションを取得する関数
async def get_current_user_db(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    # DBセッションとユーザ情報を取得
    user = crud.get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    # 取得したDBセッションとユーザ情報をインスタンスに格納して返す
    session_user = SessionUser(user=user, db=db)
    return session_user

# JWTトークン発行用API（POST）
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password, pwd_context)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = crud.create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

###### GET ######
# ユーザー一覧を取得するAPI（GET）
@app.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, session_user: SessionUser = Depends(get_current_user_db)):
    users = crud.get_users(session_user.db, skip=skip, limit=limit)
    return users

# user_idに基づきUser情報を取得するAPI（GET）
@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, session_user: SessionUser = Depends(get_current_user_db)):
    db_user = crud.get_user(session_user.db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

# Item一覧を取得するAPI（GET）
@app.get("/items/", response_model=List[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, session_user: SessionUser = Depends(get_current_user_db)):
    items = crud.get_items(session_user.db, skip=skip, limit=limit)
    return items

###### POST ######
# Userを追加するAPI（POST）
@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # 既に同様のemailのユーザーが存在しないか検索
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.create_user(db=db, user=user, pwd_context=pwd_context)

# user_idに基づきItemを追加するAPI（POST）
@app.post("/users/{user_id}/items/", response_model=schemas.Item)
def create_item_for_user(user_id: int, item: schemas.ItemCreate, session_user: SessionUser = Depends(get_current_user_db)):
    return crud.create_user_item(db=session_user.db, item=item, user_id=user_id)

###### PUT ######
# user_idに基づきUser情報を更新するAPI（PUT）
@app.put("/users/{user_id}", response_model=schemas.User)
def update_user(user_id: int, user: schemas.UserCreate, session_user: SessionUser = Depends(get_current_user_db)):
    # 既に同様のemailのユーザーが存在しないか検索
    db_user = crud.get_user_by_email(session_user.db, email=user.email)
    if db_user:
        raise HTTPException(status_code=409, detail="Email already registered")
    return crud.update_user(db=session_user.db, user=user, user_id=user_id)

# item_idに基づきItem情報を更新するAPI（PUT）
@app.put("/items/{item_id}", response_model=schemas.Item)
def update_item(item_id: int, item: schemas.ItemCreate, session_user: SessionUser = Depends(get_current_user_db)):
    return crud.update_item(db=session_user.db, item=item, item_id=item_id)

###### DELETE ######
# item_idに基づきItemを削除するAPI（DELETE）
@app.delete("/items/{item_id}", response_model=schemas.Item)
def delete_item(item_id: int, session_user: SessionUser = Depends(get_current_user_db)):
    return crud.delete_item(db=session_user.db, item_id=item_id)

# user_idに基づきUserを削除するAPI（DELETE）
@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, session_user: SessionUser = Depends(get_current_user_db)):
    return crud.delete_user(db=session_user.db, user_id=user_id)