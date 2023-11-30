from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base

# "users"テーブル用のクラス
class User(Base):
    # テーブル名を記載
    __tablename__ = "users"
    # 各列の定義を記載
    id = Column(Integer, primary_key=True, index=True)  # primary_key=Trueで主キーとなる
    email = Column(String, unique=True, index=True)  # unique=Trueで重複を許容しない
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)  # default引数でデフォルト値を指定
    username = Column(String, unique=True, index=True)  # 認証用のユーザー名（unique=Trueで重複を許容しない）
    # テーブル間の関係性を記述
    items = relationship("Item", back_populates="owner")

# "items"テーブル用のクラス
class Item(Base):
    # テーブル名を記載
    __tablename__ = "items"
    # 各列の定義を記載
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)  # index=Trueで検索高速化用のインデックスを張る
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))  # ForeignKeyクラスで外部キーを指定
    # テーブル間の関係性を記述
    owner = relationship("User", back_populates="items")