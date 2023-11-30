from sqlalchemy.orm import Session
from fastapi import HTTPException
from passlib.hash import pbkdf2_sha256

from . import models, schemas

###### Read向けの処理 ######
# "users"テーブルからuser_idに基づき1レコード取得
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# "users"テーブルからemailに基づき1レコード取得
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

# "users"テーブルから最大100レコードを一覧取得
def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

# "items"テーブルから最大100レコードを一覧取得
def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


###### Create向けの処理 ######
# "users"テーブルに1レコード追加（ユーザーの追加に相当。パスワードはハッシュ化してDB保存する必要があるので注意）
def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = pbkdf2_sha256.hash(user.password)  # パスワードをハッシュ化
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# "items"テーブルに指定したuser_idの1レコード追加（Itemの追加に相当）
def create_user_item(db: Session, item: schemas.ItemCreate, user_id: int):
    # 指定したuser_idが存在しないとき
    if not db.get(models.User, user_id):
        raise HTTPException(status_code=404, detail="The specified user_id doesn't exist")
    # Item追加
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


###### Update向けの処理 ######
# "users"テーブルの特定のuser_idのレコードを更新
def update_user(db: Session, user: schemas.UserCreate, user_id: int):
    # 指定したuser_idが存在しないとき
    if not db.get(models.User, user_id):
        raise HTTPException(status_code=404, detail="The specified user_id doesn't exist")
    # Update実行
    db.query(models.User).filter_by(
        user_id=user_id).update(
        user.dict())
    db.commit()
    # Updateしたデータを取得して返す
    db_user = db.query(models.User).filter(models.User.user_id == user_id).first()
    return db_user

# "items"テーブルの特定のitem_idのレコードを更新
def update_item(db: Session, item: schemas.ItemCreate, item_id: int):
    # 指定したitem_idが存在しないとき
    if not db.get(models.Item, item_id):
        raise HTTPException(status_code=404, detail="The specified item_id doesn't exist")
    # Update実行
    db.query(models.Item).filter_by(
        item_id=item_id).update(
        item.dict())
    db.commit()
    # Updateしたデータを取得して返す
    db_item = db.query(models.Item).filter(models.Item.item_id == item_id).first()
    return db_item


###### Delete向けの処理 ######
# "items"テーブルの特定のitem_idのレコードを削除
def delete_item(db: Session, item_id: int):
    # 削除対象のItemを探す
    item = db.get(models.User, item_id)
    if not item:  # 指定したitem_idが存在しないとき
        raise HTTPException(status_code=404, detail="The specified item_id doesn't exist")
    # Delete実行
    db.delete(item)
    db.commit()
    # Deleteしたデータを返す
    return item

# "users"テーブルの特定のuser_idのレコードを削除
def delete_user(db: Session, user_id: int):
    # 削除対象のUserを探す
    user = db.get(models.User, user_id)
    if not user:  # 指定したuser_idが存在しないとき
        raise HTTPException(status_code=404, detail="The specified user_id doesn't exist")
    # 先に外部キーのレコードを削除（"items"テーブルのowner_idが指定したuser_idのレコード）
    items = db.query(models.Item).filter(models.Item.owner_id == user_id).all()
    for item in items:
        delete_item(db, item.item_id)
    # Delete実行
    db.delete(user)
    db.commit()
    # Deleteしたデータを返す
    return user