"""
Author: your name
Date: 2024-09-25 16:21:55
"""

# third-party packages
from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    create_engine,
)
from sqlalchemy.engine.base import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, relationship, sessionmaker
from sqlalchemy.sql import func

# user-defined packages


# SQLiteエンジンを作成（メモリ上にデータベースを作成）
# 永続化したい場合は 'sqlite:///example.db' のようにファイル名を指定
DATABASE_URL = "sqlite:///mydatabase.db"


# データベースのベースクラスを定義
Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 更新日時
    status = Column(String, nullable=False)

    # リレーションシップ
    input_addresses = relationship(
        "InputAddress",  # 関連付けるモデルクラス名
        back_populates="task",  # 相手側のリレーションシップ名
        cascade="all, delete-orphan",  # カスケードオプション：すべての操作を伝播し、孤立した子オブジェクトを削除
    )
    files = relationship("File", back_populates="task", cascade="all, delete-orphan")


class InputAddress(Base):
    __tablename__ = "input_addresses"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    address_text = Column(String, nullable=False)

    # リレーションシップ
    task = relationship(
        "Task",  # 関連付けるモデルクラス名
        back_populates="input_addresses",  # 相手側のリレーションシップ名
    )
    extracted_table_rows = relationship(
        "ExtractedTableRow",
        back_populates="input_address",
        # カスケードオプションは指定しない
    )


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    uploaded_at = Column(DateTime, default=func.now())

    # リレーションシップ
    task = relationship(
        "Task",
        back_populates="files",
        # カスケードオプションは指定しない
    )
    pages = relationship(
        "Page",
        back_populates="file",
        cascade="all, delete-orphan",  # 子オブジェクトを削除
    )


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True)
    file_id = Column(Integer, ForeignKey("files.id"), nullable=False)
    page_number = Column(Integer, nullable=False)
    image_path = Column(String, nullable=False)
    status = Column(String, nullable=False)
    error_message = Column(Text)
    processed_at = Column(DateTime)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # 更新日時

    # リレーションシップ
    file = relationship(
        "File",
        back_populates="pages",
        # カスケードオプションは指定しない
    )
    extracted_table_rows = relationship(
        "ExtractedTableRow", back_populates="page", cascade="all, delete-orphan"
    )


class ExtractedTableRow(Base):
    __tablename__ = "extracted_table_rows"

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey("pages.id"), nullable=False)
    row_number = Column(Integer, nullable=False)
    text_content = Column(Text, nullable=False)
    position_top_left = Column(String)
    position_bottom_right = Column(String)
    input_address_id = Column(Integer, ForeignKey("input_addresses.id"), nullable=True)

    # リレーションシップ
    page = relationship("Page", back_populates="extracted_table_rows")
    input_address = relationship("InputAddress", back_populates="extracted_table_rows")
