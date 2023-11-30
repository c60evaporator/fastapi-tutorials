from typing import List, Union

from pydantic import BaseModel

# "items"テーブルで常に必要な列
class ItemBase(BaseModel):
    title: str
    description: Union[str, None] = None
# "items"テーブルでCreate時のみ必要な列
class ItemCreate(ItemBase):
    pass  # 該当列がないときはpassを渡す
# "items"テーブルでRead時のみ必要な列
class Item(ItemBase):
    id: int
    owner_id: int
    # ORMによるデータ連携を有効化するサブクラス
    class Config:
        orm_mode = True

# "users"テーブルで常に必要な列
class UserBase(BaseModel):
    email: str
# "users"テーブルでCreate時のみ必要な列
class UserCreate(UserBase):
    password: str
# "users"テーブルでRead時のみ必要な列
class User(UserBase):
    id: int
    is_active: bool
    items: List[Item] = []
    # ORMによるデータ連携を有効化するサブクラス
    class Config:
        orm_mode = True