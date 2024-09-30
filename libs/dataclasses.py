from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import List, Optional

from .sql_handler import File, Task


@dataclass
class FileData:
    id: int
    file_name: str
    file_type: str

    @classmethod
    def from_sqlalchemy(cls, file: File):
        return cls(
            id=file.id,
            file_name=file.file_name,
            file_type=file.file_type,
        )

    @classmethod
    def from_dict(cls, data: dict):
        return cls(**data)


@dataclass
class TaskWithFile:
    id: int
    created_at: str
    updated_at: str
    status: str
    files: List[FileData]

    @classmethod
    def from_sqlalchemy(cls, task: Task):
        return cls(
            id=task.id,
            created_at=str(task.created_at),
            updated_at=str(task.updated_at),
            status=task.status,
            files=[FileData.from_sqlalchemy(f) for f in task.files],
        )

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            id=data["id"],
            created_at=data["created_at"],
            updated_at=data["updated_at"],
            status=data["status"],
            files=[FileData.from_dict(d) for d in data["files"]],
        )
